# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

**What task did you give the agent?**

I used Claude Code to implement the plan in `plan/plan.md` one phase at a time: reviews data, retriever and RAG, playlist agent, guardrails and logging, Streamlit UI, evaluation harness, prompt specialization, and finally the documentation and diagram.

**Prompts used:**

I created an initial prompt based on what I wanted to make and the rubric criteria. I tweaked the plan for each phase and used it as a prompt while following up on prompts when I wanted more information how the model implemented the request. For example, asking "How can I fix error X" and reviewing potential recommendation and comparing with documentation. 

> I am working on my final project for an AI course. I want my project to extend the music recommender. My first idea is to extend the recommender by adding 1) song reviews to the data;  the 2) a rag system that lets answers questions about songs in the database using retrival and the gemini API, 3) an agentic work flow that will create a playlist based on a users description of what they want; 4) a user interface in streamlit for users to see the song library and chat with an agent. 
> Help me create a plan to implement this app that fits the project description and fulfills the the points in the rubric.  

**What did the agent generate or change?**

One commit per phase (see `git log`): `src/reviews.py`, `src/retriever.py`, `src/rag.py`, `src/agent.py`, `src/guardrails.py`, `src/logging_config.py`, `src/prompts.py`, `src/app.py`, `scripts/evaluate.py`, `scripts/compare_prompts.py`, `scripts/demo.py`, the tests in `tests/`, `diagrams/system_architecture.mmd`, and the README and model card updates.

**What did you verify or fix manually?**

I had to fix how the application called Gemini. Claude recommended the incorrect gemini model or the tier I was using. I checked the documentation and updated the code to use the correct model. 

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

### Trace 3: successful live run (full file: [logs/sample_trace_live.json](logs/sample_trace_live.json))

Request: `rainy Sunday studying, no vocals, 21 minutes`, real Gemini (`gemini-3.5-flash-lite`). This run did **not** trigger a revision: the rule checks passed on the first draft, so there is no check-failure-to-revision example yet.

| Step | What happened |
|---|---|
| plan | lofi/focused, energy 0.2, valence 0.3, acousticness 0.8, size 6, excluded genres from the model |
| tool:search_songs | top 15 candidates ranked by `recommend_songs` |
| tool:get_reviews | review snippets fetched for those 15 |
| draft (iteration 1) | picked song IDs 4, 9, 2, 15, 6, 17 |
| check (iteration 1) | no failures |
| critique | score 0.5: "Includes folk and classical tracks, violating the lofi/ambient requirement, and lacks track durations to verify the 21-minute runtime." |

The critic's complaint is a fair one: the catalog has no track lengths, so the "21 minutes" part of the request cannot actually be verified.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

<!-- e.g., Strategy, Factory, Observer, etc. -->

**How did AI help you brainstorm or implement it?**

<!-- Describe the conversation or suggestions that led to your decision -->

**How does the pattern appear in your final code?**

<!-- Point to the relevant class or method -->
