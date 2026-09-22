import io
import cv2
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
from src.preprocessing import preprocess
from src.detection import detect_defects, summarize
from src.analytics import aggregate
from src.reporting import create_report

st.set_page_config(page_title="VisionGuard", page_icon="🛣️", layout="wide")

st.title("🛣️ VisionGuard")
st.caption("Computer Vision prototype for road-surface defect detection and severity analysis")

with st.sidebar:
    st.header("Modules")
    st.markdown("**1. Image Analysis** — preprocess and detect candidate defects")
    st.markdown("**2. Batch Analytics** — compare multiple images")
    st.markdown("**3. Reporting** — export an analysis summary")
    st.divider()
    st.info("This academic prototype uses classical OpenCV techniques. It is not a production road-inspection system.")

uploaded = st.file_uploader("Upload one or more road images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if not uploaded:
    st.warning("Upload at least one image to begin.")
    st.stop()

results = []
for file in uploaded:
    raw = np.array(Image.open(file).convert("RGB"))
    bgr = cv2.cvtColor(raw, cv2.COLOR_RGB2BGR)
    processed, _ = preprocess(bgr)
    annotated, defects = detect_defects(processed)
    s = summarize(defects)
    results.append({"image": file.name, **s})

first = results[0]
col1, col2, col3, col4 = st.columns(4)
col1.metric("Images", len(results))
col2.metric("Candidate defects", sum(r["total"] for r in results))
col3.metric("High severity", sum(r["high"] for r in results))
col4.metric("Overall", aggregate(results)["severity"])

st.subheader("1. Image Analysis")
selected_name = st.selectbox("Select image", [f.name for f in uploaded])
selected = next(f for f in uploaded if f.name == selected_name)
raw = np.array(Image.open(selected).convert("RGB"))
bgr = cv2.cvtColor(raw, cv2.COLOR_RGB2BGR)
processed, gray = preprocess(bgr)
annotated, defects = detect_defects(processed)
annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

c1, c2 = st.columns(2)
c1.image(raw, caption="Original", use_container_width=True)
c2.image(annotated_rgb, caption="Detected candidate regions", use_container_width=True)

if defects:
    st.dataframe(pd.DataFrame(defects), use_container_width=True)
else:
    st.success("No candidate regions met the detection threshold for this image.")

st.subheader("2. Batch Analytics")
df = pd.DataFrame(results)
st.dataframe(df, use_container_width=True)

agg = aggregate(results)
st.write(f"**Batch summary:** {agg['images']} images, {agg['defects']} candidate defects, {agg['high_risk_images']} high-severity image(s).")

st.subheader("3. Reporting")
summary = {
    "images": len(results),
    "defects": sum(r["total"] for r in results),
    "low": sum(r["low"] for r in results),
    "medium": sum(r["medium"] for r in results),
    "high": sum(r["high"] for r in results),
    "severity": agg["severity"],
}
if st.button("Generate PDF report"):
    path = create_report("/tmp/visionguard_report.pdf", summary)
    with open(path, "rb") as f:
        st.download_button("Download report", f, file_name="VisionGuard_Report.pdf", mime="application/pdf")
