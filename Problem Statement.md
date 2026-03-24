1. **Case Background (Business Problem)**

   Software companies receive thousands of bug reports through various channels: frantic emails, "rage-click" automated alerts, and vague support tickets.

* **The "Noise" Problem:** Most reports are buried in irrelevant context (e.g., "I was having a great day until this happened...").  
* **The Triage Bottleneck:** Senior engineers or Product Managers spend hours manually reading reports to decide which team (Frontend, Backend, Mobile) should fix it.  
* **The Inconsistency:** Two different people might report the same bug differently, leading to **duplicate tickets** and wasted resources.  
2. **Problem Statement**

   How can we automate the ingestion of unstructured bug reports to provide engineers with a standardized, "clean" technical brief that allows them to start fixing the issue immediately without asking clarifying questions?

3. **Core Requirements**

* **Signal-to-Noise Filtering:** The ability to strip away emotional language and identify only technical facts.  
* **Structural Standardization:** Every output must follow the exact same format (e.g., Summary, Steps, Expected vs. Actual).  
* **Cross-Reference Capability:** The AI should be able to look at system logs (if provided) and map them to the user's description.  
* **Categorization Logic:** Identifying the "blast radius" (how many users are affected) to assign a severity level automatically.  
    
4. **Input**

The system accepts a **Raw BUG Report Extract**

5. **Expected Output**

   A structured JSON object ready to be injected into a tool like Jira or GitHub Issues:

   JSON

   {

     "issue\_summary": "Inconsistent 'Purchase' button failure on iPad/Safari",

     "steps\_to\_reproduce": \[

       "Open app on iPad (v17.2)",

       "Add item to cart",

       "Navigate to Checkout",

       "Click 'Purchase' button multiple times"

     \],

     "technical\_details": {

       "detected\_error": "Timeout in API call /v1/transactions",

       "environment": "iOS Safari"

     },

     "severity": "P1 (Critical \- Revenue Impacting)",

     "suggested\_owner": "Payments-Backend-Team"

   }

6. **Solution Design Questions for the Trainee**

* **Q1: How do you handle "Duplicate Detection"?**  
  * *Challenge:* If 10 people report the same bug, we don't want 10 tickets.  
  * *Solution:* How can we use **Embeddings and Vector Similarity** to compare a new report against existing open tickets before creating a new one?  
* **Q2: Logic vs. Hallucination in "Steps to Reproduce"?**  
  * *Challenge:* If the user says "It just broke," they didn't provide steps. Should the AI "invent" steps based on common knowledge?  
  * *Solution:* Explain why the AI should be prompted to say *"Steps not provided by user"* rather than guessing, to avoid leading engineers down a false path.  
* **Q3: Defining "Severity" thresholds?**  
  * *Challenge:* Users always think their bug is a "P1."  
  * *Solution:* How do you give the AI a **Policy Guide** (e.g., "If it affects 1 user, it's a P3; if it prevents login, it's a P1") to ensure objective triage?  
* **Q4: The "Log Parsing" limit?**  
  * *Challenge:* Error logs can be thousands of lines long.  
  * *Solution:* Discuss how to use **Log Summarization** or "Regex Filtering" to feed the LLM only the relevant "stack trace" instead of the whole file.

7. **Submission Guideline**

* Source code (GitHub or zip)  
* Architecture diagram  
* Tech stack  
* Agent definitions & prompts  
* Sample questions and generated SQL outputs  
* Cost estimation to process 100 user queries  
* Evaluation method and metrics  
* Average Response time per query.  
* Demo UI (Streamlit or React-based)

