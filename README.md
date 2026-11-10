# EvalLoop
Improves an agent's instructions on a fixed test set (SERV judge, Prompt Guard + Shadow Agent), keeps a revision only if it passes a statistical acceptance rule with a held-out guard, then has Reppo audit baseline vs final. Everything is written to a hash-chained ledger.

    node evalloop.mjs --selftest   # offline checks, no keys
    node evalloop.mjs --demo       # sandbox server on :8787, no keys
    # live: export the variables in .env.example, then
    node evalloop.mjs

## Deploy (Fly.io, one machine: state lives in a JSON/JSONL volume)
    fly launch --no-deploy --copy-config
    fly volumes create evalloop_data --size 1
    fly secrets set OPENSERV_API_KEY=... REPPO_API_KEY=... SESSION_SECRET=$(openssl rand -hex 32) ADMIN_TOKEN=$(openssl rand -hex 16)
    fly deploy
Grant Pro to a design partner: `curl -X POST https://YOURAPP.fly.dev/api/admin/plan -H 'x-evalloop: 1' -H "x-admin-token: $ADMIN_TOKEN" -H 'content-type: application/json' -d '{"email":"them@co.com","plan":"pro"}'`
Upgrade requests are appended to `/data/leads.jsonl`. Back up `/data`.

## Known limits
Reppo request/response field names are partly unverified (see `toPayload`/`fromResult`). Reppo allows one pending evaluation per account, so audits are sequential and small. No billing integration yet: Pro is granted by hand. Single machine only.

## CI gate
    EVALLOOP_KEY=elk_... node evalloop.mjs gate --file run.json --url https://YOURAPP.fly.dev --min 0.7
Exit 0 pass, 1 fail, 2 error. `run.json` is the body of `POST /api/runs`. The key comes from the console's API key button.

## Audit
Reppo when its API answers; otherwise a different model family through SERV (`SERV_AUDIT_MODEL`), labelled as a weaker cross-model audit.

Verify a downloaded ledger offline: `node evalloop.mjs verify ledger.json`.
