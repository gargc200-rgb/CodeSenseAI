# CodeSense AI – 90–150 Second Video Demonstration Script
**Course:** Prompt Engineering (SCSE4041)  
**Milestone:** Milestone 2 (Total Marks: 12) | **Component:** Video Demonstration (2 Marks)  
**Project ID:** C4 | **Working Title:** CodeSense AI  
**Target Duration:** ~125 seconds (within 90–150s range)  

---

### [00:00 – 00:15] SECTION 1: Introduction & Problem Context
*(Visual: Presenter introduces themselves, showing the CodeSense AI web dashboard header with course code SCSE4041, Milestone 2, and Project ID C4).*

**Speaker (Voiceover / On Camera):**
> "Hello faculty and evaluators. I am presenting **CodeSense AI**, an educational code review assistant developed for our Prompt Engineering course, SCSE4041, Milestone 2, Project C4. 
> 
> As first-year programming students learn C++, Python, and Java, they constantly run into syntax and runtime errors. While commercial AI assistants often just spit out the entire corrected program—depriving students of the chance to learn—CodeSense AI uses advanced prompt engineering to act as a genuine Socratic tutor."

---

### [00:15 – 00:35] SECTION 2: Pedagogical & Prompt Engineering Architecture
*(Visual: Zoom in on the Prompt Architecture selector and the 5-step task decomposition diagram).*

**Speaker:**
> "Our core innovation is our prompt engineering architecture. We iteratively evolved three prompt versions: Baseline P1, Improved P2, and Final Optimized P3. 
> 
> P3 incorporates **Role Prompting** as a Senior CS Instructor, **Context Prompting** calibrated for first-year undergraduates, **5-Stage Task Decomposition**, multi-language **Few-Shot Exemplars**, and strict **Negative Constraints**. Crucially, it guarantees zero complete-solution leakage: no rewritten programs, no spoilers—only guided Socratic inquiry."

---

### [00:35 – 00:65] SECTION 3: Live Demonstration – Buggy Code Submission
*(Visual: Screen recording of the web dashboard. Select Python from language dropdown. Click example dropdown and select 'Python: Runtime Error (ZeroDivisionError)'. Click 'Analyze Code'. Show loading spinner and instant results).*

**Speaker:**
> "Let’s see CodeSense AI in action on a live submission. 
> 
> Here, a student is trying to calculate a class average score, but their denominator can be zero without defensive validation. 
> 
> I click **'Analyze Code'**. Within milliseconds, the backend sanitizes the request, formats our P3 prompt, invokes the model, and validates the output against our strict RFC-8259 JSON schema."

---

### [00:65 – 00:95] SECTION 4: Inspecting Results, Socratic Hints & Anti-Leakage
*(Visual: Mouse cursor smoothly highlights Overall Assessment, the High Severity badge, the Socratic Hint card, Positive Reinforcement, and Next Step).*

**Speaker:**
> "Look at the structured results dashboard:
> First, an **Overall Assessment** clearly summarizing the code health.
> Second, the detected bug is classified with a **High Severity badge**, pinpointing the unhandled ZeroDivisionError.
> Third, notice our **Socratic Learning Hint**: instead of handing the student the answer, it asks: *'What conditional construct could you place before the division to check whether your denominator is zero?'*
> Fourth, it provides **Positive Feedback** praising their variable naming, and recommends the exact curricular concept to revise. 
> Notice the green badge: **Zero Solution Leakage** verified!"

---

### [00:95 – 01:20] SECTION 5: Prompt Experimentation & Comparison Matrix
*(Visual: Click 'Compare P1 / P2 / P3' to show the 3-column side-by-side comparison. Then scroll to the Phase 5 Benchmarking Section showing the Matplotlib comparison chart and metrics).*

**Speaker:**
> "To prove our prompt engineering effectiveness for Milestone 2, we built a dedicated comparison and experimentation engine.
> 
> Running the same code across P1, P2, and P3 side-by-side reveals that Baseline P1 leaked the complete code in 80% of our 10 test cases and failed JSON validation. 
> 
> In contrast, our final prompt P3 achieved **100% JSON schema validity**, **98% pedagogical hint usefulness**, and **0% solution leakage**. All results are logged in our reproducible CSV and comparison chart."

---

### [01:20 – 01:35] SECTION 6: Report Generation, Repository & Conclusion
*(Visual: Click 'PDF Report' to download the styled review report. Show GitHub repository structure, tests passing with 26/26 in terminal, and submission checklist).*

**Speaker:**
> "Students can immediately export their review as a styled PDF report. 
> 
> Our automated test suite passes 26 out of 26 tests across all API endpoints and validators. The repository is organized professionally with comprehensive documentation, prompt files, and experimental logs. 
> 
> Thank you for evaluating CodeSense AI!"

---
*Target Video Duration: 125 seconds. Meets the 90–150s requirement.*
