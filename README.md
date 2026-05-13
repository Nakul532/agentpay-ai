# 💸 AgentPay AI

**Autonomous Agent Payment Gateway**
Built by Nakul Shriman Karthikeyan · Fintech Analyst

### 🌐 [→ LIVE DEMO](https://agentpay-ai.streamlit.app)

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://agentpay-ai.streamlit.app)

---

## 🎯 Overview

AgentPay AI is a working autonomous agent payment gateway. Three AI agents (ResearchBot-α, TradingBot-β, ContentBot-γ) reason in real time using Google Gemini, decide which paid APIs to call, and settle payments to a mock USDC ledger. End-to-end reference implementation of the agentic commerce pattern inspired by Coinbase x402, Visa Intelligent Commerce, and Google Pay.sh.

Try it live: https://agentpay-ai.streamlit.app

## ✨ Features

- Real Gemini 2.0 Flash reasoning (each agent makes contextual buying decisions, not scripted ones)
- 3 distinct AI agents with USDC wallets, spending policies, and AI-defined goals
- 10-API marketplace (Weather, News, Market Data, Sentiment, Translation, GPU Compute, AI Image Gen, Code Execution, Price Prediction, Volatility)
- Mock USDC settlement with sub-400ms latency
- Live treasury analytics, transaction ledger, agent fleet dashboard
- Dark fintech aesthetic (green accent, mock blockchain txn hashes)

## 🤖 The 3 Autonomous Agents

| Agent | Role | Wallet | Policy |
|---|---|---|---|
| ResearchBot-α 🟢 | Market research and news synthesis | $250 USDC | Conservative spending, prefers verified sources |
| TradingBot-β 🟡 | Quantitative trading signals | $500 USDC | Aggressive, latency-sensitive, willing to pay premium for fresh data |
| ContentBot-γ 🔴 | Content generation and translation | $150 USDC | Budget-conscious, prefers cheap APIs |

The agents decide which APIs to call based on their goals. No hardcoded buying flows.

## 🌐 Why This Matters in 2025-2026

The autonomous agent payments category went mainstream:

- **Coinbase x402** (May 2025) — HTTP 402 standard for AI agent payments
- **Visa Intelligent Commerce** (Oct 2025) — AI agents shopping autonomously
- **Google Pay.sh** — Agent-friendly payment rails
- **Stripe** — Agentic payments work
- **Citi forecast** — $4.6T agentic AI commerce by 2030

AgentPay AI is a working reference implementation. The architecture: agents reason about cost vs benefit, choose APIs, settle payments, observe results.

## 🛠️ Tech Stack

Python · Streamlit · Google Gemini 2.0 Flash · Plotly · python-dotenv

## 🚀 Run Locally

Clone the repo, install requirements, copy .env.example to .env, add your Gemini API key (free at https://aistudio.google.com/apikey), then run streamlit run app.py.

## 👤 About the Builder

**Nakul Shriman Karthikeyan**
M.S. Engineering Management, Northeastern University · Fintech Analyst · IEEE Published

🔗 [LinkedIn](https://linkedin.com/in/shriman-nakul) · [Portfolio](https://nakul532.github.io)

## ⚖️ Disclaimer

Mock USDC ledger only. No real blockchain, no real payments, no real API integrations beyond Gemini for agent reasoning. Demonstrates the autonomous agent payment architecture, not a production payment system.
