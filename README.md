# Image search with YOLOv11

A project to search a folder of images by the objects in them. For example, "images with a person and a dog" or "images with at most 2 cars".

I used the 500 image subset of COCO val 2017 as the dataset (kept in `data_for_prj`).

## How it works

There are two separate steps.

1. `run_inference.py` runs a pretrained YOLOv11m model on every image and saves the detections to `metadata.json`. For each image it stores the class, confidence, bounding box and a count per class.
2. `app.py` only reads `metadata.json`. You pick classes, choose OR/AND, optionally set a max count, and it filters the metadata and shows the matching images with boxes drawn on them.

## Project layout

```
app.py              streamlit app
run_inference.py    builds metadata.json
metadata.json       detections for all images
configs/default.yaml  confidence threshold, image extensions
src/                inference code used by run_inference.py
data_for_prj/       images
```

## Running it

Install the requirements:

```
pip install -r requirements.txt
```

Generate the metadata (only needed if you change the images or the threshold):

```
python run_inference.py
```

Start the app:

```
streamlit run app.py
```

Run both commands from the repo root, otherwise the image paths stored in the metadata won't line up.

