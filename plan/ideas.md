# Ideas and Rubric

## Clear Identification of the Base Project and Its Original Scope

Student identifies the original project they are extending:

- Music Recommender Simulation

Student provides a short description of the original system's goal and capabilities.

    This project is a small, content-based music recommender that runs from the command line. It loads a 20-song catalog from `data/songs.csv`, where each song has a genre, a mood, and numeric traits (energy, valence, danceability, acousticness, and tempo). It compares every song to a user's taste profile (a favorite genre and mood, plus target values for each numeric trait). Numeric traits earn points for how *close* they are to the target, and a matching mood or genre earns a bonus. The points add up to a score out of 100, and the songs are ranked from highest to lowest. The top five are printed with a short list of reasons showing where each song's points came from. The project runs four sample profiles (Late-Night Study, High-Energy Pop, Chill Lofi, and Deep Intense Rock) so you can see how the weights and the catalog shape the results and where the system is biased.

Description is accurate and sets clear context for extensions.

    - I want to extend to music recommendation system to also include a journal for music therapy.
    - I'll try to introduce a UI that shows game information.

## Substantial New AI Feature Added (RAG, Agent, Specialization, or Reliability Mechanism)

Student adds at least one substantial AI feature such as RAG, a multi-step agent or planning workflow, specialized behavior (mini fine-tune or structured prompting), or a reliability harness (evaluation loop, guardrails, self-checking).
  
- Add RAG. I want to add a RAG system that can search a user's music listening journal and answer questions like "Which artists did I say I wanted to listen to more?" or "What was the reasons I liked songs?"

Feature is integrated into the working system (not an isolated demo).

- Put the output of answers in the command line for now. 

Feature is functional and produces meaningful changes in system behavior.

- This introduces a new behavior: taking information from a song journal. Adds a new feature that uses a new set of music journal data.

## System Architecture Diagram

Architecture diagram is submitted as a Mermaid source file (.mmd or embedded in a .md file); a PNG image alone is not sufficient.

- Level 1:
  - Extend the diagram to discuss the Retrieval and answer Generation.

- Level 2: Factor in journal information into the score somehow? TBD

Diagram clearly illustrates data flow (input, then processing steps, then output).

-  Show rag pipeline:  USer Query + Retrival + Context + Generation + Output

Diagram matches actual project implementation (not theoretical).

## Functional End-to-End System Demonstration

Student provides a working script or UI that demonstrates full system workflow.

README includes example commands and sample outputs in code blocks showing the system running end-to-end.

System responds consistently to at least 2-3 example inputs.

## Reliability, Evaluation, or Guardrail Component

**TODO:**  Review lecture for this topic.

System includes a reliability mechanism such as input validation, output guardrails, self-critique or multi-model agreement, or an evaluation script that tests sample inputs.

- Validate the input

Mechanism is functional and meaningfully improves reliability.

- Check this.

Student provides examples in markdown format (showing input, behavior, and result) demonstrating how the guardrail or evaluator behaves.

- Student provides examples in markdown format (showing input, behavior, and result) demonstrating how the guardrail or evaluator behaves.
