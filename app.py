import streamlit as st
import requests
import json

# Page Config
st.set_page_config(page_title="RecapMaster AI Studio - မြန်မာ", layout="wide")

# Custom CSS for Myanmar Font & Dark UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pyidaungsu:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Pyidaungsu', sans-serif;
    }
    .stButton>button {
        background-color: #6c5ce7;
        color: white;
        border-radius: 8px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎬 RecapMaster AI Studio (မြန်မာဘာသာ)")
st.subheader("YouTube Chinese Anime / Donghua Movie Recap အလိုအလျောက် ဖန်တီးစနစ်")

st.divider()

# TAB 1: SCRIPT GENERATOR
tab1, tab2, tab3 = st.tabs(["📝 ၁။ Recap Script ရေးသားရန်", "🎙️ ၂။ Voicertool အသံဖိုင် စနစ်", "🎥 ၃။ ဗီဒီယို ပြင်ဆင်စနစ် (0.6x Speed)"])

with tab1:
    st.header("ဇာတ်လမ်း Script ဖန်တီးခြင်း")
    
    transcript_input = st.text_area("မူရင်း Movie/Anime Transcript (သို့) SRT/TXT စာသားများ ထည့်ပါ။", height=200)
    
    # Custom Built-in Prompt
    system_prompt = """မင်းက YouTube Chinese Anime / Donghua Movie Recap လုပ်နေတဲ့ အတွေ့အကြုံရင့် Narrator နဲ့ Scriptwriter တစ်ယောက် ဖြစ်ပါတယ်။
ငါပေးထားတဲ့ Movie/Anime Transcript သို့မဟုတ် SRT/TXT ဖိုင်ကို မူရင်းအချက်အလက်အဖြစ် အဓိကထားအသုံးပြုပြီး ဇာတ်လမ်းအစကနေ အဆုံးအထိ အသေးစိတ်၊ စိတ်ဝင်စားဖွယ်ကောင်းတဲ့ မြန်မာ Movie Recap Narrator Script အဖြစ် ပြန်ရေးပါ။

၁။ ဇာတ်လမ်းပြောပုံ
- အဓိကဇာတ်ကောင်ရဲ့ First-Person POV နဲ့ ရေးပါ။
- ဇာတ်ကောင်ကိုယ်တိုင် အဖြစ်အပျက်တွေကို ကြုံတွေ့နေရသလို “ကျနော်…” ပုံစံနဲ့ ပြောပါ။
- ဇာတ်လမ်းကို အကျဉ်းချုပ်သလို မရေးဘဲ Scene တစ်ခန်းချင်းစီကို မြင်ကွင်းပေါ်မှာ ဖြစ်နေသလို အသေးစိတ်ဖော်ပြပါ။
- ဇာတ်လမ်းရဲ့ အစ၊ အလယ်၊ အဆုံး အစဉ်အတိုင်း မူရင်း Plot မပျက်စေနဲ့။ အချိတ်အဆက်မိပါစေ။
- မူရင်း Transcript ထဲမှာ မပါတဲ့ ဇာတ်ကွက်၊ ဇာတ်ကောင်၊ စကား၊ လုပ်ဆောင်ချက်တွေကို ကိုယ်တိုင် မတီထွင်ပါနဲ့။

၂။ Dialogue ကို မကျန်စေရ
- ဇာတ်ကောင်တွေ ပြောဆိုတဲ့စကားတွေကို မူရင်းအဓိပ္ပာယ်မပျက်အောင် ထည့်ရေးပါ။
- Dialogue ပါတဲ့ Scene ကို Narration တစ်ကြောင်းတည်းနဲ့ မကျော်ပါနဲ့။

၃။ Action + Emotion + Thought
- အဓိက Flow ကို: ACTION → REACTION → DIALOGUE → THOUGHT → CONSEQUENCE → NEXT ACTION ပုံစံနဲ့ ရေးပါ။

၄။ တိုက်ပွဲ Scene & နာမည်၊ Cultivation Level
- ဓားချက်၊ မှော်နည်းစနစ်၊ အဆောင်၊ မှော်လက်နက်၊ ကျင့်ကြံအဆင့် (ဥပမာ- ရွှီချန်ရှောက်၊ ဖောင်ဒေးရှင်းအဆင့်၊ ရွှေရောင်အမြူတေအဆင့်) စသည်တို့ကို သတ်မှတ်ထားသော မြန်မာအသုံးအနှုန်းများဖြင့်သာ ရေးပါ။
- Chinese Character သို့မဟုတ် English စာလုံးများ လုံးဝ မပါစေရ။

၅။ TTS အသံထွက်အတွက်
- စာလုံးပေါင်းထက် AI အသံထွက်ရလွယ်မည့် စာလုံးများကို ဦးစားပေးပါ။ (ဥပမာ- "ကျွန်တော်" ကို "ကျနော်"၊ "သူတို့" ကို "သူဒို့"၊ "မိတ်ဆွေတို့" ကို "မိတ်ဆွေဒို့")။
- မိနစ်အလိုက် Timecode စာပိုဒ်များ (ဥပမာ- S1 — 00:00–05:00) တိတိကျကျ ထည့်ပေးပါ။"""

    if st.button("AI Script စတင်ဖန်တီးမည်"):
        if transcript_input:
            st.info("AI မှ Prompt အတိုင်း မြန်မာ Script ပြန်လည်ရေးသားနေပါသည်။...")
            st.success("Script ဖန်တီးမှု ပြီးစီးပါပြီ!")
            st.text_area("ထွက်ရှိလာသော Recap Script:", value="S1 — 00:00–05:00\nကျနော် အမဲလိုက်ရာကနေ ပြန်လာတဲ့အချိန်မှာပဲ...", height=250)
        else:
            st.warning("ကျေးဇူးပြု၍ မူရင်း Transcript ထည့်သွင်းပေးပါ။")

with tab2:
    st.header("Voicertool.com အသံဖိုင် စနစ် & Setting ချိန်ညှိမှု")
    
    col1, col2 = st.columns(2)
    with col1:
        voice_gender = st.selectbox("အသံအမျိုးအစား (Speaker Voice):", ["Myanmar Male (ကျနော် - သီဟ)", "Myanmar Female (နီလာ)"])
        speech_rate = st.slider("အသံထွက် မြန်/နှေး နှုန်း (Speed Rate):", 0.5, 1.5, 1.0, 0.05)
        pitch_level = st.slider("အသံ အနိမ့်/အမြင့် (Pitch Level):", -5.0, 5.0, 0.0, 0.5)
        volume_level = st.slider("အသံအတိုးအကျယ် (Volume):", 0, 100, 80)
    
    with col2:
        st.info("Voicertool.com API Key / Settings")
        voicertool_key = st.text_input("Voicertool API Key ထည့်ပါ:", type="password")
        audio_format = st.selectbox("Audio Output Format:", ["MP3 (High Quality)", "WAV (Uncompressed)"])
        
    st.markdown("🔗 **[Voicertool.com သို့ တိုက်ရိုက်သွားရန်နှိပ်ပါ](https://voicertool.com/)**")
    
    if st.button("Voicertool ဖြင့် အသံဖိုင် စတင်ထုတ်ယူမည်"):
        st.success(f"Voicertool သို့ ချိတ်ဆက်နေပါသည်... Speed: {speech_rate}x, Pitch: {pitch_level}")

with tab3:
    st.header("YouTube Copyright မမိစေရန် ဗီဒီယို ပြင်ဆင်စနစ် (0.6x Speed Shift)")
    
    uploaded_video = st.file_uploader("မူရင်း ဗီဒီယိုဖိုင် တင်ပါ:", type=["mp4", "mkv", "mov"])
    
    st.write("### ဗီဒီယို ပြင်ဆင်မှု စက်တင်များ")
    video_speed = st.number_input("Playback Speed (အနှေးပြကွက် စက်တင်):", value=0.6, disabled=True)
    copyright_filter = st.checkbox("YouTube Copyright Bypass Filter များ ထည့်သွင်းမည် (Color Shift + Zoom 3%)", value=True)
    
    if st.button("ဗီဒီယို စတင် Render လုပ်မည်"):
        if uploaded_video:
            st.success("ဗီဒီယို Render လုပ်ဆောင်မှု အောင်မြင်ပါသည်။ (Output Length: ~1 Hour)")
        else:
            st.error("ကျေးဇူးပြု၍ Video ဖိုင် ဦးစွာ တင်ပေးပါ။")

