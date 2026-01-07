# CloudKnox-The Copilot “Mandate” - A Fact-Check on Digital Sovereignty and Cloud Governance

**By Philipp Schmidt**

Recently, a notification from the Bundeshaus (the seat of the Swiss Parliament) caused a stir: the Microsoft Copilot icon had suddenly appeared on the screens of parliamentarians. The reaction was one of uncertainty and criticism, fueled by the narrative that a US corporation was unilaterally deciding on the technology used at the heart of Swiss democracy. This concern was amplified when parliamentary services announced that deactivating the feature was “only partially possible.” [1]

While the concern for digital sovereignty is both valid and crucial, a closer technical examination reveals a different story. The situation is less dramatic than it first appeared, but it highlights a much more fundamental challenge that many organizations face in the cloud era.

## 1. Not Every Copilot Reads Your Emails

The most significant misunderstanding must be addressed first. When a colorful new icon appears in the taskbar, it is most likely not the fully integrated “Microsoft 365 Copilot” that has access to internal emails, SharePoint documents, or Teams chats.

Instead, this version is “Microsoft 365 Copilot Chat” (formerly known as “Copilot with Commercial Data Protection” or Bing Chat Enterprise). Here are the verified facts about this service, according to official Microsoft documentation:

*   **No Access to Internal Data:** This version is essentially an AI-powered search engine grounded in web data. It is completely “blind” to your organization’s internal documents and communications. [3]
*   **Contractual Data Protection:** Microsoft guarantees that user prompts and responses are not used to train its foundation AI models. This is a core component of its Enterprise Data Protection (EDP) commitment. [3]
*   **A Secure Alternative:** It provides a secure, enterprise-grade environment for employees who might otherwise turn to unprotected public AI tools for work-related queries, thereby creating a real security risk.

## 2. “Turning It Off Isn’t Possible” – Yes, It Is.

The statement that deactivation is not possible is, from a technical standpoint, incorrect. While it is true that Microsoft does not provide a simple “off switch” in a user-facing menu, administrators have complete control.

According to Microsoft’s own documentation, Copilot can be managed and disabled organization-wide through several methods, including the Microsoft 365 admin center, Integrated Apps policies, and PowerShell scripts. [2] The fact that this was communicated as “not possible” in the Swiss Parliament points less to a mandate from Microsoft and more toward the complexities of internal IT processes or a potential knowledge gap in managing these new, rapidly evolving service plans.

This assessment is supported by the NZZ report, which noted that the Swiss bank UBS successfully implemented a controlled rollout of Copilot. UBS initially blocked the feature for all employees, then gradually enabled it—first for staff without access to customer data, and later for all employees with a filter to detect sensitive information. [1]

## 3. The Real Issue: Governance is the Customer’s Responsibility

The incident in the Swiss Parliament is symptomatic of a challenge facing countless organizations today. Cloud providers like Microsoft operate on an “evergreen” model, rolling out new features at a rapid pace. That is their business model.

However, the responsibility for governing how these tools are deployed and used lies squarely with the customer—the company or the public authority. Digital sovereignty is not achieved by blocking technology, but by actively steering it.

This is the core of the Shared Responsibility Model, a framework clearly defined by Microsoft: [4]

| Responsibility                  | Microsoft | Customer |
| ------------------------------- | :-------: | :------: |
| Cloud Infrastructure & Platform |     ✔     |          |
| Security                        |           |          |
| Data Governance & Classification|           |    ✔     |
| User Access Management          |           |    ✔     |
| Policy Definition & Enforcement |           |    ✔     |
| User Training & Enablement      |           |    ✔     |

## Conclusion: Technology Requires Leadership, Not Reaction

Confronting parliamentarians with a new AI tool without warning or training was the actual failure in this scenario. The problem was not the technology itself, but the absence of a proactive change management and governance strategy.

Uncertainty is a byproduct of ignorance. Any organization introducing AI—whether intentionally or as a result of an automatic update—must ensure three things:

1.  **Technical Clarity:** Understand what the tool can and cannot do.
2.  **Robust Governance:** Establish clear guidelines that go beyond basic data protection laws.
3.  **User Enablement:** Provide training so that users are not just passengers but confident pilots of the new technology.

> Complex IT? I make it simple – with M365, which protects, scales and brings clarity. For SMEs that rely on smart solutions.

Need support with your AI governance strategy? It is perfectly normal for internal IT departments to feel overwhelmed by the sheer speed of AI development. I can help you separate fact from fiction, configure your environment securely, and empower your employees for the future. So you can decide how AI works for you—not the other way around.

Feel free to contact me: [easym365.de](https://easym365.de)

### References

[1]: NZZ, "Vertrauliche Dokumente als Trainingsdaten für amerikanische KI? Die Computer im Parlament wurden von Microsoft eigenmächtig umgerüstet," January 4, 2026. [https://www.nzz.ch/schweiz/vertrauliche-dokumente-als-trainingsdaten-fuer-amerikanische-ki-die-computer-im-parlament-wurden-von-microsoft-eigenmaechtig-umgeruestet-ld.1917478](https://www.nzz.ch/schweiz/vertrauliche-dokumente-als-trainingsdaten-fuer-amerikanische-ki-die-computer-im-parlament-wurden-von-microsoft-eigenmaechtig-umgeruestet-ld.1917478)

[2]: Microsoft Learn, "Manage Microsoft 365 Copilot Chat," December 8, 2025. [https://learn.microsoft.com/en-us/copilot/manage](https://learn.microsoft.com/en-us/copilot/manage)

[3]: Microsoft Learn, "Enterprise data protection in Microsoft 365 Copilot and Microsoft 365 Copilot Chat," December 8, 2025. [https://learn.microsoft.com/en-us/copilot/microsoft-365/enterprise-data-protection](https://learn.microsoft.com/en-us/copilot/microsoft-365/enterprise-data-protection)

[4]: Microsoft Learn, "Shared responsibility in the cloud," December 3, 2025. [https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility](https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility)
