# Project Description

This final project is your opportunity to bring everything together, from debugging and design (Module 1-2) to reasoning and retrieval (Module 3-4), and finally agentic workflows and reliability testing (Module 5).

You'll choose one of your previous projects from Modules 1-3 and extend it into a full applied AI system that solves a meaningful problem or automates a reasoning task. This is your chance to evolve an earlier prototype into a polished, professional artifact.

Your system should demonstrate responsible design, technical creativity, and clear explanation of how the AI works and why it's trustworthy.


## ⚙️ Project Requirements
Your final project is about taking what you've already built and making it stronger, smarter, and more reliable. You'll extend one of your previous projects (from Modules 1-3) into a complete applied AI system.



### 1. Functionality: What Your System Should Do
Your project should do something useful with AI. For example:

Summarize text or documents
Retrieve information or data from a source
Plan and complete a step-by-step task
Help debug, classify, or explain something
To make your project more advanced, it must include at least one of the following AI features:

Feature	What It Means	Example
Retrieval-Augmented Generation (RAG)	Your AI looks up or retrieves information before answering.	A study bot that searches notes before generating a quiz question.
Agentic Workflow	Your AI can plan, act, and check its own work.	A coding assistant that writes, tests, and then fixes code automatically.
Fine-Tuned or Specialized Model	You use a model that’s been trained or adjusted for a specific task.	A chatbot tuned to respond in a company’s tone of voice.
Reliability or Testing System	You include ways to measure or test how well your AI performs.	A script that checks if your AI gives consistent answers.
The feature should be fully integrated into the main application logic. It is not enough to have standalone script; the feature must meaningfully change how the system behaves or processes information. For example, if you add RAG, your AI should actively use the retrieved data to formulate its response rather than just printing the data alongside a standard answer.

Also, make sure your project:

Runs correctly and reproducibly: If someone follows your instructions, it should work.
Includes logging or guardrails: Your code should track what it does and handle errors safely.
Has clear setup steps: Someone else should be able to run it without guessing what to install.

### 2. Design and Architecture: How Your System Fits Together
Show how your project is organized by creating a short system diagram. Your diagram should include:

The main components (like retriever, agent, evaluator, or tester).
How data flows through the system (input, then process, then output).
Where humans or testing are involved in checking AI results.
Submit your diagram as a Mermaid source file (.mmd) or a Markdown (.md) file containing Mermaid syntax — do not submit it only as a screenshot or image. This lets the diagram's structure be read directly from the source.

### 3. Documentation: How You Explain Your Work
You'll write a README file that clearly explains your project. It should include:

Explicitly name your original project (from Modules 1-3) and provide a 2-3 sentence summary of its original goals and capabilities.
Title and Summary: What your project does and why it matters.
Architecture Overview: A short explanation of your system diagram.
Setup Instructions: Step-by-step directions to run your code.
Sample Interactions: Include at least 2-3 examples of inputs and the resulting AI outputs to demonstrate the system is functional.
Design Decisions: Why you built it this way, and what trade-offs you made.
Testing Summary: What worked, what didn't, and what you learned.
Reflection: A brief note on what this project taught you about AI and problem-solving. Your graded responsible-AI reflection — how you collaborated with AI, one suggestion you accepted and one you rejected or revised, and your system's limitations — goes in model_card.md (see Step 5), not here. Reflection content placed only in the README does not earn the reflection points.
Write this for a future employer who might look at your GitHub portfolio! Clarity and completeness matter more than perfection.

### 4. Reliability and Evaluation: How You Test and Improve Your AI
Your AI should prove that it works, not just seem like it does. Include at least one way to test or measure its reliability, such as:

Automated tests (e.g., unit tests or simple checks for key functions).
Confidence scoring (the AI rates how sure it is).
Logging and error handling (your code records what failed and why).
Human evaluation (you or a peer review the AI's output).
Summarize your testing in a few lines, like:

5 out of 6 tests passed; the AI struggled when context was missing. Confidence scores averaged 0.8; accuracy improved after adding validation rules.

If you use human evaluation, document it in a parseable format such as a markdown table or structured text/JSON so your results can be read without watching a demo. For example:
Test Input	Evaluation Criteria	Result
"Summarize this article"	Accurate, under 100 words	Pass
Empty input	Handles gracefully	Fail — crashed
Put evaluation tables or structured test logs in README.md or model_card.md; keep them text-based and parseable, not screenshots

### 5. Reflection and Ethics: Thinking Critically About Your AI
AI isn't just about what works -- it's about what's responsible. Document your reflection in model_card.md under clearly labeled section headers, answering the following questions:

What are the limitations or biases in your system?
Could your AI be misused, and how would you prevent that?
What surprised you while testing your AI's reliability?
describe your collaboration with AI during this project. Identify one suggestion you accepted and one you did not accept as written, and say why you rejected or changed it. It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for your system all count. If nothing the AI suggested was outright wrong, look for one you still changed: shortened, simplified, renamed, or scoped down. That counts.
🚀 Optional: Stretch Features for Extra Points
These features are completely optional and go beyond the required 21 points. Completing them can earn up to +8 additional points, allowing your score to exceed 100%. See the Grading Rubric for how each is evaluated.

Feature	What To Build	Points
RAG Enhancement	Extend your retrieval system to use custom documents or multiple data sources. Document the improvement in your README.md or model_card.md — a before/after example or a short written description of how retrieval improved your output.	+2
Agentic Workflow Enhancement	Implement multi-step reasoning with tool-calls, planning steps, or a decision-making chain. Save the intermediate reasoning traces to ai_interactions.md (embed them, or link a committed log file from it).	+2
Fine-Tuning or Specialization	Demonstrate specialized model behavior using few-shot patterns, synthetic datasets, or constrained tone/style. Show that output measurably differs from the baseline.	+2
Test Harness or Evaluation Script	Build a script that runs your system on a set of predefined inputs and prints a summary (pass/fail scores, confidence ratings, or similar).	+2
Note: These stretch features build directly on the required AI feature you chose in Step 1. For example, if you added RAG as your required feature, the RAG Enhancement stretch would extend that same component further.

### 6. Presentation and Portfolio: Sharing Your Work Professionally
You'll wrap up by sharing your final project.

Prepare a 5-7 minute presentation showing your system, demo, and what you learned.
Add a portfolio artifact:
A GitHub link to your code
A short reflection paragraph: What this project says about me as an AI engineer.
Include reproducible execution evidence in your README (required): So your system can be graded without watching a video, your README.md must include, in markdown (code blocks or generated .txt logs):
Sample command executions
Example inputs
Example outputs
Reliability/guardrail results
Record a Loom video walkthrough (optional, for human reviewers): A short walkthrough showing your system running end-to-end is encouraged for human reviewers. To record, we recommend using Loom. Include the link in your README. Grading is based on the text-based evidence above, not the video.
[IMPORTANT]
To receive an accurate grade, make sure your text-based execution evidence in the README clearly demonstrates:

✅ End-to-end system run (2–3 inputs)
✅ AI feature behavior (RAG, agent, etc.)
✅ Reliability/guardrail or evaluation behavior
✅ Clear outputs for each case
If you include a Loom video, it does not need to show code setup, file structure, or installation steps.

If you are unsure about including something, consult the Grading Rubric.

📬 Submitting Your Project
Once you've completed all the required features for your project, use the following checklist to prepare your work for submission.

Code is pushed to the correct GitHub repository
Repo is public
Required files are present: You must include your runnable functional code, a comprehensive README.md, a model_card.md for reflections, and a System Architecture Diagram saved as a Mermaid source file (.mmd or .md with Mermaid code block) in a diagrams/ folder.
Reproducible Execution Evidence: Instead of demo screenshots, include reproducible command outputs or interaction logs in markdown or .txt files. Your diagram source file and any optional supplementary images should be stored in dedicated /assets or /diagrams folders.
Commit history shows multiple meaningful commits
Standardized Documentation: Your README.md must identify your base project, and your model_card.md must answer all reflection prompts regarding AI collaboration, biases, and testing results.
Demo evidence is included: Your README.md contains at least 2-3 example inputs with their outputs pasted as fenced code blocks that demonstrate your system's behavior without relying on a video. A Loom walkthrough is optional but helpful for human reviewers; if you include one, add the link to your README.
Final changes are committed and pushed before the deadline