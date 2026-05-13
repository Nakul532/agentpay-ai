# 🤖 AgentPay AI

**Autonomous Agent Payment Gateway · Stablecoin-Powered API Marketplace**
Built by Nakul Shriman Karthikeyan · Fintech Analyst

### 🌐 [**→ LIVE DEMO**](#) *(deploy URL pending)*

---

## 🎯 Overview

AgentPay AI is a working simulation of the **agentic commerce economy** — the next frontier of fintech where AI agents autonomously pay each other for services using stablecoins. Inspired by Coinbase's x402 protocol, Google Cloud's Pay.sh, and Visa's AI Commerce announcement (2025).

**Three AI agents** with different goals reason in real-time (powered by Google Gemini) about which APIs to call, then execute mock USDC payments with on-chain-style settlement.

## ✨ Features

- **3 Autonomous AI Agents**: ResearchBot-α, TradingBot-β, ContentBot-γ — each with unique goals, spending policies, and preferred API categories
- **10-API Marketplace**: Weather, News, Market Data, Price Prediction, Volatility, Sentiment, GPU Compute, AI Image Gen, Translation, Code Execution
- **Live AI Reasoning**: Gemini 2.0 Flash decides each agent's next API call based on their goal and recent activity
- **Mock USDC Settlement**: Every transaction generates a blockchain-style hash, block number, gas cost, and settlement time
- **Treasury Analytics**: Real-time spend by agent, API revenue, category split, cumulative spend timeline
- **Spending Policies**: Per-transaction limits, daily limits, balance checks on every settlement

## 🛠️ Tech Stack

Python · Streamlit · Google Gemini API · Pandas · Plotly

## 🚀 Run Locally

```bash
git clone https://github.com/Nakul532/agentpay-ai.git
cd agentpay-ai
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your Gemini API key (free at https://aistudio.google.com/apikey)
streamlit run app.py
```

Works without an API key too — falls back to mock decision logic.

## 🧠 The Agentic Economy Context

In 2026, AI agents are transitioning from chatbots to autonomous economic actors. Industry signals:

- **Coinbase x402 (Apr 2025)**: HTTP-native protocol for AI agents to make stablecoin micropayments per API call
- **Google Pay.sh + Solana (Aug 2025)**: Stablecoin-powered agentic checkout
- **Visa Intelligent Commerce (Oct 2025)**: AI-powered commerce platform with embedded agent payments
- **McKinsey forecast**: $3-5T agentic commerce market by 2030

AgentPay AI demonstrates the core fintech infrastructure this economy needs:
1. Agent identity (wallet addresses)
2. Spending policies (per-txn limits, daily caps)
3. Sub-cent micropayments (settlement in ms, not days)
4. Audit trails (every payment includes AI reasoning + on-chain receipt)

## 👤 About the Builder

**Nakul Shriman Karthikeyan**
M.S. Engineering Management, Northeastern University · Fintech Analyst · IEEE Published

🔗 [LinkedIn](https://linkedin.com/in/shriman-nakul) · [Portfolio](https://nakul532.github.io)

## ⚖️ Disclaimer

All payments are mock USDC. No real blockchain transactions occur. No real funds. This project demonstrates the technical architecture of agentic payments, not a production payment system.
