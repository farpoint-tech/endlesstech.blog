# AI Code Review Policy — endlesstech.blog

**Repository:** farpoint-tech/endlesstech.blog  
**Owner:** Philipp Schmidt  
**Effective Date:** 2026-03-17  
**Status:** ACTIVE  
**Reason:** Remediation of OWASP Pentest Finding G-01 (CSLAB-2026-03-17-001)

---

## 1. Purpose

This policy defines the mandatory human review process for all commits authored by AI coding assistants (Claude, Manus, GitHub Copilot, or any other AI agent). It ensures that no AI-generated code is deployed to production without documented human oversight, in alignment with the security posture expected of a professional Microsoft 365 Security Architect.

---

## 2. Scope

This policy applies to all commits where the Git author email matches any of the following patterns:

| AI Agent | Email Pattern |
|---|---|
| Anthropic Claude | `*@anthropic.com` |
| Manus AI | `*@manus.im` |
| GitHub Copilot | `*@github.com` (bot commits) |
| Any other AI | Any commit message containing `[AI]`, `[bot]`, or `[automated]` |

---

## 3. Mandatory Review Checklist

Before any AI-authored commit is merged into `master`, the human reviewer **must** verify:

- [ ] **Security Headers:** Confirm that no security headers (CSP, X-Frame-Options, HSTS, X-Content-Type-Options) have been removed or weakened.
- [ ] **External Resources:** Confirm that no new external CDN links, tracking scripts, or third-party JavaScript has been introduced.
- [ ] **Sensitive Data:** Confirm that no API keys, session URLs, Personal Access Tokens, or credentials appear in the commit diff or commit message.
- [ ] **HTML Integrity:** Confirm that all HTML files are valid and render correctly in a local browser preview.
- [ ] **Link Integrity:** Confirm that no existing internal links have been broken.
- [ ] **No Malicious Payloads:** Confirm that no `<script>` tags with unexpected `src` attributes or inline JavaScript have been added.

---

## 4. Process

1. AI agent creates a branch and opens a Pull Request.
2. The GitHub Actions workflow `ai-commit-check.yml` automatically detects the AI author and labels the PR with `ai-authored`.
3. A human reviewer (Philipp Schmidt) works through the checklist above.
4. The reviewer approves the PR only after all checklist items are confirmed.
5. The reviewer adds a comment: `✅ AI Code Review Complete — [date] — [reviewer name]`.
6. The PR is merged by the reviewer. Direct push to `master` by AI agents is blocked by branch protection rules.

---

## 5. Commit Message Hygiene

Commit messages **must not** contain:
- Session URLs from AI tools (e.g., `claude.ai/*/session_*`, `manus.im/*/session_*`)
- Personal Access Tokens or secrets
- Internal IP addresses or infrastructure details

A pre-commit hook (`.git/hooks/commit-msg`) is recommended to enforce this locally.

---

## 6. Incident Response

If an AI-authored commit is discovered to have been pushed directly to `master` without human review:

1. Immediately revert the commit: `git revert <commit-hash>`
2. Audit the diff for any of the items in Section 3.
3. Document the incident in the repository's Security Log.
4. Re-apply the commit after completing the full review checklist.

---

## 7. Policy Review

This policy is reviewed every 6 months or after any security incident. Next review: **2026-09-17**.

---

*This policy was created as part of the remediation of OWASP Pentest Assessment CSLAB-2026-03-17-001, Finding G-01.*
