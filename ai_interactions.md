# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

**What task did you give the agent?**

I used Claude Code to implement the plan in `plan/plan.md` one phase at a time: reviews data, retriever and RAG, playlist agent, guardrails and logging, Streamlit UI, evaluation harness, prompt specialization, and finally the documentation and diagram.

**Prompts used:**

<!-- TODO: paste the key prompts you gave (for example the initial planning prompt in plan/plan.md and the "Implement Phase N" prompts). -->

**What did the agent generate or change?**

One commit per phase (see `git log`): `src/reviews.py`, `src/retriever.py`, `src/rag.py`, `src/agent.py`, `src/guardrails.py`, `src/logging_config.py`, `src/prompts.py`, `src/app.py`, `scripts/evaluate.py`, `scripts/compare_prompts.py`, `scripts/demo.py`, the tests in `tests/`, `diagrams/system_architecture.mmd`, and the README and model card updates.

**What did you verify or fix manually?**

<!-- TODO: describe what you checked or corrected yourself (for example live Gemini runs, model name fixes, reviewing refusals and citations). -->

---

## Agent Traces

The playlist agent appends every run to `logs/agent_traces.jsonl` (gitignored because it can hold user input). Each record has the plan, the tool calls, each draft, the rule check results and the critic score. Curated examples are committed so they can be read without running anything.

### Trace 1: offline stub LLM (full file: [logs/sample_trace_study.json](logs/sample_trace_study.json))

Request: `rainy Sunday studying, no vocals, 21 minutes`. The LLM steps here are the deterministic stub, so the plan and critic comment are canned. The tool calls and rule checks are the real code.

| Step | What happened |
|---|---|
| plan | profile: lofi/chill, energy 0.3, valence 0.5, danceability 0.5, acousticness 0.8, tempo 0.2, size 6, no excluded genres |
| tool:search_songs | `recommend_songs` ranked all 20 songs; top candidates were song IDs 4, 2, 6, 9, 17, 7 |
| tool:get_reviews | review snippets fetched for the candidates |
| draft (iteration 1) | picked song IDs 4, 2, 6, 9, 17, 7 |
| check (iteration 1) | no failures (size, duplicates, valid IDs, excluded genres all pass) |
| critique | score 0.8 (stub), final confidence 0.80 |

### Trace 2: a real failure from a live run

The first record in `logs/agent_traces.jsonl` on my machine is a live run that failed:

```json
{"description": "Give me a playlist to dance to", "status": "error", "confidence": 0.0,
 "trace": [{"step": "error", "error": "Gemini call failed: ClientError"}]}
```

The agent caught the API error, recorded it in the trace and returned a friendly error to the UI instead of crashing.

<!-- TODO: after a successful live run, paste a trace with a revision (a check failure fed back to the draft) here. -->

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

<!-- e.g., Strategy, Factory, Observer, etc. -->

**How did AI help you brainstorm or implement it?**

<!-- Describe the conversation or suggestions that led to your decision -->

**How does the pattern appear in your final code?**

<!-- Point to the relevant class or method -->
