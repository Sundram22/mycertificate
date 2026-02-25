import streamlit as st
from PIL import Image, ImageDraw
from io import BytesIO
import gdown
import os
from my_fonts import load_font, fonts_dict

# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(page_title="Certificate Generator", layout="centered")
st.title("🎓 Get Your Certificate")
st.markdown("Fill in your details below to generate your certificate.")

# -----------------------------
# Step 1: Student Input
# -----------------------------
name = st.text_input("Enter Your Name")

# ---------- BRANCH ----------
st.markdown("### Branch")
branch_mode = st.radio(
    "Branch input mode",
    ["Select from list", "Enter manually"],
    horizontal=True,
    label_visibility="collapsed"
)

branch_options = [
    "CSE", "IT", "ECE", "EE", "EEE", "ME", "CE",
    "BCA", "MCA",
    "AI", "DS", "CY",
    "HR", "FIN", "MKT"
]

if branch_mode == "Select from list":
    branch = st.selectbox("Select Branch", branch_options)
else:
    branch = st.text_input("Enter Branch Manually")

# ---------- YEAR ----------
st.markdown("### Year")
year_mode = st.radio(
    "Year input mode",
    ["Select from list", "Enter manually"],
    horizontal=True,
    label_visibility="collapsed"
)

year_options = ["1st", "2nd", "3rd", "4th"]

if year_mode == "Select from list":
    year_raw = st.selectbox("Select Year", year_options)
else:
    year_raw = st.text_input("Enter Year Manually")

# -----------------------------
# Step 2: Load Certificate Template (UPDATED DRIVE LINK)
# -----------------------------
FILE_ID = "1SnVrwMx07fuR0-mofW1DmPjXiPoBjAr1"
IMAGE_PATH = "template.png"

try:
    if not os.path.exists(IMAGE_PATH):
        gdown.download(
            url=f"https://drive.google.com/uc?id={FILE_ID}",
            output=IMAGE_PATH,
            quiet=False,
            fuzzy=True
        )
    template = Image.open(IMAGE_PATH).convert("RGB")
except Exception as e:
    st.error(f"❌ Failed to load certificate template! Error: {e}")
    st.stop()

# -----------------------------
# Step 3: TEXT POSITIONS
# -----------------------------
name_pos = (807, 474)
course_pos = (605, 533)

# -----------------------------
# Step 4: Font & Size Settings
# -----------------------------
st.subheader("🖊 Font & Size Settings")

font_options = list(fonts_dict.keys())
col1, col2 = st.columns(2)

with col1:
    font_name = st.selectbox("Font for Name", font_options)
    size_name = st.slider("Name Font Size", 20, 80, 30)

with col2:
    font_course = st.selectbox("Font for Course Line", font_options)
    size_course = st.slider("Course Font Size", 20, 80, 25)

# -----------------------------
# Step 5: Generate Certificate
# -----------------------------
if st.button("Generate Certificate"):

    if not name or not branch or not year_raw:
        st.warning("⚠️ Please fill all fields")
    else:
        cert = template.copy()
        draw = ImageDraw.Draw(cert)

        f_name = load_font(font_name, size_name)
        f_main = load_font(font_course, size_course)
        f_sup = load_font(font_course, int(size_course * 0.6))

        def draw_centered(text, pos, font):
            bbox = draw.textbbox((0, 0), text, font=font)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            x, y = pos
            draw.text((x - w / 2, y - h / 2), text, font=font, fill=(0, 0, 0))

        def draw_year_superscript(draw, pos, number, suffix, font_main, font_sup):
            text_main = f"{branch} ({number}"
            bbox_main = draw.textbbox((0, 0), text_main, font=font_main)
            main_width = bbox_main[2] - bbox_main[0]

            suffix_bbox = draw.textbbox((0, 0), suffix, font=font_sup)
            year_bbox = draw.textbbox((0, 0), " Year)", font=font_main)

            full_width = main_width + suffix_bbox[2] + year_bbox[2]
            x, y = pos
            start_x = x - full_width / 2

            draw.text((start_x, y), text_main, font=font_main, fill=(0, 0, 0))

            sup_x = start_x + main_width
            sup_y = y - font_main.size * 0.35
            draw.text((sup_x, sup_y), suffix, font=font_sup, fill=(0, 0, 0))

            year_x = sup_x + suffix_bbox[2]
            draw.text((year_x, y), " Year)", font=font_main, fill=(0, 0, 0))

        num = "".join(filter(str.isdigit, year_raw))
        suf = year_raw.replace(num, "")

        draw_centered(name, name_pos, f_name)
        draw_year_superscript(draw, course_pos, num, suf, f_main, f_sup)

        st.image(cert, caption="🖼 Generated Certificate Preview", use_container_width=True)

        pdf_buffer = BytesIO()
        cert.save(pdf_buffer, format="PDF")
        pdf_buffer.seek(0)

        st.success("🎉 Your certificate is ready!")
        st.download_button(
            "📥 Download Certificate PDF",
            pdf_buffer,
            file_name=f"certificate_{name.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )

# -----------------------------
# Footer
# -----------------------------
st.markdown("""
<div style="position: fixed; bottom: 0; left: 0; right: 0;
background-color: #f8f9fa; padding: 10px;
text-align: center; font-size: 16px;
font-family: Arial; color: #0b5394;
border-top: 1px solid #ddd;">
✅ Made by <b>Asst. Prof. Sundram Tiwari</b>
</div>
""", unsafe_allow_html=True)