"""
GAQL query templates organized by audit category.

Each template is a practical query that a Google Ads professional would use
during account audits, optimization passes, and performance reviews.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class QueryTemplate:
    name: str
    category: str
    description: str
    query: str
    when_to_use: str


TEMPLATES: list[QueryTemplate] = [
    # ── Campaign Performance ──────────────────────────────────────────
    QueryTemplate(
        name="campaign_performance_30d",
        category="Campaign Performance",
        description="Campaign metrics for the last 30 days, sorted by spend",
        query=(
            "SELECT campaign.name, campaign.status, campaign.bidding_strategy_type, "
            "metrics.cost_micros, metrics.conversions, metrics.conversions_value, "
            "metrics.clicks, metrics.impressions, metrics.ctr, metrics.average_cpc "
            "FROM campaign "
            "WHERE segments.date DURING LAST_30_DAYS "
            "AND campaign.status != 'REMOVED' "
            "ORDER BY metrics.cost_micros DESC"
        ),
        when_to_use=(
            "First query in any audit. Shows where money is going and which "
            "campaigns convert. Flag campaigns with high spend and zero conversions."
        ),
    ),
    QueryTemplate(
        name="campaign_budget_utilization",
        category="Budget Utilization",
        description="Compare daily spend against budget to find limited campaigns",
        query=(
            "SELECT campaign.name, campaign_budget.amount_micros, "
            "campaign_budget.has_recommended_budget, "
            "metrics.cost_micros, metrics.impressions, metrics.search_impression_share "
            "FROM campaign "
            "WHERE segments.date DURING LAST_7_DAYS "
            "AND campaign.status = 'ENABLED' "
            "ORDER BY metrics.search_impression_share ASC"
        ),
        when_to_use=(
            "Find budget-limited campaigns that could scale. Low impression share "
            "with good CPA means raising budget will bring more conversions."
        ),
    ),
    QueryTemplate(
        name="campaign_conversion_lag",
        category="Campaign Performance",
        description="Conversion values by conversion action to detect tracking gaps",
        query=(
            "SELECT campaign.name, conversion_action.name, conversion_action.type, "
            "metrics.conversions, metrics.conversions_value, metrics.cost_per_conversion "
            "FROM campaign "
            "WHERE segments.date DURING LAST_30_DAYS "
            "AND metrics.conversions > 0 "
            "ORDER BY campaign.name, metrics.conversions DESC"
        ),
        when_to_use=(
            "Verify all conversion actions are firing. Missing conversion types "
            "mean your smart bidding is optimizing on incomplete data."
        ),
    ),

    # ── Search Term Analysis ──────────────────────────────────────────
    QueryTemplate(
        name="wasted_search_terms",
        category="Search Term Analysis",
        description="Search terms with clicks but zero conversions — negative candidates",
        query=(
            "SELECT search_term_view.search_term, search_term_view.status, "
            "campaign.name, ad_group.name, "
            "metrics.clicks, metrics.cost_micros, metrics.conversions, metrics.ctr "
            "FROM search_term_view "
            "WHERE segments.date DURING LAST_30_DAYS "
            "AND metrics.clicks > 5 "
            "AND metrics.conversions = 0 "
            "ORDER BY metrics.cost_micros DESC "
            "LIMIT 50"
        ),
        when_to_use=(
            "Run weekly. These search terms are burning budget with no return. "
            "Add them as negatives or restructure ad groups to improve relevance."
        ),
    ),
    QueryTemplate(
        name="converting_search_terms",
        category="Search Term Analysis",
        description="Top converting search terms to mine for new keywords",
        query=(
            "SELECT search_term_view.search_term, campaign.name, "
            "metrics.clicks, metrics.conversions, metrics.conversions_value, "
            "metrics.cost_micros, metrics.ctr "
            "FROM search_term_view "
            "WHERE segments.date DURING LAST_30_DAYS "
            "AND metrics.conversions > 0 "
            "ORDER BY metrics.conversions DESC "
            "LIMIT 30"
        ),
        when_to_use=(
            "Find search terms driving conversions that aren't yet added as exact "
            "match keywords. Promoting these gives you more control over bids."
        ),
    ),
    QueryTemplate(
        name="search_term_match_type_leak",
        category="Search Term Analysis",
        description="Broad match terms that don't match any keyword intent",
        query=(
            "SELECT search_term_view.search_term, "
            "ad_group_criterion.keyword.text, "
            "ad_group_criterion.keyword.match_type, "
            "metrics.clicks, metrics.cost_micros, metrics.conversions "
            "FROM search_term_view "
            "WHERE segments.date DURING LAST_30_DAYS "
            "AND metrics.clicks > 3 "
            "ORDER BY metrics.cost_micros DESC "
            "LIMIT 40"
        ),
        when_to_use=(
            "Compare triggered search terms against the keyword that matched them. "
            "Large semantic gaps mean your broad match is leaking into irrelevant territory."
        ),
    ),

    # ── Keyword Metrics ───────────────────────────────────────────────
    QueryTemplate(
        name="keyword_quality_scores",
        category="Quality Score",
        description="Keywords with quality score components for optimization",
        query=(
            "SELECT ad_group.name, ad_group_criterion.keyword.text, "
            "ad_group_criterion.keyword.match_type, "
            "ad_group_criterion.quality_info.quality_score, "
            "ad_group_criterion.quality_info.creative_quality_score, "
            "ad_group_criterion.quality_info.post_click_quality_score, "
            "ad_group_criterion.quality_info.search_predicted_ctr, "
            "metrics.clicks, metrics.impressions, metrics.cost_micros "
            "FROM keyword_view "
            "WHERE ad_group_criterion.status = 'ENABLED' "
            "AND campaign.status = 'ENABLED' "
            "AND metrics.impressions > 50 "
            "ORDER BY ad_group_criterion.quality_info.quality_score ASC"
        ),
        when_to_use=(
            "Low quality scores increase CPC. Sort ascending to find worst offenders. "
            "Fix by improving ad relevance (creative_quality) or landing page (post_click)."
        ),
    ),
    QueryTemplate(
        name="keyword_bid_landscape",
        category="Keyword Metrics",
        description="Keywords with bid info to find overbidding or underbidding",
        query=(
            "SELECT ad_group_criterion.keyword.text, "
            "ad_group_criterion.keyword.match_type, "
            "ad_group_criterion.effective_cpc_bid_micros, "
            "metrics.average_cpc, metrics.clicks, metrics.conversions, "
            "metrics.cost_per_conversion "
            "FROM keyword_view "
            "WHERE segments.date DURING LAST_30_DAYS "
            "AND campaign.status = 'ENABLED' "
            "AND metrics.clicks > 10 "
            "ORDER BY metrics.cost_per_conversion DESC"
        ),
        when_to_use=(
            "Compare effective CPC bid against actual average CPC and CPA. "
            "Keywords where CPA exceeds target should have bids lowered or be paused."
        ),
    ),
    QueryTemplate(
        name="low_impression_keywords",
        category="Keyword Metrics",
        description="Enabled keywords getting almost no impressions",
        query=(
            "SELECT campaign.name, ad_group.name, "
            "ad_group_criterion.keyword.text, "
            "ad_group_criterion.keyword.match_type, "
            "ad_group_criterion.quality_info.quality_score, "
            "metrics.impressions, metrics.search_impression_share "
            "FROM keyword_view "
            "WHERE campaign.status = 'ENABLED' "
            "AND ad_group.status = 'ENABLED' "
            "AND ad_group_criterion.status = 'ENABLED' "
            "AND segments.date DURING LAST_30_DAYS "
            "AND metrics.impressions < 10 "
            "ORDER BY metrics.impressions ASC"
        ),
        when_to_use=(
            "Dead keywords waste account structure. Low impressions usually means "
            "low search volume, poor quality score, or budget starvation."
        ),
    ),

    # ── Geographic Performance ────────────────────────────────────────
    QueryTemplate(
        name="geo_performance",
        category="Geographic Performance",
        description="Performance by geographic location to find best and worst areas",
        query=(
            "SELECT geographic_view.country_criterion_id, "
            "geographic_view.location_type, "
            "campaign.name, "
            "metrics.clicks, metrics.impressions, metrics.conversions, "
            "metrics.cost_micros, metrics.ctr "
            "FROM geographic_view "
            "WHERE segments.date DURING LAST_30_DAYS "
            "AND metrics.clicks > 5 "
            "ORDER BY metrics.conversions DESC"
        ),
        when_to_use=(
            "Find which cities/regions convert best. Increase bids for top performers, "
            "exclude or reduce bids for areas burning budget with no conversions."
        ),
    ),
    QueryTemplate(
        name="geo_wasted_spend",
        category="Geographic Performance",
        description="Locations with spend but no conversions — exclusion candidates",
        query=(
            "SELECT geographic_view.country_criterion_id, "
            "campaign.name, "
            "metrics.clicks, metrics.cost_micros, metrics.conversions "
            "FROM geographic_view "
            "WHERE segments.date DURING LAST_30_DAYS "
            "AND metrics.cost_micros > 5000000 "
            "AND metrics.conversions = 0 "
            "ORDER BY metrics.cost_micros DESC"
        ),
        when_to_use=(
            "Locations spending over $5 with zero conversions. Either exclude them "
            "or check if the landing page serves that area at all."
        ),
    ),

    # ── Ad Copy Performance ───────────────────────────────────────────
    QueryTemplate(
        name="rsa_asset_performance",
        category="Ad Copy Performance",
        description="RSA headline and description performance ratings",
        query=(
            "SELECT campaign.name, ad_group.name, "
            "ad_group_ad.ad.responsive_search_ad.headlines, "
            "ad_group_ad.ad.responsive_search_ad.descriptions, "
            "ad_group_ad.ad.final_urls, "
            "metrics.clicks, metrics.impressions, metrics.conversions, "
            "metrics.ctr "
            "FROM ad_group_ad "
            "WHERE segments.date DURING LAST_30_DAYS "
            "AND ad_group_ad.ad.type = 'RESPONSIVE_SEARCH_AD' "
            "AND ad_group_ad.status = 'ENABLED' "
            "ORDER BY metrics.impressions DESC"
        ),
        when_to_use=(
            "Review RSA asset combinations. Google rates headlines/descriptions as "
            "BEST, GOOD, or LOW. Replace LOW-rated assets to improve ad strength."
        ),
    ),
    QueryTemplate(
        name="ad_landing_page_metrics",
        category="Ad Copy Performance",
        description="Landing page performance by ad to find broken or slow pages",
        query=(
            "SELECT ad_group_ad.ad.final_urls, "
            "landing_page_view.unexpanded_final_url, "
            "metrics.clicks, metrics.conversions, metrics.cost_micros, "
            "metrics.mobile_friendly_clicks_percentage "
            "FROM landing_page_view "
            "WHERE segments.date DURING LAST_30_DAYS "
            "AND metrics.clicks > 10 "
            "ORDER BY metrics.conversions ASC"
        ),
        when_to_use=(
            "Find landing pages with high traffic but low conversions. Low "
            "mobile_friendly_clicks_percentage means mobile UX needs fixing."
        ),
    ),

    # ── Negative Keywords ─────────────────────────────────────────────
    QueryTemplate(
        name="campaign_negatives_audit",
        category="Negative Keyword Audit",
        description="All negative keywords by campaign to check for conflicts",
        query=(
            "SELECT campaign.name, "
            "campaign_criterion.keyword.text, "
            "campaign_criterion.keyword.match_type, "
            "campaign_criterion.negative "
            "FROM campaign_criterion "
            "WHERE campaign_criterion.negative = TRUE "
            "AND campaign_criterion.type = 'KEYWORD' "
            "ORDER BY campaign.name"
        ),
        when_to_use=(
            "Audit negatives to prevent conflicts — a negative that blocks a "
            "converting keyword silently kills performance."
        ),
    ),
    QueryTemplate(
        name="shared_negative_lists",
        category="Negative Keyword Audit",
        description="Shared negative keyword lists and their campaign assignments",
        query=(
            "SELECT shared_set.name, shared_set.member_count, "
            "shared_set.status, shared_set.type "
            "FROM shared_set "
            "WHERE shared_set.type = 'NEGATIVE_KEYWORDS'"
        ),
        when_to_use=(
            "Check that shared negative lists exist and are applied to all relevant "
            "campaigns. Missing shared lists mean duplicating negatives everywhere."
        ),
    ),

    # ── Device & Schedule ─────────────────────────────────────────────
    QueryTemplate(
        name="device_performance",
        category="Campaign Performance",
        description="Performance split by device to set bid adjustments",
        query=(
            "SELECT campaign.name, segments.device, "
            "metrics.clicks, metrics.impressions, metrics.conversions, "
            "metrics.cost_micros, metrics.ctr, metrics.cost_per_conversion "
            "FROM campaign "
            "WHERE segments.date DURING LAST_30_DAYS "
            "AND campaign.status = 'ENABLED' "
            "ORDER BY campaign.name, segments.device"
        ),
        when_to_use=(
            "Compare CPA across mobile/desktop/tablet. If mobile CPA is 3x desktop, "
            "set a negative bid adjustment for mobile on that campaign."
        ),
    ),
    QueryTemplate(
        name="hourly_performance",
        category="Campaign Performance",
        description="Performance by hour of day to optimize ad scheduling",
        query=(
            "SELECT campaign.name, segments.hour, "
            "metrics.clicks, metrics.conversions, metrics.cost_micros "
            "FROM campaign "
            "WHERE segments.date DURING LAST_14_DAYS "
            "AND campaign.status = 'ENABLED' "
            "ORDER BY campaign.name, segments.hour"
        ),
        when_to_use=(
            "Find hours that waste budget (clicks but no conversions). Set ad "
            "schedules to reduce bids during off-peak hours."
        ),
    ),
]


def get_categories() -> list[str]:
    seen = []
    for t in TEMPLATES:
        if t.category not in seen:
            seen.append(t.category)
    return seen


def get_by_category(category: str) -> list[QueryTemplate]:
    return [t for t in TEMPLATES if t.category == category]


def get_by_name(name: str) -> QueryTemplate | None:
    for t in TEMPLATES:
        if t.name == name:
            return t
    return None
