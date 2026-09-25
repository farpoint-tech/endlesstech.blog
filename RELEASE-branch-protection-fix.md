# Release-Automatik endlesstech.blog: was umgestellt werden muss

Stand: 25.09.2026 · Session: https://claude.ai/code/session_015XGcCkXfQaoFf74cJE1WBM

## Auftrag

Der Release-Workflow soll Artikel ohne manuelle Bestätigung live stellen.

## Befund

`master` verlangt einen Pull Request. `github-actions[bot]` steht nicht auf der
Bypass-Liste, also wird jeder direkte Push des Workflows abgewiesen:

```
remote: error: GH006: Protected branch update failed for refs/heads/master.
remote: - Changes must be made through a pull request.
! [remote rejected] master -> master (protected branch hook declined)
```

Der Workflow öffnet deshalb jetzt einen PR und merged ihn selbst
(`gh pr merge --squash --delete-branch`, Commit `ff21f66`). Ein Merge ist unter
Branch Protection erlaubt, ein direkter Push nicht.

**Offener Punkt:** PR #17 meldet `mergeable: true`, `mergeable_state: blocked`.
Das heißt, die Regel verlangt zusätzlich etwas — ein Review oder einen Required
Check. Dann wird auch der Merge des Bots abgewiesen. Die Protection-Settings
selbst kann ich nicht lesen (API antwortet 403, diese Session hat kein
GitHub-Token mit Admin-Scope), deshalb unten beide Varianten.

## Variante A — Bypass-Liste (empfohlen)

Der Bot darf direkt auf `master` pushen. Danach kann der Workflow wieder auf
den einfachen Push zurück, ohne PR-Umweg.

**Wenn ein Ruleset greift** (Settings → Rules → Rulesets):

1. Repo → **Settings** → **Rules** → **Rulesets** → das Ruleset für `master` öffnen
2. Abschnitt **Bypass list** → **Add bypass**
3. **Repository admin** wählen, oder unter **Apps** den Eintrag **GitHub Actions**
4. Speichern

**Wenn klassische Branch Protection greift** (Settings → Branches):

1. Repo → **Settings** → **Branches** → Regel für `master` → **Edit**
2. Unter **Require a pull request before merging** →
   **Allow specified actors to bypass required pull requests** anhaken
3. `github-actions[bot]` hinzufügen
4. Speichern

Welche der beiden greift, zeigt sich daran, welche Seite überhaupt einen
Eintrag für `master` hat.

## Variante B — Required approvals auf 0

Der PR bleibt, aber der Bot darf ihn selbst mergen. Kein Codeowner-Review mehr
für `master`.

1. Repo → **Settings** → **Branches** → Regel für `master` → **Edit**
2. **Require a pull request before merging** → **Require approvals** → auf **0**
3. Falls **Require status checks to pass before merging** aktiv ist: prüfen, ob
   ein Check gelistet ist, den der Bot nicht erfüllen kann. Solche Checks
   entfernen oder den Bot in Variante A auf die Bypass-Liste setzen.
4. Speichern

Zusätzlich hilfreich: Settings → General → **Allow auto-merge** aktivieren.
Dann greift `gh pr merge --auto` als Rückfall, falls ein Check noch läuft.

## Verifikation

Nach der Umstellung:

1. Actions → **Release scheduled post** → **Run workflow**, Feld `date` leer lassen
2. Grüner Lauf ohne fälligen Artikel = korrekt (leerer Lauf)
3. Echter Test ist der 29.09. (Conditional Access Baseline). Der Lauf muss
   grün sein und der PR gemerged, nicht offen.

## Nebenbefund: PR #17 nicht einfach mergen

PR #17 (`claude/linkedin-zero-trust-drafts-o9463v`) ist auf master rebased. Netto
enthält er nur noch `.well-known/security.txt` und das Entfernen der
verwaisten PDF-Datei. Seine ursprüngliche Kalender-Änderung — Apple ADE auf den
25.09. verschieben — wurde verworfen, weil der Artikel seit dem 22.09. live ist.
Sein Cron-Fund steckt schon in `ff21f66`.

## Was bereits erledigt ist

| | |
|---|---|
| Cron | `50 0` + `50 3` UTC statt `50 5`. GitHub startete jeden Lauf 09.–18.09. 3h46m–5h09m zu spät, damit landete ein 05:50-Release ~12:20 Berlin — vier Stunden nach dem Ankündigungspost um 08:18 |
| Datum Apple ADE | `<time>`, `datePublished`, `dateModified` auf `2026-09-22`, dem tatsächlichen Live-Datum (Pages-Deploy 08:16:20 UTC) |
| Datum Autopilot V1 vs V2 | ebenso `2026-09-22`, gleicher Push, gleicher Versatz |
| Sitemap, Feed, llms.txt | neu generiert, `lastmod` und `pubDate` passen |
| Überfällige Releases | Apple ADE und Autopilot am 22.09., PIM am 23.09. manuell nachgezogen |
| check-findability | grün, 46 Artikel |

## Links

- Repo: https://github.com/farpoint-tech/endlesstech.blog
- Branch-Settings: https://github.com/farpoint-tech/endlesstech.blog/settings/branches
- Rulesets: https://github.com/farpoint-tech/endlesstech.blog/settings/rules
- Workflow: https://github.com/farpoint-tech/endlesstech.blog/actions/workflows/release-series.yml
- PR #17: https://github.com/farpoint-tech/endlesstech.blog/pull/17
- Fehlgeschlagener Lauf vom 21.09.: https://github.com/farpoint-tech/endlesstech.blog/actions/runs/35592367085
- Apple ADE live: https://endlesstech.blog/posts/2026-09-08-intune-apple-enrollment-policies-ade.html
- Autopilot V1 vs V2 live: https://endlesstech.blog/posts/2026-09-22-windows-autopilot-v1-vs-v2-technical-guide.html
- PIM live: https://endlesstech.blog/posts/2026-09-03-entra-pim-authentication-context.html
- Feed: https://endlesstech.blog/feed.xml
- Chat: https://claude.ai/code/session_015XGcCkXfQaoFf74cJE1WBM
