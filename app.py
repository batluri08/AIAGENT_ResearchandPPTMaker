import streamlit as st
from agent1_research import research_and_summarize
from agent2_organizer import organize_ppt, generate_pptx
import requests
from streamlit_lottie import st_lottie
import base64

# --- Load Lottie animations ---
def load_lottie_url(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

lottie_ai = load_lottie_url("https://lottie.host/660c5dc5-f70d-4a3c-83ad-3a9d0dc5198e/b1YuCBBK1P.json")
lottie_slide = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_47pyyfcg.json")

st.set_page_config(page_title="AI Agents Playground", page_icon="🤖", layout="centered")

st.title("🤖 AI Agents Collaboration Playground")
st.markdown("""
### 🔍 How this app works:
1️⃣ **Fetch & Summarize** a topic using real-time search & AI summarization.  
2️⃣ **Generate a PowerPoint outline** with the number of slides you choose.  
3️⃣ **Download** the final `.pptx` file!

---
""")

if lottie_ai:
    st_lottie(lottie_ai, height=200, key="ai_agent")

# --- User inputs ---
st.subheader("🎯 Let’s Get Started!")
topic = st.text_input("🔎 Enter a research topic:", placeholder="e.g., Indus Valley Civilization")
num_slides = st.slider("🖼️ How many slides would you like?", 3, 10, 5)

# Session state to track progress
if "step" not in st.session_state:
    st.session_state.step = 1

# --- Step 1: Fetch Summary ---
if st.session_state.step == 1:
    if st.button("🚀 Fetch & Summarize (Agent 1)"):
        if topic:
            result = research_and_summarize(topic)
            st.session_state.summary = result
            st.session_state.step = 2
            st.success("✅ Research summary created and stored!")
            st.markdown("### 📝 Here's the summary:")
            st.info(result)
        else:
            st.warning("⚠️ Please enter a topic.")

# --- Step 2: Generate PPT Outline ---
if st.session_state.step >= 2:
    if st.session_state.step == 2:
        st.success("✅ Summary fetched! Now generate your PowerPoint outline.")
        if st.button("🎨 Generate PowerPoint Outline (Agent 2)"):
            ppt_outline = organize_ppt(topic, num_slides)
            st.session_state.ppt_outline = ppt_outline
            st.session_state.step = 3
            if lottie_slide:
                st_lottie(lottie_slide, height=150, key="ppt_outline")
            st.markdown("### 🎥 Here's your presentation outline:")
            st.markdown(ppt_outline)

# --- Step 3: Download PPTX ---
if st.session_state.step == 3:
    st.success("✅ PowerPoint outline created and ready to download.")
    if st.button("💾 Download PowerPoint File"):
        pptx_path = generate_pptx(topic, num_slides)
        if pptx_path:
            with open(pptx_path, "rb") as f:
                pptx_data = f.read()
            b64 = base64.b64encode(pptx_data).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="{topic}.pptx">📥 Download {topic} Presentation</a>'
            st.markdown(href, unsafe_allow_html=True)
        else:
            st.warning("⚠️ No summary found to generate a presentation.")

st.markdown("---")