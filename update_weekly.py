#!/usr/bin/env python3
"""Weekly profile README updater — auto-runs every Sunday via GitHub Actions."""
import re
from datetime import date

START_DATE = date(2026, 6, 15)   # first Sunday after deploy

# ── 52 missions (loops for year 2) ──────────────────────────────────────────
# (title, quest, stack, quote, difficulty_bar, gif_url)
MISSIONS = [
    # Wk 1
    ("⚡ EfficientNet Mastery",
     "Compound-scale EfficientNetB0–B7 from scratch",
     "PyTorch &bull; TensorFlow &bull; Keras",
     "Scale width, depth &amp; resolution together 📐",
     "████████░░ Hard",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
    # Wk 2
    ("🔗 ResNet Revolution",
     "Build ResNet-18/34/50/101/152 with skip connections",
     "PyTorch &bull; TensorFlow",
     "Residual learning — the idea that changed everything 🔗",
     "████████░░ Hard",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
    # Wk 3
    ("🌿 DenseNet Deep Dive",
     "Connect every layer to every other layer (DenseNet121/169/201)",
     "PyTorch &bull; TensorFlow",
     "Dense connections, dense knowledge 🧠",
     "████████░░ Hard",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),
    # Wk 4
    ("🌲 ConvNeXt Chronicles",
     "Modernise ResNet into ConvNeXt T/S/B/L/XL",
     "PyTorch &bull; TensorFlow",
     "What if ResNet was born in the transformer era? 🤔",
     "█████████░ Expert",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
    # Wk 5
    ("👁️ Vision Transformer Voyage",
     "ViT-B/16 — patches are all you need",
     "PyTorch &bull; JAX",
     "Attention beats convolutions? Challenge accepted! ⚔️",
     "██████████ Expert",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
    # Wk 6
    ("📱 MobileNet Magic",
     "Depthwise separable convolutions for edge devices",
     "TFLite &bull; PyTorch",
     "Big brains, tiny footprint 📲",
     "███████░░░ Medium",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),
    # Wk 7
    ("🚀 EfficientNetV2 Explorer",
     "Fused-MBConv + progressive training (B0–B3, S/M/L)",
     "TensorFlow &bull; PyTorch",
     "Faster, smaller, stronger 🚀",
     "█████████░ Expert",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
    # Wk 8
    ("🎭 Inception &amp; Xception",
     "InceptionV3 + Xception depthwise separable magic",
     "TensorFlow &bull; Keras",
     "Inception: thinking inside the block 🎭",
     "████████░░ Hard",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
    # Wk 9
    ("🎨 GAN Genesis",
     "Train DCGAN to generate photorealistic images",
     "PyTorch &bull; TensorFlow",
     "Teaching machines to hallucinate beautifully 🎨",
     "████████░░ Hard",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),
    # Wk 10
    ("✨ Diffusion Model Dreams",
     "Implement DDPM — noise to beauty step by step",
     "PyTorch &bull; Diffusers",
     "Reverse the entropy, reveal the art ✨",
     "██████████ Expert",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
    # Wk 11
    ("🧠 Attention Is All You Need",
     "Implement multi-head self-attention from scratch",
     "PyTorch &bull; NumPy",
     "One mechanism to rule them all 💫",
     "█████████░ Expert",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
    # Wk 12
    ("🌉 CLIP Challenge",
     "Contrastive Language-Image Pretraining",
     "PyTorch &bull; HuggingFace",
     "Images and words — same latent space 🌉",
     "█████████░ Expert",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),
    # Wk 13
    ("⚡ YOLO Speed Run",
     "Real-time object detection — YOLOv8 from paper to code",
     "PyTorch &bull; OpenCV",
     "You Only Look Once — but see everything 🏎️",
     "█████████░ Expert",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
    # Wk 14
    ("📦 Faster R-CNN",
     "Region proposal networks for object detection",
     "PyTorch &bull; torchvision",
     "Find it. Box it. Classify it. 📦",
     "█████████░ Expert",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
    # Wk 15
    ("🧩 U-Net Architect",
     "Encoder-decoder segmentation — every pixel matters",
     "PyTorch &bull; TensorFlow",
     "Semantics in every single pixel 🧩",
     "████████░░ Hard",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),
    # Wk 16
    ("🌆 Semantic Segmentation",
     "DeepLab v3+ atrous convolutions for scene parsing",
     "TensorFlow &bull; PyTorch",
     "Understand the scene, pixel by pixel 🌆",
     "█████████░ Expert",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
    # Wk 17
    ("🏔️ Transfer Learning Master",
     "Fine-tune ImageNet models on custom datasets",
     "TF Hub &bull; PyTorch Hub",
     "Stand on the shoulders of giants 🏔️",
     "███████░░░ Medium",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
    # Wk 18
    ("📝 Knowledge Distillation",
     "Compress a ResNet-50 teacher into MobileNet student",
     "PyTorch &bull; TensorFlow",
     "The student learns what the teacher earned 📝",
     "████████░░ Hard",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),
    # Wk 19
    ("⚡ Mixed Precision Training",
     "FP16 AMP — 2× speed, same accuracy",
     "PyTorch AMP &bull; TF tf.keras.mixed_precision",
     "Fast, furious &amp; accurate ⚡",
     "████████░░ Hard",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
    # Wk 20
    ("🔬 Grad-CAM &amp; XAI",
     "Visualise exactly what the CNN is looking at",
     "PyTorch &bull; OpenCV &bull; SHAP",
     "Black box? Not anymore 🔬",
     "███████░░░ Medium",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
    # Wk 21
    ("🤝 SimCLR Self-Supervised",
     "Contrastive learning — no labels needed",
     "PyTorch &bull; TensorFlow",
     "Labels are overrated 🤫",
     "█████████░ Expert",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),
    # Wk 22
    ("🎯 Few-Shot Learning",
     "5-shot classification with Prototypical Networks",
     "PyTorch &bull; learn2learn",
     "Humans do it — machines can too 🧠",
     "██████████ Expert",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
    # Wk 23
    ("✂️ Model Pruning",
     "Cut 50% of weights, keep 99% of accuracy",
     "PyTorch &bull; TF Model Optimization",
     "Less is more, if done right ✂️",
     "████████░░ Hard",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
    # Wk 24
    ("🌍 ONNX Cross-Framework",
     "PyTorch → ONNX → TensorFlow — deploy anywhere",
     "ONNX &bull; TensorRT &bull; ONNX Runtime",
     "Train anywhere, deploy everywhere 🌍",
     "███████░░░ Medium",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),
    # Wk 25
    ("🏎️ TensorRT Turbo",
     "Optimise models for NVIDIA GPU inference",
     "TensorRT &bull; CUDA &bull; ONNX",
     "Speed is not a feature — it is a requirement 🏎️",
     "████████░░ Hard",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
    # Wk 26
    ("📲 TFLite Edge Deployment",
     "Deploy CV models on Android/Raspberry Pi",
     "TFLite &bull; ONNX Runtime &bull; CoreML",
     "AI in your pocket — no cloud needed 📲",
     "████████░░ Hard",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
    # Wk 27
    ("📈 WandB Experiment Lab",
     "Log, visualise &amp; compare 100 training runs",
     "WandB &bull; PyTorch &bull; TensorFlow",
     "If you cannot measure it, you cannot improve it 📈",
     "███████░░░ Medium",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),
    # Wk 28
    ("🎲 Optuna Tuning",
     "Bayesian hyperparameter search — stop guessing",
     "Optuna &bull; PyTorch &bull; Sklearn",
     "Bayesian optimisation &gt; grid search 🎲",
     "███████░░░ Medium",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
    # Wk 29
    ("🚂 Data Pipeline Pro",
     "Build blazing-fast tf.data + PyTorch DataLoader",
     "TF Data &bull; PyTorch DataLoader &bull; Albumentations",
     "Starving the GPU is a sin 🖥️",
     "███████░░░ Medium",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
    # Wk 30
    ("🎭 Advanced Augmentation",
     "Albumentations, CutMix, MixUp, RandAugment",
     "Albumentations &bull; torchvision &bull; TF",
     "Your data is never large enough — augment! 🎭",
     "███████░░░ Medium",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),
    # Wk 31
    ("🔍 Anomaly Detection",
     "AutoEncoder for industrial defect detection",
     "PyTorch &bull; TensorFlow &bull; OpenCV",
     "Find the needle in the haystack 🔍",
     "███████░░░ Medium",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
    # Wk 32
    ("🏥 Medical Imaging AI",
     "Chest X-ray diagnosis — DenseNet meets healthcare",
     "PyTorch &bull; TensorFlow &bull; MONAI",
     "AI that saves lives 🏥",
     "█████████░ Expert",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
    # Wk 33
    ("🌐 3D Vision PointNet",
     "Point cloud classification &amp; segmentation",
     "PyTorch &bull; Open3D &bull; NumPy",
     "3D world, 3D understanding 🌐",
     "█████████░ Expert",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),
    # Wk 34
    ("🖼️ Neural Style Transfer",
     "Gram matrix magic — turn photos into artwork",
     "PyTorch &bull; TensorFlow &bull; PIL",
     "Every photo can be a Picasso 🎨",
     "███████░░░ Medium",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
    # Wk 35
    ("⬆️ Super Resolution GAN",
     "SRGAN — 4× upscaling with perceptual loss",
     "PyTorch &bull; TensorFlow",
     "Pixels are just the beginning 🔭",
     "████████░░ Hard",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
    # Wk 36
    ("🔐 Face Recognition",
     "ArcFace loss for high-accuracy face identification",
     "PyTorch &bull; InsightFace",
     "Every face tells a story — AI learns them all 🔐",
     "█████████░ Expert",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),
    # Wk 37
    ("🤸 Human Pose Estimation",
     "HRNet — body keypoint detection",
     "PyTorch &bull; OpenPose &bull; MMPose",
     "Understanding the human body, one keypoint at a time 🤸",
     "█████████░ Expert",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
    # Wk 38
    ("🎬 Video Classification",
     "TimeSformer — attention over space and time",
     "PyTorch &bull; TorchVideo",
     "Every frame is a word; every clip is a sentence 🎬",
     "█████████░ Expert",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
    # Wk 39
    ("🎯 Multi-Task Learning",
     "One backbone, detection + segmentation + classification",
     "PyTorch &bull; TensorFlow",
     "Why specialise when you can generalise? 🎯",
     "████████░░ Hard",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),
    # Wk 40
    ("🔒 Federated Learning",
     "Train across distributed devices — privacy preserved",
     "PySyft &bull; TensorFlow Federated",
     "Privacy-preserving AI for everyone 🔒",
     "█████████░ Expert",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
    # Wk 41
    ("🤖 Neural Architecture Search",
     "AutoML — let AI design the neural network",
     "PyTorch &bull; NAS-Bench &bull; Optuna",
     "When AI designs AI 🤯",
     "██████████ Expert",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
    # Wk 42
    ("🏆 Model Ensembles",
     "Stacking, blending &amp; boosting — squeeze every 0.1%",
     "PyTorch &bull; Sklearn &bull; XGBoost",
     "The whole is greater than the sum of its parts 🏆",
     "████████░░ Hard",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),
    # Wk 43
    ("⚡ MoCo Contrastive",
     "Momentum Contrast v3 — self-supervised powerhouse",
     "PyTorch &bull; TensorFlow",
     "Push negatives apart, pull positives together ⚡",
     "█████████░ Expert",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
    # Wk 44
    ("🌌 Zero-Shot Generalisation",
     "Classify classes never seen during training",
     "PyTorch &bull; HuggingFace CLIP",
     "Generalise to the unknown 🌌",
     "██████████ Expert",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
    # Wk 45
    ("🎮 Deep Reinforcement Learning",
     "Deep Q-Networks — AI that learns by playing games",
     "PyTorch &bull; Gym &bull; Stable-Baselines3",
     "Reward + punishment = superintelligence 🎮",
     "█████████░ Expert",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),
    # Wk 46
    ("📡 Stereo Depth Estimation",
     "Stereo vision — 3D world from 2 cameras",
     "PyTorch &bull; OpenCV &bull; Open3D",
     "Two eyes are better than one 👀",
     "█████████░ Expert",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
    # Wk 47
    ("🧬 Capsule Networks",
     "Hinton's dynamic routing — the future of CNNs?",
     "PyTorch &bull; TensorFlow",
     "Routing by agreement — smarter than pooling 🧬",
     "██████████ Expert",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
    # Wk 48
    ("🌊 Swin Transformer",
     "Shifted window attention — hierarchical vision",
     "PyTorch &bull; MMDetection",
     "Locality + globality = perfection 🌊",
     "██████████ Expert",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),
    # Wk 49
    ("🔭 DETR Detection Transformer",
     "End-to-end detection — no anchors, no NMS",
     "PyTorch &bull; HuggingFace",
     "Detection without hand-crafted components 🔭",
     "██████████ Expert",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
    # Wk 50
    ("🎭 Mask R-CNN",
     "Instance segmentation — detect and mask simultaneously",
     "PyTorch &bull; Detectron2",
     "Segment everything — paint every instance 🎭",
     "█████████░ Expert",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
    # Wk 51
    ("🏆 Kaggle Gold Mission",
     "Top 10% finish in a computer vision competition",
     "PyTorch &bull; TensorFlow &bull; Ensemble",
     "Competition is the ultimate teacher 🏆",
     "██████████ Legendary",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),
    # Wk 52
    ("🌟 Year-End Showcase",
     "Ship the complete DL Model Zoo to GitHub",
     "Git &bull; GitHub &bull; Python &bull; Markdown",
     "Done is better than perfect — SHIP IT! 🚢",
     "██████████ Legendary",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
]


TEMPLATE = """\
<!-- WEEKLY:START -->
<table>
<tr>
<td valign="top" width="62%">
<h3>{title}</h3>
<p>
🎯 <b>Quest:</b> {quest}<br/>
🔧 <b>Stack:</b> {stack}<br/>
📊 <b>Difficulty:</b> {diff}<br/>
💬 <i>{quote}</i>
</p>
<p>
<img src="https://img.shields.io/badge/Mission-Week%20{week}%20%2F%2052-ff6b6b?style=flat-square"/>
&nbsp;
<img src="https://img.shields.io/badge/Status-Active%20%F0%9F%94%A5-success?style=flat-square"/>
</p>
</td>
<td valign="top" width="38%" align="center">
<img src="{gif}" width="220"/>
</td>
</tr>
</table>
<!-- WEEKLY:END -->"""


def get_mission():
    today     = date.today()
    weeks     = max(0, (today - START_DATE).days // 7)
    idx       = weeks % len(MISSIONS)
    week_disp = (weeks % 52) + 1
    m         = MISSIONS[idx]
    return week_disp, m


def build_block(week_num, mission):
    title, quest, stack, quote, diff, gif = mission
    return TEMPLATE.format(
        title=title, quest=quest, stack=stack,
        quote=quote, diff=diff, gif=gif, week=week_num,
    )


def update_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    week_num, mission = get_mission()
    block   = build_block(week_num, mission)
    pattern = r"<!-- WEEKLY:START -->.*?<!-- WEEKLY:END -->"
    updated = re.sub(pattern, block, content, flags=re.DOTALL)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated)

    print(f"README updated — Week {week_num}: {mission[0]}")


if __name__ == "__main__":
    update_readme()
