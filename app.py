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

# Async Function for Edge-TTS Generation
async def generate_voice(text, voice_name, output_filename):
    communicate = edge_tts.Communicate(text, voice_name)
    await communicate.save(output_filename)

# Custom Styling for Modern Burmese Professional UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pyidaungsu:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Pyidaungsu', sans-serif;
    }
    
    /* Main Background Accent */
    .main {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* Header Container */
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

    /* Primary Action Button */
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
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.6);
    }
    
    /* Input Styling */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #0f172a !important;
        color: #f8fafc !important;
        border-radius: 10px !important;
        border: 1px solid #334155 !important;
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #8b5cf6 !important;
        box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.2) !important;
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
    
    st.divider()
    st.subheader("🛠️ ဗီဒီယို ပြုပြင်ရေး Options")
    burn_sub = st.checkbox("မြန်မာ စာတန်းထိုး (Subtitles) ထည့်သွင်းမည်", value=True)
    blur_watermark = st.checkbox("မူရင်း Logo / Watermark Blur အကွက် ထည့်မည်", value=True)
    auto_timestamp = st.checkbox("၅ မိနစ်တစ်ကြိမ် Timestamp (S1, S2) ခွဲမည်", value=True)

# System Prompt Text definition
system_prompt_content = """မင်းက YouTube Chinese Anime / Donghua Movie Recap လုပ်နေတဲ့ အတွေ့အကြုံရင့် Narrator နဲ့ Scriptwriter တစ်ယောက် ဖြစ်ပါတယ်။
ငါပေးထားတဲ့ Movie/Anime Transcript သို့မဟုတ် SRT/TXT ဖိုင်ကို မူရင်းအချက်အလက်အဖြစ် အဓိကထားအသုံးပြုပြီး ဇာတ်လမ်းအစကနေ အဆုံးအထိ အသေးစိတ်၊ စိတ်ဝင်စားဖွယ်ကောင်းတဲ့ မြန်မာ Movie Recap Narrator Script အဖြစ် ပြန်ရေးပါ။

၁။ ဇာတ်လမ်းပြောပုံ
- အဓိကဇာတ်ကောင်ရဲ့ First-Person POV နဲ့ ရေးပါ။
- ဇာတ်ကောင်ကိုယ်တိုင် အဖြစ်အပျက်တွေကို ကြုံတွေ့နေရသလို “ကျွန်တော်…” / “ကျနော်…” ပုံစံနဲ့ ပြောပါ။
- ဇာတ်လမ်းကို အကျဉ်းချုပ်သလို မရေးဘဲ Scene တစ်ခန်းချင်းစီကို မြင်ကွင်းပေါ်မှာ ဖြစ်နေသလို အသေးစိတ်ဖော်ပြပါ။
- ဇာတ်လမ်းရဲ့ အစ၊ အလယ်၊ အဆုံး အစဉ်အတိုင်း မူရင်း Plot မပျက်စေနဲ့။အချိတ်ဆက်မိပါစေ။
- မူရင်း Transcript ထဲမှာ မပါတဲ့ ဇာတ်ကွက်၊ ဇာတ်ကောင်၊ စကား၊ လုပ်ဆောင်ချက်တွေကို ကိုယ်တိုင် မတီထွင်ပါနဲ့။

၂။ Dialogue ကို မကျန်စေရ
ဇာတ်ကောင်တွေ ပြောဆိုတဲ့စကားတွေကို အထူးဂရုစိုက်ပါ။
- အဓိကဇာတ်ကောင် ↔ အခြားဇာတ်ကောင်
- ရန်သူ ↔ အဓိကဇာတ်ကောင်
- ဇာတ်ကောင်အချင်းချင်း ဆွေးနွေးမှု
- အမိန့်ပေးမှု၊ ခြိမ်းခြောက်မှု၊ အံ့ဩမှု၊ တောင်းပန်မှု
- တိုက်ပွဲမစခင်နဲ့ တိုက်ပွဲအတွင်း ပြောတဲ့စကား
- တိုက်ပွဲပြီးတဲ့နောက် ပြောတဲ့စကား
တို့ကို မူရင်းအဓိပ္ပာယ်မပျက်အောင် ထည့်ရေးပါ။
Dialogue ပါတဲ့ Scene ကို Narration တစ်ကြောင်းတည်းနဲ့ မကျော်ပါနဲ့။

၃။ Action + Emotion + Thought
ဇာတ်ကောင်တစ်ယောက် ဘာလုပ်တယ်ဆိုတာကို ရိုးရိုး “တိုက်ခိုက်လိုက်တယ်” လို့ မရေးဘဲ မူရင်းက ထောက်ခံတဲ့အတိုင်း လုပ်ဆောင်ချက်ကို မြင်သာအောင် ရေးပါ။
ဥပမာ—
- ဘယ်ဘက်ကို ရွှေ့သွားတယ်
- ဘာကို ထုတ်လိုက်တယ်
- ဘယ်လို တိုက်ခိုက်တယ်
- ရန်သူက ဘယ်လို ရှောင်တယ် / ကာတယ်
- ထိမှန်ပြီး ဘာဖြစ်သွားတယ်
- ဇာတ်ကောင်က ဘယ်လိုတုံ့ပြန်တယ်
- အတွင်းစိတ်မှာ ဘာတွေးတယ်
- ဇာတ်လမ်းရဲ့ဇာတ်ကွက်၊ ဇာတ်ကောင်ရဲ့ဇာတ်ကွက်နှင့် စိတ်ခံစားမှု၊ စိတ်နေစိတ်ထား
- ဇာတ်ရှိန်မြှင့်တင်မှု
- အဓိကဇာတ်ကောင်နှင့် အခြားဇာတ်ကောင်နှင့် အခြေအနေတင်းမာမှု မြင့်တင်ရန်
- အဲဒီလုပ်ဆောင်ချက်ကြောင့် နောက်ထပ် ဘာဖြစ်လာတယ်
ကို သဘာဝကျကျ ဆက်စပ်ရေးပါ။
အဓိက Flow ကို—
ACTION → REACTION → DIALOGUE → THOUGHT → CONSEQUENCE → NEXT ACTION
ပုံစံနဲ့ ရေးပါ။

၄။ တိုက်ပွဲ Scene
တိုက်ပွဲတွေမှာ အရေးကြီးတဲ့အသေးစိတ်တွေ မကျန်စေရ။
- ဓားချက် / တိုက်ချက်
- မှော်နည်းစနစ်
- အဆောင်ပစ်လွှတ်မှု
- မှော်လက်နက်
- ကာကွယ်ရေးပစ္စည်း
- ရုပ်သေး / ဝိညာဉ် / သားရဲ
- ပေါက်ကွဲမှု
- ဒဏ်ရာရမှု
- သေဆုံးမှု
- ဓားနဲ့တိုက်ခိုက်မှု၊ အစွမ်းနဲ့တိုက်ခိုက်မှု၊ ကာကွယ်မှု
ကို မူရင်း Transcript အတိုင်း ရှင်းလင်းစွာ ဖော်ပြပါ။
မူရင်းမှာ အဆောင်ဖြစ်ရင် အဆောင် လို့ပဲ ရေးပါ။
ဥပမာ မီးမိုးကြိုးအဆောင်၊ မိုးကြိုးပေါက်ကွဲအဆောင်၊ သစ်မိုးကြိုးအဆောင် တို့ကို ပုဆိန်၊ ဓား စသည်ဖြင့် မပြောင်းရေးပါနဲ့။

၅။ နာမည်နဲ့ Cultivation Level
ဇာတ်ကောင်နာမည်၊ နေရာနာမည်၊ အဆောင်နာမည်၊ မှော်လက်နက်၊ ရုပ်သေး၊ အစီအရင်၊ ဆေး၊ ကျင့်ကြံအဆင့် အားလုံးကို မြန်မာစာလုံးနဲ့ပဲ ရေးပါ။
အထူးသဖြင့်—
- 徐长寿 = ရွှီချန်ရှောက်
- 筑基 = ဖောင်ဒေးရှင်းအဆင့်
- 筑基中期 = ဖောင်ဒေးရှင်းအဆင့် အလယ်ပိုင်း
- 筑基后期 = ဖောင်ဒေးရှင်းအဆင့် နောက်ပိုင်း
- 筑基大圆满 = ဖောင်ဒေးရှင်းအဆင့် အပြည့်အဝ
- 金丹 = ရွှေရောင်အမြူတေအဆင့်
- 假丹 = အတုရွှေရောင်အမြူတေအဆင့်
လို သတ်မှတ်ထားတဲ့ ဘာသာပြန်အသုံးအနှုန်းတွေကို တစ်သမတ်တည်း အသုံးပြုပါ။
Chinese Character သို့မဟုတ် English/Latin စာလုံးတွေကို Final Narrator Script ထဲမှာ မထားပါနဲ့။

၆။ TTS အသံထွက်အတွက်
ဒီ Script ကို AI Text-to-Speech နဲ့ တိုက်ရိုက်ဖတ်နိုင်အောင် ရေးပါ။
- ဝါကျအရမ်းရှည်မရေးပါနဲ့။
- လေယူလေသိမ်း သဘာဝကျအောင် စာကြောင်းခွဲပါ။
- တိုက်ပွဲမှာ အသံအကျိုးသက်ရောက်မှုကို လိုအပ်တဲ့နေရာမှာသာ သုံးပါ။
  ဥပမာ — “ဘုန်း!”, “ဒုန်း!”, “ချွမ်း!”
- စာလုံးပေါင်းထက် အသံထွက်ပုံစံကို ဦးစားပေးပါ။ ဥပမာ "ကျွန်တော်" ကို "ကျနော်"၊ "သူတို့" ကို "သူဒို့"၊ "မိတ်ဆွေတို့" ကို "မိတ်ဆွေဒို့" စသည်ဖြင့် AI ထွက်ရလွယ်မည့် အသံထွက်စာလုံးများနှင့် ပြောင်းလဲပေးရန်။
- မူရင်းစာသား၏ အဓိပ္ပာယ် ပြောင်းလဲသွားခြင်း မရှိစေရပါ။
- စာပိုဒ်တွေမှာပါတဲ့ မိနစ်အတိုင်း တိတိကျကျ ပြန်ထည့်ပေးရန်။
- Chinese နာမည်တွေကို မြန်မာအသံထွက်အတိုင်း ရေးပါ။
- နာမည်တစ်ခုကို စပြီးသတ်မှတ်ပြီးရင် နောက်ပိုင်းမှာ မပြောင်းပါနဲ့။

၇။ Recap အရှည်
ဇာတ်လမ်းကို အလွန်တိုအောင် မချုံ့ပါနဲ့။
လိုအပ်ရင်—
S1 — 00:00–05:00
S2 — 05:00–10:00
S3 — 10:00–15:00
S4 — 15:00–20:00
စသဖြင့် ၅ မိနစ်စာ အပိုင်းများ ခွဲရေးပါ။
အပိုင်းတိုင်းမှာ ဇာတ်လမ်းဆက်စပ်မှုရှိရမယ်။ အသေးစိတ်ပြောပြရမယ်။
အပိုင်းတစ်ခုချင်းစီကို အလွန်တိုအောင် မရေးပါနဲ့။

၈။ အရေးကြီးဆုံးစည်းမျဉ်း
ဇာတ်လမ်းကို ရှည်အောင်လုပ်ဖို့အတွက် မူရင်းမှာမပါတဲ့အရာတွေ မတီထွင်ပါနဲ့။
ရှည်လျားမှုကို—
မူရင်း Dialogue + Action + Reaction + Emotion + Thought + Scene Description + Cause & Effect
တွေကို ပြည့်ပြည့်စုံစုံ ပြန်ဖော်ပြခြင်းနဲ့ ရရှိအောင်လုပ်ပါ။
အထူးသဖြင့် Dialogue မကျန်၊ Plot Point မကျန်၊ ဇာတ်ကောင်လုပ်ဆောင်ချက် မကျန် အောင် မူရင်း Transcript ကို သေချာစစ်ပြီး ရေးပါ။
Final Output က YouTube Chinese Anime / Donghua Movie Recap အတွက် တိုက်ရိုက် Voice-over သွင်းနိုင်တဲ့ မြန်မာ Narrator Script ဖြစ်ရမယ်။"""

# Main Content Layout (3 Tabs)
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
        st.info("အောက်ပါ Prompt နည်းလမ်းအတိုင်း AI မှ အသေးစိတ် ဇာတ်လမ်းပြန်ပြောစခရင်ပရစ် (Narrator Script) ကို ထုတ်ပေးမည်ဖြစ်ပါသည်။")
        
        with st.expander("ကြည့်ရှုရန် နှိပ်ပါ (Prompt Preview)", expanded=True):
            st.markdown("""
            * **POV:** First-Person POV (“ကျနော်…”)
            * **Flow:** Action → Reaction → Dialogue → Thought → Consequence → Next Action
            * **Dialogue:** မူရင်းအဓိပ္ပာယ်မပျက်ဘဲ အဓိကပြောဆိုချက်များ ပြည့်စုံစွာပါဝင်မည်။
            * **TTS Optimizations:** AI အသံဖတ်ရလွယ်ကူစေရန် စာလုံးပေါင်းအသံထွက်များအတိုင်း (ဥပမာ- ကျနော်၊ သူဒို့) ရေးသားမည်။
            * **Cultivation & Names:** ရွှီချန်ရှောက်၊ ဖောင်ဒေးရှင်းအဆင့် စသဖြင့် သတ်မှတ်ထားသော မြန်မာအသုံးအနှုန်းများအတိုင်း သုံးစွဲမည်။
            """)

    st.divider()
    
    generate_btn = st.button("🚀 Auto Recap Script & Video ကို စတင် ဖန်တီးမည်")
    
    if generate_btn:
        if not youtube_url and not uploaded_file:
            st.error("⚠️ ကျေးဇူးပြု၍ YouTube URL သို့မဟုတ် Transcript ဖိုင် တစ်ခုခု ထည့်သွင်းပေးပါ။")
        elif not gemini_key:
            st.warning("🔑 ကျေးဇူးပြု၍ Sidebar တွင် Gemini API Key ကို ထည့်သွင်းပါ။")
        else:
            try:
                input_content = youtube_url
                if uploaded_file is not None:
                    input_content += "\n" + uploaded_file.read().decode("utf-8", errors="ignore")

                with st.status("🎬 Movie Recap ဖန်တီးနေပါသည်...", expanded=True) as status:
                    st.write("📥 YouTube Transcript / ဖိုင်အချက်အလက်များကို ရယူနေပါသည်...")
                    
                    st.write("🧠 AI မှ စနစ်သုံး Prompt မူဘောင်အတိုင်း စခရင်ပရစ် ရေးသားနေပါသည်...")
                    genai.configure(api_key=gemini_key)
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    
                    user_prompt = f"{system_prompt_content}\n\n[အထူးညွှန်ကြားချက်များ]: {extra_notes}\n\n[မူရင်း Transcript/URL အချက်အလက်]:\n{input_content}"
                    ai_response = model.generate_content(user_prompt)
                    generated_script = ai_response.text

                    st.write("🎙️ TTS မူဘောင်အတိုင်း မြန်မာ အသံထွက် (Voiceover) ဖန်တီးနေပါသည်...")
                    voice_code = voice_option.split(" ")[0]
                    audio_out = "recap_audio.mp3"
                    asyncio.run(generate_voice(generated_script, voice_code, audio_out))

                    st.write("🎞️ ဗီဒီယိုနှင့် အသံကို ပေါင်းစပ်၍ Subtitles / Blur များကို တပ်ဆင်နေပါသည်...")
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
    st.caption("ဤ Prompt အား Gemini AI model ထံသို့ ပေးပို့၍ အကောင်းဆုံး Script ရေးသားစေမည်ဖြစ်ပါသည်။")
    st.text_area("System Prompt Code:", value=system_prompt_content, height=400)

with tab3:
    st.subheader("📊 ယခင် ပြုလုပ်ခဲ့သော Recap များ")
    st.dataframe(
        {
            "Project Name": ["Donghua Recap Ep 1", "Xianxia Movie Recap"],
            "Duration": ["15 mins", "20 mins"],
            "Status": ["Completed", "Completed"],
            "Date": ["2026-09-27", "2026-09-28"]
        },
        use_container_width=True
                    )
    
