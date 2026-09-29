import streamlit as st
import time

# ==============================================================================
# GameOfUs: Family Edition — Advanced System Engine & UI
# Authors: Beka (Architect), DeepSeek / DeP (Logic Engine), Gemini (Mirror)
# ==============================================================================

# --- Streamlit Page Configuration (Mobile-Friendly) ---
st.set_page_config(
    page_title="GameOfUs: Family Edition",
    page_icon="🌟",
    layout="centered"
)

# --- STATE INITIALIZATION ---
if "xp" not in st.session_state:
    st.session_state.xp = 40
if "stars" not in st.session_state:
    st.session_state.stars = 3
if "level" not in st.session_state:
    st.session_state.level = 1
if "energy" not in st.session_state:
    st.session_state.energy = 5  # Scale 1-10
if "completed_missions" not in st.session_state:
    st.session_state.completed_missions = []
if "urge_count" not in st.session_state:
    st.session_state.urge_count = 0
if "praise_count" not in st.session_state:
    st.session_state.praise_count = 0

# --- CORE HELPER FUNCTIONS ---
def get_energy_zone(energy_level: int):
    """Gemini-ს ენერგიის 3 ზონის მოდელი"""
    if energy_level <= 3:
        return "🔴 წითელი (დაბალი ენერგია / Re-charge)", "red", "ტვინი ითხოვს დასვენებას და აღდგენას."
    elif 4 <= energy_level <= 7:
        return "🟢 მწვანე (ოპტიმალური / Focus)", "green", "საუკეთესო დროა სწავლისა და შემოქმედებისთვის."
    else:
        return "🟡 ყვითელი (მაღალი აგზნება / Cool-down)", "orange", "საჭიროა ტემპის დაყოვნება და დამშვიდება."

def level_up_check():
    """XP და დონის მართვის ლოგიკა"""
    needed_xp = st.session_state.level * 100
    if st.session_state.xp >= needed_xp:
        st.session_state.level += 1
        st.session_state.xp -= needed_xp
        st.balloons()
        st.toast(f"🎉 ახალი დონე! გადახვედი {st.session_state.level} დონეზე!", icon="🏆")

# --- APP HEADER ---
st.title("🌟 GameOfUs: Family Edition")
st.caption("თამაში ბავშვისთვის • მხარდაჭერა მშობლისთვის • ზრდა ორივესთვის")

# --- TABS NAVIGATION ---
tab_child, tab_parent = st.tabs(["👦 ბავშვის სივრცე", "👩‍👦 მშობლის პანელი"])

# ==============================================================================
# 👦 1. CHILD INTERFACE (თამაში და თვითრეგულაცია)
# ==============================================================================
with tab_child:
    st.header("გამარჯობა, გმირო! 👋")
    
    # 1.1 ენერგიის ზონის კალიბრაცია
    zone_label, zone_color, zone_desc = get_energy_zone(st.session_state.energy)
    st.subheader(f"⚡ შენი ენერგია: {st.session_state.energy}/10")
    st.info(f"**მიმდინარე ზონა:** {zone_label}\n\n_{zone_desc}_")
    
    col_e1, col_e2 = st.columns(2)
    if col_e1.button("🔋 დავიღალე (-2)"):
        st.session_state.energy = max(1, st.session_state.energy - 2)
        st.rerun()
    if col_e2.button("⚡ ენერგიაზე ვარ (+2)"):
        st.session_state.energy = min(10, st.session_state.energy + 2)
        st.rerun()

    st.divider()

    # 1.2 Dashboard Status
    col1, col2, col3 = st.columns(3)
    col1.metric("დონე", f"{st.session_state.level} 🏆")
    col2.metric("ვარსკვლავები", f"{st.session_state.stars} ⭐")
    col3.metric("XP ქულა", f"{st.session_state.xp} / {st.session_state.level * 100}")
    st.progress(min(1.0, st.session_state.xp / (st.session_state.level * 100)))

    # 1.3 DeP's De-escalation: „პაუზის ღილაკი“ (Urge Wave Cooldown)
    st.divider()
    st.subheader("🧘‍♂️ „პაუზის ღილაკი“ (სუნთქვის კუთხე)")
    st.write("თუ გრძნობ იმპულსს, ნერვიულობას ან აჩქარებას — ჩართე პაუზა:")
    
    if st.button("🌊 ჩართე 15-წამიანი სუნთქვის ტალღა"):
        placeholder = st.empty()
        progress_bar = st.progress(0)
        duration = 15
        
        for i in range(duration):
            remaining = duration - i
            placeholder.markdown(f"### 🎈 ისუნთქე ღრმად... დარჩენილია {remaining} წამი")
            progress_bar.progress((i + 1) / duration)
            time.sleep(1)
            
        placeholder.markdown("### ✅ ყოჩაღ! ტალღამ ჩაიარა. შენ დაამარცხე იმპულსი!")
        st.session_state.stars += 1
        st.session_state.xp += 25
        st.session_state.urge_count += 1
        level_up_check()
        st.toast("მიღებულია +1 ვარსკვლავი და +25 XP!", icon="⭐")

    st.divider()

    # 1.4 Daily & Family Missions
    st.subheader("📋 დღევანდელი მისიები")
    missions = [
        ("💧 დალიე 1 ჭიქა წყალი დილით", "m1"),
        ("🏃‍♂️ 10 წუთი ივარჯიშე / ითამაშე ჰაერზე", "m2"),
        ("📖 წაიკითხე 5 გვერდი", "m3"),
        ("👨‍👩‍👦 ოჯახური მისია: 10-წუთიანი საუბარი ემოციებზე", "m4")
    ]

    for title, key in missions:
        col_m1, col_m2 = st.columns([3, 1])
        col_m1.write(title)
        if key in st.session_state.completed_missions:
            col_m2.success("✅ შესრულებულია")
        else:
            if col_m2.button("შესრულება ⭐", key=key):
                st.session_state.completed_missions.append(key)
                st.session_state.xp += 20
                st.session_state.stars += 1
                level_up_check()
                st.rerun()

# ==============================================================================
# 👩‍👦 2. PARENT INTERFACE (ანალიტიკა და მხარდაჭერა)
# ==============================================================================
with tab_parent:
    st.header("📊 მშობლის მხარდაჭერის პანელი")
    st.info("ეს სივრცე შექმნილია დაკვირვებისა და მხარდაჭერისთვის, და არა კონტროლისთვის.")

    # 2.1 Status Overview
    st.subheader("📈 შვილის მიმდინარე სტატუსი")
    st.write(f"**დონე:** {st.session_state.level} | **შეგროვილი ვარსკვლავები:** {st.session_state.stars} ⭐")
    st.write(f"**დღეს შესრულებული მისიები:** {len(st.session_state.completed_missions)} / {len(missions)}")
    st.write(f"**გადალახული „პაუზის ტალღები“:** {st.session_state.urge_count}")

    # 2.2 Positive Reinforcement Button
    st.divider()
    st.subheader("🎁 შექება და წახალისება")
    st.write("თუ ამჩნევთ ბავშვის მონდომებას, აჩუქეთ მას ბონუს ვარსკვლავი:")
    if st.button("❤ შექება (+1 ბონუს ვარსკვლავი ბავშვს)"):
        st.session_state.stars += 1
        st.session_state.praise_count += 1
        st.success("შექება გაიგზავნა! ბავშვს დაემატა +1 ვარსკვლავი ⭐")

    # 2.3 Gemini Mirror Analytics
    st.divider()
    st.subheader("💡 Gemini Mirror-ის კონტექსტური ანალიტიკა")
    
    if st.session_state.energy <= 3:
        st.warning(
            "**ანალიზი:** ბავშვი იმყოფება წითელ ზონაში (დაბალი ენერგია).\n\n"
            "**რეკომენდაცია:** ნუ მოსთხოვთ რთულ დავალებებს ან მეცადინეობას. "
            "შესთავაზეთ წყალი, მშვიდი გარემო ან 15-წუთიანი მოსვენება."
        )
    elif 4 <= st.session_state.energy <= 7:
        st.success(
            "**ანალიზი:** ბავშვი ოპტიმალურ (მწვანე) ენერგეტიკულ ზონაშია.\n\n"
            "**რეკომენდაცია:** საუკეთესო დროა ოჯახური მისიისთვის, სწავლისთვის ან შემოქმედებითი აქტივობისთვის."
        )
    else:
        st.error(
            "**ანალიზი:** ბავშვი ყვითელ ზონაშია (მაღალი ენერგია/აგზნება).\n\n"
            "**რეკომენდაცია:** შეთავაზეთ ფიზიკური განტვირთვა ან „პაუზის ღილაკის“ გამოყენება ტემპის დასაგდებად."
        )

    # 2.4 Weekly Summary Report
    st.divider()
    st.subheader("📝 კვირის შემაჯამებელი ანგარიში")
    st.text_area(
        "რეპორტი:",
        value=(
            f"=== GameOfUs Weekly Summary ===\n"
            f"• აქტიური დონე: {st.session_state.level}\n"
            f"• სულ შეგროვილი ვარსკვლავები: {st.session_state.stars}\n"
            f"• შექებები მშობლისგან: {st.session_state.praise_count}\n"
            f"• გადალახული იმპულსები: {st.session_state.urge_count}\n"
            f"• დასკვნა: ბავშვი აქტიურად იყენებს თვითრეგულაციის ინსტრუმენტებს."
        ),
        height=150
  )
  
