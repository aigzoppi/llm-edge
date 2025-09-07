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
Create a virtual enviroment
```bash
$ cd edgedemo
$ uv venv
$ uv sync
$ source .venv/bin/activate

```
## Make sure that all submodules are initialized and Egde LLM is setup
```bash
$ cd ../BitNet
$ git submodule update --init --recursive
$ uv pip install -r requirements.txt
$ huggingface-cli download microsoft/BitNet-b1.58-2B-4T-gguf --local-dir models/BitNet-b1.58-2B-4T
$ python setup_env.py -md models/BitNet-b1.58-2B-4T -q i2_s
```

##🏃 Usage

Run YOLO detection + LLM reasoning pipeline:

```bash
uv run python main.py --source 0 --model yolov8n.pt --llm bitnet
```

## 🖥️ CLI Options

The `llm-edge` CLI provides flexible options for detection and LLM inference. Run with:

```bash
uv run llm-edge run [OPTIONS]
```

### Main Options

| Option                | Type    | Default                                         | Description                                 |
|-----------------------|---------|-------------------------------------------------|---------------------------------------------|
| `--image-path`        | str     | `data/images`                                   | Path to images                              |
| `--number-of-images`  | int     | `3`                                             | Number of images to process                 |
| `--realtime`          | bool    | `False`                                         | Enable realtime mode                        |
| `--enable-inference`  | bool    | `False`                                         | Enable LLM inference integration            |
| `--model`             | str     | `models/bitnet_b1_58-3B/ggml-model-i2_s.gguf`   | Path to LLM model file                      |
| `--n-predict`         | int     | `1`                                             | Number of tokens to predict                 |
| `--threads`           | int     | `1`                                             | Number of threads to use                    |
| `--prompt`            | str     | `Describe the image`                            | Prompt to send to the model                 |
| `--ctx-size`          | int     | `512`                                           | Context size                                |
| `--temperature`       | float   | `0.8`                                           | Sampling temperature                        |
| `--conversation`      | bool    | `False`                                         | Enable conversation mode                    |

### YOLO Model

- The CLI uses YOLO for object detection. You can specify the YOLO model file (e.g., `yolov8n.pt`, `yolov8s.pt`) using the `--model` option if running detection only.
- The current configuration is able to detect **11 classes** instead of the standard 10, allowing for extended verification and use cases.

> **Note:** LLM inference is disabled by default. Use `--enable-inference` to activate BitNet LLM reasoning.

---

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



