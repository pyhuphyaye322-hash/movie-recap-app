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

# Safe Async Function for Streamlit Cloud Loop
def generate_voice_sync(text, voice_name, output_filename):
    async def _generate():
        communicate = edge_tts.Communicate(text, voice_name)
        await communicate.save(output_filename)
    
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import nest_asyncio
            nest_asyncio.apply()
            loop.run_until_complete(_generate())
        else:
            loop.run_until_complete(_generate())
    except Exception:
        asyncio.run(_generate())

# Custom Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pyidaungsu:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Pyidaungsu', sans-serif;
    }
    
    .main {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    .header-box {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4c1d95 100%);
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #6366f1;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.3);
    }
    
    .header-title {
        color: #ffffff;
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    
    .header-subtitle {
        color: #cbd5e1;
        font-size: 15px;
    }

    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 16px 28px;
        font-size: 18px;
        font-weight: 700;
        width: 100%;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #0f172a !important;
        color: #f8fafc !important;
        border-radius: 10px !important;
        border: 1px solid #334155 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
    <div class="header-box">
        <div class="header-title">🎬 RecapMaster AI Studio Pro</div>
        <div class="header-subtitle">တရုတ် အန်နီမေးရှင်း (Donghua) / Movie Recap ဗီဒီယိုများနှင့် စခရင်ပရစ်များ သဘာဝကျကျ အလိုအလျောက် ဖန်တီးပေးသည့် စနစ်</div>
    </div>
""", unsafe_allow_html=True)

# Sidebar Options
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/movie-studio.png", width=64)
    st.title("⚙️ စနစ် ဆက်တင်များ")
    
    gemini_key = st.text_input("🔑 Gemini AI API Key ထည့်ပါ:", type="password", placeholder="AQ... သို့မဟုတ် AIzaSy...")
    
    st.divider()
    st.subheader("🎙️ Voice & TTS ဆက်တင်")
    voice_option = st.selectbox(
        "အသံအမျိုးအစား ရွေးချယ်ပါ:",
        [
            "my-MM-ThihaNeural (ကျနော် - First-Person Male Narrator)",
            "my-MM-NilarNeural (နီလာ - Burmese Female Narrator)"
        ]
    )
    
    tts_speed = st.slider("🔊 အသံဖတ်နှုန်း (Speech Speed):", 0.8, 1.5, 1.0, 0.05)

# System Prompt
system_prompt_content = """မင်းက YouTube Chinese Anime / Donghua Movie Recap လုပ်နေတဲ့ အတွေ့အကြုံရင့် Narrator နဲ့ Scriptwriter တစ်ယောက် ဖြစ်ပါတယ်။
ငါပေးထားတဲ့ Movie/Anime Transcript သို့မဟုတ် SRT/TXT ဖိုင်ကို မူရင်းအချက်အလက်အဖြစ် အဓိကထားအသုံးပြုပြီး ဇာတ်လမ်းအစကနေ အဆုံးအထိ အသေးစိတ်၊ စိတ်ဝင်စားဖွယ်ကောင်းတဲ့ မြန်မာ Movie Recap Narrator Script အဖြစ် ပြန်ရေးပါ။"""

# Main Content Layout
tab1, tab2, tab3 = st.tabs(["🚀 Auto Recap Generation", "📜 System Prompt Viewer", "📊 Project History"])

with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📥 1. မူရင်း ရင်းမြစ် ထည့်သွင်းပါ")
        youtube_url = st.text_input("🔗 YouTube Video URL သို့မဟုတ် Link:", placeholder="https://www.youtube.com/watch?v=...")
        uploaded_file = st.file_uploader("📂 Transcript / SRT / TXT ဖိုင် တင်ပါ (Optional):", type=["txt", "srt", "vtt"])
        
        st.subheader("📝 2. အထူး ညွှန်ကြားချက်များ (Optional)")
        extra_notes = st.text_area("ဇာတ်ကောင် သို့မဟုတ် Cultivation level များနှင့် ပတ်သက်၍ ထပ်မံဖြည့်စွက်ချင်သည်များ:", placeholder="ဥပမာ- ရွှီချန်ရှောက် ကို အဓိကထား၍ ရေးပေးပါ။")

    with col2:
        st.subheader("🎯 3. အသုံးပြုမည့် Prompt မူဘောင်")
        st.info("အောက်ပါ Prompt နည်းလမ်းအတိုင်း AI မှ အသေးစိတ် ဇာတ်လမ်းပြန်ပြောစခရင်ပရစ် ကို ထုတ်ပေးမည်ဖြစ်ပါသည်။")

    st.divider()
    
    generate_btn = st.button("🚀 Auto Recap Script & Video ကို စတင် ဖန်တီးမည်")
    
    if generate_btn:
        if not youtube_url and not uploaded_file:
            st.error("⚠️ ကျေးဇူးပြု၍ YouTube URL သို့မဟုတ် Transcript ဖိုင် တစ်ခုခု ထည့်သွင်းပေးပါ။")
        elif not gemini_key:
            st.warning("🔑 ကျေးဇူးပြု၍ Sidebar တွင် Gemini API Key ကို ထည့်သွင်းပါ။")
        else:
            try:
                input_content = youtube_url if youtube_url else ""
                if uploaded_file is not None:
                    input_content += "\n" + uploaded_file.read().decode("utf-8", errors="ignore")

                with st.status("🎬 Movie Recap ဖန်တီးနေပါသည်...", expanded=True) as status:
                    st.write("🧠 AI မှ စနစ်သုံး Prompt မူဘောင်အတိုင်း စခရင်ပရစ် ရေးသားနေပါသည်...")
                    genai.configure(api_key=gemini_key.strip())
                    
                    # Gemini Model Call
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    user_prompt = f"{system_prompt_content}\n\n[အထူးညွှန်ကြားချက်များ]: {extra_notes}\n\n[မူရင်း Transcript/URL အချက်အလက်]:\n{input_content}"
                    
                    ai_response = model.generate_content(user_prompt)
                    generated_script = ai_response.text

                    st.write("🎙️ TTS မူဘောင်အတိုင်း မြန်မာ အသံထွက် (Voiceover) ဖန်တီးနေပါသည်...")
                    voice_code = voice_option.split(" ")[0]
                    audio_out = "recap_audio.mp3"
                    
                    generate_voice_sync(generated_script, voice_code, audio_out)

                    status.update(label="🎉 Auto Movie Recap ဖန်တီးမှု အောင်မြင်စွာ ပြီးဆုံးပါပြီ!", state="complete", expanded=True)
                
                st.success("✨ သင်၏ Donghua Movie Recap Script နှင့် Voiceover အဆင်သင့်ဖြစ်ပါပြီ!")

                st.subheader("📜 ရရှိလာသော မြန်မာ Narrator Script")
                st.text_area("Final Script:", value=generated_script, height=300)

                st.subheader("🎧 ရရှိလာသော မြန်မာ AI Voiceover (.mp3)")
                if os.path.exists(audio_out):
                    with open(audio_out, "rb") as audio_file:
                        st.audio(audio_file.read(), format="audio/mp3")
                        st.download_button("📥 Voiceover (.mp3) ဒေါင်းလုဒ်ဆွဲရန်", audio_file, file_name="recap_voiceover.mp3", mime="audio/mp3")

            except Exception as e:
                st.error(f"❌ Error တစ်ခုခု ဖြစ်ပွားခဲ့သည်: {str(e)}")

with tab2:
    st.subheader("📜 စနစ်တွင် ထည့်သွင်းထားသော System Prompt")
    st.text_area("System Prompt Code:", value=system_prompt_content, height=300)

with tab3:
    st.subheader("📊 ယခင် ပြုလုပ်ခဲ့သော Recap များ")
    st.dataframe({"Project Name": ["Donghua Recap Ep 1"], "Status": ["Completed"]})
    
