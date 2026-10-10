"""Transparent, illustrative AI strategy assessment model.

This model is an interview demonstration, not a validated consultancy methodology
or a statement about any real company's AI readiness.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

DIMENSIONS = {
    "Data & governance": 0.25,
    "Technology infrastructure": 0.20,
    "Process readiness": 0.20,
    "People & skills": 0.20,
    "Responsible AI & risk": 0.15,
}

SECTORS = [
    "Manufacturing",
    "Financial services",
    "Professional services",
    "Retail & e-commerce",
    "Energy & infrastructure",
]

# Scores are deliberately illustrative, selected to make the logic auditable.
USE_CASES = [
    {
        "name": "Enterprise knowledge assistant",
        "category": "Knowledge management",
        "description": "Find answers in approved internal documentation with traceable sources.",
        "impact": 4.1,
        "ease": 4.4,
        "required_readiness": 38,
        "sectors": SECTORS,
        "risk": "Medium",
        "guardrail": "Use access controls, source citations, and human review for critical answers.",
        "kpi": "Average time to locate a verified answer",
    },
    {
        "name": "Document processing automation",
        "category": "Operations",
        "description": "Extract and validate data from invoices, forms, or standard operating documents.",
        "impact": 4.3,
        "ease": 4.2,
        "required_readiness": 45,
        "sectors": ["Manufacturing", "Financial services", "Retail & e-commerce", "Energy & infrastructure"],
        "risk": "Medium",
        "guardrail": "Introduce confidence thresholds, exception queues, and audit logs.",
        "kpi": "Minutes per document processed",
    },
    {
        "name": "Research & intelligence copilot",
        "category": "Strategy",
        "description": "Summarize public market, policy, and competitor documents for analyst review.",
        "impact": 4.0,
        "ease": 4.5,
        "required_readiness": 32,
        "sectors": SECTORS,
        "risk": "Medium",
        "guardrail": "Display citations and require analysts to verify material claims.",
        "kpi": "Analyst hours per research brief",
    },
    {
        "name": "Predictive maintenance analytics",
        "category": "Industrial operations",
        "description": "Use sensor and historical maintenance data to forecast equipment downtime.",
        "impact": 4.8,
        "ease": 2.8,
        "required_readiness": 70,
        "sectors": ["Manufacturing", "Energy & infrastructure"],
        "risk": "High",
        "guardrail": "Validate sensor coverage and backtest predictions before operational use.",
        "kpi": "Unplanned downtime hours",
    },
    {
        "name": "Customer service triage",
        "category": "Customer experience",
        "description": "Categorize incoming inquiries and draft responses for staff approval.",
        "impact": 4.1,
        "ease": 3.8,
        "required_readiness": 50,
        "sectors": ["Financial services", "Professional services", "Retail & e-commerce"],
        "risk": "Medium",
        "guardrail": "Keep humans involved for complaints and sensitive interactions.",
        "kpi": "First-response time",
    },
    {
        "name": "Demand forecasting support",
        "category": "Planning",
        "description": "Forecast demand and help planners compare inventory scenarios.",
        "impact": 4.6,
        "ease": 3.1,
        "required_readiness": 64,
        "sectors": ["Manufacturing", "Retail & e-commerce", "Energy & infrastructure"],
        "risk": "Medium",
        "guardrail": "Evaluate forecast accuracy across seasons and maintain planner overrides.",
        "kpi": "Forecast error / MAPE",
    },
]


def readiness_score(ratings: Dict[str, int]) -> float:
    """Map dimension scores from 1–5 to a weighted 0–100 score."""
    missing = set(DIMENSIONS) - set(ratings)
    if missing:
        raise ValueError(f"Missing dimensions: {', '.join(sorted(missing))}")
    for key in DIMENSIONS:
        if ratings[key] < 1 or ratings[key] > 5:
            raise ValueError(f"{key} must be between 1 and 5")
    return round(sum((ratings[key] - 1) / 4 * 100 * weight for key, weight in DIMENSIONS.items()), 1)


def readiness_band(score: float) -> str:
    if score < 35:
        return "Foundational"
    if score < 65:
        return "Developing"
    return "Scaling-ready"


def opportunities(sector: str, readiness: float) -> List[dict]:
    """Return ranked scenarios using disclosed heuristic weights.

    Composite = 35% impact + 30% ease + 20% sector fit + 15% readiness fit.
    All component scores are on a 1–5 scale. There is no historical training data.
    """
    if sector not in SECTORS:
        raise ValueError("Unsupported sector")
    if not 0 <= readiness <= 100:
        raise ValueError("Readiness must be between 0 and 100")
    ranked = []
    for case in USE_CASES:
        sector_fit = 5.0 if sector in case["sectors"] else 2.0
        gap = max(0.0, case["required_readiness"] - readiness)
        readiness_fit = max(1.0, 5.0 - gap / 15.0)
        priority = 20 * (
            0.35 * case["impact"]
            + 0.30 * case["ease"]
            + 0.20 * sector_fit
            + 0.15 * readiness_fit
        )
        ranked.append({**case, "sector_fit": sector_fit, "readiness_fit": round(readiness_fit, 2), "priority": round(priority, 1)})
    return sorted(ranked, key=lambda case: case["priority"], reverse=True)


@dataclass(frozen=True)
class RoiInputs:
    affected_staff: int = 40
    hours_saved_per_staff_per_week: float = 2.0
    hourly_cost_usd: float = 35.0
    adoption_rate: float = 0.60
    one_time_cost_usd: float = 40000.0
    recurring_cost_usd_per_year: float = 18000.0
    working_weeks: int = 48


@dataclass(frozen=True)
class RoiResult:
    annual_hours_released: float
    annual_gross_capacity_value: float
    annual_net_capacity_value: float
    first_year_net_value: float
    first_year_roi_pct: float | None
    payback_months: float | None
    three_year_net_value: float
    cumulative_cash_equivalent: List[float]


def calculate_roi(p: RoiInputs) -> RoiResult:
    """Calculate an illustrative capacity-value scenario, not booked cash savings."""
    if (p.affected_staff < 0 or p.hours_saved_per_staff_per_week < 0 or
        p.hourly_cost_usd < 0 or p.one_time_cost_usd < 0 or
        p.recurring_cost_usd_per_year < 0 or p.working_weeks < 0 or
        not 0 <= p.adoption_rate <= 1):
        raise ValueError("ROI assumptions cannot be negative; adoption must be 0–1")
    hours = p.affected_staff * p.hours_saved_per_staff_per_week * p.working_weeks * p.adoption_rate
    gross = hours * p.hourly_cost_usd
    annual_net = gross - p.recurring_cost_usd_per_year
    year_one = annual_net - p.one_time_cost_usd
    roi = 100 * year_one / p.one_time_cost_usd if p.one_time_cost_usd > 0 else None
    payback = 12 * p.one_time_cost_usd / annual_net if annual_net > 0 else None
    cumulative = [-p.one_time_cost_usd]
    for _ in range(3):
        cumulative.append(cumulative[-1] + annual_net)
    return RoiResult(
        annual_hours_released=hours,
        annual_gross_capacity_value=gross,
        annual_net_capacity_value=annual_net,
        first_year_net_value=year_one,
        first_year_roi_pct=roi,
        payback_months=payback,
        three_year_net_value=cumulative[-1],
        cumulative_cash_equivalent=cumulative,
    )


def strategy_report(company: str, sector: str, staff: int, ratings: Dict[str, int],
                    ranked: List[dict], p: RoiInputs, r: RoiResult) -> str:
    score = readiness_score(ratings)
    top = ranked[:3]
    ranked_text = "\n".join(
        f"{i}. **{case['name']}** (priority {case['priority']:.1f}/100; risk: {case['risk']})\n"
        f"   - Why: {case['description']}\n"
        f"   - Pilot KPI: {case['kpi']}\n"
        f"   - Guardrail: {case['guardrail']}"
        for i, case in enumerate(top, 1)
    )
    dimension_lines = "\n".join(f"- {k}: {ratings[k]}/5 (weight {weight:.0%})" for k, weight in DIMENSIONS.items())
    roi_str = "N/A (zero initial cost)" if r.first_year_roi_pct is None else f"{r.first_year_roi_pct:.1f}%"
    payback_str = "Not reached under current assumptions" if r.payback_months is None else f"{r.payback_months:.1f} months"
    return f"""# AI TRANSFORMATION NAVIGATOR
## Illustrative AI strategy assessment

**Company:** {company}  
**Sector:** {sector}  
**Employees:** {staff:,}  
**Assessment:** {score:.1f}/100 ({readiness_band(score)})

### 1. Baseline assessment
{dimension_lines}

The readiness score is a self-assessed heuristic on five dimensions, not an externally validated benchmark.

### 2. Prioritized use cases
{ranked_text}

The priority model uses 35% impact, 30% implementation ease, 20% sector fit, and 15% readiness fit. Inputs are illustrative judgments, not measured company outcomes.

### 3. Pilot business case (USD)
- Employees in scope: {p.affected_staff}
- Hours saved per employee per week: {p.hours_saved_per_staff_per_week:.1f}
- Adoption rate: {p.adoption_rate:.0%}
- Fully loaded hourly labor cost: ${p.hourly_cost_usd:,.0f}
- One-time implementation cost: ${p.one_time_cost_usd:,.0f}
- Annual recurring cost: ${p.recurring_cost_usd_per_year:,.0f}
- Annual hours released: {r.annual_hours_released:,.0f}
- Indicative annual capacity value: ${r.annual_gross_capacity_value:,.0f}
- First-year net value after costs: ${r.first_year_net_value:,.0f}
- First-year ROI on initial cost: {roi_str}
- Simple payback: {payback_str}

**Important:** The potential labor-capacity value is not equivalent to realized cash savings. Financial benefits depend on redeployment, demand, execution, and measurement.

### 4. Suggested 90-day pilot roadmap
- **Days 1–30 — Discover:** Map process, interview stakeholders, establish data permissions and baseline KPI.
- **Days 31–60 — Pilot:** Build a limited prototype, test with a small user group, document model risks and failure modes.
- **Days 61–90 — Validate:** Measure actual adoption and time savings against the baseline; decide whether to scale.

### 5. Limitations
This report is a personal demonstration prototype for learning and interviews. It is not affiliated with Deloitte, it does not use proprietary data, and it is not a professional assessment or prediction.
"""
