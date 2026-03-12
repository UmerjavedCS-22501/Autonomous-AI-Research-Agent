import streamlit as st
import time

from agents.researcher import resercher
from agents.writer import writer
from agents.critic import critic
from agents.improver import improver

# Set page config for a professional look
st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for a professional, responsive, modern look
st.markdown("""
<style>
    /* Main background & fonts */
    .stApp {
        background-color: #0f111a;
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #ffffff;
        font-weight: 700;
    }
    
    /* Text input styling */
    .stTextInput > div > div > input {
        background-color: #1e2130;
        color: #fff;
        border-radius: 8px;
        border: 1px solid #33384f;
        padding: 12px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 1px #6366f1;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #151823;
    }
    
    /* Report Container */
    .report-container {
        background-color: #1e2130;
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #33384f;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        margin-top: 1rem;
    }
    
    /* Metrics / Score Card */
    .metric-card {
        background-color: #1e2130;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #33384f;
        text-align: center;
    }
    .score-value {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(to right, #10b981, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# Title & Description
st.title("🧠 Autonomous AI Research Agent")
st.markdown("Enter a topic below to receive a high-quality, comprehensive research report.")

# Main layout
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### Configuration")
    topic = st.text_input("Research Topic", placeholder="e.g. Quantum Computing Applications", label_visibility="collapsed")
    run_btn = st.button("Generate Report", type="primary")
    
    # Placeholder for metrics
    metrics_placeholder = st.empty()
    status_placeholder = st.empty()

with col2:
    report_heading_placeholder = st.empty()
    report_heading_placeholder.markdown("### Live Report")
    report_placeholder = st.empty()
    
    if not topic and not run_btn:
        report_placeholder.info("Enter a topic and click 'Generate Report' to start.")

if run_btn and topic:
    # State reset
    state = {"topic": topic}
    
    with status_placeholder.container():
        st.markdown("### Progress")
        
        # Step 1: Research
        with st.status("🔍 Researching...", expanded=True) as status:
            st.write(f"Searching web for: **{topic}**")
            state.update(resercher(state))
            status.update(label="✅ Found research sources!", state="complete", expanded=False)
            metrics_placeholder.markdown("""
                <div class="metric-card">
                    <p style='color: #94a3b8; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;'>Status</p>
                    <h3 style='color: #60a5fa;'>Pipeline Running...</h3>
                </div>
            """, unsafe_allow_html=True)
            
            # Step 2: Write
            status.update(label="✍️ Drafting Initial Report...", state="running", expanded=True)
            st.write("Synthesizing information into a structured report...")
            state.update(writer(state))
            report_placeholder.markdown(f"<div class='report-container'>{state['report']}</div>", unsafe_allow_html=True)
            status.update(label="✅ Initial Draft Complete!", state="complete", expanded=False)
            
            # Iteration Loop
            iteration = 0
            score_history = []
            while True:
                iteration += 1
                
                # Step 3: Critic evaluates
                status.update(label=f"🧐 Evaluating Draft (Pass {iteration})...", state="running", expanded=True)
                st.write("Scoring content depth, clarity, and formatting...")
                state.update(critic(state))
                
                score = state["score"]
                feedback = state["feedback"]
                score_history.append(score)
                
                # Show score history during loop
                history_text = " ➡️ ".join(map(str, score_history))
                metrics_placeholder.markdown(f"""
                    <div class="metric-card">
                        <p style='color: #94a3b8; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;'>Status</p>
                        <h3 style='color: #60a5fa;'>Refining Draft (Pass {iteration})</h3>
                        <p style='color: #cbd5e1; font-size: 0.85rem; margin-top: 0.5rem;'>Past Scores: {history_text}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                if score >= 9:
                    status.update(label="🎉 Report Meets Quality Standards!", state="complete", expanded=False)
                    break
                    
                # Step 4: Improve
                status.update(label=f"🔧 Improving Report based on feedback...", state="running", expanded=True)
                st.write(f"Applying feedback: {feedback}")
                state.update(improver(state))
                
                # Update live view
                report_placeholder.markdown(f"<div class='report-container'>{state['report']}</div>", unsafe_allow_html=True)
                time.sleep(1) # Small pause for UI effect
                
    st.balloons()
    st.success("Research Report Finalized!")
    report_heading_placeholder.markdown("### Final Result")
    
    # Show final score
    score_color = "#10b981" if score >= 9 else "#6366f1" if score >= 7 else "#f59e0b"
    history_html = f"<p style='color: #94a3b8; font-size: 0.8rem; margin-top: 0.5rem;'>Score progression: {' ➡️ '.join(map(str, score_history))}</p>" if len(score_history) > 1 else ""
    
    metrics_placeholder.markdown(f"""
        <div class="metric-card">
            <p style='color: #94a3b8; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;'>Final Quality Score</p>
            <div class="score-value" style="background: {score_color}; -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{score}/10</div>
            <p style='font-size: 0.85rem; color: #cbd5e1; margin-top: 0.5rem;'>{feedback}</p>
            {history_html}
        </div>
    """, unsafe_allow_html=True)
    
    # Download button for the report
    st.download_button(
        label="Download Full Report (Markdown)",
        data=state["report"],
        file_name=f"{topic.replace(' ', '_').lower()}_report.md",
        mime="text/markdown"
    )
