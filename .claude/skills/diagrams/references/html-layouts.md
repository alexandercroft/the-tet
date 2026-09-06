# Diagrams in HTML artifacts

Purpose: how to build each diagram family inside an HTML page (a Claude
artifact or any standalone HTML file). This is the format where the "XMind
look" habit lived: a root node on the left with branches fanning to the right.
That layout is one variant of a mind map. It is correct for a topic with
unordered associations on a wide screen and wrong for everything else. Choose
the family and direction with `SKILL.md` first, then build it with the pattern
below.

Contents

1. Two ways to render: Mermaid block or hand-built markup
2. Shared rules for hand-built diagrams
3. Vertical flow (TD)
4. Horizontal flow (LR) and wrapped rows
5. Decision flowchart
6. Radial mind map (SVG, polar placement)
7. Logic chart: the XMind layout, and when it is right
8. Ring (cycle)
9. Tree and org chart
10. Grid: matrix, quadrant, dashboard
11. Swimlanes with real lanes
12. Timeline
13. Funnel and stack
14. Side-by-side comparison
15. XMind structure names mapped to families

---

## 1. Two ways to render

**Mermaid block.** Artifacts render Mermaid natively:

```html
<pre class="mermaid">
flowchart TD
  A([Start]) --> B{Paid?}
  B -->|Yes| C[Ship]
  B -->|No| D[Remind]
</pre>
```

Use it when the content is the point and the look is secondary. Every family
in `layout-catalog.md` works this way with no extra code. Default to this for
a first draft. Switch to hand-built markup only when the user asks for a
specific look, when the layout needs real lanes or a true circle, or when the
diagram is the centerpiece of the page.

**Hand-built markup.** HTML, CSS and inline SVG. Full control over placement,
colors and typography. More work, more room for layout mistakes. The patterns
in sections 3 to 14 cover each family.

Whichever way: one figure, one claim. Wrap the diagram in `<figure>` with a
`<figcaption>` that says what it shows.

## 2. Shared rules for hand-built diagrams

- **Boxes are HTML, connectors are SVG.** Text in HTML wraps and scales.
  Arrows need SVG. For simple TD and LR flows, arrows can be CSS
  pseudo-elements or a Unicode arrow between flex items. For anything with
  branches, draw an `<svg>` and place both boxes and lines inside it, or
  overlay an SVG on the box grid.
- **Size by `viewBox`.** `viewBox="0 0 W H"` with `width:100%; height:auto`.
  Pick W and H from the content: a TD diagram is taller than wide, an LR one
  wider than tall, a radial one square.
- **Theme-safe colors.** Strokes and text in `currentColor`. Node fills from
  CSS variables defined for light and dark. One accent color for the one thing
  the diagram is about. Never encode meaning in color alone: add a label, a
  dashed stroke, or a shape difference.
- **Arrowheads.** One `<marker id="arrow">` in `<defs>`, referenced by
  `marker-end="url(#arrow)"`. Never an image.
- **Grid.** Round every coordinate to a grid of 8 or 10 px. Equal gaps between
  peers. Equal box sizes for peers.
- **Text.** 12 to 14 px at the drawn scale. Labels 1 to 4 words. Explanations
  go in the caption.
- **Responsive.** Max width 100%, the page never scrolls horizontally. A wide
  LR diagram wraps into rows or switches to TD under 600 px. A diagram that
  cannot reflow (tree, lanes, logic chart) sits in a wrapper with
  `overflow-x:auto`, so only the figure scrolls.
- **No decoration.** No gradients, shadows or icons that do not carry meaning.
  A diagram that looks like a slide template reads as marketing, not as a
  mechanism.

Arrow marker used by every SVG sample below:

```html
<defs>
  <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5"
          markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0 0 L10 5 L0 10 z" fill="currentColor"/>
  </marker>
</defs>
```

## 3. Vertical flow (TD)

Flex column, boxes full width up to a max, arrows as short SVG lines or a
CSS-drawn connector between items. Best for phones, long labels, 4 to 10 steps.

```html
<style>
  .flow-td { display:flex; flex-direction:column; align-items:center; gap:0; max-width:420px; margin:auto; }
  .flow-td .node { border:1.5px solid currentColor; border-radius:6px; padding:10px 16px; width:100%; text-align:center; }
  .flow-td .node.terminal { border-radius:999px; }
  .flow-td .edge { width:2px; height:28px; background:currentColor; position:relative; }
  .flow-td .edge::after { content:""; position:absolute; left:-5px; bottom:-1px; border:6px solid transparent; border-top-color:currentColor; }
  .flow-td .edge[data-label]::before { content:attr(data-label); position:absolute; left:10px; top:4px; font-size:12px; white-space:nowrap; }
</style>
<div class="flow-td">
  <div class="node terminal">Request received</div>
  <div class="edge"></div>
  <div class="node">Check stock</div>
  <div class="edge" data-label="in stock"></div>
  <div class="node">Issue invoice</div>
  <div class="edge"></div>
  <div class="node terminal">Shipped</div>
</div>
```

## 4. Horizontal flow (LR) and wrapped rows

Flex row for up to 6 short steps. For more, wrap into rows of 4 to 5 and let
the last box of a row connect down to the first box of the next row (a
"snake" layout), or switch to TD.

```html
<style>
  .flow-lr { display:flex; align-items:center; flex-wrap:wrap; gap:8px; justify-content:center; }
  .flow-lr .node { border:1.5px solid currentColor; border-radius:6px; padding:10px 14px; min-width:110px; text-align:center; }
  .flow-lr .arrow { font-size:20px; line-height:1; }
  @media (max-width:600px) { .flow-lr { flex-direction:column; } .flow-lr .arrow { transform:rotate(90deg); } }
</style>
<div class="flow-lr">
  <div class="node">Receive</div><div class="arrow">→</div>
  <div class="node">Prepare</div><div class="arrow">→</div>
  <div class="node">Invoice</div><div class="arrow">→</div>
  <div class="node">Ship</div>
</div>
```

The media query turns the row into a column on narrow screens, and rotates the
arrows. This is the responsive rule from section 2 in practice.

## 5. Decision flowchart

Branches need real coordinates. Draw everything in one SVG. Main path runs
straight down the center, `No` branches go to the right and either rejoin or
loop back on the left. Diamonds are `<polygon>`. Labels on branches sit next
to the line start.

```html
<svg viewBox="0 0 520 420" role="img" aria-label="Payment check with reminder loop" style="max-width:520px;width:100%;height:auto;font-size:13px">
  <defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>
  <g fill="none" stroke="currentColor" stroke-width="1.5">
    <rect x="180" y="20" width="160" height="44" rx="22"/>
    <polygon points="260,110 340,150 260,190 180,150"/>
    <rect x="180" y="240" width="160" height="44" rx="6"/>
    <rect x="380" y="128" width="120" height="44" rx="6"/>
    <rect x="180" y="340" width="160" height="44" rx="22"/>
    <line x1="260" y1="64" x2="260" y2="108" marker-end="url(#arrow)"/>
    <line x1="260" y1="190" x2="260" y2="238" marker-end="url(#arrow)"/>
    <line x1="340" y1="150" x2="378" y2="150" marker-end="url(#arrow)"/>
    <line x1="260" y1="284" x2="260" y2="338" marker-end="url(#arrow)"/>
    <path d="M440 128 V86 H261"/>
  </g>
  <g fill="currentColor" text-anchor="middle">
    <text x="260" y="47">Invoice sent</text>
    <text x="260" y="154">Paid?</text>
    <text x="260" y="267">Ship</text>
    <text x="440" y="155">Send reminder</text>
    <text x="260" y="367">Done</text>
    <text x="272" y="222" text-anchor="start">Yes</text>
    <text x="350" y="142" text-anchor="start">No</text>
    <text x="300" y="80" text-anchor="start">after 3 days</text>
  </g>
</svg>
```

Coordinates: center column at x=260, rank spacing 100 px, branch column at
x=440. Compute, do not eyeball. The loop back from `Send reminder` joins the
main line above the diamond as a junction (no arrowhead) instead of crossing
the main arrow. A loop that must cross the main path is a sign to move the
branch to the other side or to route the loop around the outside.

## 6. Radial mind map (SVG, polar placement)

The center node sits at the middle. First-level branches are placed on a
circle with equal angular spacing. Each branch's children are placed on a
larger circle inside the angular sector of their parent. Compute positions,
never place by hand.

```html
<figure>
<svg id="mindmap" viewBox="0 0 720 720" role="img" aria-label="Personal brand: four areas and their parts" style="max-width:720px;width:100%;height:auto;font-size:13px"></svg>
<figcaption>Personal brand and its four areas. No order between branches.</figcaption>
</figure>
<script>
(function () {
  const data = { label: "Personal brand", children: [
    { label: "Content", children: ["Long posts", "Reels", "Carousels"] },
    { label: "Audience", children: ["Segments", "Pains", "Objections"] },
    { label: "Monetization", children: ["Consulting", "Course", "Community"] },
    { label: "Distribution", children: ["Telegram", "Instagram", "YouTube"] },
  ]};
  const svg = document.getElementById("mindmap");
  const cx = 360, cy = 360, r1 = 170, r2 = 300;
  const el = (n, a) => { const e = document.createElementNS("http://www.w3.org/2000/svg", n); for (const k in a) e.setAttribute(k, a[k]); return e; };
  const node = (x, y, text, big) => {
    const w = big ? 130 : 100, h = big ? 40 : 30;
    svg.appendChild(el("rect", { x: x - w/2, y: y - h/2, width: w, height: h, rx: h/2, fill: "var(--node, #fff)", stroke: "currentColor", "stroke-width": 1.5 }));
    const t = el("text", { x, y: y + 4.5, "text-anchor": "middle", fill: "currentColor" }); t.textContent = text; svg.appendChild(t);
  };
  const line = (x1, y1, x2, y2) => svg.appendChild(el("line", { x1, y1, x2, y2, stroke: "currentColor", "stroke-width": 1.5 }));
  const n = data.children.length;
  data.children.forEach((b, i) => {
    const a = -Math.PI/2 + i * 2*Math.PI/n;               // start at the top, go clockwise
    const bx = cx + r1*Math.cos(a), by = cy + r1*Math.sin(a);
    line(cx, cy, bx, by);
    const m = b.children.length, spread = (2*Math.PI/n) * 0.8;  // children stay inside the parent's sector
    b.children.forEach((c, j) => {
      const ca = a - spread/2 + (m === 1 ? spread/2 : j * spread/(m-1));
      const x = cx + r2*Math.cos(ca), y = cy + r2*Math.sin(ca);
      line(bx, by, x, y); node(x, y, c, false);
    });
    node(bx, by, b.label, true);
  });
  node(cx, cy, data.label, true);
})();
</script>
```

Rules: 3 to 7 branches, otherwise the sectors get too narrow. Draw lines
before nodes so boxes cover line ends. Longest label decides the box width.
If labels do not fit, shorten the labels, not the font.

## 7. Logic chart: the XMind layout, and when it is right

Root on the left, first-level branches in a column to the right, children
further right. This is XMind's "logic chart (right)". Build it as nested flex
rows: each node is a row with the label on the left and a column of children
on the right, connectors drawn with CSS borders.

```html
<style>
  .lc { overflow-x:auto; }
  .lc, .lc ul { display:flex; align-items:center; list-style:none; margin:0; padding:0; }
  .lc ul { flex-direction:column; align-items:flex-start; }
  .lc li { display:flex; align-items:center; position:relative; padding:3px 0 3px 16px; }
  .lc > ul > li { padding-left:0; }
  .lc .label { border:1.5px solid currentColor; border-radius:6px; padding:6px 12px; white-space:nowrap; }
  .lc li > ul { margin-left:28px; position:relative; }
  .lc li > ul::before { content:""; position:absolute; left:-12px; top:50%; width:12px; border-top:1.5px solid currentColor; }
  .lc li > ul > li::before { content:""; position:absolute; left:0; top:0; bottom:0; border-left:1.5px solid currentColor; }
  .lc li > ul > li:first-child::before { top:50%; }
  .lc li > ul > li:last-child::before { bottom:50%; }
  .lc li > ul > li:only-child::before { display:none; }
  .lc li > ul > li::after { content:""; position:absolute; left:0; top:50%; width:16px; border-top:1.5px solid currentColor; }
</style>
<div class="lc">
  <ul><li><span class="label">Personal brand</span>
    <ul>
      <li><span class="label">Content</span><ul><li><span class="label">Long posts</span></li><li><span class="label">Reels</span></li></ul></li>
      <li><span class="label">Audience</span><ul><li><span class="label">Segments</span></li><li><span class="label">Pains</span></li></ul></li>
      <li><span class="label">Monetization</span><ul><li><span class="label">Course</span></li><li><span class="label">Consulting</span></li></ul></li>
    </ul>
  </li></ul>
</div>
```

When it is right: a topic with unordered branches, wide screen, 2 to 3
levels, short labels. When it is wrong: any process (order is invisible), any
decision (branches cannot be labeled Yes/No), any cycle, anything with more
than 3 levels (runs off the right edge), anything read on a phone (rotate to
the tree in section 9 instead). This layout was the default before this skill.
It is now one option among the families, chosen only by the Step 1 table.

## 8. Ring (cycle)

Nodes on a circle, arrows along the arc between neighbors. Compute positions
with the same polar formula as section 6, radius fixed, angles equal. Arrows
are SVG `<path>` arcs (`A rx ry 0 0 1 x y`) shortened so they stop at the box
edge.

```html
<svg id="ring" viewBox="0 0 480 480" role="img" aria-label="Plan, do, check, act cycle" style="max-width:480px;width:100%;height:auto;font-size:14px">
  <defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>
</svg>
<script>
(function () {
  const steps = ["Plan", "Do", "Check", "Act"];
  const svg = document.getElementById("ring"), cx = 240, cy = 240, r = 160, n = steps.length;
  const el = (t, a) => { const e = document.createElementNS("http://www.w3.org/2000/svg", t); for (const k in a) e.setAttribute(k, a[k]); return e; };
  const pos = i => { const a = -Math.PI/2 + i*2*Math.PI/n; return [cx + r*Math.cos(a), cy + r*Math.sin(a), a]; };
  const gap = 0.22; // radians trimmed at both ends of each arc so it stops at the box
  for (let i = 0; i < n; i++) {
    const a1 = pos(i)[2] + gap, a2 = pos((i+1)%n)[2] - gap;
    const p = el("path", { d: `M${cx + r*Math.cos(a1)} ${cy + r*Math.sin(a1)} A${r} ${r} 0 0 1 ${cx + r*Math.cos(a2)} ${cy + r*Math.sin(a2)}`, fill: "none", stroke: "currentColor", "stroke-width": 1.5, "marker-end": "url(#arrow)" });
    svg.appendChild(p);
  }
  steps.forEach((s, i) => {
    const [x, y] = pos(i);
    svg.appendChild(el("rect", { x: x-55, y: y-20, width: 110, height: 40, rx: 8, fill: "var(--node, #fff)", stroke: "currentColor", "stroke-width": 1.5 }));
    const t = el("text", { x, y: y+5, "text-anchor": "middle", fill: "currentColor" }); t.textContent = s; svg.appendChild(t);
  });
})();
</script>
```

Clockwise from the top. 3 to 8 steps. An exit condition, if any, is a box
outside the ring connected from the step where the exit happens, with the
condition on the arrow.

## 9. Tree and org chart

Root on top, children in a row below, connectors from the parent's bottom
center to each child's top center. Nested flex columns with CSS connectors
work for 2 to 3 levels. Lines have no arrowheads.

```html
<style>
  .tree { overflow-x:auto; }
  .tree > ul { width:max-content; margin:0 auto; }
  .tree ul { display:flex; justify-content:center; list-style:none; padding:24px 0 0; margin:0; position:relative; }
  .tree li { display:flex; flex-direction:column; align-items:center; padding:0 10px; position:relative; }
  .tree li::before { content:""; position:absolute; top:-24px; height:24px; border-left:1.5px solid currentColor; }
  .tree > ul > li::before { display:none; }
  .tree li:not(:only-child)::after { content:""; position:absolute; top:-24px; left:0; right:0; border-top:1.5px solid currentColor; }
  .tree li:first-child::after { left:50%; }
  .tree li:last-child::after { right:50%; }
  .tree .label { border:1.5px solid currentColor; border-radius:6px; padding:6px 12px; white-space:nowrap; }
</style>
<div class="tree">
  <ul><li><span class="label">CEO</span>
    <ul>
      <li><span class="label">Marketing</span><ul><li><span class="label">Content</span></li><li><span class="label">Paid ads</span></li></ul></li>
      <li><span class="label">Product</span><ul><li><span class="label">Backend</span></li><li><span class="label">Design</span></li></ul></li>
      <li><span class="label">Finance</span></li>
    </ul>
  </li></ul>
</div>
```

Wide and shallow trees (one root, 8+ leaves) go on their side: the logic chart
from section 7 with lines instead of arrows.

## 10. Grid: matrix, quadrant, dashboard

CSS grid with named areas. A 2x2 matrix is a 3x3 grid: axis labels in the
first row and first column, four cells for the quadrants. Put items inside the
cells as a list. A dashboard-like block diagram (services in a fixed
arrangement) is the same grid with arrows drawn by an overlaid SVG.

```html
<style>
  .quad { display:grid; grid-template-columns:auto 1fr 1fr; grid-template-rows:auto 1fr 1fr; gap:4px; max-width:560px; aspect-ratio:1.1; }
  .quad .axis { font-size:12px; text-align:center; align-self:center; }
  .quad .axis.y { writing-mode:vertical-rl; transform:rotate(180deg); }
  .quad .cell { border:1.5px solid currentColor; padding:8px; }
  .quad .cell h4 { margin:0 0 4px; font-size:13px; }
  .quad .cell ul { margin:0; padding-left:16px; font-size:13px; }
</style>
<div class="quad">
  <div></div><div class="axis">Low effort</div><div class="axis">High effort</div>
  <div class="axis y">High reach</div>
  <div class="cell"><h4>Do first</h4><ul><li>Reels from old posts</li></ul></div>
  <div class="cell"><h4>Plan carefully</h4><ul><li>Long case study</li></ul></div>
  <div class="axis y">Low reach</div>
  <div class="cell"><h4>Drop</h4><ul><li>Daily stories</li></ul></div>
  <div class="cell"><h4>Batch later</h4><ul><li>Webinar</li></ul></div>
</div>
```

## 11. Swimlanes with real lanes

This is the one family HTML does better than Mermaid. CSS grid: one row per
role, one column per time step. The role name is a sticky first column. Each
step sits in the cell of its role and its time slot. Handoffs are arrows in an
overlaid SVG, or, simpler, a numbered order on the boxes plus a short arrow
glyph at the cell edge.

```html
<style>
  .lanes-wrap { overflow-x:auto; }
  .lanes { display:grid; min-width:560px; grid-template-columns:110px repeat(4, 1fr); gap:0; border:1.5px solid currentColor; }
  .lanes .role { padding:10px; border-right:1.5px solid currentColor; font-weight:600; display:flex; align-items:center; }
  .lanes .cell { padding:10px; min-height:64px; display:flex; align-items:center; }
  .lanes .row { display:contents; }
  .lanes .row:not(:last-child) > * { border-bottom:1.5px solid currentColor; }
  .lanes .step { border:1.5px solid currentColor; border-radius:6px; padding:6px 10px; font-size:13px; }
  .lanes .step small { display:block; opacity:.7; }
</style>
<div class="lanes-wrap"><div class="lanes">
  <div class="row"><div class="role">Client</div>
    <div class="cell"><div class="step"><small>1</small>Sends request</div></div>
    <div class="cell"></div>
    <div class="cell"><div class="step"><small>3</small>Confirms offer</div></div>
    <div class="cell"><div class="step"><small>5</small>Pays invoice</div></div>
  </div>
  <div class="row"><div class="role">Manager</div>
    <div class="cell"></div>
    <div class="cell"><div class="step"><small>2</small>Prepares offer</div></div>
    <div class="cell"></div>
    <div class="cell"></div>
  </div>
  <div class="row"><div class="role">Accounting</div>
    <div class="cell"></div>
    <div class="cell"></div>
    <div class="cell"><div class="step"><small>4</small>Issues invoice</div></div>
    <div class="cell"><div class="step"><small>6</small>Confirms payment</div></div>
  </div>
</div></div>
```

Columns are time slots, so a step that follows another goes one column to the
right even when the role changes. Up to 5 roles and 8 time slots. Beyond that,
split the process.

## 12. Timeline

Horizontal line with markers, labels alternating above and below to avoid
overlap. On narrow screens, a vertical line with entries on the right.

```html
<style>
  .tl { position:relative; display:flex; justify-content:space-between; padding:56px 0; }
  .tl::before { content:""; position:absolute; left:0; right:0; top:50%; border-top:2px solid currentColor; }
  .tl .ev { position:relative; flex:1; text-align:center; font-size:13px; }
  .tl .ev::before { content:""; display:block; width:12px; height:12px; border-radius:50%; background:currentColor; margin:0 auto; }
  .tl .ev span { position:absolute; left:0; right:0; }
  .tl .ev:nth-child(odd) span { bottom:22px; }
  .tl .ev:nth-child(even) span { top:22px; }
  @media (max-width:600px) { .tl { flex-direction:column; padding:0 0 0 24px; gap:20px; }
    .tl::before { top:0; bottom:0; left:5px; right:auto; border-top:0; border-left:2px solid currentColor; }
    .tl .ev { text-align:left; } .tl .ev::before { position:absolute; left:-24px; top:2px; margin:0; }
    .tl .ev span { position:static; } }
</style>
<div class="tl">
  <div class="ev"><span><b>Week 1</b><br>Announce</span></div>
  <div class="ev"><span><b>Week 2</b><br>Case studies</span></div>
  <div class="ev"><span><b>Week 3</b><br>Open sales</span></div>
  <div class="ev"><span><b>Week 4</b><br>Close, onboard</span></div>
</div>
```

## 13. Funnel and stack

Funnel: stacked bands whose widths follow the counts. Compute width as a
percentage of the top count. Put the count in the band and the conversion
between bands.

```html
<style>
  .funnel { display:flex; flex-direction:column; align-items:center; gap:4px; }
  .funnel .band { border:1.5px solid currentColor; padding:8px; text-align:center; font-size:13px; min-width:120px; }
  .funnel .drop { font-size:12px; opacity:.7; }
</style>
<div class="funnel">
  <div class="band" style="width:100%">Reach: 50 000</div><div class="drop">4 %</div>
  <div class="band" style="width:60%">Profile visits: 2 000</div><div class="drop">25 %</div>
  <div class="band" style="width:40%">Subscribers: 500</div><div class="drop">20 %</div>
  <div class="band" style="width:26%">Applications: 100</div><div class="drop">30 %</div>
  <div class="band" style="width:18%">Buyers: 30</div>
</div>
```

Real proportions (2000/50000 = 4 %) make the lower bands unreadable. Use a
compressed scale (for example square root of the share) and say so in the
caption.

Stack: full-width bands, foundation at the bottom, no arrows, no gaps.
Same markup as the funnel with `width:100%` on every band and `gap:0`.

## 14. Side-by-side comparison

Two columns on wide screens, stacked on narrow. Same family and direction in
both. The changed element gets the one accent color and a label.

```html
<style>
  .cmp { display:grid; grid-template-columns:1fr 1fr; gap:24px; }
  .cmp > figure { margin:0; }
  .cmp figcaption { font-weight:600; margin-bottom:8px; }
  .cmp .changed { border-color:var(--accent, #b8860b); box-shadow:inset 0 0 0 1.5px var(--accent, #b8860b); }
  @media (max-width:700px) { .cmp { grid-template-columns:1fr; } }
</style>
<div class="cmp">
  <figure><figcaption>Before</figcaption>
    <div class="flow-td"><div class="node">Client writes</div><div class="edge"></div><div class="node">Manager answers</div><div class="edge"></div><div class="node">Manager invoices</div><div class="edge"></div><div class="node">Manager checks payment</div></div>
  </figure>
  <figure><figcaption>After</figcaption>
    <div class="flow-td"><div class="node">Client writes</div><div class="edge"></div><div class="node changed">Bot answers and invoices</div><div class="edge"></div><div class="node changed">Payment auto-confirmed</div></div>
  </figure>
</div>
```

`.flow-td`, `.node` and `.edge` come from section 3.

## 15. XMind structure names mapped to families

The user may name a layout in XMind's vocabulary. Translate it, then check
with the Step 1 table whether that layout fits the content.

| XMind name            | Family here                  | Section                 |
|-----------------------|------------------------------|-------------------------|
| Mind map              | Mind map, radial             | 6                       |
| Logic chart (right)   | Mind map, one-sided          | 7                       |
| Logic chart (left)    | Mirror of 7, rarely useful   | 7                       |
| Brace map             | Whole and parts, one level   | 7 with lines, or a list |
| Org chart (down)      | Hierarchy                    | 9                       |
| Org chart (up)        | Convergence, bottom-up       | 9 flipped, or Mermaid BT|
| Tree chart            | Hierarchy, vertical lists    | 9                       |
| Timeline              | Timeline                     | 12                      |
| Fishbone              | Causes of one effect         | 6 or Mermaid LR into one node |
| Matrix                | Grid                         | 10                      |

If the user asks for "like XMind" without naming a structure, they usually
mean the logic chart. Confirm the family fits before using it.
