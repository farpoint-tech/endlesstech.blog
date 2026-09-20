# Release prep — "Windows Autopilot Local Admin: Which Setting Actually Wins"

Status: **blocked on connectors** for the Confluence pull and the Simplified/SocialBu check.
Everything below is ready to paste the moment they are back.

## 1. Learn cross-check (done, via learn.microsoft.com directly)

| Claim | Verdict | Source |
|---|---|---|
| Autopilot deployment-profile endpoint is documented only under `/beta` | **Confirmed.** `windowsAutopilotDeploymentProfile` GET carries only the `graph-rest-beta` moniker; no v1.0 page exists. Example request is `https://graph.microsoft.com/beta/deviceManagement/windowsAutopilotDeploymentProfiles/{id}` | graph/api/intune-shared-windowsautopilotdeploymentprofile-get |
| Least-privilege scope is `Policy.Read.DeviceConfiguration`, not `Policy.Read.All` | **Confirmed — but for a different endpoint.** It is the least-privileged scope for `GET /policies/deviceRegistrationPolicy` (delegated and application). `Policy.Read.All` is listed as higher-privileged. | graph/api/deviceregistrationpolicy-get |
| ...and that same scope for the Autopilot profile call | **Wrong.** The Autopilot profile endpoint uses `DeviceManagementServiceConfig.Read.All` / `.ReadWrite.All`. No `Policy.Read.*` permission appears on that page at all. | same two pages |
| Device Preparation does not use the ESP | **Confirmed, verbatim:** "Windows Autopilot device preparation doesn't use the Enrollment Status Page (ESP)... If the ESP displays during the deployment, then the device isn't running a Windows Autopilot device preparation deployment." | autopilot/device-preparation/troubleshooting-faq |
| Classic Autopilot profiles take precedence over Device Preparation policies | **Confirmed, verbatim:** "Windows Autopilot profiles take precedence over Windows Autopilot device preparation policies." | same |
| Add-then-remove group mechanic for **classic** deployment profiles | **Not documented.** Described only for Device Preparation. Keep marked untested. | — |
| Skipped provisioning (standard user + Entra local-admin setting) for **classic** profiles | **Not documented for classic.** It *is* fully documented for Device Preparation, with the complete combination table, under "Conflict between Microsoft Entra ID and Windows Autopilot device preparation local administrator setting" (added 3 June 2024, still open). Nothing equivalent appears on the classic known-issues page. Keep the classic claim marked untested. | autopilot/device-preparation/known-issues |
| UTC / time-zone failures | **Documented and resolved.** "Deployment fails for devices not in the Coordinated Universal Time (UTC) time zone", added 8 July 2024, marked resolved July 2024. Do not carry it as an open issue. | same |

### Two things worth adding before go-live

1. **Split the two endpoints explicitly.** They are different APIs with different permissions, and conflating them is the kind of error a reviewer will find:
   - `GET /beta/deviceManagement/windowsAutopilotDeploymentProfiles/{id}` → `DeviceManagementServiceConfig.Read.All` — beta only.
   - `GET /beta/policies/deviceRegistrationPolicy` → `Policy.Read.DeviceConfiguration` (least privileged) — a v1.0 page for this one does exist. The local-admin setting lives here, at `azureADJoin.localAdmins.registeringUsers`.
2. **The documented combination table is the strongest material in the piece.** Microsoft lists three setting combinations that leave the user a standard non-administrator, and two of them require the policy's **User account type** to be set to **Administrator** &mdash; the opposite of what the setting name suggests. Only the third (Entra **Local administrator settings** = **All**) uses **Standard user**. If the article does not already lead the answer with that inversion, it should.
3. **A second documented local-admin conflict, on the classic side.** From the Autopilot known-issues page: user-driven **hybrid** Entra join does not grant the user administrator rights even when the Autopilot profile specifies it, if another account on the device already has them (for example one created by a provisioning script or policy). That is Microsoft's own statement of "which setting wins" in one real case, and it is currently unsourced in the draft.
   Also on that page, the least-privilege built-in roles for reading the device-registration policy: Global Reader, Cloud Device Administrator, Intune Administrator, Windows 365 Administrator, Directory Reviewer.

## 2. Announcement post — LinkedIn draft (English, easym365, link in first comment, delay 1)

A device provisioned last week with the user as local admin. The Autopilot profile said standard user. Both settings were configured correctly, and only one of them won.

Windows Autopilot lets you set the user account type in the deployment profile. Microsoft Entra has its own device-registration setting that decides who lands in the local Administrators group on join. When the two disagree, nothing warns you. The device just comes up with the wrong answer, and you find out when someone installs something they should not have been able to install.

I wrote up which combination produces which result, the Graph calls to read both settings before you ship a batch, and the one Microsoft-documented case where a hybrid-joined user silently does not get admin rights even though the profile grants them. Every load-bearing claim is sourced back to a Learn page. Two points I could not source are marked as untested rather than dressed up as fact, because Microsoft does not document them.

If you run Autopilot and have never read both settings side by side in the same tenant, that is the fifteen minutes I would spend this week.

Link in the first comment.

#Microsoft365 #Intune #WindowsAutopilot #Entra

**First comment (delay: 1 = one minute):** `<final published URL>`

## 3. Image description for Simplified (Simplified generates the image, not Claude)

Neon cyber-comic split panel, 1200x627, dark navy background with cyan and magenta rim light.
Left panel: a laptop mid-out-of-box-experience, screen showing a user icon labelled "Standard User", lit cold cyan, a small padlock closed beside it.
Right panel: the same laptop, screen showing the same user icon now wearing a magenta crown labelled "Local Admin", padlock open, a faint warning triangle in the corner.
Between the panels, a vertical seam of glitched circuitry with two labelled cables crossing each other: one tagged "Autopilot Profile", one tagged "Entra Device Setting", the magenta one visibly overriding the cyan one at the crossover.
Bottom-right corner: small gold accent line. No text other than the four labels. No logos, no faces, no stock-photo people.

## 4. Open items for me

- Pull the article body + fact-check table + release procedure from Confluence FPS/1069121547 and the release patch FPS/1121353747, build the post on the current gen3 template, push, and hand over the review URL.
- Check Simplified drafts and SocialBu posts for an existing announcement before creating one. If one exists: report when and where, do not duplicate.
