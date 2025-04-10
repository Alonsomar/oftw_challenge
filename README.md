# OFTW Dash App – Data & Metrics Dashboard

This repository hosts a **Dash** application for **One for the World (OFTW)**, enabling you to track pledges, donations, and key performance metrics. It provides:

1. **Money Moved** dashboards (including counterfactual estimates),
2. **Objectives & Key Results (OKRs)** metrics,
3. **Pledge Performance** insights,
4. A **Chat LLM** page for natural-language data queries.

The code is primarily in **Python** (Dash, Plotly, Flask), structured around modular components for data ingestion, cleaning, transformations, caching, and visualization.

## 🌐 **Visit the Live Site:** [oftw.alonsovaldes.com](https://oftw.alonsovaldes.com)

---

## Table of Contents
- [Repository](#repository)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Configuration](#configuration)
- [Quick Start (Local)](#quick-start-local)
- [Deployment (Docker)](#deployment-docker)
- [Additional Notes](#additional-notes)

---

## Repository

- **Project URL**: [https://github.com/Alonsomar/oftw_challenge](https://github.com/Alonsomar/oftw_challenge)

---

## Features

1. **Money Moved**  
   - Monthly breakdown of donations, with side-by-side accumulated vs. actual views  
   - Counterfactual Money Moved (0–1 scaling for unique impact by OFTW)  

2. **OKRs**  
   - Tracks Active Donors, Pledge Attrition Rate, Chapter-level ARR (Annualized Run Rate)  
   - Compare progress against organizational targets  

3. **Pledge Performance**  
   - Summarizes total pledges, future pledges, channel breakdown, and monthly attrition  
   - Differentiates Active donor, Pledged donor, Payment failure, Churned donor  

4. **Chat LLM**  
   - Natural-language queries about filtered data (by Year, Portfolio, etc.)  
   - Powered by OpenAI (or swappable for another LLM)  
   - Uses environment variable from a `.env` file for the API key  

5. **Robust Code Structure**  
   - Separate modules for data ingestion, cleaning, metrics, and UI callbacks  
   - Server-side caching via `flask_caching`  

---

## Project Structure

A quick overview of relevant directories and files:

```
.
├── assets/                      # Custom CSS (styles.css) and static assets
├── data/                        # JSON data files (pledges, payments) & metadata
├── src/
│   ├── callbacks/              # Dash callbacks (LLM chat, money moved, pledge perf, etc.)
│   ├── components/             # Layout / UI pieces (header, sidebar, layout containers)
│   ├── data_ingestion/         # Data loading & cleaning from JSON => DataFrame
│   ├── metrics_calculations/   # Core logic for money moved, ARR, performance stats
│   ├── metrics_vizualizations/ # Plotly figure generation
│   ├── pages/                  # Dash page layouts (money_moved, notes, objectics, etc.)
│   └── utils/                  # Caching, financial calculations, filtering, etc.
├── main.py                      # Dash entry point (app initialization)
├── gunicorn_config.py           # Gunicorn config for production
├── log_config.py                # Logging (loguru) setup
├── .env                         # Environment variables (e.g., OPENAI_API_KEY)
└── README.md                    # This file
```

---

## Prerequisites

1. **Python 3.12+**  
2. **OpenAI API key** (if using the Chat LLM)  
   - Placed in `.env` at the project root under the key `OPENAI_API_KEY=sk-...`

Main dependencies:

- `dash`, `dash_bootstrap_components`, `plotly`
- `pandas`, `flask_caching`
- `openai` (for Chat LLM)

---

## Configuration

### Environment Variables in `.env`

- **`OPENAI_API_KEY`**  
  To enable the Chat LLM feature, define it in `.env` at your project root:
  ```txt
  OPENAI_API_KEY="sk-..."
  ```

- **Logging / Other**  
  Additional environment variables or log-level adjustments can be configured in `log_config.py`.  

### Gunicorn Config (Optional)

- The file `gunicorn_config.py` specifies default workers and threads (`workers = 1`, `threads = 1` using `gthread`). Adjust as desired for concurrency/scalability in production.

---

## Quick Start (Local)

For a quick local run (without Docker), you can:

1. **Clone the repo**:
   ```bash
   git clone https://github.com/Alonsomar/oftw_challenge.git
   cd oftw_challenge
   ```
2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate       # Mac/Linux
   # or venv\Scripts\activate     # Windows
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.in
   ```
4. **Set up the `.env` file** if you need the Chat LLM:
   ```txt
   OPENAI_API_KEY="sk-..."
   ```
5. **Run the app**:
   ```bash
   python main.py
   ```
6. Navigate to `http://127.0.0.1:8050` in your browser.

---

## Deployment (Docker)

A convenient way to deploy is via **Docker**. Make sure you have your `.env` file in the project root.

**Build** the Docker image:
```bash
docker build -t oftw .
```

**Run** the container, mapping port 8050 and supplying the `.env` file:
```bash
docker run -d -p 8050:8050 \
  --env-file .env \
  --restart unless-stopped \
  --name oftw_app \
  oftw
```

This container will start up the app, which you can then access at:
```
http://<your-server-ip>:8050
```

---

## Additional Notes

- **Caching**: The application uses `flask_caching` (in-memory by default). If you handle high traffic or need persistent caching, consider using Redis or another backend.  
- **Data Integrity**: The code logs warnings if active donors < active pledges, or if currency conversions detect anomalies. Check `log_config.py` for how logs are configured.  
- **Chat LLM**: If you’d like to swap in a different LLM, see `src/callbacks/chat_llm_callbacks.py`. The environment variable `OPENAI_API_KEY` is expected in `.env`.  

For more details on how the metrics are computed and how the data flows through the system, please see the `notes.py` page within the app.

Happy building! If you have any questions, feel free to open an issue or reach out to [Alonsomar](https://github.com/Alonsomar). 
