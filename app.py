"""AI Transformation Navigator — an interview-ready Python/Streamlit prototype.

All scoring parameters are disclosed, illustrative assumptions. No external API calls.
"""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from engine import (
    DIMENSIONS,
    SECTORS,
    RoiInputs,
    calculate_roi,
    opportunities,
    readiness_band,
    readiness_score,
    strategy_report,
)

st.set_page_config(
    page_title="AI Transformation Navigator",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp { background: radial-gradient(circle at 88% -8%, rgba(14,152,145,.10), transparent 32%), #0b1421; }
    .block-container { padding-top: 2.0rem; max-width: 1340px; }
    [data-testid="stSidebar"] { background: #101e2e; border-right: 1px solid #284053; }
    [data-testid="stSidebar"] .block-container { padding-top: 1.7rem; }
    h1, h2, h3 { letter-spacing: -.035em; }
    h1 { font-weight: 790 !important; }
    h3 { font-size: 1.18rem !important; }
    .eyebrow { font-size: .76rem; color: #37c9b9; font-weight: 700; letter-spacing: .15em; text-transform: uppercase; }
    .brandmark { display: inline-block; padding: .26rem .65rem; background: rgba(37,195,173,.10); border: 1px solid rgba(45,199,180,.38); color: #4ae1ca; border-radius: 9px; font-size: .76rem; font-weight: 750; letter-spacing: .06em; }
    .hero-sub { font-size: 1.08rem; color: #a7bacb; max-width: 850px; line-height: 1.7; }
    .status { display: inline-block; border-radius: 20px; padding: .26rem .65rem; background: rgba(255,255,255,.05); border: 1px solid #31506a; color: #c3d5e6; font-size: .79rem; }
    .dividerline { border-top: 1px solid #21394d; margin: 1.3rem 0; }
    .smallnote { font-size: .81rem; line-height: 1.55; color: #9eb2c3; }
    .section-intro { color: #9db1c6; font-size: .94rem; margin-bottom: 1.0rem; }
    [data-testid="stMetric"] { background: #132439; border: 1px solid #243e55; border-radius: 14px; padding: 1.0rem 1.1rem; }
    [data-testid="stMetricLabel"] { color: #a7becd; }
    [data-testid="stMetricValue"] { color: #f1fafc; }
    [data-testid="stTabs"] [data-baseweb="tab-list"] { gap: 10px; }
    [data-testid="stTabs"] [data-baseweb="tab"] { border-radius: 9px; background: #15283a; padding: 0 16px; }
    [data-testid="stTabs"] [aria-selected="true"] { background: #174337; }
    div[data-testid="stVerticalBlockBorderWrapper"] > div { border-color: #294057; }
    a { color: #6be5d0 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown('<span class="brandmark">ATN / STRATEGY LAB</span>', unsafe_allow_html=True)
    st.header("Client brief")
    st.caption("Configure an illustrative company to see how the assessment changes.")
    company = st.text_input("Company name", value="Northstar Manufacturing (Demo)", max_chars=90)
    sector = st.selectbox("Industry", SECTORS)
    employees = st.number_input("Total employees", min_value=1, max_value=1000000, value=420, step=10)
    st.divider()
    st.markdown("**Assessment inputs**")
    st.caption("Score each statement from 1 (not ready) to 5 (highly ready).")
    descriptions = {
        "Data & governance": "Data is accessible, reliable, owned, and governed.",
        "Technology infrastructure": "Secure, scalable systems can support AI pilots.",
        "Process readiness": "Processes are documented and measurable.",
        "People & skills": "Employees can adopt, operate, and challenge AI tools.",
        "Responsible AI & risk": "Privacy, model risk and oversight controls are defined.",
    }
    initial_values = [3, 3, 4, 2, 3]
    ratings = {}
    for idx, dimension in enumerate(DIMENSIONS):
        ratings[dimension] = st.slider(
            dimension,
            min_value=1,
            max_value=5,
            value=initial_values[idx],
            help=descriptions[dimension],
        )
    st.divider()
    st.caption("Independent educational demo · No company data transmitted to an AI API · Not affiliated with Deloitte")

score = readiness_score(ratings)
band = readiness_band(score)
ranked = opportunities(sector, score)

st.markdown('<span class="eyebrow">Enterprise AI · Decision intelligence</span>', unsafe_allow_html=True)
st.title("AI Transformation Navigator")
st.markdown(
    '<p class="hero-sub">A practical decision-support prototype for moving from AI ambition '
    'to prioritized use cases, transparent economics, and a 90-day pilot plan.</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<span class="status">● Illustrative consulting case</span> '
    '<span class="status">Transparent assumptions</span> '
    '<span class="status">No paid APIs required</span>',
    unsafe_allow_html=True,
)
st.write("")

m1, m2, m3, m4 = st.columns(4)
m1.metric("AI readiness", f"{score:.1f} / 100")
m2.metric("Maturity stage", band)
m3.metric("Potential use cases", str(len(ranked)))
m4.metric("Top priority", f"{ranked[0]['priority']:.1f} / 100")

st.write("")
tabs = st.tabs(["01 · Diagnose", "02 · Prioritize", "03 · ROI simulator", "04 · Strategy report"])

with tabs[0]:
    st.subheader("Assess the organization's starting point")
    st.markdown('<p class="section-intro">An explainable, self-assessed maturity model. Edit inputs in the left sidebar to see all outputs update.</p>', unsafe_allow_html=True)
    left, right = st.columns([1.05, 1], gap="large")
    with left:
        st.markdown("#### Readiness by dimension")
        for dimension, weight in DIMENSIONS.items():
            result = round((ratings[dimension] - 1) * 25)
            st.markdown(f"**{dimension}** · {ratings[dimension]}/5 · {weight:.0%} weight")
            st.progress(result)
        st.caption("Formula: Σ [(dimension rating − 1) / 4 × weight × 100]. This is not an external benchmark.")
    with right:
        cats = list(DIMENSIONS)
        vals = [(ratings[d] - 1) * 25 for d in cats]
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=vals + vals[:1],
            theta=cats + cats[:1],
            mode="lines+markers",
            fill="toself",
            line=dict(color="#36c7b6", width=3),
            marker=dict(size=7),
            fillcolor="rgba(54,199,182,0.20)",
            name="Readiness",
        ))
        fig.update_layout(
            height=390,
            showlegend=False,
            margin=dict(l=75, r=75, t=30, b=45),
            paper_bgcolor="rgba(0,0,0,0)",
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(range=[0, 100], showline=False, gridcolor="#2c445c", tickfont=dict(color="#829aad")),
                angularaxis=dict(gridcolor="#2c445c", tickfont=dict(color="#c9dce9", size=10)),
            ),
        )
        st.plotly_chart(fig, use_container_width=True)
    weakest = sorted(DIMENSIONS, key=lambda dimension: ratings[dimension])[:2]
    st.info("**Initial consulting hypothesis:** Strengthen " + " and ".join(weakest).lower() + " before scaling high-risk use cases. Validate ratings with stakeholder interviews and process evidence.")

with tabs[1]:
    st.subheader("Identify and prioritize AI opportunities")
    st.markdown('<p class="section-intro">Priority is based on business impact (35%), ease (30%), sector fit (20%) and readiness fit (15%). Scenario ratings are illustrative, not learned from a training dataset.</p>', unsafe_allow_html=True)
    st.markdown("#### Top three pilot candidates")
    cols = st.columns(3, gap="medium")
    for i, case in enumerate(ranked[:3]):
        with cols[i]:
            with st.container(border=True):
                st.caption(f"0{i + 1} · {case['category'].upper()}")
                st.markdown(f"### {case['name']}")
                st.metric("Priority score", f"{case['priority']:.1f}/100")
                st.write(case["description"])
                st.caption(f"Risk: {case['risk']} · KPI: {case['kpi']}")
    st.write("")
    st.markdown("#### Opportunity matrix")
    fig = go.Figure()
    for case in ranked:
        fig.add_trace(go.Scatter(
            x=[case["ease"]],
            y=[case["impact"]],
            mode="markers+text",
            text=[case["name"]],
            textposition="top center",
            textfont=dict(size=10, color="#cfe4ee"),
            marker=dict(
                size=case["priority"] * .48,
                color="#32c1b1" if case["name"] == ranked[0]["name"] else "#668fbd",
                line=dict(width=1, color="#b5e5e6"),
                opacity=.87,
            ),
            hovertemplate=f"<b>{case['name']}</b><br>Priority: {case['priority']:.1f}/100<br>Ease: %{{x:.1f}}/5<br>Impact: %{{y:.1f}}/5<extra></extra>",
            showlegend=False,
        ))
    fig.update_layout(
        height=430,
        margin=dict(l=25, r=40, t=25, b=20),
        xaxis=dict(title="Ease of implementation →", range=[1.4, 5.25], gridcolor="#244059"),
        yaxis=dict(title="Business impact →", range=[2.2, 5.3], gridcolor="#244059"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#c8d8e6"),
        hoverlabel=dict(bgcolor="#21394e"),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("#### Governance before scale")
    risk_table = pd.DataFrame([
        {"Candidate": c["name"], "Risk": c["risk"], "Critical guardrail": c["guardrail"], "Pilot KPI": c["kpi"]}
        for c in ranked[:4]
    ])
    st.dataframe(risk_table, hide_index=True, use_container_width=True)

with tabs[2]:
    st.subheader("Build a defendable pilot business case")
    st.markdown('<p class="section-intro">Model employee capacity released by automation using adjustable assumptions. These estimates should never be presented as guaranteed cost savings.</p>', unsafe_allow_html=True)
    inp, out = st.columns([.88, 1.12], gap="large")
    with inp:
        with st.container(border=True):
            st.markdown("#### Change assumptions")
            case_name = st.selectbox("Use case to model", [case["name"] for case in ranked])
            affected_staff = st.number_input("Employees using the solution", min_value=1, max_value=int(employees), value=min(int(employees), 40), step=1)
            hours_saved = st.slider("Hours saved / user / week", min_value=0.0, max_value=15.0, value=2.0, step=0.5)
            adoption_pct = st.slider("Effective adoption (%)", min_value=0, max_value=100, value=60, step=5)
            hourly_cost = st.number_input("Fully loaded cost per hour (USD)", min_value=0.0, max_value=1000.0, value=35.0, step=5.0)
            upfront = st.number_input("One-time implementation cost (USD)", min_value=0.0, max_value=10000000.0, value=40000.0, step=5000.0)
            recurring = st.number_input("Recurring annual cost (USD)", min_value=0.0, max_value=10000000.0, value=18000.0, step=1000.0)
            weeks = st.number_input("Working weeks per year", min_value=1, max_value=52, value=48, step=1)
    model = RoiInputs(
        affected_staff=int(affected_staff),
        hours_saved_per_staff_per_week=float(hours_saved),
        adoption_rate=float(adoption_pct) / 100,
        hourly_cost_usd=float(hourly_cost),
        one_time_cost_usd=float(upfront),
        recurring_cost_usd_per_year=float(recurring),
        working_weeks=int(weeks),
    )
    roi = calculate_roi(model)
    with out:
        st.markdown("#### Financial scenario · USD")
        z1, z2 = st.columns(2)
        z1.metric("Annual hours released", f"{roi.annual_hours_released:,.0f} h")
        z2.metric("Gross capacity value / year", f"${roi.annual_gross_capacity_value:,.0f}")
        z3, z4 = st.columns(2)
        z3.metric("First-year net value", f"${roi.first_year_net_value:,.0f}")
        z4.metric("Simple payback", f"{roi.payback_months:.1f} mo" if roi.payback_months is not None else "Not reached")
        st.markdown("#### Illustrative cumulative net value")
        fig = go.Figure()
        fig.add_hline(y=0, line_color="#839aac", line_dash="dash")
        fig.add_trace(go.Scatter(
            x=["Initial", "Year 1", "Year 2", "Year 3"],
            y=roi.cumulative_cash_equivalent,
            mode="lines+markers",
            line=dict(color="#3cd7c0", width=4),
            marker=dict(size=9),
            fill="tozeroy",
            fillcolor="rgba(34,183,165,0.12)",
            hovertemplate="%{x}: $%{y:,.0f}<extra></extra>",
        ))
        fig.update_layout(
            height=285, margin=dict(l=15, r=10, t=15, b=10),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#c5d8e7"), yaxis=dict(tickprefix="$", gridcolor="#244059"),
            xaxis=dict(showgrid=False),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Year 0 includes implementation investment; years 1–3 add estimated annual capacity value minus recurring operating costs. Undiscounted, simplified model.")
    st.warning("**Business interpretation:** Hours released × hourly labor cost is an estimate of productive capacity. Turning capacity into cash savings requires verifiable changes in staffing, costs, throughput, or revenue. Actual results may differ.")
    with st.expander("View the exact ROI formulas"):
        st.code(
            "Annual hours released = staff × hours saved/week × working weeks × adoption rate\n"
            "Annual capacity value = annual hours released × loaded hourly cost\n"
            "Annual net capacity value = annual capacity value − recurring annual cost\n"
            "First-year net value = annual net capacity value − one-time implementation cost\n"
            "First-year ROI = first-year net value / one-time implementation cost\n"
            "Simple payback (months) = one-time implementation cost / annual net capacity value × 12",
            language="text",
        )

with tabs[3]:
    st.subheader("Turn analysis into an actionable 90-day plan")
    st.markdown('<p class="section-intro">The report below is automatically assembled from the current assessment, prioritized scenarios, and the ROI assumptions. No LLM or external API is used in version 1.</p>', unsafe_allow_html=True)
    plan1, plan2, plan3 = st.columns(3, gap="medium")
    with plan1:
        with st.container(border=True):
            st.caption("DAYS 01–30")
            st.markdown("#### Discover")
            st.write("Map the existing workflow, interview users, agree on a baseline metric and define data access rules.")
    with plan2:
        with st.container(border=True):
            st.caption("DAYS 31–60")
            st.markdown("#### Pilot")
            st.write("Build a limited prototype, collect user feedback, stress-test failures and document controls.")
    with plan3:
        with st.container(border=True):
            st.caption("DAYS 61–90")
            st.markdown("#### Validate")
            st.write("Measure adoption, time saved, reliability and cost. Present an evidence-based scale/no-scale decision.")
    report = strategy_report(company, sector, int(employees), ratings, ranked, model, roi)
    with st.expander("Preview strategy report", expanded=True):
        st.markdown(report)
    st.download_button(
        label="↓ Download strategy report (.md)",
        data=report,
        file_name="ai_transformation_strategy_report.md",
        mime="text/markdown",
        type="primary",
    )
    assumptions = pd.DataFrame([
        {"Assumption": "Affected employees", "Value": model.affected_staff},
        {"Assumption": "Hours saved weekly", "Value": model.hours_saved_per_staff_per_week},
        {"Assumption": "Adoption rate", "Value": model.adoption_rate},
        {"Assumption": "Hourly labor cost USD", "Value": model.hourly_cost_usd},
        {"Assumption": "Implementation cost USD", "Value": model.one_time_cost_usd},
        {"Assumption": "Annual recurring cost USD", "Value": model.recurring_cost_usd_per_year},
        {"Assumption": "Annual hours released", "Value": roi.annual_hours_released},
        {"Assumption": "Annual capacity value USD", "Value": roi.annual_gross_capacity_value},
        {"Assumption": "First-year net value USD", "Value": roi.first_year_net_value},
    ])
    st.download_button(
        label="↓ Download assumptions (.csv)",
        data=assumptions.to_csv(index=False).encode("utf-8"),
        file_name="ai_business_case_assumptions.csv",
        mime="text/csv",
    )

st.markdown('<div class="dividerline"></div>', unsafe_allow_html=True)
st.markdown('<p class="smallnote">AI Transformation Navigator · Personal portfolio prototype. Readiness and prioritization scores are heuristic, and all company inputs are illustrative. No endorsement by or affiliation with Deloitte.</p>', unsafe_allow_html=True)
