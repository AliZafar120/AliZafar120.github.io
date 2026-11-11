# Encrypted session logs

Claude Code session records behind the LeetGPU course pages. Each `.enc` file is AES-256-CBC with PBKDF2 (200000 iterations, salted), made with OpenSSL. The passphrase is not stored here.

Decrypt one file:

    openssl enc -d -aes-256-cbc -pbkdf2 -iter 200000 -in FILE.enc -out FILE -pass pass:PASSPHRASE

Files:

- `12f763b1-leetgpu-prompts.jsonl.enc` / `.md.enc`: recovered prompts from the Oct 5-6 2026 session that built these pages.
- `c8b2710f-current-session.jsonl.enc`: full transcript of the Nov 2026 session that investigated and published them.
