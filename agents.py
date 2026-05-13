"""
AgentPay AI - Agent definitions and AI-powered decision making.
Uses Google Gemini for autonomous agent reasoning.
"""
import json
import random
import os
from datetime import datetime
import google.generativeai as genai

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Pre-configured agents
AGENTS = {
    "ResearchBot-α": {
        "id": "agent_001",
        "name": "ResearchBot-α",
        "role": "Market Research Agent",
        "wallet_address": "0xR3s34rch...8a7f",
        "starting_balance": 100.0,
        "spending_limit_per_txn": 5.0,
        "daily_limit": 50.0,
        "goal": "Gather market intelligence and trending news data",
        "preferred_apis": ["News API", "Market Data API", "Sentiment Analysis API"],
        "color": "#00d9a3",
        "emoji": "🔬",
    },
    "TradingBot-β": {
        "id": "agent_002",
        "name": "TradingBot-β",
        "role": "Algorithmic Trading Agent",
        "wallet_address": "0xTr4d3...9b2c",
        "starting_balance": 250.0,
        "spending_limit_per_txn": 10.0,
        "daily_limit": 100.0,
        "goal": "Identify trading opportunities through real-time market data and predictions",
        "preferred_apis": ["Market Data API", "Price Prediction API", "Volatility API"],
        "color": "#ffaa00",
        "emoji": "📈",
    },
    "ContentBot-γ": {
        "id": "agent_003",
        "name": "ContentBot-γ",
        "role": "Content Generation Agent",
        "wallet_address": "0xC0nt3nt...4e1d",
        "starting_balance": 75.0,
        "spending_limit_per_txn": 3.0,
        "daily_limit": 30.0,
        "goal": "Produce high-quality content using research data and AI image generation",
        "preferred_apis": ["News API", "AI Image Gen API", "Translation API"],
        "color": "#ff4757",
        "emoji": "✍️",
    },
}


# API marketplace
API_MARKETPLACE = [
    {"name": "Weather API", "provider": "WeatherCorp", "price": 0.001, "category": "Data", "description": "Real-time weather data globally"},
    {"name": "News API", "provider": "NewsHub", "price": 0.002, "category": "Data", "description": "Breaking news + historical archive"},
    {"name": "Market Data API", "provider": "FinStream", "price": 0.005, "category": "Finance", "description": "Real-time stock/crypto prices"},
    {"name": "Price Prediction API", "provider": "OracleAI", "price": 0.015, "category": "Finance", "description": "ML-powered price forecasts (24h horizon)"},
    {"name": "Volatility API", "provider": "FinStream", "price": 0.008, "category": "Finance", "description": "VIX-like volatility scoring per asset"},
    {"name": "Sentiment Analysis API", "provider": "MoodSync", "price": 0.003, "category": "AI", "description": "Sentiment scoring on text/social media"},
    {"name": "GPU Compute API", "provider": "ComputeMesh", "price": 0.050, "category": "Compute", "description": "On-demand H100 GPU compute (per minute)"},
    {"name": "AI Image Gen API", "provider": "PixelMint", "price": 0.020, "category": "AI", "description": "Stable Diffusion image generation"},
    {"name": "Translation API", "provider": "LinguaNet", "price": 0.001, "category": "AI", "description": "100+ language translation"},
    {"name": "Code Execution API", "provider": "CodeSandbox", "price": 0.010, "category": "Compute", "description": "Sandboxed code execution"},
]


def get_agent_decision_with_ai(agent, marketplace, recent_purchases):
    """Use Gemini to make agent decide which API to call."""
    if not GEMINI_API_KEY:
        return get_agent_decision_mock(agent, marketplace, recent_purchases)

    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')

        # Build context
        available_apis = "\n".join([
            f"- {api['name']} (${api['price']:.4f}/call): {api['description']}"
            for api in marketplace
        ])

        recent = "\n".join([f"- {p['api_name']} at ${p['amount']:.4f}" for p in recent_purchases[-5:]]) if recent_purchases else "None yet"

        prompt = f"""You are {agent['name']}, an autonomous AI agent.

ROLE: {agent['role']}
GOAL: {agent['goal']}
WALLET BALANCE: ${agent['current_balance']:.2f} USDC
SPENDING LIMIT PER TRANSACTION: ${agent['spending_limit_per_txn']:.2f}
PREFERRED API CATEGORIES: {', '.join(agent['preferred_apis'])}

AVAILABLE APIs IN MARKETPLACE:
{available_apis}

YOUR RECENT PURCHASES:
{recent}

Decide which ONE API to call next to advance your goal. Respond ONLY in this exact JSON format:
{{"api_name": "<exact API name>", "reasoning": "<brief 1-sentence reason>"}}

Choose an API that matches your goal and is within your per-transaction spending limit."""

        response = model.generate_content(prompt)
        text = response.text.strip()

        # Strip code fences if present
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:].strip()

        decision = json.loads(text.strip())
        return decision
    except Exception as e:
        # Fallback to mock if AI fails
        return get_agent_decision_mock(agent, marketplace, recent_purchases)


def get_agent_decision_mock(agent, marketplace, recent_purchases):
    """Fallback decision logic without AI."""
    # Match to preferred APIs
    preferred = [api for api in marketplace if api['name'] in agent['preferred_apis']]
    candidates = preferred if preferred else marketplace
    # Filter by spending limit
    affordable = [api for api in candidates if api['price'] <= agent['spending_limit_per_txn']]
    if not affordable:
        affordable = candidates
    chosen = random.choice(affordable)

    reasonings = [
        f"This API directly serves my goal of {agent['goal'][:40]}...",
        f"Highest relevance to my role as {agent['role']}",
        f"Best ROI per call for my current objective",
        f"Pre-approved category in my spending policy",
    ]

    return {
        "api_name": chosen['name'],
        "reasoning": random.choice(reasonings),
    }


def simulate_api_response(api_name, agent):
    """Generate a mock response from the API call."""
    responses = {
        "Weather API": "72°F, partly cloudy, NYC",
        "News API": "Breaking: Fed announces rate decision...",
        "Market Data API": f"BTC: $94,231 | ETH: $3,421 | NVDA: $145.20",
        "Price Prediction API": "BTC 24h forecast: +2.3% (confidence: 0.78)",
        "Volatility API": "VIX-equivalent: 18.4 (low)",
        "Sentiment Analysis API": "Market sentiment: 0.62 (bullish)",
        "GPU Compute API": "Job ID: gpu_8a7f2 | H100 reserved for 60s",
        "AI Image Gen API": "Image generated: img_4e1d.png (1024x1024)",
        "Translation API": "Translation complete: 1,234 chars processed",
        "Code Execution API": "Code executed: stdout captured, exit 0",
    }
    return responses.get(api_name, "Response received")
