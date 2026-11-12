// Browser-side scene illustrator: SD-Turbo (one step) on ONNX Runtime.
// Ported from Microsoft's onnxruntime-web sd-turbo example. Works in the browser
// (WebGPU, fp16) and headlessly in Node for tests when an `ort` module is injected.

/* ---------------- CLIP BPE tokenizer (OpenCLIP variant: pad id 0) ---------------- */
function bytesToUnicode(){
  const bs = []; for (let i = 33; i <= 126; i++) bs.push(i); for (let i = 161; i <= 172; i++) bs.push(i); for (let i = 174; i <= 255; i++) bs.push(i);
  const cs = bs.slice(); let n = 0;
  for (let b = 0; b < 256; b++){ if (!bs.includes(b)){ bs.push(b); cs.push(256 + n); n++; } }
  const m = new Map(); bs.forEach((b, i) => m.set(b, String.fromCharCode(cs[i]))); return m;
}
export class ClipTokenizer {
  constructor(vocab, mergesText){
    this.encoder = vocab;
    const lines = mergesText.split("\n").filter(l => l && !l.startsWith("#version"));
    this.ranks = new Map(lines.map((l, i) => [l.trim(), i]));
    this.byteEnc = bytesToUnicode(); this.cache = new Map();
    this.bos = 49406; this.eos = 49407; this.pad = 0; this.maxLen = 77;
  }
  bpe(token){
    if (this.cache.has(token)) return this.cache.get(token);
    let word = [...token.slice(0, -1), token.slice(-1) + "</w>"];
    const pairs = w => { const p = new Set(); for (let i = 0; i < w.length - 1; i++) p.add(w[i] + " " + w[i+1]); return p; };
    let ps = pairs(word);
    if (!ps.size){ this.cache.set(token, token + "</w>"); return token + "</w>"; }
    while (true){
      let best = null, bestRank = Infinity;
      for (const p of ps){ const r = this.ranks.get(p); if (r !== undefined && r < bestRank){ bestRank = r; best = p; } }
      if (best === null) break;
      const [a, b] = best.split(" "); const out = []; let i = 0;
      while (i < word.length){
        const j = word.indexOf(a, i);
        if (j < 0){ out.push(...word.slice(i)); break; }
        out.push(...word.slice(i, j)); i = j;
        if (word[i] === a && i < word.length - 1 && word[i+1] === b){ out.push(a + b); i += 2; } else { out.push(word[i]); i += 1; }
      }
      word = out; if (word.length === 1) break; ps = pairs(word);
    }
    const res = word.join(" "); this.cache.set(token, res); return res;
  }
  encode(text){
    text = text.toLowerCase().replace(/\s+/g, " ").trim();
    const re = /<\|startoftext\|>|<\|endoftext\|>|'s|'t|'re|'ve|'m|'ll|'d|[\p{L}]+|[\p{N}]|[^\s\p{L}\p{N}]+/gu;
    const ids = [this.bos];
    for (const tok of text.match(re) || []){
      const bytes = new TextEncoder().encode(tok); let t = ""; for (const b of bytes) t += this.byteEnc.get(b);
      for (const piece of this.bpe(t).split(" ")){ const id = this.encoder[piece]; if (id !== undefined) ids.push(id); }
    }
    ids.length = Math.min(ids.length, this.maxLen - 1); ids.push(this.eos);
    while (ids.length < this.maxLen) ids.push(this.pad);
    return ids;
  }
}

/* ---------------- pipeline ---------------- */
const SIGMA = 14.6146;               // EulerDiscrete sigma at t=999 for the scaled-linear SD schedule
const VAE_SCALE = 0.18215;
const LAT = 64;                      // 512x512 image
export const MODEL_FILES = {
  unet: {path:"unet/model.onnx", mb:1653, opt:{freeDimensionOverrides:{batch_size:1, num_channels:4, height:LAT, width:LAT, sequence_length:77}}},
  text_encoder: {path:"text_encoder/model.onnx", mb:650, opt:{freeDimensionOverrides:{batch_size:1}}},
  vae_decoder: {path:"vae_decoder/model.onnx", mb:95, opt:{freeDimensionOverrides:{batch_size:1, num_channels_latent:4, height_latent:LAT, width_latent:LAT}}},
};
export const TOKENIZER_FILES = ["tokenizer/vocab.json", "tokenizer/merges.txt"];
export const DEFAULT_BASE = "https://huggingface.co/schmuell/sd-turbo-ort-web/resolve/main";

function mulberry32(seed){ return () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
function randn(n, scale, seed){
  const rnd = seed == null ? Math.random : mulberry32(seed); const out = new Float32Array(n);
  for (let i = 0; i < n; i += 2){ const u = Math.max(rnd(), 1e-12), v = rnd(); const r = Math.sqrt(-2 * Math.log(u)); out[i] = r * Math.cos(2 * Math.PI * v) * scale; if (i + 1 < n) out[i+1] = r * Math.sin(2 * Math.PI * v) * scale; }
  return out;
}

export function createIllustrator({ort, fetchBytes, fetchText, baseUrl = DEFAULT_BASE, provider = "webgpu", onProgress = () => {}, sessionExtra = {}}){
  const sessions = {}; let tokenizer = null; let loaded = false;
  const baseOpt = { executionProviders:[provider], enableMemPattern:false, enableCpuMemArena:false,
    extra:{ session:{ disable_prepacking:"1", use_device_allocator_for_initializers:"1", use_ort_model_bytes_directly:"1", use_ort_model_bytes_for_initializers:"1" } }, ...sessionExtra };
  async function load(){
    if (loaded) return;
    onProgress({stage:"tokenizer", frac:0});
    const [vocab, merges] = await Promise.all([fetchText(`${baseUrl}/${TOKENIZER_FILES[0]}`), fetchText(`${baseUrl}/${TOKENIZER_FILES[1]}`)]);
    tokenizer = new ClipTokenizer(JSON.parse(vocab), merges);
    const total = Object.values(MODEL_FILES).reduce((n, m) => n + m.mb, 0); let done = 0;
    for (const [name, m] of Object.entries(MODEL_FILES)){
      const bytes = await fetchBytes(`${baseUrl}/${m.path}`, (loadedMb) => onProgress({stage:`downloading ${name}`, frac:(done + Math.min(loadedMb, m.mb)) / total}));
      onProgress({stage:`compiling ${name}`, frac:(done + m.mb) / total});
      sessions[name] = await ort.InferenceSession.create(bytes, {...baseOpt, ...m.opt});
      done += m.mb;
    }
    loaded = true; onProgress({stage:"ready", frac:1});
  }
  // Returns {width, height, rgba: Uint8ClampedArray}
  async function generate(prompt, {seed = null} = {}){
    if (!loaded) throw new Error("illustrator not loaded");
    const ids = tokenizer.encode(prompt);
    const {last_hidden_state} = await sessions.text_encoder.run({input_ids: new ort.Tensor("int32", Int32Array.from(ids), [1, ids.length])});
    const n = 4 * LAT * LAT, dims = [1, 4, LAT, LAT];
    const latent = randn(n, SIGMA, seed);
    const scaled = new Float32Array(n); const div = Math.sqrt(SIGMA * SIGMA + 1); for (let i = 0; i < n; i++) scaled[i] = latent[i] / div;
    const {out_sample} = await sessions.unet.run({ sample:new ort.Tensor("float32", scaled, dims), timestep:new ort.Tensor("int64", [999n], [1]), encoder_hidden_states:last_hidden_state });
    if (last_hidden_state.dispose) last_hidden_state.dispose();
    const eps = out_sample.data; const denoised = new Float32Array(n);
    for (let i = 0; i < n; i++) denoised[i] = (latent[i] - SIGMA * eps[i]) / VAE_SCALE;   // one Euler step to sigma=0, then VAE scaling
    const {sample} = await sessions.vae_decoder.run({latent_sample:new ort.Tensor("float32", denoised, dims)});
    const [, , H, W] = sample.dims; const px = sample.data; const rgba = new Uint8ClampedArray(W * H * 4);
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++){ const o = (y * W + x) * 4, i = y * W + x;
      rgba[o] = (px[i] / 2 + 0.5) * 255; rgba[o+1] = (px[H*W + i] / 2 + 0.5) * 255; rgba[o+2] = (px[2*H*W + i] / 2 + 0.5) * 255; rgba[o+3] = 255; }
    return {width:W, height:H, rgba};
  }
  async function unload(){ for (const s of Object.values(sessions)) try{ await s.release(); }catch{} for (const k in sessions) delete sessions[k]; loaded = false; }
  return {load, generate, unload, get loaded(){ return loaded; }, tokenize: t => tokenizer?.encode(t)};
}
