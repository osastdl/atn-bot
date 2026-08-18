"""Template-based caption + hashtag generation -- same proven approach as
VV Outreach's poster.py, not a vision/AI API call. No external dependency,
no billing, works right now.

A bigger opener pool than VV's on purpose: this account posts a lot more
often, so more variety matters more here to avoid repeats feeling obvious.
Whatever caption you type alongside the photo on Telegram gets folded in
as `hint` -- same mechanism as yours, so you can still add your own
write-up any time you want to.
"""

import random

_CAPTION_OPENERS = [
    "Another day doing the work that matters. 🌍\n\n{hint}",
    "Behind every strong organisation is a lot of unglamorous groundwork. 📌\n\n{hint}",
    "Strategy on paper is easy. This is what implementation actually looks like. 🛠️\n\n{hint}",
    "Grateful to be in the room for this one. 🙌\n\n{hint}",
    "Consulting beyond advice, one engagement at a time. ✅\n\n{hint}",
    "From strategy to implementation -- that's the whole point. ✨\n\n{hint}",
    "Building systems, strengthening communities. 🏗️\n\n{hint}",
    "Some days you're in the boardroom. Some days you're on the ground. Both matter. 🎯\n\n{hint}",
    "Real impact doesn't happen in a report -- it happens here. 📊\n\n{hint}",
    "Proud to walk with organisations doing the real work. 🤝\n\n{hint}",
    "This is what showing up looks like. 👀\n\n{hint}",
    "Another conversation that reminded me why this work matters. 💬\n\n{hint}",
    "Capacity isn't built overnight -- but moments like this add up. 📈\n\n{hint}",
    "Community-centred isn't a tagline, it's a practice. 🌱\n\n{hint}",
    "Good things happening here. 📍\n\n{hint}",
    "Proudly African. Globally impactful. 🌍\n\n{hint}",
    "Taking a moment to document the process, not just the outcome. 🎨\n\n{hint}",
    "Sharing a glimpse of the work in progress. 🔍\n\n{hint}",
    "Movements are built by people who show up consistently. 🙏\n\n{hint}",
    "Here for the long game, not the quick win. ⏳\n\n{hint}",
    "This one's staying with me for a while. 💭\n\n{hint}",
    "The kind of day that reminds you why you do this work. ☀️\n\n{hint}",
    "Learning something new in every room I walk into. 📚\n\n{hint}",
    "Grateful for the people and organisations that let us in on their journey. 💛\n\n{hint}",
    "A snapshot from where the work actually happens. 📷\n\n{hint}",
    "Sustainable impact takes patience -- and moments like this. 🌿\n\n{hint}",
    "Strengthening organisations, one honest conversation at a time. 🗣️\n\n{hint}",
    "This is what partnership looks like, not just a client relationship. 🤝\n\n{hint}",
    "Not every win is measurable, but you can feel it in the room. ✨\n\n{hint}",
    "Documenting the journey, not just the destination. 🛤️\n\n{hint}",
]

_HASHTAG_POOL = [
    "#ZAFConsultancy", "#StrategicPlanning", "#OrganisationalDevelopment",
    "#NGOs", "#SocialImpact", "#AfricanBusiness", "#CapacityBuilding",
    "#Governance", "#CommunityDevelopment", "#NonProfitConsulting",
    "#ImpactDriven", "#ProudlyAfrican", "#ConsultingBeyondAdvice",
    "#EventManagement", "#TrainingAndDevelopment", "#GrantManagement",
    "#AdvocacyWork", "#StrategicPartner", "#CivilSociety",
    "#DevelopmentSector", "#InstitutionalStrengthening", "#AfricaRising",
    "#SustainableImpact", "#MovementBuilding", "#StrengtheningOrganisations",
]


def generate_caption(hint_text=None):
    """hint_text is whatever caption the sender typed alongside the photo
    on Telegram -- folded into a template rather than posted bare, same
    mechanism as VV Outreach's Quick Post."""
    opener = random.choice(_CAPTION_OPENERS)
    hint = (hint_text or "").strip()
    body = opener.format(hint=hint) if hint else opener.replace("{hint}\n\n", "").replace("{hint}", "")
    body = body.rstrip()

    tags = " ".join(random.sample(_HASHTAG_POOL, k=random.randint(5, 6)))
    return f"{body}\n\n{tags}"
