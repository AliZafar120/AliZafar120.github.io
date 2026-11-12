# Isekai Engine

A static, browser-only interactive-story engine. The model runs in the reader's
browser through WebGPU (WebLLM), or through any OpenAI-compatible API with the
reader's own key. No server, no accounts, nothing leaves the machine with the
local engine. Saves live in the browser's localStorage; Export downloads one.

## Files

- `index.html`: the whole app.
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
