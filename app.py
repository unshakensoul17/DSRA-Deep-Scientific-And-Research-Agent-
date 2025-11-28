import streamlit as st
from core.retriever import Retriever
from core.synthesizer import Synthesizer
from core.dashboard import DashboardGenerator

st.title("🔍 DRSA — Deep Research & Synthesis Agent")

topic = st.text_input("Enter research topic")

if st.button("Generate Report"):
    retriever = Retriever()
    results = retriever.fetch_all_sources(topic)

    synthesizer = Synthesizer()
    report = synthesizer.synthesize_report(topic, results)
    
    st.subheader("📄 Summary")
    st.write(report["summary"])

    st.subheader("🔍 Key Findings")
    for point in report["key_findings"]:
        st.write("•", point)

if st.button("Build Dashboard"):
    dash = DashboardGenerator()
    dash.build_dashboard()
    st.success("Dashboard created → Check data/outputs/")
