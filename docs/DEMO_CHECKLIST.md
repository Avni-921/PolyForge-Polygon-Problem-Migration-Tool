# Screen Recording Demo Checklist

Follow this click-by-click order while recording your screen:

1. **Setup/Startup**
   - **Action:** Open terminal, run `make check_setup`.
   - **Say:** "I built a diagnostic command that proves my database, Polygon API credentials, and Cloud Storage connectivity are working perfectly before we even start."
   - *Reminder: Make sure your `.env` is NOT open on the screen to hide credentials.*

2. **Login & Fetch**
   - **Action:** Open browser to `http://127.0.0.1:8000/migrate/new/`. Enter your problem ID.
   - **Say:** "Here I am entering my Polygon problem ID. The backend securely signs an API request to Codeforces and fetches the problem details."

3. **Review & Tags**
   - **Action:** On the review page, type `50` for difficulty, and `graphs, dp` for tags. 
   - **Say:** "I can review the problem metadata here, and I am adding two tags and a difficulty score before committing it to our database."

4. **Migrate & Upload**
   - **Action:** Click "Migrate & Upload".
   - **Say:** "This is where the magic happens. The structured data is saved to PostgreSQL in an idempotent way, and the massive test case files are concurrently streamed to my Cloud Storage provider."

5. **Verification**
   - **Action:** Point at the Verification screen.
   - **Say:** "As you can see, the verification panel confirms the exact number of test cases saved to PostgreSQL, and lists the exact storage keys created in the bucket."

6. **Folder Structure Check**
   - **Action:** Open your Storage Bucket UI (or `./local_storage` if demonstrating locally). Open `test_cases/{problem_id}/01.a`.
   - **Say:** "And if we look at the raw storage bucket, the files are correctly mapped using the enforced path structures, and the contents are preserved perfectly."
