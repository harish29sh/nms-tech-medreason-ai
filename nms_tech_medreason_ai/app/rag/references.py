"""
NMS Tech Proprietary Material
Copyright © 2026 NMS Tech. All Rights Reserved.

This file contains original NMS Tech project material. Unauthorized copying,
redistribution, republication, or commercial use is prohibited without prior
written authorization from NMS Tech.

Third-party libraries, frameworks, models, medical references, and standards
remain subject to their respective licences and ownership rights.
"""

# Reference registry.
# Do NOT ingest copyrighted textbooks unless you have the necessary licence.

REFERENCES = [
    {
        "id": "WHO-AI-2021",
        "title": "Ethics and governance of artificial intelligence for health",
        "organization": "World Health Organization",
        "url": "https://www.who.int/publications/i/item/9789240029200",
        "note": "AI health governance, safety, human oversight and ethical principles."
    },
    {
        "id": "CDSCO-MDS-2026",
        "title": "Guidance document on Medical Device Software under MDR-2017",
        "organization": "Central Drugs Standard Control Organisation, Government of India",
        "url": "https://www.cdsco.gov.in/opencms/opencms/en/Medical-Device-Diagnostics/Medical-Device-Diagnostics/",
        "note": "Official CDSCO medical-device software guidance page."
    },
    {
        "id": "NICE-GUIDANCE",
        "title": "NICE Guidance",
        "organization": "National Institute for Health and Care Excellence",
        "url": "https://www.nice.org.uk/guidance",
        "note": "Evidence-based guidance portal; individual content licences must be checked before ingestion."
    },
    {
        "id": "CDC",
        "title": "Centers for Disease Control and Prevention",
        "organization": "CDC",
        "url": "https://www.cdc.gov/",
        "note": "Public-health and infectious-disease guidance portal."
    }
]

def search_references(query, limit=5):
    q = query.lower()
    scored = []
    for ref in REFERENCES:
        text = f"{ref['title']} {ref['organization']} {ref['note']}".lower()
        score = sum(1 for token in q.split() if token in text)
        scored.append((score, ref))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [r for _, r in scored[:limit]]
