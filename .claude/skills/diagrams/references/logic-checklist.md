# Logic checklist for diagrams

Purpose: catch the errors that make a diagram wrong even when it renders. Run
every item before delivering. Each item has the check, an example of the
failure, and the fix. The short version lives in `SKILL.md`, Step 4.

Contents

1. Family matches the relationship
2. Direction matches meaning
3. Decisions are complete
4. Every path ends
5. Nodes are atomic and named consistently
6. Arrows mean one thing
7. Shapes mean one thing
8. Levels and peers
9. Size and grouping
10. Comparisons show the difference
11. Labels
12. Final read-through as a cold reader

---

## 1. Family matches the relationship

Check: the diagram family (Step 1 in `SKILL.md`) matches how the items relate.

Failure: "How to launch a course" drawn as a mind map with branches
`Announce`, `Warm up`, `Sell`, `Deliver`. The reader cannot tell that these
happen in order.

Fix: linear process or flowchart. Mind map only for the parts of one branch
that have no order (for example, the content formats inside `Warm up`).

Failure: an org chart drawn as a flowchart with arrows from the CEO down.
The arrows read as "the CEO does something to Marketing".

Fix: lines without arrowheads.

Failure: a message exchange between a user and a bot drawn as a flowchart.
The reader loses who sends what.

Fix: sequence diagram.

## 2. Direction matches meaning

Check: time, cause and data flow down or right. Growth goes up. Rank sits on
top. The whole diagram uses one main direction.

Failure: a funnel drawn LR. It reads as a pipeline, the shrinking is invisible.

Fix: TD, widest stage on top, counts in labels.

Failure: a 9-step process drawn LR with 5-word labels. The diagram is 2 000 px
wide and unreadable on a phone.

Fix: TD, or LR split into two rows with subgraphs.

Failure: a flowchart with `direction LR` in one subgraph and `TD` in another
with no reason. The eye changes reading direction mid-diagram.

Fix: one direction, unless a subgraph is a swimlane or a ring on purpose.

## 3. Decisions are complete

Check: every diamond has two or more exits. Every exit is labeled. Labels are
mutually exclusive and together cover all cases.

Failure: `{Paid?}` with one arrow to `Ship`. What happens when not paid?

Fix: add `No` exit to `Send reminder`, which loops back to the check or ends in
`Cancel`.

Failure: `{Budget?}` with exits `Small` and `Large`. Medium budgets have no
path.

Fix: exits `Under 50k`, `50k to 200k`, `Over 200k`, or two exits with a
threshold.

Failure: a decision written as an action: `[Check payment]` followed by two
unlabeled arrows.

Fix: `{Paid?}` as a diamond with `Yes` and `No` on the arrows.

## 4. Every path ends

Check: start from each start node and follow every arrow. Each path reaches an
end node or an explicitly labeled loop back to an earlier step.

Failure: a `No` branch leads to `Send reminder` and stops. The reader does not
know whether the process waits, retries or gives up.

Fix: `Send reminder` returns to `Paid?` with label `after 3 days`, and
`Paid?` gets a third exit `No, 3 reminders sent` to `Cancel`.

Failure: an orphan node `Legal review` with no arrows in or out.

Fix: connect it or remove it. A node that connects to nothing is not part of
the mechanism.

## 5. Nodes are atomic and named consistently

Check: one idea per node. Same thing, same name, one node. Verbs for actions,
questions for decisions, nouns for data and objects.

Failure: `[Prepare offer and send invoice and wait for payment]`.

Fix: three nodes in sequence. If they are one step for the reader, name the
step at the level the reader cares about: `[Close the deal]`, and put the three
substeps in a detail diagram.

Failure: `Order`, `The order`, `Client order` as three separate nodes.

Fix: one node `Order` with several incoming arrows.

Failure: mixed grammar: `Planning`, `Do the work`, `Checked`, `Act`.

Fix: `Plan`, `Do`, `Check`, `Act`.

## 6. Arrows mean one thing

Check: an arrow means "then", "causes", "sends" or "depends on", and the
diagram uses the same meaning everywhere. Where the meaning matters, the arrow
carries a label.

Failure: in an architecture diagram, `UI --> API` means "calls" and
`API --> DB` means "stores in", and neither is labeled.

Fix: `UI -->|POST /order| API`, `API -->|insert| DB`.

Failure: an arrow going up against the main direction with no label.

Fix: label it with the reason (`retry`, `changes requested`) or remove it.

Failure: a response drawn as a separate solid arrow next to the request, so the
pair looks like two independent flows.

Fix: one arrow labeled `request / response`, or a dashed arrow for the
response, or a sequence diagram.

## 7. Shapes mean one thing

Check: one shape per meaning across the whole diagram. Start and end are
stadiums, actions are rectangles, decisions are diamonds, storage is a cylinder.

Failure: rectangles for everything.

Fix: apply the shape table in `SKILL.md`, Step 3.

Failure: a hexagon used once "for variety".

Fix: remove it, or use it for every preparation step.

## 8. Levels and peers

Check: items of the same kind sit at the same level and use the same shape.
In a hierarchy, every child of one parent is the same kind of thing.

Failure: under `Marketing`: `Content`, `Paid ads`, `Anna`. Two departments and
a person at one level.

Fix: `Anna` goes under her department, or the chart shows only departments.

Failure: in a mind map, one branch with 12 children next to one with 1.

Fix: group the 12 into 3 or 4 sub-branches. Merge the lonely child into its
parent or find its siblings.

## 9. Size and grouping

Check: at most about 12 nodes in one diagram. More than that, group into
subgraphs or split into overview plus detail (catalog, section 19).

Failure: a 30-node flowchart of the whole business.

Fix: an overview with 5 phase nodes, then one detail diagram per phase.

Failure: crossing arrows that could be avoided.

Fix: reorder the siblings so that arrows to the same target are adjacent, or
switch TD and LR. Accept a crossing only after both fail.

## 10. Comparisons show the difference

Check: two options or before and after are drawn with the same family, the
same direction and the same node names. The difference is the only thing that
changes, and it is highlighted.

Failure: two boxes `Option A: agency` and `Option B: in-house` with bullet
points inside. This is a list, not a diagram.

Fix: draw the same process twice, with the extra hop, the removed hop or the
changed actor highlighted.

## 11. Labels

Check: node labels are 1 to 5 words. Arrow labels are 1 to 4 words. Full
sentences go into the caption or the text around the diagram.

Failure: `[The manager, after receiving the request from the client, checks
whether the requested items are available in the warehouse]`.

Fix: `[Check stock]`. The explanation goes into the text before the diagram.

Exception: a vertical timeline or a TD process meant for a phone can carry one
sentence per node, because the boxes become full-width rows.

## 12. Final read-through as a cold reader

Check: read the diagram top to bottom or left to right, without the text around
it. Answer these:

- What is this a picture of? (the family should be obvious in one glance)
- Where does it start and where does it end?
- At each diamond, what are my options?
- Is there anything I would have to guess?

If any answer needs the surrounding text, fix the diagram, not the text.
