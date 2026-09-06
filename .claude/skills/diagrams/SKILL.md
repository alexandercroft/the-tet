---
name: diagrams
description: Build flowcharts, block diagrams, mind maps, process maps, decision trees, cycles, hierarchies, org charts, timelines, matrices, funnels, swimlanes, sequence and state diagrams. Picks the diagram type, direction (top-down, left-to-right, bottom-up, radial, circular, grid) and node shapes from the structure of the content instead of one default template. Use whenever the user asks for a блок-схема, схема, диаграмма, майнд-карта, ментальная карта, карта процесса, дерево решений, воронка, цикл, таймлайн, оргструктура, архитектура, mind map, flowchart, process map, decision tree, funnel, timeline, org chart, architecture diagram, or says "нарисуй", "покажи схемой", "визуализируй", "изобрази", "draw", "map out", "sketch the flow", "diagram this" — even without naming a diagram type. Also use when an answer describes a process, hierarchy, cycle, or comparison that a reader would grasp faster as a picture.
---

# Diagrams

Purpose of this skill: choose the diagram type, direction and shapes from the
content. Do not reuse one layout (the horizontal left-to-right mind map) for
everything. A mind map drawn for a process loses the order of steps. A process
drawn left-to-right with long labels runs off the screen. A hierarchy drawn with
arrows reads as a flow. Each of these is a logic error, not a style choice.

Every diagram goes through the five steps below. The tables in this file cover
the common cases. The files in `references/` hold the full catalog, the full
logic checklist, Mermaid syntax, and plain-text templates.

## Step 1. Classify the content

Ask one question first: what is the relationship between the items?
The answer picks the diagram family. The family picks the default direction.

| The content is...                                        | Family                      | Default direction                                   |
|----------------------------------------------------------|-----------------------------|-----------------------------------------------------|
| Steps in order, one path, no branches                    | Linear process              | LR if 6 or fewer short steps, otherwise TD           |
| Steps with yes/no branches, checks, retries              | Flowchart with decisions    | TD                                                   |
| Rules: if X then Y, else Z                               | Decision tree               | TD. LR only when 4+ levels deep and labels are short |
| Steps that repeat and return to the start                | Cycle                       | Ring, clockwise (`block-beta` grid or state diagram)   |
| Whole and its parts, who reports to whom                 | Hierarchy, org chart, tree  | TD. LR when wide and shallow                         |
| A topic and its associations, no order between them      | Mind map                    | Radial (center node, branches around it)             |
| Many-to-many links, who talks to whom                    | Network, relationship map   | No fixed direction, lines without arrowheads         |
| Data or requests moving between components               | Data flow, architecture     | LR for pipelines. TD for layered stacks               |
| Events placed in time                                    | Timeline                    | LR. TD when entries carry long descriptions          |
| Actors exchanging messages in order                      | Sequence diagram            | Actors across the top, time runs down                |
| One object switching between modes                       | State diagram               | LR for up to 5 states, TD for more                   |
| Items scored on two independent criteria                 | 2x2 matrix, quadrant        | Grid                                                 |
| Stages where the count shrinks (visitors to buyers)      | Funnel                      | TD, widest stage on top                              |
| Several roles each doing their own steps                 | Swimlanes                   | Sequence diagram (roles on top) or color per role     |
| Before vs after, option A vs option B                    | Side-by-side comparison     | Two diagrams, same layout, the difference highlighted |
| Layers built on top of each other                        | Stack                       | TD with the foundation at the bottom                 |
| Many inputs combine into one result                      | Convergence                 | LR or BT, many nodes into one                        |
| One source feeds many targets                            | Fan-out, hub and spoke      | TD or radial                                         |
| Quantities that split and merge                          | Sankey                      | LR                                                   |

If the content mixes two families (a process where one step is a hierarchy),
draw the dominant family and put the other one in a second, smaller diagram.
Do not merge them into one picture.

Full catalog with a working Mermaid sample for each family:
`references/layout-catalog.md`.

## Step 2. Choose the direction

Apply in this order. The first rule that applies decides.

1. **Meaning.** Time, cause and data move down or right. Growth and
   building up move bottom-to-top (BT). Importance and rank sit at the top.
   Right-to-left (RL) is only for a mirrored comparison next to an LR diagram.
2. **Shape of the graph.** One node with 3 or more children reads best TD, the
   children line up under the parent. A chain of 7 or more nodes goes TD, or LR
   broken into rows with subgraphs. Deep and narrow goes LR. Wide and shallow
   goes TD.
3. **Label length.** Labels longer than 3 words push the diagram to TD, because
   wide boxes stacked vertically stay inside the screen. Short labels allow LR.
4. **Where it is viewed.** Phone, Telegram, Notion column: TD. Slide, wide
   dashboard: LR. README or code comment: plain text, 80 characters wide max.
5. **Consistency.** Inside one document, diagrams of the same family keep the
   same direction.

Do not pick LR because the previous diagram was LR. Do not mix directions inside
one flowchart unless each subgraph sets its own `direction` on purpose.

## Step 3. Choose shapes by meaning

One shape means one thing across the whole diagram. Shapes are not decoration.

| Meaning                              | Shape                   | Mermaid            |
|--------------------------------------|-------------------------|--------------------|
| Start, end                           | Stadium (pill)          | `A([Start])`       |
| Action, process step                 | Rectangle               | `A[Send invoice]`  |
| Decision, question                   | Diamond                 | `A{Paid?}`         |
| Input or output, document, data      | Parallelogram           | `A[/Order form/]`  |
| Database, storage                    | Cylinder                | `A[(Orders DB)]`   |
| Subprocess defined elsewhere         | Double-bordered box     | `A[[Verify KYC]]`  |
| Preparation, setup                   | Hexagon                 | `A{{Load config}}` |
| Event, connector, small state        | Circle                  | `A((Event))`       |
| Final state (state diagrams)         | Double circle           | `A(((Done)))`      |
| Manual step                          | Trapezoid               | `A[/Sign paper\]`  |
| Soft grouping, optional step         | Rounded rectangle       | `A(Optional)`      |

Mind maps use one shape for all nodes. Hierarchies and networks use lines
without arrowheads (`---`), because an arrowhead means flow, cause or time.

## Step 4. Run the logic checklist

Before delivering, check every item. These are the errors that made earlier
diagrams wrong.

- Every diamond has at least two exits, and every exit is labeled
  (`Yes`, `No`, or the condition).
- Every path from Start reaches an End or an explicitly labeled loop back.
- No orphan nodes. No two nodes that mean the same thing under different names.
- Arrows point in the direction of time, cause or data. An arrow that goes
  against the main direction is a loop and carries a label saying why.
- Action nodes are verbs (`Send invoice`). Decision nodes are questions
  (`Paid?`). Data and objects are nouns (`Order form`).
- One idea per node. A node that needs "and" is two nodes.
- Peer items sit at the same level and use the same shape.
- A mind map branch holds parts or aspects of its parent, never steps in order.
  Steps in order are a flowchart.
- More than 12 nodes: group into subgraphs, or split into an overview diagram
  plus detail diagrams.
- Crossing arrows: reorder siblings or change direction first. Accept a
  crossing only when both fail.
- Labeled arrows where the relation matters: `writes`, `polls every 30 s`,
  `escalates to`. An unlabeled arrow means only "then".

Full checklist with failure examples and fixes:
`references/logic-checklist.md`.

## Step 5. Pick the render format for the target

| Target                                                 | Format                                                         |
|--------------------------------------------------------|----------------------------------------------------------------|
| Chat reply, Notion page, GitHub markdown, Obsidian     | Mermaid in a ```` ```mermaid ```` fence                           |
| HTML artifact                                          | `<pre class="mermaid">` block for a draft, hand-built HTML/SVG per `references/html-layouts.md` for the final look |
| README, code comment, Telegram post, any plain text    | Box-drawing characters, see `references/ascii-diagrams.md`      |
| FigJam board                                           | Figma MCP `generate_diagram`, same structure as the Mermaid draft |
| Miro board                                             | Miro canvas tools, same structure as the Mermaid draft          |
| Image file (PNG, SVG, PDF)                             | `mmdc` CLI, see the cheatsheet                                  |

Mermaid syntax, direction keywords, subgraphs, styling, and differences between
renderers: `references/mermaid-cheatsheet.md`. When the renderer version is
unknown (Notion, older wikis), avoid `-beta` diagram types and the
`A@{ shape: ... }` syntax. Plain `flowchart`, `mindmap`, `sequenceDiagram`,
`stateDiagram-v2` and `timeline` are safe.

## HTML artifacts and the XMind habit

Most diagrams for this user are delivered as HTML artifacts. Before this skill,
every HTML diagram used one layout: root on the left, branches fanning to the
right (XMind's "logic chart"). That is one variant of a mind map. It fits a
topic with unordered associations on a wide screen and nothing else. In HTML,
run Steps 1 to 4 exactly as for Mermaid, then build the chosen family with the
matching pattern in `references/html-layouts.md`: vertical and horizontal flows,
decision flowcharts in SVG, radial mind maps with computed polar positions,
rings, trees, grids, real swimlanes, timelines, funnels, comparisons. Use the
logic chart only when Step 1 says mind map and the screen is wide.

## Delivering

Write one line before the diagram: the family, the direction, and the reason.
Example: `Decision tree, top-down: three rules, each with two branches, labels
are long.` If two layouts fit equally well, name the alternative in one
sentence. Do not draw both unless asked.

Node labels follow the language of the user's content. Everything else in this
skill and its files is English.

## Anti-patterns

- Every diagram drawn as a horizontal mind map.
- A process drawn as a mind map, so the order of steps is lost.
- A hierarchy drawn with arrows, so it reads as a flow.
- A decision diamond with unlabeled exits, or with one exit.
- Rectangles for everything, including start, end and decisions.
- A "comparison" that is two boxes with option names and nothing that shows
  what differs between them.
- Ten nodes in one horizontal row.
- A cycle drawn as a straight line with one long arrow back to the start.
- Shapes chosen for variety instead of meaning.

## Files in this skill

- `references/layout-catalog.md`. One section per family: when to use it, the
  direction, a working Mermaid sample, common mistakes. Read it when the family
  is not obvious or the family is rare (swimlanes, funnel, sankey, quadrant).
- `references/logic-checklist.md`. The full checklist with wrong and fixed
  examples.
- `references/mermaid-cheatsheet.md`. Shapes, arrows, subgraphs, direction,
  styling, other diagram types, renderer differences, export to image.
- `references/ascii-diagrams.md`. Templates for plain-text diagrams in every
  direction.
- `references/html-layouts.md`. How to build each family in an HTML artifact:
  CSS and SVG patterns per family, the polar formula for radial and ring
  layouts, real swimlanes with CSS grid, XMind structure names mapped to
  families. Read it whenever the output is an HTML page.
