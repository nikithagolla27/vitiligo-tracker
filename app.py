import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Vitiligo Tracker",
    page_icon="🌿",
    layout="centered"
)

# Custom Cover Page
st.markdown(
    """
    <div style='text-align: center; padding: 30px 0;'>
        <h1 style='color: #4CAF50;'>🌿 Vitiligo Lifestyle & Diet Tracker</h1>
        <p style='font-size: 18px; color: #555;'>Track your daily habits, food, sunlight, and emotions.</p>
        <img src='https://cdn.pixabay.com/photo/2017/09/15/13/28/leaves-2757525_960_720.png' width='250'/>
        <hr style='margin-top: 30px; border: 1px solid #ccc;'/>
    </div>
    """,
    unsafe_allow_html=True
)

import streamlit as st
import sqlite3
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import random

# -------------------- PAGE SETTINGS --------------------
st.set_page_config(page_title="Vitiligo Tracker", page_icon="🌿", layout="centered")

st.markdown("<h1 style='text-align: center; color: white;'>🌿 Vitiligo Diet & Lifestyle Tracker</h1>", unsafe_allow_html=True)

# -------------------- MOTIVATIONAL MESSAGE --------------------
motivational_quotes = [
    "💚 You are beautiful. Your skin does not define your worth.",
    "🌟 Keep smiling! You’re stronger than you think.",
    "🌈 Vitiligo is just a part of you — not your identity.",
    "🌸 You are loved. You are worthy. Have a wonderful day!",
    "🌞 You’re doing amazing. One day at a time.",
    "💪 Your journey is valid, your courage is inspiring."
]
quote = random.choice(motivational_quotes)
st.info(quote)

# -------------------- SIDEBAR: DIET GUIDE --------------------
with st.sidebar:
    st.subheader("🧾 Vitiligo Diet Guide")

    st.markdown("### ❌ Avoid These Foods:")
    st.markdown("""
    - Citrus fruits (lemon, orange)  
    - Milk and dairy products  
    - Tomatoes  
    - Seafood  
    - Pickles, vinegar  
    - Junk/processed food  
    - Red meat  
    - Alcohol, excess tea/coffee
    """)

    st.markdown("### ✅ Recommended Foods:")
    st.markdown("""
    - Green leafy vegetables  
    - Beets, carrots  
    - Whole grains (brown rice, oats)  
    - Turmeric + black pepper  
    - Figs and dates  
    - Walnuts, almonds  
    - Iron & zinc rich foods (seeds, lentils)
    """)

# -------------------- DATABASE SETUP --------------------
conn = sqlite3.connect('vitiligo.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS tracker
             (date TEXT, food TEXT, sun_exposure REAL, sleep_hours REAL, mood TEXT)''')
conn.commit()

# -------------------- DAILY ENTRY FORM --------------------
st.subheader("📋 Daily Entry")

with st.form(key='entry_form'):
    date = st.date_input("Date", value=datetime.date.today())
    food = st.text_area("What did you eat today?")
    sun = st.slider("Sun exposure (hours)", 0.0, 5.0, step=0.5)
    sleep = st.slider("Sleep hours", 0.0, 12.0, step=0.5)
    mood = st.radio("Mood", ["😊 Happy", "😐 Okay", "😞 Sad"])
    submit = st.form_submit_button("Save Entry")

    if submit:
        c.execute("INSERT INTO tracker (date, food, sun_exposure, sleep_hours, mood) VALUES (?, ?, ?, ?, ?)",
                  (str(date), food, sun, sleep, mood))
        conn.commit()
        st.success("✅ Entry saved!")

        # --- Check food input for risky items ---
        unsafe_foods = ['milk', 'lemon', 'orange', 'seafood', 'tomato', 'vinegar', 'cheese', 'coffee', 'junk', 'meat', 'pickle']
        for item in unsafe_foods:
            if item in food.lower():
                st.warning(f"⚠️ Note: '{item}' is not recommended for vitiligo patients.")

# -------------------- DISPLAY DATA --------------------
st.subheader("📊 Past Records")

df = pd.read_sql_query("SELECT * FROM tracker ORDER BY date DESC", conn)

if not df.empty:
    st.dataframe(df, use_container_width=True)

    # --- Sun exposure chart ---
    st.subheader("☀️ Sun Exposure Over Time")
    fig, ax = plt.subplots()
    df['date'] = pd.to_datetime(df['date'])
    ax.plot(df['date'], df['sun_exposure'], marker='o', color='orange')
    ax.set_xlabel("Date")
    ax.set_ylabel("Sun Exposure (hours)")
    ax.set_title("Sun Exposure Trend")
    plt.xticks(rotation=30)
    st.pyplot(fig)
else:
    st.info("No records yet. Fill in the form above to get started.")

conn.close()

