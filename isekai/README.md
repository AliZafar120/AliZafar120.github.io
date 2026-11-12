# Isekai Engine

A static, browser-only interactive-story engine. The model runs in the reader's
browser through WebGPU (WebLLM), or through any OpenAI-compatible API with the
reader's own key. No server, no accounts, nothing leaves the machine with the
local engine. Saves live in the browser's localStorage; Export downloads one.

## Files

- `index.html`: the app.
- `illustrator.js`: in-browser scene illustrator (LCM Dreamshaper v7, 4 steps, 512px) on ONNX Runtime WebGPU, with its own CLIP tokenizer and LCM scheduler.
- `worlds/index.json`: list shown in the world picker. One entry per world:
  `{ "id", "title", "tagline", "genre" }`.
- `worlds/<id>.json`: a world card.

## World card

Required for every world:

| Field | Meaning |
|---|---|
| `id`, `title`, `genre` | Identity. `id` must match the file name. |
| `player_summary` | What the reader sees before starting. |
| `style` | One or two sentences of prose guidance for the narrator. |
| `reminder` | Rules pinned after every player message. Keep the "three numbered choices" rule, the UI parses them. |
| `characters[]` | `{ name, role, personality }`. |
| `opening` | The first scene, shown before the player types anything. |

Optional:

| Field | Meaning |
|---|---|
| `ai_plot` | Freeform worlds only: a private plot plan. Ignored when `story` exists. |
| `lore[]` | Short world facts given to the narrator every turn. |
| `state.flags[]` | Flags set at the start of a new game. |
| `story` | The event spine. Without it the world is freeform and no director runs. |
| `art_style` | Appended to every image prompt so a world's pictures share one look. |

`{{user}}` anywhere in text is replaced with "the player".

## Story spine

```
"story": {
  "acts":  [ { "id", "title", "events": ["e1", "e2", ...] }, ... ],
  "extra_flags": ["wounded", ...],
  "events": {
    "e1": {
      "title", "location", "npcs": [...],
      "summary":     what happens in this event,
      "goal":        when the director may mark it complete,
      "max_turns":   hard cap; the event ends here even if the goal is unmet,
      "forbid":      things the narrator must not do yet,
      "on_complete": ["flag", ...]   set when the event ends,
      "variants":    [ { "when": ["flag", ...], "summary_add": "..." } ],
      "pivot":       { "id", "when", "options": [ { "id", "label", "sets": ["flag"] } ] },
      "final":       true on the last event
    }
  }
}
```

How it plays out each turn:

1. The narrator gets the world card, the opening, the last 14 messages, and a
   bracketed director brief: current event, goal, forbid, turn N of max, flags,
   the last 10 memory notes, and the pivot options when a pivot is pending.
2. The director reads the new scene and returns JSON: `event_complete`,
   `pivot_choice`, `set_flags` (only flags the world defines), a one-line
   `memory_note`, and an `image_prompt` for a future illustrator.
3. The event advances when the goal is met or turns run out, but never while
   its pivot is unresolved. A pending pivot shows three highlighted buttons;
   clicking one applies its flags deterministically. Free text is mapped to an
   option by the director if the player clearly committed.
4. Variants whose `when` flags are all set have their `summary_add` appended
   to the event summary, which is how pivots change later events.

Design rule: ordinary choices change the scene, relationships and memory notes.
Only pivots change the spine. Keep two to four pivots per story.

## Authoring tips

- Three to five turns per event. Twelve events is a two-hour story.
- Every flag used in a `variants[].when` must be set somewhere: `on_complete`,
  a pivot `sets`, or listed in `extra_flags` so the director may set it.
- Put the pivot in an event with `max_turns` of at least 3 so the scene has a
  turn to build before the choice is forced.
- `forbid` is the main tool against a small model jumping ahead. Name the
  later reveals explicitly.

## Storage panel

"Storage on this device" in the engine card lists what the browser holds for
the site: cached text models (WebLLM's cache), the illustrator's ONNX files,
generated images per world, and saved stories, each with its size and a Clear
button. Loaded models also get an "Unload from GPU" button. "Clear everything"
removes all of it; models then download again on the next load.

## Illustrator

Pick an illustrator in the engine panel and load it. Each turn the director's
`image_prompt` plus the world's `art_style` is rendered to a 512px image and
shown under the scene. Images are kept in the browser's IndexedDB per world and
cleared by New game. Older scenes without a picture get an "Illustrate this
scene" button.

Requirements and limits:

- WebGPU with the `shader-f16` feature. Chrome or Edge on a desktop GPU.
- About 2.1 GB of model download, cached by the browser after the first load.
- Roughly 8 GB of GPU memory to hold the text model and the illustrator together.

Licensing: LCM Dreamshaper v7 is MIT, its base Dreamshaper 7 is CreativeML
OpenRAIL-M. Both allow hosted and commercial use, with OpenRAIL's use-based
restrictions on harmful content. The module also carries an SD-Turbo config
for reference, unused by the page, because Stability's non-commercial license
forbids offering it through a hosted service.

The LCM scheduler and guidance embedding follow diffusers' LCMScheduler and
LatentConsistencyModelPipeline. The headless tests in the project's work
folder run the same module on CPU with onnxruntime-node and check the
tokenizer against Transformers.js.
