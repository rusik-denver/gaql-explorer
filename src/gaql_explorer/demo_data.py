"""
Realistic demo dataset for a home services business (TV mounting & installation).

All data is synthetic but mirrors real Google Ads account patterns:
campaign naming, keyword structures, search term diversity, and
geographic distribution for a service area.
"""

ACCOUNT = {
    "id": "123-456-7890",
    "name": "Premier Home Services (Demo)",
    "currency": "USD",
    "timezone": "America/New_York",
}

CAMPAIGNS = [
    {
        "campaign.name": "Brand - Exact Match",
        "campaign.id": "10001",
        "campaign.status": "ENABLED",
        "campaign.bidding_strategy_type": "TARGET_CPA",
        "campaign_budget.amount_micros": 50_000_000,
        "metrics.cost_micros": 1_247_000_000,
        "metrics.clicks": 342,
        "metrics.impressions": 1_856,
        "metrics.conversions": 48.0,
        "metrics.conversions_value": 14_400.0,
        "metrics.ctr": 0.1842,
        "metrics.average_cpc": 3_646_198,
        "metrics.cost_per_conversion": 25_979_166,
        "metrics.search_impression_share": 0.91,
    },
    {
        "campaign.name": "Services - Broad Match",
        "campaign.id": "10002",
        "campaign.status": "ENABLED",
        "campaign.bidding_strategy_type": "MAXIMIZE_CONVERSIONS",
        "campaign_budget.amount_micros": 150_000_000,
        "metrics.cost_micros": 3_456_000_000,
        "metrics.clicks": 891,
        "metrics.impressions": 12_340,
        "metrics.conversions": 31.0,
        "metrics.conversions_value": 9_300.0,
        "metrics.ctr": 0.0722,
        "metrics.average_cpc": 3_879_910,
        "metrics.cost_per_conversion": 111_483_870,
        "metrics.search_impression_share": 0.64,
    },
    {
        "campaign.name": "Emergency - Phrase Match",
        "campaign.id": "10003",
        "campaign.status": "ENABLED",
        "campaign.bidding_strategy_type": "MANUAL_CPC",
        "campaign_budget.amount_micros": 40_000_000,
        "metrics.cost_micros": 892_000_000,
        "metrics.clicks": 67,
        "metrics.impressions": 890,
        "metrics.conversions": 12.0,
        "metrics.conversions_value": 4_800.0,
        "metrics.ctr": 0.0753,
        "metrics.average_cpc": 13_313_432,
        "metrics.cost_per_conversion": 74_333_333,
        "metrics.search_impression_share": 0.78,
    },
    {
        "campaign.name": "Competitor - Broad Match",
        "campaign.id": "10004",
        "campaign.status": "ENABLED",
        "campaign.bidding_strategy_type": "MAXIMIZE_CLICKS",
        "campaign_budget.amount_micros": 80_000_000,
        "metrics.cost_micros": 1_890_000_000,
        "metrics.clicks": 234,
        "metrics.impressions": 5_670,
        "metrics.conversions": 2.0,
        "metrics.conversions_value": 600.0,
        "metrics.ctr": 0.0413,
        "metrics.average_cpc": 8_076_923,
        "metrics.cost_per_conversion": 945_000_000,
        "metrics.search_impression_share": 0.45,
    },
    {
        "campaign.name": "Local - City Targeting",
        "campaign.id": "10005",
        "campaign.status": "ENABLED",
        "campaign.bidding_strategy_type": "TARGET_CPA",
        "campaign_budget.amount_micros": 70_000_000,
        "metrics.cost_micros": 2_100_000_000,
        "metrics.clicks": 456,
        "metrics.impressions": 6_780,
        "metrics.conversions": 22.0,
        "metrics.conversions_value": 6_600.0,
        "metrics.ctr": 0.0672,
        "metrics.average_cpc": 4_605_263,
        "metrics.cost_per_conversion": 95_454_545,
        "metrics.search_impression_share": 0.72,
    },
]

SEARCH_TERMS = [
    {"search_term_view.search_term": "tv mounting service near me", "campaign.name": "Services - Broad Match", "ad_group.name": "TV Mounting", "metrics.clicks": 89, "metrics.cost_micros": 345_000_000, "metrics.conversions": 14.0, "metrics.ctr": 0.0923, "search_term_view.status": "ADDED"},
    {"search_term_view.search_term": "wall mount tv installation", "campaign.name": "Services - Broad Match", "ad_group.name": "TV Mounting", "metrics.clicks": 67, "metrics.cost_micros": 267_000_000, "metrics.conversions": 11.0, "metrics.ctr": 0.0845, "search_term_view.status": "NONE"},
    {"search_term_view.search_term": "tv mount installer philadelphia", "campaign.name": "Local - City Targeting", "ad_group.name": "Philadelphia", "metrics.clicks": 45, "metrics.cost_micros": 198_000_000, "metrics.conversions": 9.0, "metrics.ctr": 0.0791, "search_term_view.status": "ADDED"},
    {"search_term_view.search_term": "professional tv mounting", "campaign.name": "Services - Broad Match", "ad_group.name": "TV Mounting", "metrics.clicks": 34, "metrics.cost_micros": 156_000_000, "metrics.conversions": 7.0, "metrics.ctr": 0.0712, "search_term_view.status": "NONE"},
    {"search_term_view.search_term": "flat screen tv wall mount service", "campaign.name": "Services - Broad Match", "ad_group.name": "Wall Mount", "metrics.clicks": 28, "metrics.cost_micros": 112_000_000, "metrics.conversions": 5.0, "metrics.ctr": 0.0634, "search_term_view.status": "NONE"},
    {"search_term_view.search_term": "how to mount tv on wall", "campaign.name": "Services - Broad Match", "ad_group.name": "TV Mounting", "metrics.clicks": 42, "metrics.cost_micros": 168_000_000, "metrics.conversions": 0.0, "metrics.ctr": 0.0312, "search_term_view.status": "EXCLUDED"},
    {"search_term_view.search_term": "tv mount bracket amazon", "campaign.name": "Services - Broad Match", "ad_group.name": "TV Mounting", "metrics.clicks": 31, "metrics.cost_micros": 124_000_000, "metrics.conversions": 0.0, "metrics.ctr": 0.0287, "search_term_view.status": "EXCLUDED"},
    {"search_term_view.search_term": "cheap tv mounting", "campaign.name": "Competitor - Broad Match", "ad_group.name": "Competitors", "metrics.clicks": 18, "metrics.cost_micros": 90_000_000, "metrics.conversions": 0.0, "metrics.ctr": 0.0198, "search_term_view.status": "NONE"},
    {"search_term_view.search_term": "same day tv installation", "campaign.name": "Emergency - Phrase Match", "ad_group.name": "Emergency", "metrics.clicks": 23, "metrics.cost_micros": 207_000_000, "metrics.conversions": 6.0, "metrics.ctr": 0.0856, "search_term_view.status": "NONE"},
    {"search_term_view.search_term": "tv mounting cost estimate", "campaign.name": "Services - Broad Match", "ad_group.name": "TV Mounting", "metrics.clicks": 56, "metrics.cost_micros": 224_000_000, "metrics.conversions": 3.0, "metrics.ctr": 0.0445, "search_term_view.status": "NONE"},
]

KEYWORDS = [
    {"ad_group.name": "Brand Terms", "ad_group_criterion.keyword.text": "premier home services", "ad_group_criterion.keyword.match_type": "EXACT", "ad_group_criterion.quality_info.quality_score": 9, "ad_group_criterion.quality_info.creative_quality_score": "ABOVE_AVERAGE", "ad_group_criterion.quality_info.post_click_quality_score": "ABOVE_AVERAGE", "ad_group_criterion.quality_info.search_predicted_ctr": "ABOVE_AVERAGE", "metrics.clicks": 342, "metrics.impressions": 1856, "metrics.cost_micros": 1_247_000_000, "metrics.ctr": 0.1842, "ad_group_criterion.effective_cpc_bid_micros": 5_000_000, "metrics.average_cpc": 3_646_198, "metrics.conversions": 48.0, "metrics.cost_per_conversion": 25_979_166},
    {"ad_group.name": "TV Mounting", "ad_group_criterion.keyword.text": "tv mounting service", "ad_group_criterion.keyword.match_type": "BROAD", "ad_group_criterion.quality_info.quality_score": 7, "ad_group_criterion.quality_info.creative_quality_score": "AVERAGE", "ad_group_criterion.quality_info.post_click_quality_score": "ABOVE_AVERAGE", "ad_group_criterion.quality_info.search_predicted_ctr": "AVERAGE", "metrics.clicks": 234, "metrics.impressions": 4120, "metrics.cost_micros": 912_000_000, "metrics.ctr": 0.0568, "ad_group_criterion.effective_cpc_bid_micros": 8_000_000, "metrics.average_cpc": 3_897_435, "metrics.conversions": 12.0, "metrics.cost_per_conversion": 76_000_000},
    {"ad_group.name": "Wall Mount", "ad_group_criterion.keyword.text": "wall mount installation", "ad_group_criterion.keyword.match_type": "PHRASE", "ad_group_criterion.quality_info.quality_score": 6, "ad_group_criterion.quality_info.creative_quality_score": "AVERAGE", "ad_group_criterion.quality_info.post_click_quality_score": "AVERAGE", "ad_group_criterion.quality_info.search_predicted_ctr": "BELOW_AVERAGE", "metrics.clicks": 167, "metrics.impressions": 3450, "metrics.cost_micros": 734_000_000, "metrics.ctr": 0.0484, "ad_group_criterion.effective_cpc_bid_micros": 6_000_000, "metrics.average_cpc": 4_395_209, "metrics.conversions": 8.0, "metrics.cost_per_conversion": 91_750_000},
    {"ad_group.name": "Emergency", "ad_group_criterion.keyword.text": "emergency tv mounting", "ad_group_criterion.keyword.match_type": "PHRASE", "ad_group_criterion.quality_info.quality_score": 5, "ad_group_criterion.quality_info.creative_quality_score": "BELOW_AVERAGE", "ad_group_criterion.quality_info.post_click_quality_score": "AVERAGE", "ad_group_criterion.quality_info.search_predicted_ctr": "AVERAGE", "metrics.clicks": 67, "metrics.impressions": 890, "metrics.cost_micros": 892_000_000, "metrics.ctr": 0.0753, "ad_group_criterion.effective_cpc_bid_micros": 15_000_000, "metrics.average_cpc": 13_313_432, "metrics.conversions": 12.0, "metrics.cost_per_conversion": 74_333_333},
    {"ad_group.name": "Philadelphia", "ad_group_criterion.keyword.text": "tv installer philadelphia", "ad_group_criterion.keyword.match_type": "EXACT", "ad_group_criterion.quality_info.quality_score": 8, "ad_group_criterion.quality_info.creative_quality_score": "ABOVE_AVERAGE", "ad_group_criterion.quality_info.post_click_quality_score": "ABOVE_AVERAGE", "ad_group_criterion.quality_info.search_predicted_ctr": "AVERAGE", "metrics.clicks": 156, "metrics.impressions": 2340, "metrics.cost_micros": 687_000_000, "metrics.ctr": 0.0667, "ad_group_criterion.effective_cpc_bid_micros": 7_000_000, "metrics.average_cpc": 4_403_846, "metrics.conversions": 15.0, "metrics.cost_per_conversion": 45_800_000},
    {"ad_group.name": "Competitors", "ad_group_criterion.keyword.text": "taskrabbit tv mounting", "ad_group_criterion.keyword.match_type": "BROAD", "ad_group_criterion.quality_info.quality_score": 3, "ad_group_criterion.quality_info.creative_quality_score": "BELOW_AVERAGE", "ad_group_criterion.quality_info.post_click_quality_score": "BELOW_AVERAGE", "ad_group_criterion.quality_info.search_predicted_ctr": "BELOW_AVERAGE", "metrics.clicks": 234, "metrics.impressions": 5670, "metrics.cost_micros": 1_890_000_000, "metrics.ctr": 0.0413, "ad_group_criterion.effective_cpc_bid_micros": 10_000_000, "metrics.average_cpc": 8_076_923, "metrics.conversions": 2.0, "metrics.cost_per_conversion": 945_000_000},
]

GEO = [
    {"geographic_view.country_criterion_id": "Philadelphia, PA", "campaign.name": "Local - City Targeting", "metrics.clicks": 342, "metrics.impressions": 5100, "metrics.conversions": 48.0, "metrics.cost_micros": 1_500_000_000, "metrics.ctr": 0.0671},
    {"geographic_view.country_criterion_id": "Camden, NJ", "campaign.name": "Local - City Targeting", "metrics.clicks": 89, "metrics.impressions": 1340, "metrics.conversions": 12.0, "metrics.cost_micros": 390_000_000, "metrics.ctr": 0.0664},
    {"geographic_view.country_criterion_id": "Wilmington, DE", "campaign.name": "Local - City Targeting", "metrics.clicks": 45, "metrics.impressions": 780, "metrics.conversions": 6.0, "metrics.cost_micros": 198_000_000, "metrics.ctr": 0.0577},
    {"geographic_view.country_criterion_id": "Trenton, NJ", "campaign.name": "Services - Broad Match", "metrics.clicks": 34, "metrics.impressions": 560, "metrics.conversions": 4.0, "metrics.cost_micros": 150_000_000, "metrics.ctr": 0.0607},
    {"geographic_view.country_criterion_id": "King of Prussia, PA", "campaign.name": "Local - City Targeting", "metrics.clicks": 28, "metrics.impressions": 420, "metrics.conversions": 3.0, "metrics.cost_micros": 123_000_000, "metrics.ctr": 0.0667},
    {"geographic_view.country_criterion_id": "Chester, PA", "campaign.name": "Services - Broad Match", "metrics.clicks": 22, "metrics.impressions": 380, "metrics.conversions": 0.0, "metrics.cost_micros": 97_000_000, "metrics.ctr": 0.0579},
    {"geographic_view.country_criterion_id": "Atlantic City, NJ", "campaign.name": "Services - Broad Match", "metrics.clicks": 15, "metrics.impressions": 290, "metrics.conversions": 0.0, "metrics.cost_micros": 66_000_000, "metrics.ctr": 0.0517},
]


DATASET_MAP = {
    "campaign": CAMPAIGNS,
    "search_term_view": SEARCH_TERMS,
    "keyword_view": KEYWORDS,
    "geographic_view": GEO,
}


def resolve_query(query: str) -> tuple[list[str], list[dict]]:
    """Parse a GAQL query and return matching demo data (headers, rows)."""
    q = query.lower()

    for resource_key, dataset in DATASET_MAP.items():
        if f"from {resource_key}" in q:
            break
    else:
        if "from campaign_criterion" in q or "from shared_set" in q:
            return ["name", "status"], [{"name": "Global Negatives", "status": "ENABLED"}]
        if "from landing_page_view" in q:
            return ["url", "clicks"], [{"url": "https://example.com/services", "clicks": 342}]
        return [], []

    select_part = q.split("from")[0].replace("select", "").strip()
    fields = [f.strip() for f in select_part.split(",")]

    rows = list(dataset)

    if "where" in q:
        where_part = q.split("where")[1].split("order by")[0].split("limit")[0]
        if "metrics.conversions = 0" in where_part:
            rows = [r for r in rows if r.get("metrics.conversions", 1) == 0.0]
        if "metrics.conversions > 0" in where_part:
            rows = [r for r in rows if r.get("metrics.conversions", 0) > 0]
        if "metrics.clicks > " in where_part:
            for part in where_part.split("and"):
                part = part.strip()
                if "metrics.clicks >" in part:
                    try:
                        threshold = int(part.split(">")[1].strip())
                        rows = [r for r in rows if r.get("metrics.clicks", 0) > threshold]
                    except (ValueError, IndexError):
                        pass

    if "order by" in q:
        order_part = q.split("order by")[1].split("limit")[0].strip()
        desc = "desc" in order_part
        order_field = order_part.split()[0].strip().rstrip(",")
        rows = sorted(rows, key=lambda r: r.get(order_field, 0), reverse=desc)

    if "limit" in q:
        try:
            limit_val = int(q.split("limit")[-1].strip())
            rows = rows[:limit_val]
        except (ValueError, IndexError):
            pass

    available_fields = []
    for f in fields:
        for key in (dataset[0] if dataset else {}):
            if f in key or key.endswith(f.split(".")[-1]):
                available_fields.append(key)
                break
        else:
            available_fields.append(f)

    return available_fields, rows
