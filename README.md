# AI Transformation Navigator

A Python/Streamlit demo for **enterprise AI strategy and transformation**. Created as a personal interview and learning project.

## What it does

1. **Diagnose:** Score organizational AI readiness across five self-assessed dimensions.
2. **Prioritize:** Rank illustrative AI use cases by impact, ease, industry fit and readiness.
3. **Model:** Simulate the value of released staff capacity and estimate simple payback.
4. **Report:** Export a tailored Markdown strategy report and CSV of assumptions.

> All examples, scores and use cases are hypothetical. The readiness model is a transparent heuristic, not a validated industry benchmark. Annual labor-capacity value should not be treated as actual realized cost savings. This v1 uses **no generative AI API**. A later version can add an LLM with appropriate security and cost safeguards.

## Project structure

```text
ai-transformation-navigator/
├── app.py                   # Streamlit interface
├── engine.py                # Transparent scoring and ROI formulas
├── requirements.txt         # Python dependencies
├── .streamlit/config.toml   # Theme
├── tests/test_engine.py     # Logic tests
├── .gitignore               # Keeps local and secret files out of Git
└── README.md
```

## Run locally (Mac)

**Prerequisite:** Python 3.10+ and Terminal.

```bash
cd ~/Downloads/ai-transformation-navigator
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
streamlit run app.py
```

If your folder is in a different location, adjust the first line. Streamlit will print a local URL (typically `http://localhost:8501`) in Terminal. Press `Ctrl+C` to stop.

## Run tests

```bash
python3 -m unittest discover -s tests -v
```

## Publish using your GitHub account

We recommend creating a **new** public GitHub repository named `ai-transformation-navigator`, so the existing `Equationfakeit/my-website` personal homepage stays untouched.

1. On GitHub, select **+ → New repository**.
2. Set repository name to `ai-transformation-navigator`, select **Public**, and create it **without** an auto-generated README, .gitignore, or license (those files are already included here).
3. From the project folder in Terminal, run:

```bash
cd ~/Downloads/ai-transformation-navigator
git init
git add .
git commit -m "Build AI transformation strategy demo"
git branch -M main
git remote add origin https://github.com/Equationfakeit/ai-transformation-navigator.git
git push -u origin main
```

If using GitHub via the browser, instead upload the project files and keep their relative paths, particularly `.streamlit/config.toml` and `tests/test_engine.py`.

## Deploy from GitHub with Streamlit Community Cloud

GitHub hosts code. **GitHub Pages does not run a Python server.** For this project:

1. Open https://share.streamlit.io and sign in with GitHub.
2. Click **Create app**, then choose to deploy an existing app.
3. Repository: `Equationfakeit/ai-transformation-navigator`
4. Branch: `main`
5. Main file path: `app.py`
6. Select a custom app subdomain if available, then click **Deploy**.
7. Streamlit generates a public `*.streamlit.app` link you can share or link from your original `my-website` page.

Official docs: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy

## Model specification

**Readiness:** `sum((rating − 1) / 4 × dimension_weight × 100)`; dimension weights: Data 25%, Technology 20%, Process 20%, People 20%, Responsible AI 15%.

**Opportunity:** `20 × (0.35 × impact + 0.30 × ease + 0.20 × sector_fit + 0.15 × readiness_fit)`; all component ratings use a 1–5 scale. Scenario impacts, ease scores and readiness thresholds are demonstrative assumptions.

**ROI:** Annual hours released = affected staff × hours saved/user/week × working weeks × adoption. Annual gross capacity value = hours released × loaded hourly cost. Annual net value = gross capacity value − recurring cost. First-year net value = annual net − initial cost. Simple payback applies only if annual net is positive. Inputs are **not** client observations.
