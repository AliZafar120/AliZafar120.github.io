// Browser-side scene illustrator on ONNX Runtime (WebGPU in the browser, CPU in Node tests).
// Default pipeline: LCM Dreamshaper v7 (Stable Diffusion 1.5 distilled with Latent Consistency,
// MIT / CreativeML OpenRAIL-M), 4 steps, 512x512. An SD-Turbo config is kept for reference only
// because its license forbids hosted use.

/* ---------------- CLIP BPE tokenizer ---------------- */
function bytesToUnicode(){
  const bs = []; for (let i = 33; i <= 126; i++) bs.push(i); for (let i = 161; i <= 172; i++) bs.push(i); for (let i = 174; i <= 255; i++) bs.push(i);
  const cs = bs.slice(); let n = 0;
  for (let b = 0; b < 256; b++){ if (!bs.includes(b)){ bs.push(b); cs.push(256 + n); n++; } }
  const m = new Map(); bs.forEach((b, i) => m.set(b, String.fromCharCode(cs[i]))); return m;
}
export class ClipTokenizer {
  constructor(vocab, mergesText, {pad = 49407} = {}){
    this.encoder = vocab;
    const lines = mergesText.split("\n").filter(l => l && !l.startsWith("#version"));
    this.ranks = new Map(lines.map((l, i) => [l.trim(), i]));
    this.byteEnc = bytesToUnicode(); this.cache = new Map();
    this.bos = 49406; this.eos = 49407; this.pad = pad; this.maxLen = 77;
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

/* ---------------- pipelines ---------------- */
const LAT = 64;  // 512x512
export const PIPELINES = {
  lcm: {
    label: "LCM Dreamshaper v7 · 512px · 4 steps · ~2.1 GB",
    base: "https://huggingface.co/aislamov/lcm-dreamshaper-v7-onnx/resolve/main",
    license: "MIT (LCM) and CreativeML OpenRAIL-M (Dreamshaper 7)",
    pad: 49407, steps: 4, guidance: 8.0, scheduler: "lcm", timestepType: "float32",
    files: {
      text_encoder: {path:"text_encoder/model.onnx", mb:235, opt:{freeDimensionOverrides:{textenc_inputids_batch:1, textenc_inputids_sequence:77}}},
      unet: {path:"unet/model.onnx", data:"unet/model.onnx_data", mb:1658, opt:{freeDimensionOverrides:{unet_sample_batch:1, unet_sample_channels:4, unet_sample_height:LAT, unet_sample_width:LAT, unet_timestep_batch:1, unet_ehs_batch:1, unet_ehs_sequence:77, unet_timestep_cond_batch:1}}},
      vae_decoder: {path:"vae_decoder/model.onnx", data:"vae_decoder/model.onnx_data", mb:95, opt:{freeDimensionOverrides:{vaedec_sample_batch:1, vaedec_sample_channels:4, vaedec_sample_height:LAT, vaedec_sample_width:LAT}}},
    },
  },
  sdturbo: {
    label: "SD-Turbo · 512px · 1 step · ~2.4 GB (non-commercial license)",
    base: "https://huggingface.co/schmuell/sd-turbo-ort-web/resolve/main",
    license: "Stability AI Non-Commercial Research Community License",
    pad: 0, steps: 1, guidance: 0, scheduler: "euler1", timestepType: "int64",
    files: {
      text_encoder: {path:"text_encoder/model.onnx", mb:650, opt:{freeDimensionOverrides:{batch_size:1}}},
      unet: {path:"unet/model.onnx", mb:1653, opt:{freeDimensionOverrides:{batch_size:1, num_channels:4, height:LAT, width:LAT, sequence_length:77}}},
      vae_decoder: {path:"vae_decoder/model.onnx", mb:95, opt:{freeDimensionOverrides:{batch_size:1, num_channels_latent:4, height_latent:LAT, width_latent:LAT}}},
    },
  },
};
export const TOKENIZER_FILES = ["tokenizer/vocab.json", "tokenizer/merges.txt"];
const VAE_SCALE = 0.18215;

function mulberry32(seed){ return () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
function randn(n, scale, rnd){
  const out = new Float32Array(n);
  for (let i = 0; i < n; i += 2){ const u = Math.max(rnd(), 1e-12), v = rnd(); const r = Math.sqrt(-2 * Math.log(u)); out[i] = r * Math.cos(2 * Math.PI * v) * scale; if (i + 1 < n) out[i+1] = r * Math.sin(2 * Math.PI * v) * scale; }
  return out;
}

/* Scaled-linear DDPM schedule shared by SD 1.x/2.x */
const ALPHAS_CUMPROD = (() => { const T = 1000, b0 = Math.sqrt(0.00085), b1 = Math.sqrt(0.012); const a = new Float64Array(T); let p = 1; for (let i = 0; i < T; i++){ const beta = (b0 + (b1 - b0) * i / (T - 1)) ** 2; p *= 1 - beta; a[i] = p; } return a; })();

/* LCMScheduler (diffusers): timesteps, boundary scalings, step */
export function lcmTimesteps(steps, original = 50){
  const k = 1000 / original; const origin = []; for (let i = 1; i <= original; i++) origin.push(i * k - 1);
  const skip = Math.floor(origin.length / steps); const rev = origin.reverse(); const ts = []; for (let i = 0; i < rev.length && ts.length < steps; i += skip) ts.push(rev[i]); return ts;
}
function lcmScalings(t){ const s = t * 10, sd = 0.5; return {c_skip: sd*sd / (s*s + sd*sd), c_out: s / Math.sqrt(s*s + sd*sd)}; }
export function guidanceEmbedding(w, dim = 256){
  const half = dim / 2, emb = new Float32Array(dim); const f = Math.log(10000) / (half - 1); const ws = w * 1000;
  for (let i = 0; i < half; i++){ const e = ws * Math.exp(-f * i); emb[i] = Math.sin(e); emb[half + i] = Math.cos(e); } return emb;
}

export function createIllustrator({ort, fetchBytes, fetchText, pipeline = "lcm", baseUrl, provider = "webgpu", onProgress = () => {}, sessionExtra = {}, createSession = null}){
  const P = PIPELINES[pipeline]; if (!P) throw new Error("unknown pipeline " + pipeline);
  const timestepType = P.timestepType;
  const base = baseUrl || P.base; const sessions = {}; let tokenizer = null; let loaded = false;
  const baseOpt = { executionProviders:[provider], enableMemPattern:false, enableCpuMemArena:false,
    extra:{ session:{ disable_prepacking:"1", use_device_allocator_for_initializers:"1", use_ort_model_bytes_directly:"1", use_ort_model_bytes_for_initializers:"1" } }, ...sessionExtra };
  const makeSession = createSession || (async (name, m, opt, report) => {
    let doneMb = 0;                                   // bytes of files already fetched for this model, so the bar never jumps back
    const bytes = await fetchBytes(`${base}/${m.path}`, mb => report(doneMb + mb)); doneMb += bytes.byteLength / 1048576;
    let externalData; if (m.data){ const d = await fetchBytes(`${base}/${m.data}`, mb => report(doneMb + mb)); externalData = [{path:m.data.split("/").pop(), data:new Uint8Array(d)}]; }
    return ort.InferenceSession.create(bytes, {...opt, ...(externalData ? {externalData} : {})});
  });
  async function load(){
    if (loaded) return;
    onProgress({stage:"tokenizer", frac:0});
    const [vocab, merges] = await Promise.all([fetchText(`${base}/${TOKENIZER_FILES[0]}`), fetchText(`${base}/${TOKENIZER_FILES[1]}`)]);
    tokenizer = new ClipTokenizer(JSON.parse(vocab), merges, {pad:P.pad});
    const total = Object.values(P.files).reduce((n, m) => n + m.mb, 0); let done = 0;
    for (const [name, m] of Object.entries(P.files)){
      onProgress({stage:`downloading ${name}`, frac:done / total});
      sessions[name] = await makeSession(name, m, {...baseOpt, ...m.opt}, mb => onProgress({stage:`downloading ${name}`, frac:(done + Math.min(mb, m.mb)) / total, mb:Math.min(mb, m.mb), fileMb:m.mb, doneMb:done, totalMb:total}));
      onProgress({stage:`compiling ${name}`, frac:(done + m.mb) / total});
      done += m.mb; onProgress({stage:`loaded ${name}`, frac:done / total});
    }
    loaded = true; onProgress({stage:"ready", frac:1});
  }
  const tsTensor = t => timestepType === "int64" ? new ort.Tensor("int64", [BigInt(t)], [1]) : new ort.Tensor(timestepType, [t], [1]);
  // Returns {width, height, rgba}
  async function generate(prompt, {seed = null, steps = P.steps, guidance = P.guidance, onStep = () => {}} = {}){
    if (!loaded) throw new Error("illustrator not loaded");
    const rnd = seed == null ? Math.random : mulberry32(seed);
    const ids = tokenizer.encode(prompt);
    const {last_hidden_state} = await sessions.text_encoder.run({input_ids:new ort.Tensor("int32", Int32Array.from(ids), [1, ids.length])});
    const n = 4 * LAT * LAT, dims = [1, 4, LAT, LAT];
    let latent;
    if (P.scheduler === "euler1"){
      const SIGMA = 14.6146; latent = randn(n, SIGMA, rnd);
      const scaled = new Float32Array(n); const div = Math.sqrt(SIGMA * SIGMA + 1); for (let i = 0; i < n; i++) scaled[i] = latent[i] / div;
      const {out_sample} = await sessions.unet.run({sample:new ort.Tensor("float32", scaled, dims), timestep:tsTensor(999), encoder_hidden_states:last_hidden_state});
      const eps = out_sample.data; for (let i = 0; i < n; i++) latent[i] = (latent[i] - SIGMA * eps[i]) / VAE_SCALE;
    } else {
      latent = randn(n, 1, rnd);
      const ts = lcmTimesteps(steps); const wEmb = new ort.Tensor("float32", guidanceEmbedding(guidance - 1), [1, 256]);
      for (let s = 0; s < ts.length; s++){
        const t = ts[s];
        const {out_sample} = await sessions.unet.run({sample:new ort.Tensor("float32", latent, dims), timestep:tsTensor(t), encoder_hidden_states:last_hidden_state, timestep_cond:wEmb});
        const eps = out_sample.data; const a = ALPHAS_CUMPROD[t], b = 1 - a; const {c_skip, c_out} = lcmScalings(t);
        const last = s === ts.length - 1; const aPrev = last ? 1 : ALPHAS_CUMPROD[ts[s+1]], bPrev = 1 - aPrev;
        const noise = last ? null : randn(n, 1, rnd); const next = new Float32Array(n);
        for (let i = 0; i < n; i++){ const x0 = (latent[i] - Math.sqrt(b) * eps[i]) / Math.sqrt(a); const den = c_out * x0 + c_skip * latent[i]; next[i] = last ? den : Math.sqrt(aPrev) * den + Math.sqrt(bPrev) * noise[i]; }
        latent = next; onStep(s + 1, ts.length);
      }
      for (let i = 0; i < n; i++) latent[i] /= VAE_SCALE;
    }
    if (last_hidden_state.dispose) last_hidden_state.dispose();
    const {sample} = await sessions.vae_decoder.run({latent_sample:new ort.Tensor("float32", latent, dims)});
    const [, , H, W] = sample.dims; const px = sample.data; const rgba = new Uint8ClampedArray(W * H * 4);
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++){ const o = (y * W + x) * 4, i = y * W + x;
      rgba[o] = (px[i] / 2 + 0.5) * 255; rgba[o+1] = (px[H*W + i] / 2 + 0.5) * 255; rgba[o+2] = (px[2*H*W + i] / 2 + 0.5) * 255; rgba[o+3] = 255; }
    return {width:W, height:H, rgba};
  }
  async function unload(){ for (const s of Object.values(sessions)) try{ await s.release(); }catch{} for (const k in sessions) delete sessions[k]; loaded = false; }
  return {load, generate, unload, pipeline:P, get loaded(){ return loaded; }, tokenize:t => tokenizer?.encode(t)};
}
