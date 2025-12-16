# Real-Time Quant Analytics Dashboard

## Overview

This project implements a **Real-Time Quantitative Analytics System** focused on pair trading and mean-reversion research.  
It ingests live market data, stores it efficiently, computes core statistical metrics, and presents them through an interactive dashboard designed for research and monitoring.
---

## Problem Being Solved

Quantitative researchers need to:

- monitor relationships between correlated assets in real time,
- detect statistically meaningful deviations,
- evaluate whether those deviations are reliable enough to investigate further.

This system addresses that need by combining **live data ingestion**, **standard quantitative analytics**, and **contextual interpretation of signals** in a single workflow.

---

## Architecture Diagram

<img width="11629" height="2670" alt="Architecture-Diagram" src="https://github.com/user-attachments/assets/f329ffdc-88e2-46d7-acc7-6287a844e211" />


---

## Architectural Principles

### Clear Separation of Concerns
Ingestion, storage, analytics, and presentation are isolated into separate modules.

### Frontend–Backend Decoupling
The frontend interacts only with a service layer and does not directly access raw data sources or databases.

### Pluggable Components
Data providers and storage backends can be replaced with minimal changes.

### Minimal Necessary Complexity
No REST APIs, message queues, or microservices were introduced, as they are not required for the assignment scope.

---
## Methodology

The project was built step by step, focusing on getting each part working correctly before moving to the next.

First, live market data is streamed using a WebSocket connection. At this stage, the system only focuses on reliably receiving and storing data, without running any analytics. Keeping ingestion lightweight helps avoid delays or dropped data when the stream is active.

Next, the incoming raw trade data is stored in duckDB database. For analysis, this raw data is resampled into fixed time intervals and aligned across assets. All calculations are performed on this resampled, time-aligned data so that statistical metrics remain stable and comparable across different timeframes.

Once the data is prepared, core analytics are computed using standard quantitative techniques. This includes estimating the hedge ratio using OLS regression, computing the spread between assets, and calculating rolling statistics such as z-score and correlation. Stationarity checks using the Augmented Dickey-Fuller test are provided as an on-demand diagnostic rather than being forced continuously.

On top of the raw analytics, an interpretation and alerting layer was added. Instead of only displaying numbers, the system explains what the current signals indicate and highlights conditions that deserve attention, such as extreme deviations, weakening correlations, volatility spikes, or potential stationarity issues. These alerts are informational and meant to support monitoring, not automated decision-making.

Finally, everything is presented through an interactive dashboard. Prices, signals, alerts, and diagnostics are separated into different views so the system remains easy to explore. Changing inputs like asset pairs or rolling windows updates the analytics in real time, making the dashboard suitable for exploratory research.

---

## Technology Stack 

### Language
- **Python 3**

Chosen for its strong ecosystem in data processing, statistics, and rapid prototyping.

---

### Market Data Ingestion
- **WebSocket (Binance Futures)**
- `asyncio`, `websockets`

Chosen to support:
- low-latency streaming data,
- event-driven ingestion,

---

### Storage
- **DuckDB**

Chosen because:
- optimized for analytical workloads,
- columnar and fast for time-series queries,
- zero external infrastructure,
- well-suited for research and local execution.

---

### Analytics
- `pandas`, `numpy`
- `statsmodels`
- `scipy`

Chosen to implement:
- regression-based hedge ratios,
- rolling statistics,
- stationarity testing using standard statistical methods.

All analytics are implemented as **stateless functions** for reuse and clarity.

---

### Frontend
- **Streamlit**
- **Plotly**

Chosen because:
- lightweight and fast for research dashboards,
- minimal boilerplate,
- interactive visualizations without frontend over-engineering.

The frontend is intentionally **research-oriented**, not a production trading UI.

---

## Analytics Implemented

### Hedge Ratio (OLS Regression)
Estimates the linear relationship between two assets using ordinary least squares, a standard approach in statistical arbitrage.

### Spread
Computed as the residual between the hedged assets, representing deviations from their historical relationship.

### Rolling Z-Score
Measures how far the spread deviates from its recent mean over a configurable window.

### Rolling Correlation
Used to evaluate the stability of the relationship and qualify signal reliability.

### Augmented Dickey-Fuller (ADF) Test
Provided as an on-demand diagnostic to assess stationarity of the spread, a key assumption in mean-reversion strategies.

---

## Alerting & Interpretation

### Alerts Implemented
- Z-score extremes (large deviations)
- Correlation breakdown (relationship weakening)
- Spread volatility spikes (possible regime change)
- Stationarity risk (ADF-based warning)

### Interpretation Layer
Numerical signals are accompanied by:
- qualitative explanations of what the signal implies,
- confidence assessment based on correlation,
- guidance on what a researcher might monitor next.

This avoids prescriptive trading advice while improving **decision interpretability**.

---

## Frontend Design Philosophy

The dashboard is designed as an **internal research tool**:

- split views for prices, signals, and diagnostics,
- compact KPI strip for high-level context,
- minimal styling focused on clarity.

The goal is to reflect how quantitative analytics are consumed in practice, not to replicate retail trading platforms.

---

## Handling of Data Limitations

Rolling metrics require sufficient historical data.  
Until enough data is available:

- NaN values may appear,
- the UI explicitly communicates these conditions.


---
##

## Running the Project

```bash
python -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows

pip install -r requirements.txt
streamlit run app.py

