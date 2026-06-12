#!/usr/bin/env python3
"""Weekly profile README updater — auto-runs every Sunday via GitHub Actions."""
import re
from datetime import date

START_DATE = date(2026, 6, 15)   # first Sunday after deploy

# ── 52 missions (loops for year 2) ──────────────────────────────────────────
# (title, quest, stack, quote, difficulty_bar, gif_url)
MISSIONS = [
    # Wk 1
    ("EfficientNet Mastery",
     "Compound-scale EfficientNetB0&ndash;B7 from scratch",
     "PyTorch &bull; TensorFlow &bull; Keras",
     "Scale width, depth &amp; resolution together",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9617;&#9617; Hard",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
    # Wk 2
    ("ResNet Revolution",
     "Build ResNet-18/34/50/101/152 with skip connections",
     "PyTorch &bull; TensorFlow",
     "Residual learning &mdash; the idea that changed everything",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9617;&#9617; Hard",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
    # Wk 3
    ("DenseNet Deep Dive",
     "Connect every layer to every other layer (DenseNet121/169/201)",
     "PyTorch &bull; TensorFlow",
     "Dense connections, dense knowledge",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9617;&#9617; Hard",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),
    # Wk 4
    ("ConvNeXt Chronicles",
     "Modernise ResNet into ConvNeXt T/S/B/L/XL",
     "PyTorch &bull; TensorFlow",
     "What if ResNet was born in the transformer era?",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9617; Expert",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
    # Wk 5
    ("Vision Transformer Voyage",
     "ViT-B/16 &mdash; patches are all you need",
     "PyTorch &bull; JAX",
     "Attention beats convolutions? Challenge accepted!",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608; Expert",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
    # Wk 6
    ("MobileNet Magic",
     "Depthwise separable convolutions for edge devices",
     "TFLite &bull; PyTorch",
     "Big brains, tiny footprint",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9617;&#9617;&#9617; Medium",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),
    # Wk 7
    ("EfficientNetV2 Explorer",
     "Fused-MBConv + progressive training (B0&ndash;B3, S/M/L)",
     "TensorFlow &bull; PyTorch",
     "Faster, smaller, stronger",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9617; Expert",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
    # Wk 8
    ("Inception &amp; Xception",
     "InceptionV3 + Xception depthwise separable magic",
     "TensorFlow &bull; Keras",
     "Inception: thinking inside the block",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9617;&#9617; Hard",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
    # Wk 9
    ("GAN Genesis",
     "Train DCGAN to generate photorealistic images",
     "PyTorch &bull; TensorFlow",
     "Teaching machines to hallucinate beautifully",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9617;&#9617; Hard",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),
    # Wk 10
    ("Diffusion Model Dreams",
     "Implement DDPM &mdash; noise to beauty step by step",
     "PyTorch &bull; Diffusers",
     "Reverse the entropy, reveal the art",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608; Expert",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
    # Wk 11
    ("Attention Is All You Need",
     "Implement multi-head self-attention from scratch",
     "PyTorch &bull; NumPy",
     "One mechanism to rule them all",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9617; Expert",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
    # Wk 12
    ("CLIP Challenge",
     "Contrastive Language-Image Pretraining",
     "PyTorch &bull; HuggingFace",
     "Images and words &mdash; same latent space",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9617; Expert",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),
    # Wk 13
    ("YOLO Speed Run",
     "Real-time object detection &mdash; YOLOv8 from paper to code",
     "PyTorch &bull; OpenCV",
     "You Only Look Once &mdash; but see everything",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9617; Expert",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
    # Wk 14
    ("Faster R-CNN",
     "Region proposal networks for object detection",
     "PyTorch &bull; torchvision",
     "Find it. Box it. Classify it.",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9609;&#9617; Expert",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
    # Wk 15
    ("U-Net Architect",
     "Encoder-decoder segmentation &mdash; every pixel matters",
     "PyTorch &bull; TensorFlow",
     "Semantics in every single pixel",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9617;&#9617; Hard",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),
    # Wk 16
    ("Semantic Segmentation",
     "DeepLab v3+ atrous convolutions for scene parsing",
     "TensorFlow &bull; PyTorch",
     "Understand the scene, pixel by pixel",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9609;&#9617; Expert",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
    # Wk 17
    ("Transfer Learning Master",
     "Fine-tune ImageNet models on custom datasets",
     "TF Hub &bull; PyTorch Hub",
     "Stand on the shoulders of giants",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9617;&#9617;&#9617; Medium",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
    # Wk 18
    ("Knowledge Distillation",
     "Compress a ResNet-50 teacher into MobileNet student",
     "PyTorch &bull; TensorFlow",
     "The student learns what the teacher earned",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9617;&#9617; Hard",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),
    # Wk 19
    ("Mixed Precision Training",
     "FP16 AMP &mdash; 2x speed, same accuracy",
     "PyTorch AMP &bull; TF mixed_precision",
     "Fast, furious &amp; accurate",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9617;&#9617; Hard",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
    # Wk 20
    ("Grad-CAM &amp; Explainability",
     "Visualise exactly what the CNN is looking at",
     "PyTorch &bull; OpenCV &bull; SHAP",
     "Black box? Not anymore",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9617;&#9617;&#9617; Medium",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
    # Wk 21
    ("SimCLR Self-Supervised",
     "Contrastive learning &mdash; no labels needed",
     "PyTorch &bull; TensorFlow",
     "Labels are overrated",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9609;&#9617; Expert",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),
    # Wk 22
    ("Few-Shot Learning",
     "5-shot classification with Prototypical Networks",
     "PyTorch &bull; learn2learn",
     "Humans do it &mdash; machines can too",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608; Expert",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
    # Wk 23
    ("Model Pruning",
     "Cut 50% of weights, keep 99% of accuracy",
     "PyTorch &bull; TF Model Optimization",
     "Less is more, if done right",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9617;&#9617; Hard",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
    # Wk 24
    ("ONNX Cross-Framework",
     "PyTorch &rarr; ONNX &rarr; TensorFlow &mdash; deploy anywhere",
     "ONNX &bull; TensorRT &bull; ONNX Runtime",
     "Train anywhere, deploy everywhere",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9617;&#9617;&#9617; Medium",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),
    # Wk 25
    ("TensorRT Turbo",
     "Optimise models for NVIDIA GPU inference",
     "TensorRT &bull; CUDA &bull; ONNX",
     "Speed is not a feature &mdash; it is a requirement",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9617;&#9617; Hard",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
    # Wk 26
    ("TFLite Edge Deployment",
     "Deploy CV models on Android &amp; Raspberry Pi",
     "TFLite &bull; ONNX Runtime &bull; CoreML",
     "AI in your pocket &mdash; no cloud needed",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9617;&#9617; Hard",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
    # Wk 27
    ("WandB Experiment Lab",
     "Log, visualise &amp; compare 100 training runs",
     "WandB &bull; PyTorch &bull; TensorFlow",
     "If you cannot measure it, you cannot improve it",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9617;&#9617;&#9617; Medium",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),
    # Wk 28
    ("Optuna Hyperparameter Tuning",
     "Bayesian optimisation &mdash; stop guessing, start tuning",
     "Optuna &bull; PyTorch &bull; Sklearn",
     "Bayesian beats grid search every time",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9617;&#9617;&#9617; Medium",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
    # Wk 29
    ("Data Pipeline Pro",
     "Build blazing-fast tf.data + PyTorch DataLoader",
     "TF Data &bull; PyTorch DataLoader &bull; Albumentations",
     "Starving the GPU is a sin",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9617;&#9617;&#9617; Medium",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
    # Wk 30
    ("Advanced Augmentation",
     "Albumentations, CutMix, MixUp, RandAugment",
     "Albumentations &bull; torchvision &bull; TF",
     "Your data is never large enough &mdash; augment!",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9617;&#9617;&#9617; Medium",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),
    # Wk 31
    ("Anomaly Detection",
     "AutoEncoder for industrial defect detection",
     "PyTorch &bull; TensorFlow &bull; OpenCV",
     "Find the needle in the haystack",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9617;&#9617;&#9617; Medium",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
    # Wk 32
    ("Medical Imaging AI",
     "Chest X-ray diagnosis &mdash; DenseNet meets healthcare",
     "PyTorch &bull; TensorFlow &bull; MONAI",
     "AI that saves lives",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9609;&#9617; Expert",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
    # Wk 33
    ("3D Vision &amp; PointNet",
     "Point cloud classification &amp; segmentation",
     "PyTorch &bull; Open3D &bull; NumPy",
     "3D world, 3D understanding",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9609;&#9617; Expert",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),
    # Wk 34
    ("Neural Style Transfer",
     "Gram matrix magic &mdash; turn photos into artwork",
     "PyTorch &bull; TensorFlow &bull; PIL",
     "Every photo can be a Picasso",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9617;&#9617;&#9617; Medium",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
    # Wk 35
    ("Super Resolution GAN",
     "SRGAN &mdash; 4x upscaling with perceptual loss",
     "PyTorch &bull; TensorFlow",
     "Pixels are just the beginning",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9617;&#9617; Hard",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
    # Wk 36
    ("Face Recognition",
     "ArcFace loss for high-accuracy face identification",
     "PyTorch &bull; InsightFace",
     "Every face tells a story &mdash; AI learns them all",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9609;&#9617; Expert",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),
    # Wk 37
    ("Human Pose Estimation",
     "HRNet &mdash; body keypoint detection",
     "PyTorch &bull; OpenPose &bull; MMPose",
     "Understanding the human body, one keypoint at a time",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9609;&#9617; Expert",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
    # Wk 38
    ("Video Classification",
     "TimeSformer &mdash; attention over space and time",
     "PyTorch &bull; TorchVideo",
     "Every frame is a word; every clip is a sentence",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9609;&#9617; Expert",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
    # Wk 39
    ("Multi-Task Learning",
     "One backbone, detection + segmentation + classification",
     "PyTorch &bull; TensorFlow",
     "Why specialise when you can generalise?",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9617;&#9617; Hard",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),
    # Wk 40
    ("Federated Learning",
     "Train across distributed devices &mdash; privacy preserved",
     "PySyft &bull; TensorFlow Federated",
     "Privacy-preserving AI for everyone",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9609;&#9617; Expert",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
    # Wk 41
    ("Neural Architecture Search",
     "AutoML &mdash; let AI design the neural network",
     "PyTorch &bull; NAS-Bench &bull; Optuna",
     "When AI designs AI",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608; Expert",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
    # Wk 42
    ("Model Ensembles",
     "Stacking, blending &amp; boosting &mdash; squeeze every 0.1%",
     "PyTorch &bull; Sklearn &bull; XGBoost",
     "The whole is greater than the sum of its parts",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9617;&#9617; Hard",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),
    # Wk 43
    ("MoCo Contrastive Learning",
     "Momentum Contrast v3 &mdash; self-supervised powerhouse",
     "PyTorch &bull; TensorFlow",
     "Push negatives apart, pull positives together",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9609;&#9617; Expert",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
    # Wk 44
    ("Zero-Shot Generalisation",
     "Classify classes never seen during training",
     "PyTorch &bull; HuggingFace CLIP",
     "Generalise to the unknown",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608; Expert",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
    # Wk 45
    ("Deep Reinforcement Learning",
     "Deep Q-Networks &mdash; AI that learns by playing games",
     "PyTorch &bull; Gym &bull; Stable-Baselines3",
     "Reward + punishment = superintelligence",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9609;&#9617; Expert",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),
    # Wk 46
    ("Stereo Depth Estimation",
     "Stereo vision &mdash; 3D world from 2 cameras",
     "PyTorch &bull; OpenCV &bull; Open3D",
     "Two eyes are better than one",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9609;&#9617; Expert",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
    # Wk 47
    ("Capsule Networks",
     "Hinton&#39;s dynamic routing &mdash; the future of CNNs?",
     "PyTorch &bull; TensorFlow",
     "Routing by agreement &mdash; smarter than pooling",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608; Expert",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
    # Wk 48
    ("Swin Transformer",
     "Shifted window attention &mdash; hierarchical vision",
     "PyTorch &bull; MMDetection",
     "Locality + globality = perfection",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608; Expert",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),
    # Wk 49
    ("DETR Detection Transformer",
     "End-to-end detection &mdash; no anchors, no NMS",
     "PyTorch &bull; HuggingFace",
     "Detection without hand-crafted components",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608; Expert",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
    # Wk 50
    ("Mask R-CNN",
     "Instance segmentation &mdash; detect and mask simultaneously",
     "PyTorch &bull; Detectron2",
     "Segment everything &mdash; paint every instance",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9609;&#9617; Expert",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
    # Wk 51
    ("Kaggle Gold Mission",
     "Top 10% finish in a computer vision competition",
     "PyTorch &bull; TensorFlow &bull; Ensemble",
     "Competition is the ultimate teacher",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608; Legendary",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),
    # Wk 52
    ("Year-End Showcase",
     "Ship the complete DL Model Zoo to GitHub",
     "Git &bull; GitHub &bull; Python &bull; Markdown",
     "Done is better than perfect &mdash; SHIP IT!",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608; Legendary",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),
]

# Emoji icons for each mission (cycles through 52)
ICONS = [
    "&#x26A1;","&#x1F517;","&#x1F33F;","&#x1F332;","&#x1F441;&#xFE0F;",
    "&#x1F4F1;","&#x1F680;","&#x1F3AD;","&#x1F3A8;","&#x2728;",
    "&#x1F9E0;","&#x1F309;","&#x26A1;","&#x1F4E6;","&#x1F9E9;",
    "&#x1F306;","&#x1F3D4;&#xFE0F;","&#x1F4DD;","&#x26A1;","&#x1F52C;",
    "&#x1F91D;","&#x1F3AF;","&#x2702;&#xFE0F;","&#x1F30D;","&#x1F3CE;&#xFE0F;",
    "&#x1F4F2;","&#x1F4C8;","&#x1F3B2;","&#x1F682;","&#x1F3AD;",
    "&#x1F50D;","&#x1F3E5;","&#x1F310;","&#x1F5BC;&#xFE0F;","&#x2B06;&#xFE0F;",
    "&#x1F510;","&#x1F93C;","&#x1F3AC;","&#x1F3AF;","&#x1F512;",
    "&#x1F916;","&#x1F3C6;","&#x26A1;","&#x1F30C;","&#x1F3AE;",
    "&#x1F4E1;","&#x1F9EC;","&#x1F30A;","&#x1F52D;","&#x1F3AD;",
    "&#x1F3C6;","&#x1F31F;",
]

TEMPLATE = """\
<!-- WEEKLY:START -->
<div align="center">
<table width="90%">
<tr>
<td valign="top" width="58%">
<h3>{icon} {title}</h3>
<p>
&#127919; <b>Quest:</b> {quest}<br/>
&#128296; <b>Stack:</b> {stack}<br/>
&#128202; <b>Difficulty:</b> {diff}<br/>
&#128172; <i>&quot;{quote}&quot;</i>
</p>
<p>
<img src="https://img.shields.io/badge/Week-{week}%20%2F%2052-ff6b6b?style=for-the-badge&amp;labelColor=161b22"/>
&nbsp;
<img src="https://img.shields.io/badge/Status-Active%20%F0%9F%94%A5-success?style=for-the-badge&amp;labelColor=161b22"/>
</p>
</td>
<td valign="middle" width="42%" align="center">
<img src="{gif}" width="260"/>
</td>
</tr>
</table>
</div>
<!-- WEEKLY:END -->"""


def get_mission():
    today     = date.today()
    weeks     = max(0, (today - START_DATE).days // 7)
    idx       = weeks % len(MISSIONS)
    week_disp = (weeks % 52) + 1
    return week_disp, MISSIONS[idx], ICONS[idx]


def build_block(week_num, mission, icon):
    title, quest, stack, quote, diff, gif = mission
    return TEMPLATE.format(
        icon=icon, title=title, quest=quest, stack=stack,
        quote=quote, diff=diff, gif=gif, week=week_num,
    )


def update_readme():
    import re
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    week_num, mission, icon = get_mission()
    block   = build_block(week_num, mission, icon)
    pattern = r"<!-- WEEKLY:START -->.*?<!-- WEEKLY:END -->"
    updated = re.sub(pattern, block, content, flags=re.DOTALL)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated)

    print(f"README updated — Week {week_num}: {mission[0]}")


if __name__ == "__main__":
    update_readme()
