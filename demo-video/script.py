# Builds the narration and captions from real.json so the numbers always match the data.
import json
def build(real):
    r = real["run"]; f = lambda x: f"{x:.2f}"; d = r["auditFinal"] - r["auditBase"]
    if d <= -0.05: audit = f"Then Reppo audits the before and after. The judge scored this run from {f(r['judgeBase'])} to {f(r['judgeFinal'])}. Reppo scored it from {f(r['auditBase'])} to {f(r['auditFinal'])}, which is lower, and EvalLoop flagged the disagreement. That is why one judge is not enough."
    elif d >= 0.05: audit = f"Then Reppo audits the before and after. The judge scored this run from {f(r['judgeBase'])} to {f(r['judgeFinal'])}. Reppo scored the audited case from {f(r['auditBase'])} to {f(r['auditFinal'])}. Two independent graders agree on the direction."
    else: audit = f"Then Reppo audits the before and after. The judge moved from {f(r['judgeBase'])} to {f(r['judgeFinal'])}, Reppo from {f(r['auditBase'])} to {f(r['auditFinal'])}. That is inconclusive, and EvalLoop says so."
    return {
      "s1": "You changed one line in your agent's prompt. Did it actually get better?",
      "s2": "Most teams check a few examples and ship. Or they ask the same model to grade its own work. Neither is evidence, and the first sign of trouble is an angry customer.",
      "s3": "EvalLoop is a safety check for prompt changes. It runs your agent, judges every answer, proposes one new rule at a time, and has an independent grader audit the result.",
      "s4": "Here is a live run. The agent answers a fixed test set. A SERV Reasoning judge scores it, a new rule is proposed, and every step is added to a hash-chained ledger.",
      "s5": "A rule is kept only if the average gain holds, the confidence is high, no single case collapses, and held-out cases do not get worse. Otherwise, it is rolled back.",
      "s6": audit,
      "s7": "Share a run as a public proof page or a badge. Prompts and answers stay private. Block bad changes in CI. Free to start, and Pro is a draft twenty-nine dollars a month for teams shipping support and ops agents.",
      "s8": "EvalLoop. Improve your agent, and prove it. Built on SERV Reasoning, audited by Reppo.",
    }
