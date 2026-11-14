# EvalLoop demo narration (one file per scene for ElevenLabs: s1.mp3 ... s8.mp3)

## s1 (5.67s)
You changed one line in your agent's prompt. Did it actually get better?

## s2 (12.41s)
Most teams check a few examples and ship. Or they ask the same model to grade its own work. Neither is evidence, and the first sign of trouble is an angry customer.

## s3 (12.25s)
EvalLoop is a safety check for prompt changes. It runs your agent, judges every answer, proposes one new rule at a time, and has an independent grader audit the result.

## s4 (13.77s)
Here is a live run. The agent answers a fixed test set. A SERV Reasoning judge scores it, a new rule is proposed, and every step is added to a hash-chained ledger.

## s5 (12.8s)
A rule is kept only if the average gain holds, the confidence is high, no single case collapses, and held-out cases do not get worse. Otherwise, it is rolled back.

## s6 (17.92s)
Then Reppo audits the before and after. The judge scored this run from 0.17 to 0.83. Reppo scored the audited case from 0.77 to 0.95. Two independent graders agree on the direction.

## s7 (15.67s)
Share a run as a public proof page or a badge. Prompts and answers stay private. Block bad changes in CI. Free to start, and Pro is a draft twenty-nine dollars a month for teams shipping support and ops agents.

## s8 (8.07s)
EvalLoop. Improve your agent, and prove it. Built on SERV Reasoning, audited by Reppo.

