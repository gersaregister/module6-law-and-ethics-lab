# Breach Response Simulator: Module 6 Lab

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/gersaregister/module6-law-and-ethics-lab)

**Course:** Human Aspects of Cybersecurity
**Textbook:** Whitman & Mattord, *Principles of Information Security*, 7th ed., Module 6: Legal, Ethical, and Professional Issues in Information Security

| | |
|---|---|
| **What you'll do** | Play a security analyst during the week after a data breach. Investigate stolen files, apply the law, make decisions. |
| **Time** | About 90 minutes for the simulator, plus 20–30 minutes for the write-up |
| **What you turn in** | 2 files: `results/simulator-report.txt` and `writeup.txt` |
| **Where to turn it in** | The course website, by the due date posted there |
| **Cost** | Free. You never need a credit card. |
| **Work** | Individually |
| **Everything you need** | Is in this guide, including every answer (Part 5). Read each part in order and you won't get stuck. |

---

## Contents
0. [Before you start](#part-0-before-you-start)
1. [Open the lab](#part-1-open-the-lab)
2. [Start the simulator](#part-2-start-the-simulator)
3. [How to play](#part-3-how-to-play)
4. [Your investigation toolkit](#part-4-your-investigation-toolkit)
5. [Step-by-step answers for every mission](#part-5-step-by-step-answers-for-every-mission)
6. [Write-up and turning in your work](#part-6-write-up-and-turning-in-your-work)
7. [Stopping and coming back later](#part-7-stopping-and-coming-back-later)
8. [Grading](#part-8-grading)
9. [Frequently asked questions](#part-9-frequently-asked-questions)
10. [Troubleshooting](#part-10-troubleshooting)

---

## Part 0: Before you start

**You need:**
- A laptop or desktop computer (Windows, Mac or Chromebook) with Chrome, Edge, Firefox or Safari. A phone or tablet is **not** recommended; the screen is too small.
- An internet connection.
- A free GitHub account.

**Create a free GitHub account (5 minutes; skip if you already have one):**
1. Go to **https://github.com/signup**.
2. Enter your email address. Your school email is recommended.
3. Create a password and a username. Write them down.
4. Solve the short puzzle GitHub shows you, to prove you're human.
5. GitHub emails you a code. Open that email and type the code on the GitHub page. Check your spam folder if it doesn't arrive within 2 minutes.
6. If GitHub asks you to choose a plan, choose **Free**. If it asks about personalization, you can click **Skip**.

You're done. You will **never** be asked for a credit card for this lab. If anything asks for payment, you've clicked the wrong thing. Close it and go back to this guide.

---

## Part 1: Open the lab

1. Sign in to GitHub.
2. Click this button (it's also at the top of this page):
   [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/gersaregister/module6-law-and-ethics-lab)
   Or open this link: **https://codespaces.new/gersaregister/module6-law-and-ethics-lab**
3. On the page that opens, leave all settings as they are and click the green **Create codespace** button.
4. Wait 1–2 minutes while it says "Setting up your codespace". **Don't close the tab.**

**What you'll see when it's ready:**

```
+---------------------------------------------------------------+
|  FILE LIST    |   THIS GUIDE (README.md)                      |
|  (left side)  |                                               |
|  case-files   |   Breach Response Simulator: Module 6 Lab     |
|  law-cards.md |   ...                                         |
|  README.md    |                                               |
|  simulator.py +-----------------------------------------------+
|  writeup.txt  |   TERMINAL (bottom)                           |
|               |   === Module 6 Lab ready. To start, type: ... |
|               |   @yourname -> /workspaces/... $  _           |
+---------------------------------------------------------------+
```

- **File list (left):** all the lab files.
- **Guide (top right):** these instructions.
- **Terminal (bottom):** where you type commands. If you don't see it, click the **menu** (three lines at the top left), then **Terminal**, then **New Terminal**.

**Tip:** to see the guide and the terminal side by side with more room, drag the line between them upward.

---

## Part 2: Start the simulator

1. Click inside the **terminal** at the bottom so you can type there.
2. Type exactly this and press **Enter**:
   ```
   python3 simulator.py
   ```
3. Type your **full name** and press Enter. It goes on your report, so use the name your instructor knows you by.
4. Read the welcome screen, then press Enter.
5. A short **practice round** (not scored) teaches you how to use the investigation terminal and type an answer. Follow its steps exactly.
6. Then the real missions begin.

**Terminal basics, if you've never used one:**

| To do this | Do this |
|---|---|
| Type in the terminal | Click inside it first |
| Copy a command from this guide | Select it with your mouse and press **Ctrl+C** (Mac: **Cmd+C**) |
| Paste into the terminal | **Ctrl+Shift+V**, or right-click and choose **Paste** (Mac: **Cmd+V**) |
| Run what you typed | Press **Enter** |
| Bring back the last command | Press the **Up arrow**, then edit it |
| Stop something that's stuck | Press **Ctrl+C** |
| Clear a messy screen | Type `clear` and press Enter (in the investigation terminal) |

Capital and small letters matter in commands: type them exactly as shown.

---

## Part 3: How to play

### What happens
The simulator tells a story over one week: Saturday, March 21 to Friday, March 27, 2026. For each mission:
1. A **message** arrives from someone at Brightline.
2. You get **questions** (`answer>` prompt) and **decisions** (`decide>` prompt).
3. After each one, you see whether you were right and **why**.

Every question shows a **"Where to look"** line telling you which file or law card has the answer.

### The two kinds of prompts

**`answer>` means a QUESTION with one right answer.** Type it in the format the question asks for:

| Question type | What to type | Example |
|---|---|---|
| Number | Just the number. Commas are fine. | `512` or `1,250` |
| Letter choice | One letter | `b` |
| "Choose ALL that apply" | Letters separated by commas | `a,c` |
| Yes or no | `yes` or `no` | `no` |
| Date | Year-month-day | `2026-01-31` |

If you type the wrong format (for example, a word when a number is needed), the simulator tells you what to type. That doesn't count as a wrong answer.

**`decide>` means a DECISION.** You choose what you'd do, and the simulator shows the consequence. Type the letter of your choice. Not sure? Type `hint` to see the strongest choice. To decide well, ask yourself:
- Is it **legal**?
- Is it **honest**?
- Does it go through the **proper channel**?
- Does it **fix the problem**, or just hide it or blame someone?

### Commands you can type at any `answer>` prompt

| Command | What it does |
|---|---|
| `terminal` | Opens the **investigation terminal** (prompt changes to `investigate$`) so you can search the files. Type `back` to return to the question. |
| `laws` | Opens the **law and ethics reference cards**. Scroll with the arrow keys; press `q` to return. |
| `files` | Lists all case files. |
| `hint` | **Shows the correct answer**, how to find it and why it's right, then moves on. You earn **3 points instead of 10**. |
| `status` | Shows your score, legal risk and public trust. |
| `help` | Same as `hint`. |
| `commands` | Shows the list of commands. |
| `save` | Saves and quits. See Part 7. |

At a `decide>` prompt you can use `hint` (shows the strongest choice; picking it then earns 5 points instead of 10), `terminal`, `laws`, `files`, `status` and `save`.

In Mission 7, typing `hint` at a request shows whether it's allowed and why (1 point instead of 3).

### Scoring
- **Questions:** 10 points if right on the first try, 6 on the second, 3 on the third or later. Wrong answers never take away points; they only lower what the right answer earns.
- **Hints:** `hint` (or `help`) shows the answer right away: 3 points for a question, 5 for a decision, 1 for a Mission 7 request. Try on your own first to earn full points.
- **Decisions:** up to 10 points each, depending on how sound the choice is.
- **Mission 7:** 3 points for each correct allowed/not-allowed call.
- **Maximum:** 304 points.
- **Meters:** **Legal risk** (keep it low) and **Public trust** (keep it high) change with your decisions. At the end you'll see news headlines and any fines your choices caused.
- **You can replay as many times as you like.** Every finished attempt is saved in your report, and your best attempt counts (see Part 8).

---

## Part 4: Your investigation toolkit

Type `terminal` at any `answer>` prompt to open the investigation terminal. You're already in the right folder. Copy a command below, paste it, and change the **column number**, **value** or **file name** to fit the question.

**See what files exist**
```
ls case-files case-files/leaked
```
**Read a whole text file**
```
cat case-files/incident-summary.txt
```
**See the first few lines of a file, including the column names on line 1**
```
head -5 case-files/leaked/customers.csv
```
**Count the lines in a file, skipping the header line**
```
tail -n +2 case-files/leaked/customers.csv | wc -l
```
**Count rows where a column equals a value** (here: column 6 equals FL)
```
awk -F, '$6=="FL"' case-files/leaked/customers.csv | wc -l
```
**Count rows matching two conditions** (`&&` means "and")
```
awk -F, '$6=="FL" && $8=="card"' case-files/leaked/customers.csv | wc -l
```
**Count how many times each value appears in a column** (here: column 7)
```
awk -F, 'NR>1 {print $7}' case-files/leaked/customers.csv | sort | uniq -c
```
**Search every leaked file for a pattern and count the matches**
```
grep -rEo "PATTERN" case-files/leaked | wc -l
```

**What the pieces mean**
- `|` (the "pipe", Shift + the key above Enter) passes one command's result to the next.
- `wc -l` counts lines.
- `tail -n +2` starts at line 2, skipping the header.
- `awk -F,` splits each line at the commas. `$6` means column 6. `==` means "equals". Text values go in double quotes: `"FL"`.
- `NR>1` means "skip line 1".
- `sort | uniq -c` groups identical values and counts them.

**Column numbers**

`customers.csv`: 1 customer_id, 2 first_name, 3 last_name, 4 email, 5 city, **6 state**, **7 country**, **8 payment_method** (`card` or `invoice`), 9 card_number, 10 card_cvv

`employees.csv`: 1 employee_id, 2 first_name, 3 last_name, 4 ssn, 5 department, 6 home_city, **7 home_state**, 8 salary_usd

**Watch out:** in the **country** column, `CA` means **Canada**. In the **state** column, `CA` means **California**.

For safety, the investigation terminal only allows: `ls cat head tail wc grep awk sort uniq cut less tr echo column`, and it doesn't allow `>`, `<`, `;` or `&`. Use the pipe `|` instead.

---

## Part 5: Step-by-step answers for every mission

This part gives you **every answer**, the command that finds it, and why it's right. Keep this guide open next to the simulator and follow along.

**How to use it:**
1. Read the mission's message in the simulator.
2. Find the same mission below.
3. For investigation questions, type `terminal`, copy the command shown here, paste it (**Ctrl+Shift+V**), press **Enter**, and check that you get the same number. Then type `back`.
4. Type the answer at the `answer>` or `decide>` prompt.

At a DECISION the choices appear in a **different order each time**, so the letter changes. Find the choice whose **words** match the "Best choice" below and type its letter.

---

### Practice round (not scored)
| Step | Type this |
|---|---|
| Open the investigation terminal | `terminal` |
| List the stolen files | `ls case-files/leaked` |
| You'll see 3 files: customers.csv, employees.csv, supplier-terms.txt | |
| Go back | `back` |
| **Answer** | `3` |

---

### Mission 1: Triage (from the CEO, Saturday 9:30 a.m.)

Optional first step: read the case with `terminal`, then `cat case-files/incident-summary.txt`, then `back`. It says IT discovered the breach on **Saturday, March 21, 2026, at 9:15 a.m.**

**Question 1. How many customer records are in customers.csv?**
- Command: `tail -n +2 case-files/leaked/customers.csv | wc -l`
- **Answer: `2400`**
- Why: the file has 2,401 lines. The first line is the column names, so there are 2,400 customers.

**Question 2. How many Social Security numbers appear in the leaked files?**
- Command: `grep -rEo "[0-9]{3}-[0-9]{2}-[0-9]{4}" case-files/leaked | wc -l`
- **Answer: `140`**
- Why: the command finds everything shaped like an SSN (123-45-6789). All 140 employees' SSNs were stolen.

**Question 3. Which file contains a trade secret?**
- Command (optional): `cat case-files/leaked/supplier-terms.txt`
- **Answer: `c`** (supplier-terms.txt)
- Why: its first line says "CONFIDENTIAL - TRADE SECRET". It holds secret supplier pricing, not personal data.

---

### Mission 2: Evidence (from the IT manager, Saturday 11:00 a.m.)

**Decision. Dana wants to wipe the server today.**
- **Best choice:** "First make a forensic copy of the server and save its logs, then rebuild."
- Why: wiping destroys the evidence police and lawyers need. Copying it first protects the evidence and still gets the business running.

**Question 1. Which federal law makes logging in with a stolen password a crime?**
- **Answer: `b`** (Computer Fraud and Abuse Act, CFAA)
- Why: the CFAA makes it a crime to access a computer without authorization. A stolen password isn't permission.

**Question 2. Who should the CEO report the computer crime to?**
- **Answer: `a`** (the FBI, through the Internet Crime Complaint Center, IC3)
- Why: the FBI investigates federal computer crimes.

---

### Mission 3: Florida law (from the lawyer, Sunday 10:00 a.m.)

Florida's breach law is the **Florida Information Protection Act (FIPA)**. Type `laws` to read its card.

**Question 1. How many Florida customers had their card number and security code (CVV) exposed?**
- Command: `awk -F, '$6=="FL" && $8=="card"' case-files/leaked/customers.csv | wc -l`
- **Answer: `912`**
- Why: this counts rows where the state (column 6) is FL **and** the payment method (column 8) is card. Under FIPA, a card number plus its security code counts as personal information.

**Question 2. Do invoice customers (name and email only) count as "personal information" under FIPA?**
- **Answer: `b`** (No)
- Why: FIPA needs a name **plus** something sensitive, such as an SSN, an ID number, a card number with its code, health information, or an email **with** a password. A name and email alone don't count.

**Question 3. How many employees who live in Florida had their SSNs exposed?**
- Command: `awk -F, '$7=="FL"' case-files/leaked/employees.csv | wc -l`
- **Answer: `131`**
- Why: this counts employees whose home state (column 7) is FL. An SSN with a name is personal information.

**Question 4. How many Florida residents must Brightline notify in total?**
- **Answer: `1043`**
- Why: 912 customers + 131 employees = 1,043. The invoice customers aren't included because their data isn't FIPA personal information.

**Question 5. Who must Brightline notify? (Choose all that apply.)**
- **Answer: `a,b,c`**
- Why:
  - **a)** each affected Florida resident, always
  - **b)** the Florida Department of Legal Affairs (Attorney General), because it's 500 or more people
  - **c)** the credit bureaus, because it's more than 1,000 people
  - Florida doesn't require TV stations to be told, and the U.S. Department of Health and Human Services is only for health breaches (HIPAA).

**Question 6. What's the last day to notify Florida residents?**
- **Answer: `2026-04-20`**
- Why: FIPA allows no more than 30 days after discovery. March 21 + 30 days = April 20, 2026. (March 21 to March 31 is 10 days, plus 20 days in April.)

---

### Mission 4: Pressure (from the CFO, Monday 8:30 a.m.)

**Decision 1. The CFO wants to delay the letters until after the spring sale (about 45 days).**
- **Best choice:** "Explain that Florida requires notice within 30 days, and bring it to Rosa (counsel) and the CEO."
- Why: 45 days breaks the law. The right move is to state the law politely and escalate through the proper channel.

**Decision 2. When should Brightline notify Florida residents?**
- **Best choice:** "Friday, March 27 (6 days after discovery)."
- Why: it's legal and fast, so customers can protect themselves early. May 5 is 15 days late, which means a $15,000 fine.

---

### Mission 5: Beyond Florida (from the lawyer, Monday 10:00 a.m.)

**Question 1. How many customers live in the European Union?**
- Command: `awk -F, 'NR>1 {print $7}' case-files/leaked/customers.csv | sort | uniq -c`
- The result lists: CA 30, **DE 40**, **ES 18**, **FR 30**, **IE 20**, **NL 12**, US 2250. (CA here means Canada, which isn't in the EU.)
- **Answer: `120`**
- Why: 40 + 18 + 30 + 20 + 12 = 120.

**Question 2. How many hours does GDPR allow to report the breach?**
- **Answer: `72`**
- Why: GDPR, the EU privacy law, requires reporting to the EU authority within 72 hours of finding out.

**Decision. It's Monday 10:00 a.m. What do you recommend?**
- **Best choice:** "Report to the EU supervisory authority today. We're at about 49 hours."
- Why: Saturday 9:15 a.m. to Monday 10:00 a.m. is about 49 hours, still inside 72. Waiting until Friday would be too late.

**Question 3. What applies to customers from other U.S. states?**
- **Answer: `b`** (each state's own breach law)
- Why: every state has its own breach law protecting its own residents.

**Question 4. Does HIPAA apply to Brightline?**
- **Answer: `no`**
- Why: HIPAA only covers health plans, health care providers, health care clearinghouses and their business partners. Brightline sells office supplies.

---

### Mission 6: Card data (from the card processor, Tuesday 9:00 a.m.)

**Question 1. Which standard forbids storing card security codes?**
- **Answer: `c`** (PCI DSS)
- Why: the Payment Card Industry Data Security Standard forbids keeping CVVs after a payment is approved.

**Question 2. Is PCI DSS a law passed by the government?**
- **Answer: `no`**
- Why: it's an industry standard set by the card companies and enforced through contracts. Breaking it still brings fines.

**Question 3. Which federal agency investigates payment-card crimes?**
- **Answer: `b`** (the U.S. Secret Service)
- Why: the Secret Service investigates financial crimes, including card fraud.

**Decision. Should the developer delete the stored CVVs?**
- **Best choice:** "Delete all stored CVVs now and change checkout so they're never saved."
- Why: Brightline isn't allowed to keep them at all. Even encrypted, they're still forbidden.

---

### Mission 7: Is it authorized? (from the security tester, Tuesday 11:00 a.m.)

The rules (`cat case-files/rules-of-engagement.txt`) allow testing **only** the server 10.10.10.20, on ports 80 and 443, **March 23–27, 8 a.m.–6 p.m.**, with no social engineering, no flooding, and no copying data.

| # | Request | Type | Why |
|---|---|---|---|
| 1 | Scan 10.10.10.20, ports 80 and 443, at 10 a.m. today | **`y`** | Right server, right ports, right time |
| 2 | Scan the fileserver 10.10.10.30 too | **`n`** | Only 10.10.10.20 is allowed |
| 3 | Email the sales team a fake invoice | **`n`** | Social engineering isn't allowed |
| 4 | Run the scan at 2 a.m. | **`n`** | Only 8 a.m.–6 p.m. is allowed |
| 5 | Try the test login found in the website's code | **`y`** | Logins found during the test may be used on the allowed server |
| 6 | Download the customer database to study at home | **`n`** | Copying customer data isn't allowed |
| 7 | Flood the website with traffic | **`n`** | Flooding (denial-of-service) isn't allowed |
| 8 | Keep testing on Saturday, March 28 | **`n`** | Testing ends March 27 |

---

### Mission 8: The rest of the week (Wednesday to Friday)

| Situation | Best choice | Why |
|---|---|---|
| Should Brightline fire Kim, who clicked the phishing link, and announce it? | "No. Retrain everyone, turn on multi-factor authentication, and praise fast reporting." | Blaming people makes staff hide mistakes. Training and MFA fix the real problem. |
| A friend asks you to hack their company's website | "Decline, and explain they need written permission from the system owner..." | Testing without the owner's written permission is a crime (CFAA). |
| A recruiter offers a bonus for Brightline's supplier pricing | "Decline the condition. You'll only consider the job without it." | Taking trade secrets is illegal (Economic Espionage Act). |
| A coworker uses pirated software | "Talk to the coworker, then report it through IT's normal process." | Pirated software breaks copyright law and often carries malware. |
| A reporter calls asking how many customers were affected | "Politely refer them to Brightline's spokesperson or legal counsel." | Only the official spokesperson should speak for the company. |

---

### Final debrief
Your score, meters, headlines and fines appear, and your report is saved automatically to `results/simulator-report.txt`. Next, go to Part 6 to do the write-up and turn in your work.

---

## Part 6: Write-up and turning in your work

**Step 1: Complete the write-up**
1. In the **file list** on the left, click **`writeup.txt`**.
2. Fill in your name, your best score and its verification code. All three are in `results/simulator-report.txt`; click it in the file list to open it.
3. Type your answer under each of the 6 questions: a short paragraph each (3–5 sentences).
4. Press **Ctrl+S** (Mac: **Cmd+S**) to save. A white dot on the file's tab means it isn't saved yet.

**Step 2: Download your two files**
1. In the file list, right-click **`writeup.txt`** and choose **Download**. Save it to your computer.
2. Click the **`results`** folder to open it, right-click **`simulator-report.txt`** and choose **Download**.
3. If your browser asks whether to keep or allow the download, choose **Keep** or **Allow**.

**Step 3: Upload**
Upload both files to the Module 6 assignment on the course website before the due date posted there.

**If Download doesn't work:** open the file, press **Ctrl+A** (select all) and **Ctrl+C** (copy), paste it into a Word or Google document, and upload that instead. Do this for both files.

---

## Part 7: Stopping and coming back later

**Stop your codespace when you're done for the day.** Free accounts get a monthly allowance of hours, and a running codespace uses it up.
- Click **Codespaces** in the bottom-left corner of the screen (the blue or green area), then **Stop Current Codespace**.
- Closing the browser tab also works. The codespace stops on its own after about 30 minutes, but stopping it yourself is better.

**To come back later:**
1. Go to **https://github.com/codespaces**.
2. Click your codespace (it has a made-up name such as *"fluffy-space-waffle"*) to reopen it. **Don't** create a new one, or you'll start with empty files.
3. In the terminal, type `python3 simulator.py`. When asked **"Resume?"**, type `y`.

**About saving progress:** the simulator saves automatically at the end of each mission. If you type `save` or close it in the middle of a mission, you restart that mission (not the whole game) next time.

---

## Part 8: Grading

| Item | Points |
|---|---|
| Simulator, best attempt: 90%+ = 10 · 75%+ = 8 · 55%+ = 6 · finished below 55% = 4 | 10 |
| Write-up: 6 questions, thoughtful answers connected to Module 6 | 8 |
| Both files submitted correctly | 2 |
| **Total** | **20** |

Replaying to raise your score is encouraged. Your best finished attempt counts.

---

## Part 9: Frequently asked questions

**Do I need to install anything?**
No. Everything runs in your web browser.

**Will this cost me money?**
No. The lab uses a small part of the free hours every GitHub account gets each month. You never need a credit card.

**How long does it take?**
About 90 minutes for the simulator and 20–30 minutes for the write-up. You don't have to finish in one sitting (see Part 7).

**Can I use my phone or tablet?**
It's not recommended; the screen is too small for the terminal. Use a laptop, desktop or Chromebook.

**Can I work with classmates?**
Do the simulator and write-up individually.

**What if I get an answer wrong?**
Try again. Wrong answers don't take away points; they only lower what the right answer earns. If you're stuck, type `hint` to see the answer and move on.

**What if I make a bad decision?**
You'll see the consequences, which is part of learning. Finish the game, then replay to try a better path. Your best attempt counts.

**What does `hint` do?**
It shows the correct answer, how to find it, and why it's right, so you're never stuck. You earn fewer points (3 instead of 10 for a question), so try on your own first. Read the "How to find it" line; it teaches you how to solve similar questions.

**Can I replay the whole simulator?**
Yes, as many times as you want. Type `python3 simulator.py` after you finish. All finished attempts stay in your report.

**What is the verification code?**
A code made from your name and score that lets your instructor confirm your report is genuine. Don't edit `simulator-report.txt`; edited reports won't match their codes.

**Are these real people and real card numbers?**
No. All people, companies, card numbers and SSNs are made up. The SSNs start with 9, which the government never issues.

**Do I need to read the textbook first?**
It helps, but the law cards in the simulator (`laws`) contain everything you need to answer the questions.

**Is the investigation terminal safe? Can I break something?**
You can't break anything. It only allows read-only commands. If something odd happens, type `back`, or close the simulator and run `python3 simulator.py` again.

**I finished. What now?**
Do the write-up and submit (Part 6), then stop your codespace (Part 7).

---

## Part 10: Troubleshooting

| Problem | Fix |
|---|---|
| The **Create codespace** page asks me to sign in | Sign in to GitHub, then click the lab link again. |
| It's stuck on "Setting up your codespace" for more than 5 minutes | Refresh the page. If it's still stuck, go to github.com/codespaces, click **...** next to the codespace, choose **Delete**, then open the lab link again. |
| I don't see a terminal | Click the menu (three lines, top left), then **Terminal**, then **New Terminal**. |
| I typed `python3 simulator.py` and got "No such file or directory" | Type `cd /workspaces/module6-law-and-ethics-lab` and press Enter, then try again. |
| The guide shows strange symbols like `#` and `**` | Right-click `README.md` in the file list and choose **Open Preview**. |
| I accidentally closed the simulator | Type `python3 simulator.py` and answer `y` to resume. |
| I opened the law cards and can't get out | Press `q`. |
| The screen is full of text and confusing | Type `back` if you're in the investigation terminal, or press **Enter** at the question to see the prompt again. |
| A command says "isn't available here" | The investigation terminal only allows the commands listed in Part 4. Check your spelling. |
| A command says "turned off here" | You used `>`, `<`, `;` or `&`. Connect commands with the pipe symbol instead (Shift + the backslash key). |
| My count comes out as 0 | Check that you used the right **column number** (Part 4), straight double quotes around the value (`"FL"`, not curly quotes), and capital letters (`FL`, not `fl`). |
| My count is 1 too high | You counted the header line. Use `tail -n +2` or `NR>1`. |
| Pasting doesn't work in the terminal | Use **Ctrl+Shift+V**, or right-click and choose **Paste**. |
| The simulator seems frozen | Press **Enter**. If that doesn't help, press **Ctrl+C**, then type `python3 simulator.py` and resume. |
| I want to start over from the beginning | Type `python3 simulator.py` and answer `n` when asked to resume. |
| I lost my internet connection | Reconnect and refresh the page. Your files and saved missions are still there. |
| I reopened the lab and my files are empty | You probably created a **new** codespace. Go to github.com/codespaces and open your earlier one instead. |
| GitHub says I've used my free hours | Unlikely for this lab (about 4 hours of a 120-hour monthly allowance). Make sure you stop codespaces when finished, and delete extra ones at github.com/codespaces. |
| Download doesn't work | See "If Download doesn't work" in Part 6. |
