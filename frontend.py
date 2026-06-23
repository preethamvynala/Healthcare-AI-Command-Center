import os

# MUST come before whisper
os.environ["PATH"] += os.pathsep + r"D:\ffmpeg-8.1.1-essentials_build\ffmpeg-8.1.1-essentials_build\bin"


import streamlit as st
import requests
import plotly.express as px

from PIL import Image

from streamlit_option_menu import option_menu
from streamlit_chat import message
from streamlit_mic_recorder import mic_recorder

import tempfile
import whisper



API_URL = os.getenv(
    "BACKEND_URL",
    "https://healthcare-ai-backend-8gaa.onrender.com"
)



st.set_page_config(
    page_title="Healthcare AI Command Center",
    page_icon="🏥",
    layout="wide"
)



# =====================================================
# Whisper
# =====================================================

@st.cache_resource
def load_whisper_model():

    return whisper.load_model("base")


model = load_whisper_model()



# =====================================================
# Premium CSS
# =====================================================


st.markdown(
"""
<style>

.stApp{

background:
linear-gradient(
135deg,
#eef7ff,
#ffffff
);

}


.main-title{

font-size:38px;
font-weight:800;
color:#075985;

}


.card{

background:white;
padding:25px;
border-radius:25px;
box-shadow:
0px 8px 30px rgba(0,0,0,0.08);

}



.metric-title{

font-size:16px;
color:#64748b;

}



.metric-value{

font-size:35px;
font-weight:bold;
color:#0284c7;

}



.agent-card{

background:white;
padding:15px;
border-radius:18px;
margin:10px;

box-shadow:
0 5px 20px rgba(0,0,0,0.08);

}



.online{

color:#16a34a;
font-size:20px;

}



.voice-box{

background:#ecfeff;
padding:20px;
border-radius:20px;

}



</style>

""",
unsafe_allow_html=True
)





# =====================================================
# Header
# =====================================================


logo = Image.open(
    "assets/logo.png"
)


c1,c2 = st.columns(
    [1,5]
)


with c1:

    st.image(
        logo,
        width=100
    )


with c2:

    st.markdown(
    """
    <div class="card">

    <div class="main-title">

    🏥 Healthcare AI Command Center

    </div>

    <p>
    LangGraph + Multi Agent AI + RAG + Voice Assistant
    </p>

    </div>

    """,
    unsafe_allow_html=True
    )






# =====================================================
# Sidebar
# =====================================================


menu = option_menu(

"Navigation",

[
"Patient Portal",
"Doctor Dashboard",
"Hospital Admin"
],

icons=[
"person-heart",
"heart-pulse",
"hospital"
],

default_index=0

)





# =====================================================
# Dashboard Metrics
# =====================================================


c1,c2,c3,c4 = st.columns(4)



metrics=[

("👨‍⚕️ Doctors","120"),

("🧑 Patients","5400"),

("📅 Appointments","350"),

("🤖 AI Agents","8")

]



for col,item in zip(
    [c1,c2,c3,c4],
    metrics
):

    with col:

        st.markdown(

        f"""

        <div class="card">

        <div class="metric-title">

        {item[0]}

        </div>


        <div class="metric-value">

        {item[1]}

        </div>


        </div>

        """,

        unsafe_allow_html=True

        )






# =====================================================
# Patient Portal
# =====================================================


if menu=="Patient Portal":


    st.header(
        "🤖 AI Healthcare Assistant"
    )


    if "messages" not in st.session_state:

        st.session_state.messages=[]


    if "voice_text" not in st.session_state:

        st.session_state.voice_text=""



   # ================================
# PATIENT MODULE
# ================================

if menu == "Patient":


    # session init

    if "messages" not in st.session_state:
        st.session_state.messages=[]


    if "voice_text" not in st.session_state:
        st.session_state.voice_text=""


    # -----------------------------
    # Voice Assistant
    # -----------------------------


    st.markdown(
    """
    <div class="glass-card">

    <h3>🎙️ Voice Healthcare Assistant</h3>

    Speak your medical query and AI will convert it into text.

    </div>
    """,
    unsafe_allow_html=True
    )


    audio = mic_recorder(

        start_prompt="🎤 Start Recording",

        stop_prompt="⏹ Stop Recording",

        key="patient_voice"

    )


    if audio:


        audio_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        )


        audio_file.write(
            audio["bytes"]
        )


        audio_file.close()


        with st.spinner(
            "AI is converting speech..."
        ):

            result = model.transcribe(
                audio_file.name
            )


        st.session_state["voice_text"] = result["text"]


        st.success(
            "Voice converted successfully"
        )



    # -----------------------------
    # Patient Registration
    # -----------------------------


    st.markdown(
    """
    <div class="glass-card">

    <h3>👤 Patient Registration</h3>

    </div>
    """,
    unsafe_allow_html=True
    )


    col1,col2 = st.columns(2)


    with col1:

        patient_name = st.text_input(
            "Patient Name"
        )


        patient_email = st.text_input(
            "Email"
        )


        patient_mobile = st.text_input(
            "Mobile"
        )


        age = st.number_input(
            "Age",
            1,
            120,
            30
        )


    with col2:


        gender = st.selectbox(
            "Gender",
            [
            "Male",
            "Female",
            "Other"
            ]
        )


        question = st.text_area(

            "Describe your health problem",

            value=st.session_state.get(
                "voice_text",
                ""
            ),

            height=120
        )





    if st.button(
        "🚀 Send To AI Healthcare System"
    ):


        if (
            not patient_name
            or not patient_email
            or not question
        ):

            st.warning(
            "Please complete patient details"
            )


        else:


            response = requests.post(

                API_URL + "/chat",

                json={

                "patient_id":"P001",

                "patient_name":
                patient_name,

                "patient_email":
                patient_email,

                "patient_mobile":
                patient_mobile,

                "age":
                age,

                "gender":
                gender,

                "query":
                question

                }

            )


            if response.status_code == 200:
                try:

                  answer=response.json()

                except Exception:
                  st.error(
                      "Backend returned invalid JSON"
                    )

                  st.write(
                      response.text
                    )

                  answer = {
                      "error":
                      response.text
                    }


            else:

                st.error(
                    f"Backend Error {response.status_code}"
                )
                st.write(
                    response.text
                )    
                answer={
                "error":response.text
                }



            st.session_state.messages.append(

                (
                "user",
                question
                )

            )


            st.session_state.messages.append(

                (
                "assistant",
                answer
                )

            )




    # -----------------------------
    # Chat Display
    # -----------------------------


    st.markdown(
    """
    <div class="section-title">
    💬 AI Conversation
    </div>
    """,
    unsafe_allow_html=True
    )


    for index,(role,text) in enumerate(

        st.session_state.messages

    ):


        if role=="user":

            message(

                text,

                is_user=True,

                key=f"user_{index}"

            )


        else:

            message(

                str(text),

                is_user=False,

                key=f"assistant_{index}"

            )






# ==========================
# Doctor Dashboard
# ==========================

elif menu == "Doctor":


    st.markdown(
    """
    <div class="section-title">

    👨‍⚕️ Doctor Dashboard

    </div>
    """,
    unsafe_allow_html=True
    )



    col1,col2 = st.columns([1,2])



    with col1:

        doctor = Image.open(
            "assets/doctor.png"
        )

        st.image(
            doctor,
            width=250
        )



    with col2:


        st.markdown(
        """

        <div class="glass-card">

        <h2>
        Dr. AI Clinical Workspace
        </h2>


        <p>
        AI assisted doctor monitoring system
        </p>


        🟢 Online

        </div>

        """,
        unsafe_allow_html=True
        )




    a,b,c = st.columns(3)



    with a:

        st.metric(
            "Today's Patients",
            "45",
            "+5"
        )


    with b:

        st.metric(
            "Appointments",
            "20",
            "+3"
        )


    with c:

        st.metric(
            "Critical Cases",
            "4",
            "+1"
        )




    chart={

    "Day":
    [
    "Mon",
    "Tue",
    "Wed",
    "Thu",
    "Fri"
    ],


    "Patients":
    [
    20,
    40,
    35,
    55,
    45
    ]

    }



    fig=px.line(

        chart,

        x="Day",

        y="Patients",

        title="Doctor Patient Trend"

    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



    st.markdown(

    """

    <div class="glass-card">


    🧠 AI Doctor Assistant


    - Patient summary
    - AI clinical insights
    - Appointment review
    - Medical knowledge search


    </div>


    """,

    unsafe_allow_html=True

    )





# ==========================
# Hospital Admin Dashboard
# ==========================


elif menu == "Hospital Admin":


    st.markdown(
    """
    <div class="section-title">

    🏥 Hospital Operations Center

    </div>
    """,
    unsafe_allow_html=True
    )



    a,b,c,d=st.columns(4)


    with a:

        st.metric(
            "Doctors",
            "120"
        )


    with b:

        st.metric(
            "Patients",
            "5400"
        )


    with c:

        st.metric(
            "Beds",
            "45"
        )


    with d:

        st.metric(
            "AI Agents",
            "8"
        )




    # =====================================
# COMMON AI PLATFORM MONITORING
# =====================================


st.markdown(
"""
<div class="glass-card">

<h2>
🤖 LangGraph Agent Monitoring
</h2>

Multi Agent Healthcare Workflow

</div>
""",
unsafe_allow_html=True
)



agents=[

"Patient Coordinator",

"Clinical Agent",

"Medical RAG",

"Pharmacy Agent",

"Insurance Agent",

"Billing Agent",

"Operations Agent",

"Safety Guardrails"

]


cols=st.columns(4)


for i,agent in enumerate(agents):

    with cols[i%4]:

        st.markdown(

        f"""

        <div class="agent-card">

        🟢 <b>{agent}</b>

        <br><br>

        ACTIVE

        </div>

        """,

        unsafe_allow_html=True

        )



st.markdown(
"""
<div class="glass-card">

<h2>
🔄 AI Healthcare Workflow
</h2>


Patient

↓

LangGraph Router

↓

Specialist

↓

Agents

↓

Guardrails

↓

Safety


</div>
""",
unsafe_allow_html=True
)
st.markdown(
"""
<div class="glass-card">

<h2>
📊 AI Healthcare Request Analytics
</h2>

</div>
""",
unsafe_allow_html=True
)



c1,c2,c3,c4 = st.columns(4)


with c1:

    st.metric(
        "Total Requests",
        "5400",
        "+320"
    )


with c2:

    st.metric(
        "Clinical Queries",
        "2400",
        "+120"
    )


with c3:

    st.metric(
        "RAG Searches",
        "1500",
        "+90"
    )


with c4:

    st.metric(
        "Emergency Cases",
        "15",
        "+3"
    )



# Request distribution chart

request_data = {

    "Agent":[

        "Clinical",
        "Medical RAG",
        "Pharmacy",
        "Insurance",
        "Billing"

    ],

    "Requests":[

        2400,
        1500,
        700,
        500,
        300

    ]

}



fig = px.bar(

    request_data,

    x="Agent",

    y="Requests",

    title="Healthcare AI Request Distribution"

)


st.plotly_chart(

    fig,

    use_container_width=True

)



st.markdown(

"""
<br>

<center>

<h3>
🚀 Built with LangGraph + LangChain + FastAPI + Streamlit
</h3>

<h4>
AI Agentic Healthcare Platform
</h4>

</center>

""",

unsafe_allow_html=True

)