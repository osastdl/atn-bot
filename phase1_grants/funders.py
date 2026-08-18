"""Curated list of funders active in trans-rights / LGBTQI+ human rights
work relevant to Africa. Real, sourced data (web-researched 2026-08-18),
not guessed -- but funder landscapes shift (funds wind down, deadlines
move), so `last_verified` is tracked per entry and this list needs
periodic re-checking, not treated as permanently accurate.

funding_type:
  "rolling"        -- no fixed deadline, apply any time
  "regional_call"  -- periodic open calls for a specific region
  "cycle"          -- fixed number of funding cycles per year
  "loi_invitation" -- typically by invitation or requires an LOI first,
                      not a simple open application
"""

FUNDERS = [
    {
        "name": "UHAI EASHRI",
        "url": "http://www.uhai-eashri.org/ENG/",
        "regions": ["Burundi", "Kenya", "Rwanda", "Tanzania", "Uganda"],
        "focus": "LGBTI and sex worker-led organisations, East Africa",
        "funding_type": "rolling",
        "notes": "Flexible fund, no fixed deadline -- accepts applications on a rolling basis.",
        "last_verified": "2026-08-18",
    },
    {
        "name": "ISDAO (Initiative Sankofa d'Afrique de l'Ouest)",
        "url": "https://isdao.org/en/grants-faq/regional/",
        "regions": ["Benin", "Burkina Faso", "Cote d'Ivoire", "Ghana", "Liberia", "Mali", "Nigeria", "Senegal", "Togo"],
        "focus": "Sexual diversity and sexual rights, West Africa",
        "funding_type": "regional_call",
        "notes": "Periodic regional calls for LGBTQI-led groups/networks -- 8th call was open earlier 2026, notified applicants ~April. Check isdao.org for the current call status before assuming one is open.",
        "last_verified": "2026-08-18",
    },
    {
        "name": "Urgent Action Fund-Africa (UAF-Africa)",
        "url": "https://www.uaf-africa.org/apply-for-a-grant/",
        "regions": ["Pan-Africa"],
        "focus": "Women's and LGBTQI human rights defenders -- rapid-response/emergency grants",
        "funding_type": "rolling",
        "notes": "Directly relevant to ATN's emergency-response funding need for the wider trans network, not just programmatic grants.",
        "last_verified": "2026-08-18",
    },
    {
        "name": "Astraea Lesbian Foundation for Justice",
        "url": "https://www.astraeafoundation.org",
        "regions": ["Global", "including Africa"],
        "focus": "Lesbian, trans, intersex, and LGBTQI groups led by people of color",
        "funding_type": "cycle",
        "notes": "General support grants roughly $5,000-$30,000/year, two funding cycles.",
        "last_verified": "2026-08-18",
    },
    {
        "name": "Mama Cash",
        "url": "https://www.mamacash.org",
        "regions": ["Global", "including Africa"],
        "focus": "Women, girls, and trans-led groups and networks",
        "funding_type": "cycle",
        "notes": "2026 Solidarity Fund (up to EUR 40,000) is aimed at women's FUNDS specifically, not grassroots orgs directly -- check whether ATN qualifies as a fund/network vs. a direct grantee before applying here.",
        "last_verified": "2026-08-18",
    },
    {
        "name": "Global Philanthropy Project (GPP)",
        "url": "https://globalphilanthropyproject.org",
        "regions": ["Global"],
        "focus": "Network/coalition of LGBTQI funders, not itself a direct grantmaker to grassroots orgs",
        "funding_type": "loi_invitation",
        "notes": "Monitor for member funders' opportunities and convenings rather than applying to GPP directly.",
        "last_verified": "2026-08-18",
    },
    {
        "name": "Wellspring Philanthropic Fund",
        "url": "https://wpfund.org",
        "regions": ["US", "Africa", "Central and South America"],
        "focus": "Racial equity, gender justice, human rights, LGBTQ causes",
        "funding_type": "loi_invitation",
        "notes": "WINDING DOWN -- board decided in 2024 to cease all grantmaking by end of 2028. New funding opportunities are very limited. Keep on the list for awareness, don't prioritize outreach here.",
        "last_verified": "2026-08-18",
    },
    {
        "name": "American Jewish World Service (AJWS)",
        "url": "https://ajws.org",
        "regions": ["Global", "including Africa"],
        "focus": "LGBTQI rights groups globally",
        "funding_type": "loi_invitation",
        "notes": "Typically grants to organizations already in AJWS's partner network -- check current application process before assuming an open call.",
        "last_verified": "2026-08-18",
    },
    {
        "name": "Ford Foundation",
        "url": "https://www.fordfoundation.org",
        "regions": ["Global", "including Africa"],
        "focus": "Human rights, including LGBTQI rights",
        "funding_type": "loi_invitation",
        "notes": "Major foundation, typically by invitation/LOI rather than open application -- worth relationship-building rather than a cold application.",
        "last_verified": "2026-08-18",
    },
    {
        "name": "Open Society Foundations (OSF)",
        "url": "https://www.opensocietyfoundations.org",
        "regions": ["Global", "including Africa"],
        "focus": "Human rights, LGBTQI rights",
        "funding_type": "loi_invitation",
        "notes": "Typically by invitation/LOI -- check regional/thematic program pages for any open calls before assuming.",
        "last_verified": "2026-08-18",
    },
]
