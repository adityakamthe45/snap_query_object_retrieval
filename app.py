
import json
from pathlib import Path
 
import streamlit as st
from PIL import Image, ImageDraw
 
APP_DIR = Path(__file__).resolve().parent
 
st.set_page_config(page_title="SnapQuery", layout="wide")
st.title("Aditya's YOLO Powered Search Application")
 
 
@st.cache_data
def load_metadata(path):
    with open(path) as f:
        return json.load(f)
 
 
def find_image(raw_path):
    
    p = Path(str(raw_path).replace("\\", "/"))
    for candidate in (APP_DIR / p, APP_DIR / "data_for_prj" / p.name):
        if candidate.exists():
            return candidate
 
 
def draw_boxes(img, detections, selected):
    draw = ImageDraw.Draw(img)
    for d in detections:
        if d["class"] in selected:
            x, y = d["bbox"][:2]
            draw.rectangle(d["bbox"], outline="#FF55E3", width=3)
            draw.text((x + 4, y + 4), f'{d["class"]} {d["confidence"]:.2f}', fill="#FF55E3")
    img.thumbnail((800, 800))  
    return img
 
 

meta_path = st.text_input("Metadata file", "metadata.json")
try:
    metadata = load_metadata(APP_DIR / meta_path)
except Exception as e:
    st.error(f"Could not load metadata: {e}")
    st.stop()
 

classes = sorted({d["class"] for m in metadata for d in m["detections"]})
c1, c2, c3 = st.columns([3, 2, 2])
selected = c1.multiselect("Classes to search for", classes)
mode = c2.radio("Search mode", ["OR (any)", "AND (all)"], horizontal=True)
max_count = c3.number_input("Max count per class (0 = no limit)", min_value=0, value=0)
 
if not selected:
    st.info("Pick one or more classes to search.")
    st.stop()
 
 
def matches(item):
    hits = []
    for c in selected:
        n = item["class_counts"].get(c, 0)
        hits.append(n >= 1 and (max_count == 0 or n <= max_count))
    return any(hits) if mode.startswith("OR") else all(hits)
 
 
results = [m for m in metadata if matches(m)]
st.subheader(f"📸 {len(results)} matching images")
if not results:
    st.info("No matching images found.")
    st.stop()
 

n_cols = st.slider("Grid columns", 2, 6, 3)
grid = st.columns(n_cols)
for i, item in enumerate(results):
    path = find_image(item["image_path"])
    with grid[i % n_cols]:
        if path is None:
            st.caption(f"⚠️ Image not found: {item['image_path']}")
            continue
        img = draw_boxes(Image.open(path).convert("RGB"), item["detections"], selected)
        counts = ", ".join(f"{c}: {item['class_counts'][c]}" for c in selected if c in item["class_counts"])
        st.image(img, caption=f"{path.name} | {counts}")
