(function () {
  var posts = [
    {
      slug: "2025-10-24-getting-started-with-zero-trust",
      title: "Getting Started with Zero Trust Security",
      themes: ["zero-trust", "security"],
      related: [7, 3, 10]
    },
    {
      slug: "2025-11-10-mobile-application-management-your-quarterback-for-mobile-security",
      title: "Mobile Application Management: Your Quarterback for Mobile Security",
      themes: ["security", "mdm", "byod"],
      related: [10, 11, 2]
    },
    {
      slug: "2025-11-13-windows-365-cloud-apps-when-less-is-more",
      title: "Windows 365 Cloud Apps: When Less is More",
      themes: ["cloud", "m365"],
      related: [5, 12, 1]
    },
    {
      slug: "2025-11-15-boost-your-cyber-defense-microsoft-secure-score-for-smbs",
      title: "Boost Your Cyber Defense: Microsoft Secure Score for SMBs",
      themes: ["security", "m365"],
      related: [0, 7, 10]
    },
    {
      slug: "2025-12-17-cloudknox-mcp-servers-understanding-the-double-edged-sword-of-ai-tooling",
      title: "MCP Servers: Understanding the Double-Edged Sword of AI Tooling",
      themes: ["ai", "security"],
      related: [8, 3, 7]
    },
    {
      slug: "2025-12-18-beyond-the-basics-why-smart-m365-add-ons-are-your-best-investment",
      title: "Beyond the Basics: Why Smart M365 Add-Ons Are Your Best Investment",
      themes: ["m365", "strategy"],
      related: [12, 14, 2]
    },
    {
      slug: "2025-12-18-windows-11-hardware-lifecycle",
      title: "Windows 11 and Hardware Lifecycles: Why the Debate is Bigger Than Microsoft",
      themes: ["hardware", "security"],
      related: [14, 5, 2]
    },
    {
      slug: "2025-12-18-zero-trust-microsoft-entra-suite",
      title: "Unlocking Zero Trust: Mastering Identity and Network Security with Microsoft Entra Suite",
      themes: ["zero-trust", "identity", "entra"],
      related: [0, 9, 10]
    },
    {
      slug: "cloudknox-the-copilot-mandate",
      title: "The Copilot \"Mandate\" – A Fact-Check on Digital Sovereignty and Cloud Governance",
      themes: ["copilot", "governance", "ai"],
      related: [4, 12, 13]
    },
    {
      slug: "2026-01-02-microsoft-entra-tenant-vs-azure-subscriptions",
      title: "Microsoft Entra Tenant vs. Azure Subscriptions – What's the Difference?",
      themes: ["entra", "azure", "identity"],
      related: [7, 0, 10]
    },
    {
      slug: "2026-01-06-intune-enrollment-restrictions",
      title: "Intune Enrollment Restrictions: Your Foundational Control Against Local Admin Risk",
      themes: ["intune", "security", "zero-trust"],
      related: [1, 11, 0]
    },
    {
      slug: "2026-01-28-ios-abm-enrollment-troubleshooting",
      title: "iOS/iPadOS ABM Enrollment Troubleshooting: The 'Not Contacted' Nightmare",
      themes: ["intune", "mdm", "ios"],
      related: [10, 1, 14]
    },
    {
      slug: "2026-02-01-microsoft-dominanz-pragmatismus-alternativen",
      title: "You Don't Have to Love Microsoft – But You Should Understand Its Dominance",
      themes: ["strategy", "m365"],
      related: [5, 14, 15]
    },
    {
      slug: "2026-02-25-cloudknox-sharepoint-file-level-archiving",
      title: "The Future of SharePoint Archiving: File-Level is Coming",
      themes: ["sharepoint", "cloud"],
      related: [14, 5, 12]
    },
    {
      slug: "2026-02-25-the-golden-tenant-is-dead",
      title: "The Golden Tenant Is Dead. Here's What Replaces It.",
      themes: ["intune", "strategy"],
      related: [10, 13, 12]
    },
    {
      slug: "2026-03-16-from-nt-to-m365-a-journey-through-tech-decisions-and-people",
      title: "From NT to M365 – A Journey Through Tech, Decisions, and the People Behind Them",
      themes: ["career", "strategy", "m365"],
      related: [12, 0, 5]
    },
    {
      slug: "2026-03-26-aadsts650052-windowsdefenderatp-service-principal-missing",
      title: "AADSTS650052: WindowsDefenderATP Service Principal Missing – Cause & Fix",
      themes: ["entra", "security", "troubleshooting"],
      related: [9, 7, 10]
    },
    {
      slug: "2026-03-27-windows-autopilot-end-the-setup-chaos",
      title: "Stop the Setup Chaos: How Windows Autopilot Deploys Hundreds of Devices",
      themes: ["intune", "autopilot", "deployment"],
      related: [10, 14, 6]
    },
    {
      slug: "2026-03-30-exchange-soa-switch-reality",
      title: "The Final Exchange Server: Why the Cloud Switch Isn't a Magic Wand",
      themes: ["exchange", "cloud", "strategy"],
      related: [12, 15, 5]
    },
    {
      slug: "2026-04-08-copilot-roi-knowledge-management-guide",
      title: "Copilot ROI: Why Knowledge Management Is the Difference Between 1.4:1 and 5.4:1",
      themes: ["copilot", "ai", "strategy"],
      related: [8, 21, 4]
    },
    {
      slug: "2026-04-08-microsoft-365-vs-baramundi-the-real-story",
      title: "Microsoft 365 vs. Baramundi: The Real Story",
      themes: ["intune", "m365", "strategy"],
      related: [10, 17, 14]
    },
    {
      slug: "2026-04-17-sharepoint-permission-auditing-copilot",
      title: "Taming the SharePoint Permission Nightmare: The New Copilot Readiness Tool",
      themes: ["sharepoint", "copilot", "security"],
      related: [13, 19, 3]
    },
    {
      slug: "2026-05-21-ghost-hunting-m365-orphaned-teams-channel-sites",
      title: "Ghost Hunting in the M365 Tenant: Cleaning Up Orphaned Teams Private Channel Sites",
      themes: ["sharepoint", "m365", "powershell"],
      related: [13, 21, 14]
    }
  ];

  var path = window.location.pathname;
  var currentSlug = path.replace(/.*\/posts\//, "").replace(/\.html$/, "");
  var currentIndex = -1;

  for (var i = 0; i < posts.length; i++) {
    if (posts[i].slug === currentSlug) {
      currentIndex = i;
      break;
    }
  }

  if (currentIndex === -1) return;

  var container = document.getElementById("post-navigation");
  if (!container) return;

  var html = "";

  // Prev / Next navigation
  var prev = currentIndex > 0 ? posts[currentIndex - 1] : null;
  var next = currentIndex < posts.length - 1 ? posts[currentIndex + 1] : null;

  html += '<nav class="post-nav" aria-label="Post navigation">';
  if (prev) {
    html += '<a href="' + prev.slug + '.html" class="post-nav-link post-nav-prev">';
    html += '<span class="post-nav-label">Previous Post</span>';
    html += '<span class="post-nav-title">' + prev.title + "</span></a>";
  } else {
    html += '<span class="post-nav-link post-nav-prev post-nav-empty"></span>';
  }
  if (next) {
    html += '<a href="' + next.slug + '.html" class="post-nav-link post-nav-next">';
    html += '<span class="post-nav-label">Next Post</span>';
    html += '<span class="post-nav-title">' + next.title + "</span></a>";
  } else {
    html += '<span class="post-nav-link post-nav-next post-nav-empty"></span>';
  }
  html += "</nav>";

  // Related posts
  var relatedIndices = posts[currentIndex].related;
  html += '<section class="related-posts">';
  html += "<h2>You Might Also Like</h2>";
  html += '<div class="related-posts-grid">';
  for (var r = 0; r < relatedIndices.length; r++) {
    var rp = posts[relatedIndices[r]];
    html += '<a href="' + rp.slug + '.html" class="related-post-card">';
    html += '<span class="related-post-title">' + rp.title + "</span>";
    html += "</a>";
  }
  html += "</div></section>";

  container.innerHTML = html;
})();
