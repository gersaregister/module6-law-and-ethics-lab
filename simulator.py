#!/usr/bin/env python3
"""
BREACH RESPONSE SIMULATOR - Module 6: Legal, Ethical, and Professional Issues
Human Aspects of Cybersecurity

You are the new security analyst at Brightline Supply Co. during the week
after a data breach. Read your messages, investigate the stolen files,
apply the law, and make the calls. Every decision has consequences.

Start:   python3 simulator.py
"""
import datetime
import hashlib
import json
import os
import random
import re
import shutil
import subprocess
import sys
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")
SAVE = os.path.join(RESULTS, "progress.json")
REPORT = os.path.join(RESULTS, "simulator-report.txt")
SALT = "brightline-sim6"
WIDTH = 78

# ---------------------------------------------------------------- display
USE_COLOR = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None
def c(text, code):
    return f"\033[{code}m{text}\033[0m" if USE_COLOR else text
def bold(t): return c(t, "1")
def red(t): return c(t, "31")
def green(t): return c(t, "32")
def yellow(t): return c(t, "33")
def cyan(t): return c(t, "36")
def dim(t): return c(t, "2")

def say(text="", indent=""):
    for para in str(text).split("\n"):
        if not para.strip():
            print()
        else:
            print(textwrap.fill(para, WIDTH, initial_indent=indent,
                                subsequent_indent=" " * len(indent)))

def rule(ch="-"):
    print(dim(ch * WIDTH))

def ask(prompt):
    try:
        return input(prompt)
    except EOFError:
        print()
        raise KeyboardInterrupt

def pause():
    ask(dim("\n  [press Enter to continue] "))

def H(s):
    return hashlib.sha256((SALT + s).encode()).hexdigest()[:16]

# ---------------------------------------------------------------- state
class State:
    def __init__(self):
        self.name = ""
        self.mission = 0
        self.score = 0
        self.max_score = 0
        self.legal_risk = 25      # lower is better (0-100)
        self.trust = 60           # higher is better (0-100)
        self.fines = 0
        self.flags = {}
        self.log = []
        self.hints = 0
        self.started = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    def adjust(self, legal=0, trust=0):
        self.legal_risk = max(0, min(100, self.legal_risk + legal))
        self.trust = max(0, min(100, self.trust + trust))

    def save(self):
        os.makedirs(RESULTS, exist_ok=True)
        with open(SAVE, "w", encoding="utf-8") as fh:
            json.dump(self.__dict__, fh, indent=1)

    @classmethod
    def load(cls):
        s = cls()
        with open(SAVE, encoding="utf-8") as fh:
            s.__dict__.update(json.load(fh))
        return s

def meter(value, good_high=True):
    filled = round(value / 10)
    bar = "#" * filled + "." * (10 - filled)
    if good_high:
        col = green if value >= 60 else yellow if value >= 35 else red
    else:
        col = green if value <= 30 else yellow if value <= 60 else red
    return col(f"[{bar}] {value:3d}")

def status(st):
    rule()
    print(f"  {bold('Score')}: {st.score}   "
          f"{bold('Legal risk')}: {meter(st.legal_risk, good_high=False)}   "
          f"{bold('Public trust')}: {meter(st.trust)}")
    if st.fines:
        print(f"  {bold('Fines and penalties so far')}: {red('$' + format(st.fines, ','))}")
    rule()

# ---------------------------------------------------------------- tools
ALLOWED = {"ls", "cat", "head", "tail", "wc", "grep", "awk", "sort", "uniq",
           "cut", "less", "tr", "echo", "column"}

def terminal():
    say(cyan("INVESTIGATION TERMINAL") + dim("  (type 'help' for examples, 'back' to return)"))
    say(dim("You are in the lab folder. The stolen files are in case-files/leaked/"))
    while True:
        try:
            cmd = ask(green("investigate$ ")).strip()
        except KeyboardInterrupt:
            print()
            return
        if not cmd:
            continue
        if cmd in ("back", "exit", "quit", "q"):
            return
        if cmd == "help":
            say(dim(
                "Examples (copy one, then change it):\n"
                "  ls case-files case-files/leaked\n"
                "  cat case-files/incident-summary.txt\n"
                "  head -5 case-files/leaked/customers.csv\n"
                "  tail -n +2 case-files/leaked/customers.csv | wc -l\n"
                "  awk -F, '$6==\"FL\"' case-files/leaked/customers.csv | wc -l\n"
                "  awk -F, 'NR>1 {print $7}' case-files/leaked/customers.csv | sort | uniq -c\n"
                "  grep -c \"something\" case-files/leaked/employees.csv\n"
                "Allowed commands: " + ", ".join(sorted(ALLOWED))))
            continue
        if cmd == "clear":
            os.system("clear")
            continue
        if any(bad in cmd for bad in (";", "&", "`", "$(", ">", "<")):
            say(yellow("For safety, ; & > < ` and $( are turned off here. Use pipes ( | ) instead."))
            continue
        bad_word = None
        for part in cmd.split("|"):
            words = part.strip().split()
            if not words or words[0] not in ALLOWED:
                bad_word = words[0] if words else "(empty)"
                break
        if bad_word:
            say(yellow(f"'{bad_word}' isn't available here. Allowed: " + ", ".join(sorted(ALLOWED))))
            continue
        sys.stdout.flush()
        try:
            subprocess.run(["bash", "-c", cmd], cwd=HERE, timeout=30)
        except subprocess.TimeoutExpired:
            say(yellow("That took too long and was stopped."))

def show_laws():
    path = os.path.join(HERE, "law-cards.md")
    if shutil.which("less") and sys.stdout.isatty():
        say(dim("Opening the law cards. Use arrow keys to scroll, press q to come back."))
        pause()
        sys.stdout.flush()
        subprocess.run(["less", path])
    else:
        with open(path, encoding="utf-8") as fh:
            print(fh.read())

def show_files():
    say(cyan("CASE FILES"))
    for root in ("case-files", os.path.join("case-files", "leaked")):
        for f in sorted(os.listdir(os.path.join(HERE, root))):
            p = os.path.join(root, f)
            if os.path.isfile(os.path.join(HERE, p)):
                print("  " + p)
    say(dim("Read one with:  terminal  then  cat case-files/incident-summary.txt"))

HELP_LINE = dim("Stuck? Type  hint  to see the answer.  Other commands: terminal | laws | files | status | save | commands")

def general_help():
    say(cyan("HOW TO PLAY"))
    say("  Type your answer and press Enter, or use one of these commands:")
    say("  terminal  open the investigation terminal to search the stolen files")
    say("  laws      read the law and ethics reference cards")
    say("  files     list the case files")
    say("  hint      show the correct answer and how to find it (you earn 3 points instead of 10)")
    say("  help      same as hint")
    say("  status    show your score, legal risk and public trust")
    say("  save      save and quit; run python3 simulator.py later to resume")
    say("  commands  show this list of commands")
    say(dim("  Stuck on a mission? README.md, Part 5, explains how to solve each one."))

# ---------------------------------------------------------------- questions
MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}

def norm(kind, v, options=None):
    v = v.strip().lower()
    if kind == "num":
        m = re.search(r"\d[\d,]*", v)
        return m.group(0).replace(",", "") if m else v
    if kind == "yn":
        w = re.sub(r"[^a-z]", "", v)
        return "yes" if w.startswith("y") else "no" if w.startswith("n") else w
    if kind == "mc":
        if options:
            for L, opt in zip("abcdef", options):
                o = re.sub(r"[^a-z0-9]", "", opt.lower())
                w = re.sub(r"[^a-z0-9]", "", v)
                if len(w) > 3 and (o.startswith(w) or w == o):
                    return L
        w = re.sub(r"[^a-z]", "", v)
        return w[:1]
    if kind == "multi":
        found = re.findall(r"\b([a-f])\b", v.replace(")", " "))
        if not found and re.fullmatch(r"[a-f]+", v.replace(" ", "")):
            found = list(v.replace(" ", ""))
        return "".join(sorted(set(found)))
    if kind == "date":
        v2 = v.replace(",", " ").replace(".", " ")
        m = re.fullmatch(r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})", v2.strip())
        if m:
            return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
        m = re.fullmatch(r"(\d{1,2})[-/](\d{1,2})[-/](\d{4})", v2.strip())
        if m:
            return f"{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}"
        m = re.fullmatch(r"([a-z]+)\s+(\d{1,2})(?:st|nd|rd|th)?\s+(\d{4})", re.sub(r"\s+", " ", v2.strip()))
        if m and m.group(1)[:3] in MONTHS:
            return f"{m.group(3)}-{MONTHS[m.group(1)[:3]]:02d}-{int(m.group(2)):02d}"
        return v
    return re.sub(r"[^a-z0-9]", "", v)

def question(st, q):
    """q: id, text, kind, options?, hint, explain, reveal"""
    st.max_score += 10
    print()
    say(bold("QUESTION: ") + q["text"])
    if q["id"] in WHERE:
        say(cyan("Where to look: ") + WHERE[q["id"]], indent="  ")
    letters = "abcdef"
    if q["kind"] in ("mc", "multi"):
        for L, opt in zip(letters, q["options"]):
            say(opt, indent=f"   {L}) ")
        if q["kind"] == "multi":
            say(dim("   Choose ALL that apply, e.g.  a,c"))
    if q["kind"] == "yn":
        say(dim("   Answer yes or no."))
    if q["kind"] == "date":
        say(dim("   Answer as YYYY-MM-DD, for example 2026-01-31."))
    print(HELP_LINE)
    tries, hinted = 0, False
    while True:
        try:
            raw = ask(yellow("answer> ")).strip()
        except KeyboardInterrupt:
            raise
        low = raw.lower()
        if not raw:
            continue
        if low == "terminal":
            terminal(); print(); say(bold("Back to the question: ") + q["text"]); continue
        if low == "laws":
            show_laws(); say(bold("Back to the question: ") + q["text"]); continue
        if low == "files":
            show_files(); continue
        if low == "status":
            status(st); continue
        if low in ("commands", "menu"):
            general_help(); continue
        if low == "save":
            raise SaveAndQuit()
        if low in ("hint", "help", "skip", "answer", "?"):
            st.hints += 1
            st.score += 3
            print()
            say(cyan("ANSWER: ") + bold(q["reveal"]))
            say(cyan("How to find it: ") + q["hint"], indent="   ")
            say(cyan("Why: ") + q["explain"], indent="   ")
            say(yellow("+3 points (answer shown). Moving on."))
            st.log.append(f"{q['id']}: answer shown via hint (+3)")
            return False
        n = norm(q["kind"], raw, q.get("options"))
        if q["kind"] == "mc" and (len(n) != 1 or n not in letters[:len(q["options"])]):
            say(dim(f"Type just the letter of your choice, for example  b")); continue
        if q["kind"] == "multi" and not n:
            say(dim("Type the letters of ALL correct choices, separated by commas, for example  a,c")); continue
        if q["kind"] == "num" and not n.isdigit():
            say(dim("Type a number, for example  250   (or type  terminal  to investigate first)")); continue
        if q["kind"] == "yn" and n not in ("yes", "no"):
            say(dim("Type  yes  or  no")); continue
        if q["kind"] == "date" and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", n):
            say(dim("Type the date like this:  2026-01-31   (year-month-day)")); continue
        tries += 1
        if H(q["id"] + ":" + n) in ANS[q["id"]]:
            pts = 10 if tries == 1 else 6 if tries == 2 else 3
            st.score += pts
            say(green(f"Correct! +{pts} points"))
            say(q["explain"], indent="   ")
            st.log.append(f"{q['id']}: correct on try {tries} (+{pts})")
            return True
        say(red("Not quite. Try again, or type  hint  to see the answer."))

def decision(st, d):
    """d: id, text, choices=[(text, pts, legal, trust, flag, outcome)]"""
    st.max_score += max(ch[1] for ch in d["choices"])
    print()
    say(bold("DECISION: ") + d["text"])
    choices = d["choices"][:]
    random.shuffle(choices)
    letters = "abcdef"[: len(choices)]
    for L, ch in zip(letters, choices):
        say(ch[0], indent=f"   {L}) ")
    print(dim("Not sure? Type  hint  to see the strongest choice.  Other commands: terminal | laws | files | status | save"))
    best = max(ch[1] for ch in d["choices"])
    hinted = False
    while True:
        raw = ask(yellow("decide> ")).strip().lower()
        if raw in ("hint", "help", "?"):
            for L, ch in zip(letters, choices):
                if ch[1] == best:
                    say(cyan("HINT: ") + f"The strongest choice is  {L}) {ch[0]}")
            say(dim("Type that letter to choose it (you'll earn 5 points instead of 10), or pick another."))
            if not hinted:
                hinted = True
                st.hints += 1
            continue
        if raw == "terminal":
            terminal(); continue
        if raw == "laws":
            show_laws(); continue
        if raw == "files":
            show_files(); continue
        if raw == "status":
            status(st); continue
        if raw == "save":
            raise SaveAndQuit()
        if len(raw) == 1 and raw in letters:
            break
        say(dim(f"Type one letter ({'/'.join(letters)})."))
    text, pts, legal, trust, flag, outcome = choices[letters.index(raw)]
    if hinted:
        pts = min(pts, 5)
    st.score += pts
    st.adjust(legal, trust)
    if flag:
        st.flags[flag] = True
    label = green("STRONG CHOICE") if choices[letters.index(raw)][1] == best else yellow("RISKY CHOICE") if pts > 0 else red("BAD CHOICE")
    print()
    say(f"{label}  (+{pts} points)")
    say(outcome, indent="   ")
    st.log.append(f"{d['id']}: chose '{text}' (+{pts})")
    return flag

class SaveAndQuit(Exception):
    pass

def message(when, sender, role, body):
    print()
    rule("=")
    print(f"  {cyan(when)}")
    print(f"  {bold('NEW MESSAGE')} from {bold(sender)}, {role}")
    rule("=")
    say(body, indent="  ")

# ---------------------------------------------------------------- missions
def m0_briefing(st):
    os.system("clear")
    rule("=")
    print(bold("   BRIGHTLINE SUPPLY CO.  |  BREACH RESPONSE SIMULATOR"))
    print(dim("   Module 6: Legal, Ethical, and Professional Issues in Information Security"))
    rule("=")
    say("\nWelcome to your first week as Brightline's security analyst. It's about to get busy.\n")
    while not st.name:
        st.name = ask("Your full name (for your report): ").strip()
    print()
    say(f"Thanks, {st.name.split()[0]}. Here's how this works:")
    general_help()
    say("\nYour score goes up when you answer correctly and make sound decisions. "
        "Two meters track how you're doing:")
    say(f"  {bold('Legal risk')}: how exposed Brightline is to fines and lawsuits (keep it LOW)")
    say(f"  {bold('Public trust')}: how customers, employees and the public see Brightline (keep it HIGH)")
    say("\nEverything here is fictional, including all people, card numbers and SSNs.")
    pause()

def m0_practice(st):
    print()
    rule("=")
    print(bold("   PRACTICE ROUND (not scored)"))
    rule("=")
    say("Before the real missions start, let's practice the two things you'll do most: "
        "using the investigation terminal and typing an answer. Nothing here counts.\n")
    say(bold("PRACTICE QUESTION: ") + "How many files are inside the folder case-files/leaked ?\n")
    say("Follow these steps exactly:")
    say("1. At the  answer>  prompt below, type   terminal   and press Enter.", indent="   ")
    say("2. At the  investigate$  prompt, type   ls case-files/leaked   and press Enter. "
        "You'll see the file names.", indent="   ")
    say("3. Count the file names. Then type   back   and press Enter.", indent="   ")
    say("4. At the  answer>  prompt, type the number and press Enter.", indent="   ")
    print()
    while True:
        raw = ask(yellow("answer> ")).strip().lower()
        if raw == "terminal":
            terminal()
            say(bold("Back to the practice question. ") + "How many files are in case-files/leaked ?")
            continue
        if raw in ("hint", "help", "?"):
            say(cyan("ANSWER: ") + bold("3") + "  (customers.csv, employees.csv and supplier-terms.txt). "
                "In the real missions, hint works the same way: it shows the answer and how to find it, "
                "and you earn 3 points instead of 10.")
            break
        if raw in ("skip", "save", "commands"):
            break
        if not raw:
            continue
        if norm("num", raw) == "3":
            say(green("Correct! That's exactly how every investigation question works."))
            break
        say(red("Not quite. ") + "Type  terminal , then  ls case-files/leaked , and count the names "
            "(customers.csv, employees.csv, supplier-terms.txt...). Then type  back  and answer.")
    say("\nTwo more things to know:")
    say("- At a DECISION, you type the letter of your choice. There are no hints for decisions, "
        "so think about what is legal, honest and goes through the proper channel.", indent="  ")
    say("- Stuck on any question? Type  hint  (or  help ) to see the answer and how to find it. "
        "You'll earn 3 points instead of 10, so try first!", indent="  ")
    say("- Type  save  at any prompt to stop and come back later. Type  commands  for the full list.",
        indent="  ")
    say(bold("\nThe real missions start now. Good luck!"))
    pause()

def m1_triage(st):
    message("SATURDAY, MARCH 21, 2026, 9:30 A.M.", "Marcus Bell", "CEO",
            "IT just called me. Someone broke into our file server last night and copied files. "
            "I need facts before I call our lawyer. Dana put copies of everything they took in "
            "case-files/leaked, and her incident summary is in case-files.\n\n"
            "Start with the incident summary, then tell me how bad this is.")
    say(dim("\nTip: type  terminal  and then  cat case-files/incident-summary.txt  to read the summary."))
    question(st, dict(id="m1q1", kind="num",
        text="How many customer records are in customers.csv? (Don't count the header line.)",
        hint="Open the terminal and run:  tail -n +2 case-files/leaked/customers.csv | wc -l   "
             "('tail -n +2' skips the first line, 'wc -l' counts lines.)",
        explain="Every one of these customers is now a person whose data was exposed.",
        reveal="2,400"))
    question(st, dict(id="m1q2", kind="num",
        text="How many Social Security numbers appear anywhere in the leaked files?",
        hint="Search every file for the SSN pattern ###-##-####:  "
             "grep -rEo \"[0-9]{3}-[0-9]{2}-[0-9]{4}\" case-files/leaked | wc -l",
        explain="SSNs are among the most sensitive identifiers. They can't be changed like a password.",
        reveal="140 (every employee's SSN)"))
    question(st, dict(id="m1q3", kind="mc",
        text="One file isn't about people at all. Which file contains a trade secret?",
        options=["customers.csv", "employees.csv", "supplier-terms.txt"],
        hint="Read the short text file:  cat case-files/leaked/supplier-terms.txt",
        explain="Secret supplier pricing is a trade secret. Its theft is a separate legal issue from privacy.",
        reveal="c) supplier-terms.txt"))

def m2_evidence(st):
    message("SATURDAY, 11:00 A.M.", "Dana Whitfield", "IT Manager",
            "The sales team can't work without the file server. I want to wipe it and reinstall "
            "everything this afternoon so we're back up by Monday. That gets rid of whatever the "
            "attacker left behind, too. OK with you?")
    decision(st, dict(id="m2d1",
        text="How do you answer Dana?",
        choices=[
            ("Go ahead and wipe it now. Getting the business running comes first.", 0, +20, -5, "wiped",
             "The attacker's tracks are gone, and so is the evidence law enforcement and your lawyers "
             "needed. Destroying evidence can hurt Brightline in court and may look like a cover-up."),
            ("First make a forensic copy of the server and save its logs, then rebuild.", 10, -10, +5, None,
             "Preserving evidence first protects Brightline's legal position and lets investigators "
             "trace the attacker. The rebuild only takes a few hours longer."),
            ("Leave it running exactly as is until Monday so no one touches anything.", 3, +5, -5, None,
             "The evidence is safe, but the attacker may still have access. Preserve and contain; "
             "don't just wait."),
        ]))
    question(st, dict(id="m2q1", kind="mc",
        text="The attacker logged in with an employee's stolen password. Which federal law makes that a crime?",
        options=["HIPAA", "Computer Fraud and Abuse Act (CFAA)", "FERPA", "Sarbanes-Oxley Act (SOX)"],
        hint="Type  laws  and read the U.S. federal laws table. Look for 'access a computer without authorization'.",
        explain="The CFAA criminalizes accessing a computer without authorization. A stolen password "
                "doesn't count as authorization.",
        reveal="b) Computer Fraud and Abuse Act"))
    question(st, dict(id="m2q2", kind="mc",
        text="Marcus wants to report the computer crime to federal law enforcement. Who should he contact?",
        options=["The FBI, through the Internet Crime Complaint Center (IC3)", "The local newspaper",
                 "The U.S. Department of Health and Human Services", "Nobody. Reporting will make us look bad."],
        hint="Check the 'Who to contact' table in the law cards (type laws).",
        explain="The FBI investigates federal computer crimes, including intrusions. Reporting early helps "
                "and shows good faith.",
        reveal="a) The FBI (IC3)"))
    if st.flags.get("wiped"):
        say(red("\n  Dana: \"Server's wiped. Uh-oh. The FBI agent just asked for our logs...\""))

def m3_florida(st):
    message("SUNDAY, MARCH 22, 10:00 A.M.", "Rosa Alvarez", "Brightline's outside legal counsel",
            "I'm handling the legal side. Brightline is a Florida company, so let's start with the "
            "Florida Information Protection Act (FIPA). Read the FIPA card in the law cards first. "
            "Not every exposed record counts as 'personal information' under the law. I need exact "
            "numbers.")
    question(st, dict(id="m3q1", kind="num",
        text="How many FLORIDA customers had their card number AND security code (CVV) exposed?",
        hint="Column 6 is state and column 8 is payment_method. Run:  "
             "awk -F, '$6==\"FL\" && $8==\"card\"' case-files/leaked/customers.csv | wc -l",
        explain="Under FIPA, a card number counts as personal information when it comes with the "
                "security code, which is exactly what Brightline stored.",
        reveal="912"))
    question(st, dict(id="m3q2", kind="mc",
        text="Some Florida customers pay by invoice, so only their name and email address were exposed. "
             "Are they 'personal information' under FIPA?",
        options=["Yes. Any name with contact information counts.",
                 "No. FIPA needs a name plus something like an SSN, ID number, card number with "
                 "security code, or health information, or an email WITH a password."],
        hint="Read the FIPA card's list of what counts as personal information. Was there a password column?",
        explain="Right. Name plus email alone isn't FIPA personal information, so these customers don't "
                "count toward Florida's notice requirements. (Other laws, like GDPR, define it more broadly.)",
        reveal="b) No"))
    question(st, dict(id="m3q3", kind="num",
        text="How many employees who LIVE in Florida had their SSNs exposed?",
        hint="In employees.csv, home_state is column 7. Adapt the awk command:  "
             "awk -F, '$7==\"FL\"' case-files/leaked/employees.csv | wc -l",
        explain="Employees are protected by breach laws too, not just customers.",
        reveal="131"))
    question(st, dict(id="m3q4", kind="num",
        text="So, how many Florida residents in total must Brightline notify under FIPA?",
        hint="Add the Florida customers whose card number and CVV were exposed to the Florida "
             "employees. Don't include invoice-only customers.",
        explain="That total decides which other notices are required.",
        reveal="1,043 (912 customers + 131 employees)"))
    question(st, dict(id="m3q5", kind="multi",
        text="Based on that total, who must Brightline notify under FIPA? Choose ALL that apply.",
        options=["Each affected Florida resident",
                 "The Florida Department of Legal Affairs (Attorney General)",
                 "The nationwide consumer reporting agencies (credit bureaus)",
                 "Local TV stations",
                 "The U.S. Department of Health and Human Services"],
        hint="FIPA card: individuals always; the Attorney General at 500 or more; the credit bureaus "
             "when MORE than 1,000. Compare with your total.",
        explain="Note that the 1,000 threshold is crossed only when customers and employees are added "
                "together. Analysts who count only customers get this wrong.",
        reveal="a, b and c"))
    question(st, dict(id="m3q6", kind="date",
        text="IT discovered the breach on March 21, 2026. What's the LAST day to notify Florida residents?",
        hint="FIPA allows no more than 30 days after the breach is discovered. Count 30 days from "
             "March 21 (March has 31 days).",
        explain="Notice should go out as fast as practical. 30 days is the legal maximum, not the goal.",
        reveal="2026-04-20"))

def m4_pressure(st):
    message("MONDAY, MARCH 23, 8:30 A.M.", "Priya Raman", "Chief Financial Officer",
            "I hear legal wants to send breach letters right away. Our big spring sale starts next "
            "week and it's 20% of our annual revenue. If customers get a letter saying we were hacked, "
            "they'll shop somewhere else. Let's hold the letters until after the sale. That's about "
            "45 days from discovery. Nobody needs to know before then.")
    decision(st, dict(id="m4d1",
        text="How do you respond to Priya?",
        choices=[
            ("Agree. She's an executive and it's her call.", 0, +20, -10, "agreed_delay",
             "Following an instruction to break the law isn't a defense. You've also made yourself part "
             "of the problem."),
            ("Explain that Florida requires notice within 30 days, and bring it to Rosa (counsel) and the CEO.", 10, -10, +5, None,
             "You stayed respectful, stated the law, and escalated through the proper channel. Rosa backs "
             "you up, and the CEO overrules the delay."),
            ("Secretly tip off a reporter so the story comes out.", 2, +5, -10, "leaked_press",
             "You meant to protect customers, but you skipped internal escalation and broke "
             "confidentiality. The story runs with wrong numbers, and Brightline loses control of the message."),
            ("Quit on the spot.", 1, +5, 0, None,
             "Brightline just lost the one person who knew the deadline. Escalate first; leave only if "
             "the company refuses to follow the law."),
        ]))
    say(dim("\nLater that morning, Marcus asks you to recommend the notification date."))
    flag = decision(st, dict(id="m4d2",
        text="When should Brightline notify affected Florida residents?",
        choices=[
            ("Friday, March 27 (6 days after discovery)", 10, -10, +15, "notice_fast",
             "Fast, legal and honest. Customers can freeze their cards and watch their credit early. "
             "Trust takes a hit from the breach, but it rises because you were open about it."),
            ("Friday, April 17 (27 days after discovery)", 5, 0, -5, "notice_slow",
             "Legal, but barely. Customers spent nearly four weeks unaware that their card data was out."),
            ("Tuesday, May 5 (45 days, after the sale)", 0, +25, -20, "notice_late",
             "This is 15 days past the deadline. Florida's penalty is $1,000 per day for the first 30 days "
             "of violation, so that's $15,000, and the delay becomes the headline."),
            ("Don't notify unless the stolen data shows up online", 0, +40, -30, "notice_never",
             "A clear violation. The data surfaces two months later, and the penalties keep growing: "
             "$30,000 for the first 30 days, then $50,000 per 30-day period, up to $500,000."),
        ]))
    if flag == "notice_late":
        st.fines += 15000
    elif flag == "notice_never":
        st.fines += 180000

def m5_beyond(st):
    message("MONDAY, 10:00 A.M.", "Rosa Alvarez", "Legal counsel",
            "Florida's covered. Now the rest of the world. Brightline's online store ships "
            "internationally, so check where our customers live. I'm especially worried about Europe.")
    question(st, dict(id="m5q1", kind="num",
        text="How many customers in the leak live in the European Union? (Country codes DE, FR, IE, ES, NL.)",
        hint="Count customers by country (column 7), then add the five EU countries:  "
             "awk -F, 'NR>1 {print $7}' case-files/leaked/customers.csv | sort | uniq -c",
        explain="Under GDPR, even a name and email address are 'personal data', so all of them count.",
        reveal="120"))
    question(st, dict(id="m5q2", kind="num",
        text="Under GDPR, how many HOURS does Brightline have to report the breach to the EU authority?",
        hint="Type laws and read the International (GDPR) card.",
        explain="72 hours from becoming aware. That's much faster than Florida's 30 days.",
        reveal="72"))
    decision(st, dict(id="m5d1",
        text="It's Monday at 10:00 a.m. Brightline discovered the breach Saturday at 9:15 a.m. What do you recommend?",
        choices=[
            ("Report to the EU supervisory authority today. We're at about 49 hours.", 10, -10, +5, None,
             "Just in time, with 23 hours to spare. Working out the facts quickly on Saturday made this possible."),
            ("Wait and send everything with the Florida letters on Friday.", 0, +20, -5, "gdpr_late",
             "Friday is about 6 days after discovery, far past the 72-hour limit. GDPR fines can be very large."),
            ("Do nothing. GDPR is a European law and we're an American company.", 0, +25, -5, "gdpr_ignored",
             "GDPR applies to organizations anywhere that offer goods or services to people in the EU. "
             "Brightline's online store does exactly that."),
        ]))
    question(st, dict(id="m5q3", kind="mc",
        text="Customers from Georgia, Alabama, New York, Texas and California were also exposed. What applies to them?",
        options=["Only Florida law, because Brightline is a Florida company.",
                 "Each state's own breach law, because those laws protect that state's residents."],
        hint="Read the last bullet of the FIPA card.",
        explain="Every U.S. state has its own breach law, with different definitions and deadlines. That's "
                "why companies hire lawyers who track all of them.",
        reveal="b) Each state's own law"))
    question(st, dict(id="m5q4", kind="yn",
        text="Priya asks: 'We have employee wellness data somewhere. Does HIPAA apply to Brightline?'",
        hint="Read the HIPAA row. Who does it cover? Is an office-supply company one of them?",
        explain="No. HIPAA covers health plans, health care providers, clearinghouses and their business "
                "associates. Brightline is none of these.",
        reveal="no"))

def m6_cards(st):
    message("TUESDAY, MARCH 24, 9:00 A.M.", "Gulf Coast Payments", "Brightline's card processor",
            "We've been told about your breach. Our records show your online store saved customers' "
            "card security codes (CVVs) after processing payments. This is a serious violation of "
            "your merchant agreement. You may face fines, and we may suspend your ability to accept "
            "cards.")
    question(st, dict(id="m6q1", kind="mc",
        text="Which standard prohibits storing card security codes after a payment is approved?",
        options=["HIPAA", "Sarbanes-Oxley (SOX)", "PCI DSS", "FERPA"],
        hint="Type laws and read the 'Industry standard (not a law)' card.",
        explain="PCI DSS is created by the card brands and enforced through merchant contracts.",
        reveal="c) PCI DSS"))
    question(st, dict(id="m6q2", kind="yn",
        text="Is PCI DSS a law passed by the government?",
        hint="Read the first bullet of the PCI DSS card.",
        explain="No. It's an industry standard enforced by contract. Breaking it can still mean fines and "
                "losing the ability to accept cards, so businesses take it as seriously as a law.",
        reveal="no"))
    question(st, dict(id="m6q3", kind="mc",
        text="The stolen card numbers are being used for fraud. Which federal agency investigates payment-card crimes?",
        options=["The FTC", "The U.S. Secret Service", "CISA", "The Florida Department of Legal Affairs"],
        hint="Check the 'Who to contact' table in the law cards.",
        explain="The Secret Service investigates financial crimes, including payment-card fraud.",
        reveal="b) The U.S. Secret Service"))
    decision(st, dict(id="m6d1",
        text="The web developer asks: 'Should I delete the stored CVVs? Repeat customers like not retyping them.'",
        choices=[
            ("Delete all stored CVVs now and change checkout so they're never saved.", 10, -10, +5, None,
             "Correct. Removing data you aren't allowed to keep is the fastest way to reduce risk."),
            ("Keep them. Customer convenience matters.", 0, +15, -10, "kept_cvv",
             "You're knowingly continuing a violation. Gulf Coast Payments suspends card processing."),
            ("Keep them, but encrypt them.", 3, +5, 0, None,
             "Better than plain text, but PCI DSS still forbids keeping CVVs at all after a payment is approved."),
        ]))
    if st.flags.get("kept_cvv"):
        st.fines += 25000

def m7_pentest(st):
    message("TUESDAY, 11:00 A.M.", "Jordan Miles", "Junior tester, SecureCheck Consulting",
            "Hi! Marcus hired us to test your defenses. He signed our Rules of Engagement yesterday "
            "(case-files/rules-of-engagement.txt). I've got a list of things I want to do today. Can "
            "you tell me which ones I'm allowed to do? I want to stay legal!")
    say(dim("\nTip: type  terminal  then  cat case-files/rules-of-engagement.txt  to read the rules first."))
    print()
    say("For each request, answer  y  (allowed) or  n  (not allowed). A request is allowed only if "
        "it passes ALL of these: the right system (10.10.10.20), the right ports (80/443), the right "
        "dates and hours, and it's not on the NOT ALLOWED list.")
    ok = ask(dim("\nType  terminal  to read the rules first (recommended), or press Enter to start: ")).strip().lower()
    if ok == "terminal":
        terminal()
    reqs = [
        ("Run an Nmap scan of 10.10.10.20, ports 80 and 443, at 10 a.m. today.", True,
         "In scope: the right system, the right ports and inside the testing window."),
        ("The fileserver at 10.10.10.30 is on the same network, so I'll scan it too.", False,
         "Out of scope. Only 10.10.10.20 is authorized. Scanning other systems could violate the CFAA."),
        ("Email the sales team a fake invoice to see who clicks.", False,
         "Out of scope. Social engineering of any kind is prohibited."),
        ("Run the vulnerability scan at 2 a.m. tonight, when the site is quiet.", False,
         "Out of scope. Testing is allowed only between 8 a.m. and 6 p.m. Eastern."),
        ("Try the test login I found in the website's HTML comments on the website's login page.", True,
         "In scope. Credentials found during the test may be used against in-scope systems."),
        ("Download the customer database I found in /old-backup/ to study at home.", False,
         "Out of scope. Copying customer data is prohibited. Stop, record the location and report it "
         "to the CEO within 24 hours."),
        ("Flood the website with traffic to see how much it can take.", False,
         "Out of scope. Denial-of-service is prohibited."),
        ("We're behind, so I'll keep testing on Saturday, March 28.", False,
         "Out of scope. The testing window ends March 27."),
    ]
    right = 0
    for i, (text, allowed, why) in enumerate(reqs, 1):
        st.max_score += 3
        print()
        say(bold(f"Request {i} of {len(reqs)}: ") + f"\"{text}\"")
        shown = False
        while True:
            a = ask(yellow("Allowed? (y/n, hint to see the answer, terminal to re-read the rules) > ")).strip().lower()
            if a == "terminal":
                terminal(); continue
            if a in ("hint", "help", "?"):
                shown = True
                break
            if a in ("y", "yes", "n", "no"):
                break
        if shown:
            st.hints += 1
            st.score += 1
            say(cyan("ANSWER: ") + bold("Allowed" if allowed else "NOT allowed") + "  (+1 point)  " + why)
            continue
        correct = (a.startswith("y") == allowed)
        if correct:
            right += 1
            st.score += 3
            say(green("Correct. +3  ") + why)
        else:
            st.adjust(legal=+3)
            say(red("Wrong.  ") + why)
    st.log.append(f"m7: authorization review {right}/{len(reqs)} correct")
    say(f"\nYou judged {right} of {len(reqs)} requests correctly.")
    if right == len(reqs):
        say(green("Jordan: \"Perfect, thanks! I'll stick to the plan.\""))

def m8_week(st):
    message("WEDNESDAY TO FRIDAY, MARCH 25-27", "Your inbox", "the rest of the week",
            "The legal work is on track. Now come the people problems. A few situations land on your "
            "desk this week.")
    decision(st, dict(id="m8d1",
        text="Marcus: 'Kim Nguyen in Accounts Payable is the one who clicked the phishing link. "
             "Should we fire her and announce it to all staff as a warning?'",
        choices=[
            ("Yes. Fire her publicly so everyone takes security seriously.", 0, +5, -15, "blamed_kim",
             "Staff now hide mistakes instead of reporting them. The next phishing click goes unreported for days."),
            ("No. Retrain everyone, turn on multi-factor authentication, and praise fast reporting.", 10, -5, +10, None,
             "A no-blame culture gets mistakes reported quickly, and MFA would have stopped the stolen "
             "password from working. That fixes the system, not just one person."),
            ("Quietly let it go and change nothing.", 2, +5, -5, None,
             "No blame, but no fix either. The same attack will work again."),
        ]))
    decision(st, dict(id="m8d2",
        text="A friend at another company texts: 'Can you hack our company website tonight and see if it's secure? My boss won't care.'",
        choices=[
            ("Sure, run a scan tonight. You're helping.", 0, +5, 0, "unauthorized_scan",
             "Your friend can't authorize testing a system they don't own. This could violate the CFAA, "
             "just like Jordan's out-of-scope requests."),
            ("Decline, and explain they need written permission from the system owner, like a Rules of Engagement.", 10, 0, +2, None,
             "Right. Authorization comes in writing, from someone with the authority to give it, with a "
             "defined scope."),
            ("Only look up public info like DNS and WHOIS, nothing more.", 5, 0, 0, None,
             "Public lookups are legal, but better still to explain how to get a proper, authorized test."),
        ]))
    decision(st, dict(id="m8d3",
        text="A recruiter from a competitor offers you a job with a $10,000 bonus 'if you bring along Brightline's supplier pricing.'",
        choices=[
            ("Accept and bring the pricing file.", 0, +15, -10, "took_secret",
             "That's theft of a trade secret, which can be a federal crime under the Economic Espionage Act."),
            ("Decline the condition. You'll only consider the job without it.", 10, 0, 0, None,
             "You can change jobs; you can't take confidential information with you."),
            ("Accept, but only tell them the prices verbally.", 0, +15, -10, "took_secret",
             "Saying a trade secret out loud is still disclosing it."),
        ]))
    decision(st, dict(id="m8d4",
        text="You notice a coworker using a cracked (pirated) copy of expensive design software on a company laptop.",
        choices=[
            ("Talk to the coworker, then report it through IT's normal process.", 10, -3, 0, None,
             "Pirated software brings copyright risk and often malware, which is the last thing Brightline needs this week."),
            ("Ignore it. Not your business.", 2, +3, 0, None,
             "As the security analyst, it is your business. Cracked software is a common way malware gets in."),
            ("Ask for a copy too.", 0, +5, 0, None,
             "That's copyright infringement, and it spreads the risk."),
        ]))
    decision(st, dict(id="m8d5",
        text="Friday afternoon, a local reporter calls your desk: 'We hear Brightline was hacked. How many customers were affected?'",
        choices=[
            ("Give the numbers. The public has a right to know.", 2, +5, 0, None,
             "Transparency matters, but you aren't the authorized spokesperson, and partial numbers cause confusion."),
            ("Politely refer them to Brightline's spokesperson or legal counsel.", 10, -2, +3, None,
             "Correct. Official, accurate communication protects both the public and Brightline."),
            ("Say 'Nothing was taken.'", 0, +15, -20, "lied_press",
             "That's a lie, and it comes out when the notification letters arrive. Trust collapses."),
            ("Say 'No comment' and hang up.", 5, 0, -2, None,
             "Not wrong, but sending them to the right contact is more professional."),
        ]))

# ---------------------------------------------------------------- ending
def headlines(st):
    f = st.flags
    out = []
    if f.get("notice_fast") and not f.get("lied_press"):
        out.append("\"Brightline Moves Quickly to Warn Customers After Breach\" - Orlando Business Journal")
    if f.get("notice_late"):
        out.append("\"Brightline Waited Until After Big Sale to Disclose Hack\" - Tampa Bay Ledger")
    if f.get("notice_never"):
        out.append("\"Stolen Brightline Data Found Online; Customers Were Never Told\" - Florida Times")
    if f.get("wiped"):
        out.append("\"FBI: Key Evidence Destroyed in Brightline Hack\" - Gulf Coast Courier")
    if f.get("gdpr_late") or f.get("gdpr_ignored"):
        out.append("\"EU Regulator Opens Inquiry Into Florida Retailer\" - European Data Report")
    if f.get("lied_press"):
        out.append("\"Brightline Denied Any Data Was Stolen, Days Before Breach Letters Went Out\" - Channel 6 News")
    if f.get("leaked_press"):
        out.append("\"Insider Leaks Hack Details; Numbers Prove Wrong\" - Sunshine State Wire")
    if f.get("kept_cvv"):
        out.append("\"Card Processor Cuts Off Brightline's Online Store\" - Retail Today")
    if f.get("blamed_kim"):
        out.append("\"Employees Say Brightline Punishes People Who Report Mistakes\" - Workplace Weekly")
    if f.get("took_secret"):
        out.append("\"Former Brightline Analyst Investigated for Trade Secret Theft\" - Florida Legal News")
    if not out:
        out.append("\"Breach at Brightline Handled by the Book, Experts Say\" - Florida Tech Review")
    return out

def finale(st):
    print()
    rule("=")
    print(bold("   FINAL DEBRIEF"))
    rule("=")
    pct = round(100 * max(0, st.score) / st.max_score) if st.max_score else 0
    grade = ("Outstanding: ready for the job" if pct >= 90 else
             "Strong: a few lessons to review" if pct >= 75 else
             "Developing: review the law cards and try again" if pct >= 55 else
             "Needs work: replay the simulator")
    say(f"\nAnalyst: {bold(st.name)}")
    say(f"Score: {bold(str(st.score))} out of {st.max_score} possible ({pct}%)  -  {grade}")
    say(f"Hints used: {st.hints}")
    status(st)
    say(bold("\nHow the week played out in the news:"))
    for h in headlines(st):
        say(h, indent="  ")
    if st.fines:
        say(red(f"\nEstimated fines and penalties: ${st.fines:,}"))
    else:
        say(green("\nEstimated fines and penalties: $0"))
    say(bold("\nKey lessons from Module 6:"))
    for line in [
        "Laws set the minimum; ethics often asks for more (Florida allows 30 days, but faster is better).",
        "Not every record is 'personal information'. Definitions differ by law (FIPA vs. GDPR).",
        "Thresholds can depend on adding groups together (customers + employees = 1,043).",
        "Authorization must be in writing and in scope. Without it, testing is a crime (CFAA).",
        "Industry standards like PCI DSS aren't laws, but contracts make them binding.",
        "Preserve evidence, escalate through proper channels, and never lie to the public.",
        "People cause and stop breaches: a no-blame culture and MFA beat firing the person who clicked.",
    ]:
        say(line, indent="  - ")
    code = H(f"{st.name}|{st.score}|{st.max_score}")[:8].upper()
    lines = [
        "=" * 60,
        "BRIGHTLINE BREACH RESPONSE SIMULATOR - REPORT",
        f"Student: {st.name}",
        f"Started: {st.started}   Finished: {datetime.datetime.now():%Y-%m-%d %H:%M}",
        f"Score: {st.score} / {st.max_score} ({pct}%)   Hints used: {st.hints}",
        f"Legal risk: {st.legal_risk}   Public trust: {st.trust}   Fines: ${st.fines:,}",
        f"Verification code: {code}",
        "Headlines: " + " | ".join(headlines(st)),
        "Answer log:",
    ] + ["  " + l for l in st.log] + [""]
    os.makedirs(RESULTS, exist_ok=True)
    with open(REPORT, "a", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    if os.path.exists(SAVE):
        os.remove(SAVE)
    say(f"\nYour report was saved to {bold('results/simulator-report.txt')}  (verification code {code}).")
    rule("=")
    say(bold("WHAT TO DO NEXT"))
    say("1. Want a better score? Type   python3 simulator.py   to play again. Every finished "
        "attempt is kept in your report.", indent="   ")
    say("2. Open  writeup.txt  in the file list on the left, type your answers under each "
        "question, and press Ctrl+S to save.", indent="   ")
    say("3. Download two files: right-click  results/simulator-report.txt  and choose Download, "
        "then do the same for  writeup.txt . Upload both to your course website.", indent="   ")
    say("4. Stop your codespace: click 'Codespaces' at the bottom left, then 'Stop Current Codespace'.",
        indent="   ")
    say("Full instructions are in README.md, Part 6.")
    rule("=")

MISSIONS = [m0_briefing, m0_practice, m1_triage, m2_evidence, m3_florida, m4_pressure,
            m5_beyond, m6_cards, m7_pentest, m8_week]

def main():
    st = None
    if os.path.exists(SAVE):
        try:
            saved = State.load()
            a = ask(f"Saved game found for {saved.name} (mission {max(0, saved.mission - 1)} of {len(MISSIONS) - 2}). "
                    "Resume? (y/n) ").strip().lower()
            if a.startswith("y"):
                st = saved
        except (ValueError, KeyError):
            pass
    if st is None:
        st = State()
    try:
        while st.mission < len(MISSIONS):
            snapshot = json.dumps(st.__dict__)
            try:
                MISSIONS[st.mission](st)
            except SaveAndQuit:
                st.__dict__.update(json.loads(snapshot))
                st.save()
                say(yellow("\nSaved. You'll restart this mission next time. "
                           "Run  python3 simulator.py  to continue."))
                return
            st.mission += 1
            st.save()
            if 2 < st.mission < len(MISSIONS):
                status(st)
                pause()
        finale(st)
    except KeyboardInterrupt:
        print()
        say(yellow("Stopped. Progress from completed missions is saved. "
                   "Run  python3 simulator.py  to resume."))


WHERE = {
 "m1q1": "customers.csv in case-files/leaked. Count its lines, minus the 1 header line.",
 "m1q2": "Every file in case-files/leaked. An SSN looks like 123-45-6789.",
 "m1q3": "Read supplier-terms.txt (a short text file) with  cat .",
 "m2q1": "Law cards (type  laws ), the 'U.S. federal laws' table.",
 "m2q2": "Law cards (type  laws ), the 'Who to contact' table.",
 "m3q1": "customers.csv: column 6 = state, column 8 = payment_method. Law card: Florida (FIPA).",
 "m3q2": "Law card: Florida (FIPA), the list of what counts as 'personal information'.",
 "m3q3": "employees.csv: column 7 = home_state.",
 "m3q4": "Your answers to the last three questions. Only count people whose data meets FIPA's definition.",
 "m3q5": "Law card: Florida (FIPA). Compare your total with 500 and 1,000.",
 "m3q6": "Law card: Florida (FIPA) deadline. The discovery date is in the incident summary.",
 "m5q1": "customers.csv: column 7 = country.",
 "m5q2": "Law card: International (GDPR).",
 "m5q3": "Law card: Florida (FIPA), the last bullet.",
 "m5q4": "Law card: the HIPAA row (who it covers). The incident summary says what Brightline is.",
 "m6q1": "Law card: 'Industry standard (not a law)'.",
 "m6q2": "Law card: 'Industry standard (not a law)', first bullet.",
 "m6q3": "Law card: 'Who to contact' table."
}

# Answer fingerprints (hashed so the answers aren't readable here)
ANS = {
 "m1q1": [
  "a84c41b068dc4167"
 ],
 "m1q2": [
  "1e58eb05398ec215"
 ],
 "m1q3": [
  "10ce49733d60b7eb"
 ],
 "m2q1": [
  "4d3b035fd457f7a8"
 ],
 "m2q2": [
  "e2433ee4d6e73310"
 ],
 "m3q1": [
  "22b0538b2bccfcfe"
 ],
 "m3q2": [
  "a7f7aea680c6d9bd"
 ],
 "m3q3": [
  "99082fe75e78a673"
 ],
 "m3q4": [
  "232002eead0c63ca"
 ],
 "m3q5": [
  "d54ddb5514441a14"
 ],
 "m3q6": [
  "7d92d48c023f8beb"
 ],
 "m5q1": [
  "6d39ddc615805a39"
 ],
 "m5q2": [
  "4ac3a019b6738a93"
 ],
 "m5q3": [
  "597d3cd904443daf"
 ],
 "m5q4": [
  "03d02058da9a9298"
 ],
 "m6q1": [
  "9e5065e9306f24d2"
 ],
 "m6q2": [
  "50d7debea7b4c02e"
 ],
 "m6q3": [
  "f9adcbd4482b9639"
 ]
}

if __name__ == "__main__":
    main()
