"""
AgentPay AI - Autonomous Agent Payment Gateway
Built by Nakul Shriman Karthikeyan | Fintech Analyst
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import time
import copy
from datetime import datetime

# Load .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from agents import AGENTS, API_MARKETPLACE, get_agent_decision_with_ai, simulate_api_response
from payment_ledger import execute_payment

# Page config
st.set_page_config(
    page_title="AgentPay AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Dark theme styling
st.markdown("""
<style>
    .stApp { background-color: #0a0e1a; color: #e8eaed; }
    .main .block-container { padding-top: 2rem; max-width: 1400px; }
    h1, h2, h3 { color: #e8eaed; }
    .stMetric { background-color: #1a1f2e; padding: 1rem; border-radius: 8px; border: 1px solid #2a3142; }
    .stMetric label { color: #8b95a8 !important; }
    div[data-testid="stMetricValue"] { color: #00d9a3 !important; font-size: 1.6rem !important; }
    .stDataFrame { background-color: #1a1f2e; }
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
    .stTabs [data-baseweb="tab-list"] { background-color: #1a1f2e; }
    .stTabs [aria-selected="true"] { background-color: #00d9a3; color: #0a0e1a; }
    .agent-card { background: #1a1f2e; padding: 1.2rem; border-radius: 12px; border: 1px solid #2a3142; margin-bottom: 1rem; }
    .txn-card { background: #1a1f2e; padding: 0.8rem 1rem; border-radius: 8px; border-left: 3px solid #00d9a3; margin-bottom: 0.5rem; font-size: 0.9rem; }
    .footer { text-align: center; color: #8b95a8; font-size: 0.85rem; padding: 1rem 0; border-top: 1px solid #2a3142; margin-top: 2rem; }
    .footer a { color: #00d9a3; text-decoration: none; margin: 0 0.5rem; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div style='padding: 1rem 0; border-bottom: 1px solid #2a3142; margin-bottom: 1.5rem;'>
    <h1 style='margin: 0; color: #00d9a3;'>🤖 AgentPay AI</h1>
    <p style='margin: 0.25rem 0 0 0; color: #8b95a8; font-size: 1rem;'>
        Autonomous Agent Payment Gateway · Stablecoin-Powered API Marketplace · Built by Nakul Shriman Karthikeyan | Fintech Analyst
    </p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'agents' not in st.session_state:
    st.session_state.agents = {
        name: {**data, 'current_balance': data['starting_balance']}
        for name, data in AGENTS.items()
    }
if 'transactions' not in st.session_state:
    st.session_state.transactions = []

# ===========================
# Top metrics
# ===========================
total_balance = sum(a['current_balance'] for a in st.session_state.agents.values())
total_starting = sum(a['starting_balance'] for a in st.session_state.agents.values())
total_spent = total_starting - total_balance
total_txns = len(st.session_state.transactions)
api_revenue = sum(t['amount_usdc'] for t in st.session_state.transactions if t.get('status') == 'settled')

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Active Agents", f"{len(st.session_state.agents)}")
with col2:
    st.metric("Treasury (USDC)", f"${total_balance:,.2f}")
with col3:
    st.metric("Total Spent", f"${total_spent:,.4f}")
with col4:
    st.metric("Transactions", f"{total_txns:,}")
with col5:
    st.metric("API Marketplace", f"{len(API_MARKETPLACE)} APIs")

st.markdown("<br>", unsafe_allow_html=True)

# ===========================
# Tabs
# ===========================
tab1, tab2, tab3, tab4 = st.tabs(["🤖 Agent Fleet", "🏪 API Marketplace", "⚡ Live Activity", "📊 Treasury Analytics"])

# ===========================
# TAB 1: Agent Fleet
# ===========================
with tab1:
    st.subheader("Autonomous Agent Wallets")
    st.caption("Each agent has an on-chain USDC wallet, spending policy, and an AI-defined goal.")

    cols = st.columns(3)
    for idx, (name, agent) in enumerate(st.session_state.agents.items()):
        with cols[idx]:
            spent = agent['starting_balance'] - agent['current_balance']
            pct_spent = (spent / agent['starting_balance'] * 100) if agent['starting_balance'] > 0 else 0
            st.markdown(f"""
            <div class='agent-card' style='border-left: 4px solid {agent['color']};'>
                <h3 style='margin: 0; color: {agent['color']};'>{agent['emoji']} {agent['name']}</h3>
                <p style='color: #8b95a8; margin: 0.25rem 0 1rem 0; font-size: 0.85rem;'>{agent['role']}</p>
                <div style='font-family: monospace; color: #8b95a8; font-size: 0.75rem; margin-bottom: 0.75rem;'>{agent['wallet_address']}</div>
                <div style='font-size: 1.4rem; color: {agent['color']}; font-weight: 600;'>${agent['current_balance']:.2f} USDC</div>
                <div style='color: #8b95a8; font-size: 0.8rem; margin-top: 0.25rem;'>Spent: ${spent:.4f} ({pct_spent:.1f}%)</div>
                <hr style='border-color: #2a3142; margin: 0.75rem 0;' />
                <div style='font-size: 0.85rem; color: #c5cdd9; margin-bottom: 0.5rem;'><b>Goal:</b> {agent['goal']}</div>
                <div style='font-size: 0.8rem; color: #8b95a8;'><b>Per-txn limit:</b> ${agent['spending_limit_per_txn']:.2f}</div>
                <div style='font-size: 0.8rem; color: #8b95a8;'><b>Daily limit:</b> ${agent['daily_limit']:.2f}</div>
            </div>
            """, unsafe_allow_html=True)

# ===========================
# TAB 2: API Marketplace
# ===========================
with tab2:
    st.subheader("Agentic API Marketplace")
    st.caption("APIs available for agent-to-API microtransactions. All payments settle in mock USDC.")

    df_market = pd.DataFrame(API_MARKETPLACE)
    df_market['price'] = df_market['price'].apply(lambda x: f"${x:.4f}")
    df_market.columns = ['API Name', 'Provider', 'Price/Call', 'Category', 'Description']
    st.dataframe(df_market, use_container_width=True, hide_index=True, height=420)

    # Category breakdown
    cat_counts = pd.DataFrame(API_MARKETPLACE)['category'].value_counts().reset_index()
    cat_counts.columns = ['Category', 'Count']
    fig = px.bar(cat_counts, x='Category', y='Count', template='plotly_dark',
                 color='Count', color_continuous_scale='Tealgrn')
    fig.update_layout(plot_bgcolor='#0a0e1a', paper_bgcolor='#0a0e1a', height=300,
                      showlegend=False, margin=dict(t=20, b=20),
                      title=dict(text="APIs by Category", font_color='#e8eaed'))
    st.plotly_chart(fig, use_container_width=True)

# ===========================
# TAB 3: Live Activity
# ===========================
with tab3:
    st.subheader("Autonomous Agent Activity Feed")

    has_key = bool(os.getenv("GEMINI_API_KEY"))
    if has_key:
        st.success("✅ Gemini AI agents active — real autonomous reasoning enabled")
    else:
        st.info("ℹ️ Mock agent mode (no GEMINI_API_KEY in .env) — agents use scripted decision logic")

    col_a, col_b, col_c = st.columns([1, 1, 3])
    with col_a:
        sim_rounds = st.number_input("Simulate transactions", min_value=1, max_value=20, value=5, step=1)
    with col_b:
        run_sim = st.button("▶️ Run Simulation", type="primary", use_container_width=True)
    with col_c:
        if st.button("🔄 Reset all agents", use_container_width=False):
            for name in st.session_state.agents:
                st.session_state.agents[name]['current_balance'] = AGENTS[name]['starting_balance']
            st.session_state.transactions = []
            st.rerun()

    if run_sim:
        progress = st.progress(0)
        status = st.empty()

        for i in range(sim_rounds):
            # Pick an agent (round-robin with some randomness)
            agent_names = list(st.session_state.agents.keys())
            agent_name = agent_names[i % len(agent_names)]
            agent = st.session_state.agents[agent_name]

            status.markdown(f"🧠 **{agent['name']}** is reasoning about next API call...")
            time.sleep(0.4)

            # Get decision
            recent = [t for t in st.session_state.transactions if t.get('agent_id') == agent['id']][-5:]
            decision = get_agent_decision_with_ai(agent, API_MARKETPLACE, recent)

            # Find API
            api = next((a for a in API_MARKETPLACE if a['name'] == decision['api_name']), API_MARKETPLACE[0])

            # Get API response
            api_response = simulate_api_response(api['name'], agent)

            # Execute payment
            result = execute_payment(agent, api, decision['reasoning'], api_response)

            if result['status'] == 'settled':
                st.session_state.transactions.append(result)
                status.markdown(f"✅ **{agent['name']}** paid ${api['price']:.4f} to **{api['provider']}** for **{api['name']}** — {decision['reasoning']}")
            else:
                status.markdown(f"❌ Payment failed for {agent['name']}: {result['reason']}")

            progress.progress((i + 1) / sim_rounds)
            time.sleep(0.3)

        status.success(f"✅ Simulation complete: {sim_rounds} transactions processed")
        time.sleep(0.5)
        st.rerun()

    # Display recent transactions
    st.markdown("### Recent Transaction Feed")
    if not st.session_state.transactions:
        st.info("No transactions yet. Click 'Run Simulation' to start.")
    else:
        for txn in reversed(st.session_state.transactions[-20:]):
            agent_color = next((a['color'] for a in AGENTS.values() if a['id'] == txn['agent_id']), '#00d9a3')
            st.markdown(f"""
            <div class='txn-card' style='border-left-color: {agent_color};'>
                <div style='display: flex; justify-content: space-between;'>
                    <div>
                        <b style='color: {agent_color};'>{txn['agent_name']}</b> →
                        <span style='color: #c5cdd9;'>{txn['api_name']}</span>
                        <span style='color: #8b95a8;'>· {txn['api_provider']}</span>
                    </div>
                    <div style='color: #00d9a3; font-weight: 600;'>${txn['amount_usdc']:.4f} USDC</div>
                </div>
                <div style='color: #8b95a8; font-size: 0.8rem; margin-top: 0.25rem;'>
                    <i>"{txn['reasoning']}"</i>
                </div>
                <div style='color: #6a7388; font-size: 0.75rem; margin-top: 0.25rem; font-family: monospace;'>
                    {txn['txn_hash']} · Block #{txn['block_number']} · Settled in {txn['settlement_time_ms']}ms · Gas: ${txn['gas_used_usdc']:.5f}
                </div>
                <div style='color: #6a7388; font-size: 0.75rem; margin-top: 0.25rem;'>
                    📦 Response: {txn['api_response']}
                </div>
            </div>
            """, unsafe_allow_html=True)

# ===========================
# TAB 4: Treasury Analytics
# ===========================
with tab4:
    st.subheader("Treasury & Revenue Analytics")

    if not st.session_state.transactions:
        st.info("Run a simulation in the Live Activity tab to populate analytics.")
    else:
        df = pd.DataFrame(st.session_state.transactions)

        ana_col1, ana_col2 = st.columns(2)

        with ana_col1:
            # Spend by agent
            spend_by_agent = df.groupby('agent_name')['amount_usdc'].sum().reset_index()
            spend_by_agent = spend_by_agent.sort_values('amount_usdc', ascending=True)
            fig = px.bar(spend_by_agent, x='amount_usdc', y='agent_name', orientation='h',
                         template='plotly_dark', color='amount_usdc', color_continuous_scale='Tealgrn',
                         title='Spend by Agent (USDC)')
            fig.update_layout(plot_bgcolor='#0a0e1a', paper_bgcolor='#0a0e1a', height=300,
                              showlegend=False, margin=dict(t=40, b=20),
                              xaxis_title='', yaxis_title='')
            st.plotly_chart(fig, use_container_width=True)

        with ana_col2:
            # API revenue by provider
            api_rev = df.groupby('api_provider')['amount_usdc'].sum().reset_index()
            api_rev = api_rev.sort_values('amount_usdc', ascending=True)
            fig = px.bar(api_rev, x='amount_usdc', y='api_provider', orientation='h',
                         template='plotly_dark', color='amount_usdc', color_continuous_scale='Oranges',
                         title='API Provider Revenue (USDC)')
            fig.update_layout(plot_bgcolor='#0a0e1a', paper_bgcolor='#0a0e1a', height=300,
                              showlegend=False, margin=dict(t=40, b=20),
                              xaxis_title='', yaxis_title='')
            st.plotly_chart(fig, use_container_width=True)

        # Category split
        cat_col1, cat_col2 = st.columns(2)
        with cat_col1:
            cat_spend = df.groupby('api_category')['amount_usdc'].sum().reset_index()
            fig = px.pie(cat_spend, values='amount_usdc', names='api_category', template='plotly_dark',
                         title='Spend by API Category',
                         color_discrete_sequence=['#00d9a3', '#ffaa00', '#ff4757', '#5b8def'])
            fig.update_layout(plot_bgcolor='#0a0e1a', paper_bgcolor='#0a0e1a', height=320, margin=dict(t=40, b=20))
            st.plotly_chart(fig, use_container_width=True)

        with cat_col2:
            # Transactions over time
            df['ts'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('ts')
            df['cumulative_spend'] = df['amount_usdc'].cumsum()
            fig = px.line(df, x='ts', y='cumulative_spend', template='plotly_dark',
                          title='Cumulative Spend Over Time')
            fig.update_traces(line_color='#00d9a3', line_width=2)
            fig.update_layout(plot_bgcolor='#0a0e1a', paper_bgcolor='#0a0e1a', height=320,
                              xaxis_title='', yaxis_title='USDC', margin=dict(t=40, b=20))
            st.plotly_chart(fig, use_container_width=True)

        # Settlement time stats
        st.markdown("### Settlement Performance")
        s_col1, s_col2, s_col3, s_col4 = st.columns(4)
        with s_col1:
            st.metric("Avg Settlement", f"{df['settlement_time_ms'].mean():.0f}ms")
        with s_col2:
            st.metric("Min Settlement", f"{df['settlement_time_ms'].min()}ms")
        with s_col3:
            st.metric("Max Settlement", f"{df['settlement_time_ms'].max()}ms")
        with s_col4:
            total_gas = df['gas_used_usdc'].sum()
            st.metric("Total Gas Cost", f"${total_gas:.5f}")

# Footer
st.markdown("""
<div class='footer'>
    🤖 AgentPay AI · Built by Nakul Shriman Karthikeyan · 
    <a href='https://linkedin.com/in/shriman-nakul' target='_blank'>LinkedIn</a> · 
    <a href='https://nakul532.github.io' target='_blank'>Portfolio</a> · 
    <a href='https://github.com/Nakul532' target='_blank'>GitHub</a>
</div>
""", unsafe_allow_html=True)
