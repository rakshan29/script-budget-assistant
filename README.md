# 🎬 Script-to-Budget Executive Assistant

An intelligent, agentic AI pipeline that converts screenplay scripts into real-time, structured production budget analytics using **Google Gemini 2.5 Flash**, **ClickHouse Cloud**, and **Streamlit**.

---

## 🌟 Features

* **Autonomous Script Parsing:** Processes raw screenplay excerpts to identify scenes, department line items, and estimated costs.
* **Agentic Tool Calling:** Gemini 2.5 Flash autonomously invokes structured tools to write line items directly to ClickHouse Cloud.
* **Real-time Analytics:** Instant visual analytics powered by Plotly and Streamlit, featuring total budget metrics, category breakdowns, and scene-level cost distribution.
* **Structured Logging:** Full JSON logging for tracking agent tool executions, latencies, and database operations.

---

## 🏗️ Architecture & Tech Stack

* **LLM Engine:** Google Gemini API (`gemini-2.5-flash`)
* **Database:** ClickHouse Cloud (OLAP storage for fast aggregate analytics)
* **Frontend:** Streamlit & Plotly Express
* **Backend Runtime:** Python 3.12 (`dotenv`, `clickhouse-connect`)

---

## 📂 Project Structure

```text
├── app.py                      # Main Streamlit dashboard UI
├── agent_pipeline.py           # Gemini agent definition & function schemas
├── agent_analytical_runner.py  # Pipeline runner connecting agent to ClickHouse
├── clickhouse_tools.py        # Database query tools (summaries, breakdowns)
├── logger.py                   # Structured JSON logging framework
├── init_db.py                  # Database initialization script
├── check_db.py                 # Terminal script to verify database contents
├── reset_db.py                 # Utility script to clear/reset budget tables
├── .env                        # Local environment variables (API keys & credentials)
├── .gitignore                  # Git exclusion rules
└── requirements.txt            # Python dependency declarations