# Plain-text diagrams

Purpose: templates for diagrams in places that do not render Mermaid: README
files, code comments, Telegram posts, plain email, terminal output. Copy the
template for the family and direction chosen in `SKILL.md`, then replace the
labels.

Rules

- Monospace only. Put the diagram in a ```` ```text ```` fence in markdown.
  In Telegram use a code block (three backticks) so spacing survives.
- Width limit: 80 characters for README and code. 40 characters for Telegram
  on a phone. Measure the longest line.
- Box-drawing characters: `┌ ┐ └ ┘ │ ─ ├ ┤ ┬ ┴ ┼` for boxes, `▶ ▼ ◀ ▲` for
  arrowheads. ASCII fallback for places that break Unicode: `+ - |` for boxes
  and `> v < ^` for arrowheads.
- Every box is the same width inside one diagram. Pad labels with spaces.
- Align box edges on a grid. A one-column offset reads as sloppy.
- Labels 1 to 3 words. Longer text goes below the diagram.
- Do not draw more than 8 boxes in plain text. Above that, export a PNG.

Contents

1. Vertical process (TD)
2. Horizontal process (LR)
3. Decision with two branches
4. Cycle
5. Hierarchy or tree
6. Mind map (text outline)
7. Layered stack
8. Fan-out and convergence
9. Before and after
10. Table as a diagram substitute

---

## 1. Vertical process (TD)

Use for 4 to 8 steps, long labels, phone screens.

```text
┌────────────────────┐
│  Receive request   │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│   Prepare offer    │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│   Issue invoice    │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│       Ship         │
└────────────────────┘
```

## 2. Horizontal process (LR)

Use for up to 5 steps with short labels, README width.

```text
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ Receive │───▶│ Prepare │───▶│ Invoice │───▶│  Ship   │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
```

Labeled arrows: put the label above the arrow.

```text
┌─────────┐  POST /order  ┌─────────┐   insert   ┌─────────┐
│   UI    │──────────────▶│   API   │───────────▶│   DB    │
└─────────┘               └─────────┘            └─────────┘
```

## 3. Decision with two branches

Plain text has no diamond. Write the question in a box and label the two
exits. The main path continues down, the alternative goes to the side.

```text
┌────────────────────┐
│    Check payment   │
└─────────┬──────────┘
          ▼
     ┌─────────┐   No    ┌──────────────┐
     │  Paid?  │────────▶│ Send reminder│
     └────┬────┘         └──────┬───────┘
          │ Yes                 │ after 3 days
          ▼                     │
┌────────────────────┐          │
│        Ship        │◀─────────┘ (back to Paid?)
└────────────────────┘
```

When the loop-back arrow would cross other lines, write the loop as a text
note instead of drawing it: `Send reminder → back to "Paid?" after 3 days`.

## 4. Cycle

Four steps as a square ring, clockwise from the top left.

```text
┌─────────┐        ┌─────────┐
│  Plan   │───────▶│   Do    │
└─────────┘        └────┬────┘
     ▲                  │
     │                  ▼
┌────┴────┐        ┌─────────┐
│   Act   │◀───────│  Check  │
└─────────┘        └─────────┘
```

ASCII-only version:

```text
+---------+        +---------+
|  Plan   |------->|   Do    |
+---------+        +----+----+
     ^                  |
     |                  v
+----+----+        +---------+
|   Act   |<-------|  Check  |
+---------+        +---------+
```

## 5. Hierarchy or tree

Root on top, children indented. Use the tree form for anything deeper than
two levels, it is the only plain-text form that stays readable.

```text
Company
├── Marketing
│   ├── Content
│   └── Paid ads
├── Product and tech
│   ├── Backend
│   └── Design
└── Finance
```

Two levels, drawn with boxes:

```text
                  ┌─────────┐
                  │   CEO   │
                  └────┬────┘
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
   ┌───────────┐ ┌───────────┐ ┌───────────┐
   │ Marketing │ │  Product  │ │  Finance  │
   └───────────┘ └───────────┘ └───────────┘
```

Note: the arrowheads here are a plain-text compromise. In Mermaid, hierarchy
lines have no arrowheads.

## 6. Mind map (text outline)

Plain text cannot draw radial. Write an outline with the center as the title.
Same rules as the Mermaid mind map: 3 to 7 branches, 2 to 6 children each.

```text
PERSONAL BRAND
  • Content: long posts, reels, carousels
  • Audience: segments, pains, objections
  • Monetization: consulting, course, community
  • Distribution: Telegram, Instagram, YouTube
```

## 7. Layered stack

Foundation at the bottom. Boxes touch, no arrows.

```text
┌──────────────────────────────┐
│   Traffic: ads, collabs      │
├──────────────────────────────┤
│   Content: posts, reels      │
├──────────────────────────────┤
│   Product: offer, price      │
├──────────────────────────────┤
│   Foundation: positioning    │
└──────────────────────────────┘
```

## 8. Fan-out and convergence

Fan-out, one source to many targets:

```text
                ┌──────────────┐
                │  Long post   │
                └──────┬───────┘
      ┌────────┬───────┼───────┬────────┐
      ▼        ▼       ▼       ▼        ▼
   3 reels  carousel  email  stories  thread
```

Convergence, many inputs to one result:

```text
Audience analysis ──┐
Competitor review ──┼──▶ ┌─────────┐
Own cases ──────────┤    │  Offer  │
Price test ─────────┘    └─────────┘
```

## 9. Before and after

Same layout twice, one above the other, the changed step marked.

```text
BEFORE
┌─────────┐   ┌──────────────┐   ┌──────────────┐   ┌───────────────┐
│ Client  │──▶│ Manager      │──▶│ Manager      │──▶│ Manager       │
│ writes  │   │ answers      │   │ sends invoice│   │ checks payment│
└─────────┘   └──────────────┘   └──────────────┘   └───────────────┘

AFTER
┌─────────┐   ┌──────────────┐   ┌──────────────┐
│ Client  │──▶│ Bot answers  │──▶│ Payment      │
│ writes  │   │ and invoices │   │ auto-checked │
└─────────┘   └──────────────┘   └──────────────┘
               ^^^ changed        ^^^ changed
```

## 10. Table as a diagram substitute

A markdown table beats a plain-text diagram for: a 2x2 matrix, a comparison of
options on several criteria, a state table (state, event, next state), and a
funnel with numbers. Use it when the plain-text drawing would exceed 8 boxes
or 80 characters.

```text
| State      | Event              | Next state |
|------------|--------------------|------------|
| New        | first call         | Contacted  |
| Contacted  | fits the segment   | Qualified  |
| Contacted  | no fit             | Lost       |
| Qualified  | paid               | Won        |
```
