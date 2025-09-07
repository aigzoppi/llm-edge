# YOLO + LLM-Edge (BitNet) Project

🚀 An edge AI project that combines **real-time object detection** with **on-device large language model reasoning**.  
This system uses:

- **[YOLO](https://github.com/ultralytics/ultralytics)** for object detection  
- **llm-edge** for efficient LLM inference on constrained devices  
- **BitNet** as the LLM backend for energy-efficient, fast inference at the edge  
- **[uv](https://github.com/astral-sh/uv)** package manager for reproducible environments and dependency management  

---

## 🔥 Features

- Real-time object detection with YOLO  
- On-device reasoning with BitNet LLM (no cloud required)  
- Optimized for **edge deployment** (Raspberry Pi, Jetson, ARM SBCs)  
- Lightweight and reproducible environment with **uv**  
- Modular design → swap YOLO model or LLM backend easily  

---

## 📦 Installation

Make sure you have `uv` installed:  

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh

```

Install the deps and set virtual enviroment.

```
cd llm-edge
uv sync

```


##🏃 Usage

Run YOLO detection + LLM reasoning pipeline:

```bash
uv run python main.py --source 0 --model yolov8n.pt --llm bitnet
```

## 🧠 Example Workflow

YOLO detects objects in a frame

Detected labels + bounding boxes are passed to the LLM

BitNet LLM generates reasoning or contextual descriptions (e.g., "I see a person holding a red cup")

Output is displayed or published via MQTT/REST for downstream use

## 📊 Performance

- Runs on-device without internet
- Lower memory footprint thanks to BitNet compression
- Fast enough for real-time use on edge hardware

## Roadmap

- Add support for other quantized LLMs
- Provide prebuilt docker images for Jetson devices
- Add voice input/output integration
- B+enchmark on Raspberry Pi 5 + NVIDIA Jetson Orin Nano



