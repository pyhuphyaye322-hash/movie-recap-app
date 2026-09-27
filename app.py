import streamlit as st
import google.generativeai as genai
import asyncio
import edge_tts
import os

# Page Configuration
st.set_page_config(
    page_title="RecapMaster AI Studio Pro",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pyidaungsu:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Pyidaungsu', sans-serif; }
    .main { background-color: #0f172a; color: #f8fafc; }
    .header-box {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4c1d95 100%);
        padding: 24px; border-radius: 16px; border: 1px solid #6366f1; margin-bottom: 25px;
    }
    .header-title { color: #ffffff; font-size: 28px; font-weight: 700; }
    .header-subtitle { color: #cbd5e1; font-size: 15px; }
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%);
        color: white; border: none; border-radius: 12px; padding: 16px 28px;
        font-size: 18px; font-weight: 700; width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="header-box">
        <div class="header-title">🎬 RecapMaster AI Studio Pro</div>
        <div class="header-subtitle">Donghua / Movie Recap Script & Burmese Voiceover (MP3) Generator</div>
    </div>
""", unsafe_allow_html=True)

# Async Function for Edge-TTS
async def generate_voice(text, voice_name, output_filename):
    communicate = edge_tts.Communicate(text, voice_name)
    await communicate.save(output_filename)

# Sidebar
with st.sidebar:
    st.title("⚙️ စနစ် ဆက်တင်များ")
    gemini_key = st.text_input("🔑 Gemini AI API Key ထည့်ပါ:", type="password", placeholder="AIzaSy...")
    
    st.divider()
    st.subheader("🎙️ Voice & TTS ဆက်တင်")
    voice_choice = st.selectbox(
        "အသံအမျိုးအစား ရွေးချယ်ပါ:",
        [
            "my-MM-ThihaNeural (မြန်မာ အမျိုးသားအသံ)",
            "my-MM-NilarNeural (မြန်မာ အမျိုးသမီးအသံ)"
        ]
    )

# System Prompt Formulation
SYSTEM_PROMPT = """မင်းက YouTube Chinese Anime / Donghua Movie Recap လုပ်နေတဲ့ အတွေ့အကြုံရင့် Narrator နဲ့ Scriptwriter တစ်ယောက် ဖြစ်ပါတယ်။
ပေးထားတဲ့ Movie/Anime Transcript ကို အဓိကထားပြီး အောက်ပါ စည်းမျဉ်းများအတိုင်း မြန်မာ Movie Recap Narrator Script ပြန်ရေးပါ-

၁။ First-Person POV (“ကျနော်…”) နဲ့ ရေးပါ။ Scene အသေးစိတ်ဖော်ပြပါ။
၂။ Dialogue များ မကျန်စေရ။ Action + Emotion + Thought (ACTION → REACTION → DIALOGUE → THOUGHT → CONSEQUENCE) Flow အတိုင်း ရေးပါ။
၃။ Cultivation levels များ (ရွှီချန်ရှောက်, ဖောင်ဒေးရှင်းအဆင့် စသဖြင့်) မြန်မာလိုပဲ သုံးပါ (Chinese/English စာလုံး မပါစေရ)။
၄။ TTS ဖတ်ရလွယ်အောင် "ကျွန်တော်" ကို "ကျနော်"၊ "သူတို့" ကို "သူဒို့" စသဖြင့် အသံထွက် ဦးစားပေး ရေးပါ။
၅။ အပိုင်းများကို S1 — 00:00–05:00 စသဖြင့် ၅ မိနစ်စာ ခွဲပေးပါ။"""

# Main Form
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📥 မူရင်း Script / Transcript ထည့်ပါ")
    transcript_text = st.text_area("Transcript သို့မဟုတ် ဇာတ်လမ်းအကျဉ်းကို Paste လုပ်ထည့်ပါ:", height=250, placeholder="ဒီနေရာမှာ Chinese / English / Burmese Transcript များကို ထည့်ပါ...")

with col2:
    st.subheader("📝 အထူး ညွှန်ကြားချက်များ")
    custom_note = st.text_area("ဇာတ်ကောင် သို့မဟုတ် Cultivation level သတ်မှတ်ချက်များ:", placeholder="ဥပမာ- ရွှီချန်ရှောက် ကို အဓိကထား ရေးပေးပါ။")

st.divider()

if st.button("🚀 Auto Recap Script & Audio ကို စတင် ဖန်တီးမည်"):
    if not transcript_text:
        st.error("⚠️ ကျေးဇူးပြု၍ Transcript စာသား ထည့်သွင်းပေးပါ။")
    elif not gemini_key:
        st.warning("🔑 ကျေးဇူးပြု၍ Sidebar တွင် Gemini API Key ထည့်ပါ။")
    else:
        try:
            with st.status("🎬 Recap ဖန်တီးနေပါသည်...", expanded=True) as status:
                st.write("🧠 Gemini AI ထံသို့ Prompt ပေးပို့၍ Script ရေးသားနေပါသည်...")
                
                # Gemini Configuration
                genai.configure(api_key=gemini_key)
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                full_prompt = f"{SYSTEM_PROMPT}\n\n[အထူးညွှန်ကြားချက်]: {custom_note}\n\n[Transcript]:\n{transcript_text}"
                response = model.generate_content(full_prompt)
                script_result = response.text
                
                st.write("🎙️ မြန်မာ AI အသံထွက် (.mp3) ဖန်တီးနေပါသည်...")
                
                # Generate MP3 Audio
                selected_voice = voice_choice.split(" ")[0]
                audio_file = "recap_voiceover.mp3"
                asyncio.run(generate_voice(script_result, selected_voice, audio_file))
                
                status.update(label="🎉 Recap Script နှင့် Audio အောင်မြင်စွာ ထွက်ရှိပါပြီ!", state="complete")

            st.subheader("📜 ထွက်ရှိလာသော Donghua Movie Recap Script")
            st.text_area("Script Result:", value=script_result, height=300)
            
            st.subheader("🎧 ထွက်ရှိလာသော မြန်မာ Voiceover (MP3)")
            if os.path.exists(audio_file):
                with open(audio_file, "rb") as f:
                    st.audio(f.read(), format="audio/mp3")
                    st.download_button("📥 Voiceover (.mp3) ဒေါင်းလုဒ်ရယူရန်", f, file_name="recap_voice.mp3", mime="audio/mp3")

        except Exception as e:
            st.error(f"❌ Error တစ်ခုခု ဖြစ်ပွားခဲ့သည်: {str(e)}")
            
