#!/usr/bin/env python3
"""Weekly profile README updater — auto-runs every Sunday via GitHub Actions."""
import re
from datetime import date

START_DATE = date(2026, 6, 15)

# ── 12 deep-research missions (cycles through the year) ─────────────────────
# (title, quest, stack, topics, quote, difficulty_bar, gif_url)
MISSIONS = [

    # 1 ── TensorFlow Deep Dive
    ("TensorFlow Deep Dive",
     "Master TF2.x custom training loops, @tf.function, Keras subclassing &amp; TF Serving",
     "TensorFlow 2.x &bull; Keras &bull; TF Serving &bull; TFLite &bull; tf.data",
     "Custom Layers &bull; @tf.function &bull; SavedModel &bull; Mixed Precision &bull; TF Profiler",
     "Eager by default, graph when it truly matters",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9609;&#9617; Expert",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),

    # 2 ── PyTorch Powerhouse
    ("PyTorch Powerhouse",
     "Custom autograd engines, TorchScript, ONNX export &amp; distributed DDP training",
     "PyTorch &bull; TorchScript &bull; ONNX &bull; DDP &bull; W&amp;B &bull; PyTorch Hub",
     "Autograd &bull; Custom Datasets &bull; AMP &bull; DistributedDataParallel &bull; Profiler",
     "Dynamic graphs, infinite possibilities",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9609;&#9617; Expert",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),

    # 3 ── Model Translation
    ("Cross-Framework Model Translation",
     "Translate PyTorch &harr; TensorFlow models flawlessly via ONNX with full output validation",
     "ONNX &bull; onnx2tf &bull; torch.onnx &bull; tf2onnx &bull; Netron &bull; onnxruntime",
     "Layer Mapping &bull; Weight Transfer &bull; Op Compatibility &bull; Shape Validation &bull; Benchmark",
     "Train anywhere, deploy everywhere",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9617;&#9617; Hard",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),

    # 4 ── Model Conversion
    ("Model Conversion &amp; Optimization",
     "Build ONNX &rarr; TensorRT &rarr; TFLite pipeline with INT8 quantization for edge &amp; cloud",
     "TensorRT &bull; TFLite &bull; ONNX Runtime &bull; CoreML &bull; OpenVINO &bull; NCNN",
     "Post-Training Quantization &bull; Pruning &bull; FP16/INT8 &bull; Latency &bull; Memory Footprint",
     "Smaller model, bigger impact",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9609;&#9617; Expert",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),

    # 5 ── Custom Model Building
    ("Custom Architecture Engineering",
     "Design novel CNN &amp; Transformer hybrid architectures from scratch with full ablation studies",
     "PyTorch &bull; TensorFlow &bull; einops &bull; timm &bull; Torchinfo &bull; FLOPs counter",
     "Block Design &bull; Attention Mechanisms &bull; Skip Connections &bull; Normalization &bull; Scaling",
     "The best architecture is the one you design yourself",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9610; Expert",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),

    # 6 ── Paper Writing
    ("Research Paper Writing",
     "Author a complete IEEE &sol; arXiv paper &mdash; intro, methodology, experiments &amp; submission",
     "LaTeX &bull; Overleaf &bull; Matplotlib &bull; BibTeX &bull; IEEE Template &bull; arXiv",
     "Abstract &bull; Related Work &bull; Methodology &bull; Ablation Study &bull; Tables &bull; Figures",
     "Research not published is research half done",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9617;&#9617; Hard",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),

    # 7 ── Research Code Implementation
    ("SOTA Paper Implementation",
     "Reproduce a top-tier CVPR &sol; NeurIPS &sol; ICCV paper from scratch &mdash; code &amp; matched results",
     "PyTorch &bull; arXiv &bull; GitHub &bull; W&amp;B &bull; Paperswithcode &bull; Hydra Config",
     "Architecture Re-impl &bull; Loss Functions &bull; Training Recipe &bull; Metric Matching &bull; Ablation",
     "Show me the code, not just the theory",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9610; Expert",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),

    # 8 ── Low Light Image Enhancement
    ("Low Light Image Enhancement",
     "Implement Zero-DCE, RetinexNet &amp; LLFlow for extreme nighttime &amp; dark scene restoration",
     "PyTorch &bull; OpenCV &bull; PIL &bull; SSIM &bull; PSNR &bull; LPIPS &bull; LOL Dataset",
     "Zero-DCE &bull; RetinexNet &bull; LIME &bull; Noise Estimation &bull; Perceptual Loss &bull; BRISQUE",
     "Reveal what darkness hides",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9609;&#9617; Expert",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),

    # 9 ── Agricultural Research
    ("Agricultural AI Research",
     "Crop disease detection &amp; precision agriculture with multispectral drone &amp; satellite imagery",
     "PyTorch &bull; YOLOv8 &bull; OpenCV &bull; Albumentations &bull; NDVI &bull; Sentinel-2",
     "Disease Classification &bull; Yield Prediction &bull; Multispectral NDVI &bull; Semantic Segmentation",
     "Feed the world with intelligent vision",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9617;&#9617; Hard",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),

    # 10 ── Medical Research
    ("Medical Imaging AI",
     "Chest X-ray &amp; MRI diagnosis &mdash; U-Net segmentation meets DenseNet + Grad-CAM XAI",
     "PyTorch &bull; MONAI &bull; SimpleITK &bull; OpenCV &bull; DICOM &bull; nnU-Net",
     "Segmentation &bull; Classification &bull; Grad-CAM &bull; DICOM &bull; Class Imbalance &bull; Dice Loss",
     "AI that saves lives, one pixel at a time",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9609;&#9617; Expert",
     "https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif"),

    # 11 ── Spacecraft Image Processing
    ("Spacecraft Image Processing",
     "Satellite &amp; spacecraft image super-resolution, denoising &amp; change detection at global scale",
     "PyTorch &bull; GDAL &bull; rasterio &bull; OpenCV &bull; Sentinel Hub &bull; Google Earth Engine",
     "Super-Resolution &bull; Denoising &bull; Change Detection &bull; SAR &bull; Pansharpening &bull; NDWI",
     "See Earth and beyond with machine eyes",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9609;&#9617; Expert",
     "https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif"),

    # 12 ── NASA Dataset
    ("NASA Dataset Deep Learning",
     "Deep learning on NASA Earth &amp; space data &mdash; exoplanet transit detection &amp; aurora AI",
     "PyTorch &bull; NASA APIs &bull; Astropy &bull; FITS &bull; SpacePy &bull; Lightkurve",
     "FITS Processing &bull; Transit Photometry &bull; Anomaly Detection &bull; Time-Series &bull; Restoration",
     "The universe is the ultimate dataset",
     "&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9610; Legendary",
     "https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif"),
]

ICONS = [
    "&#x26A1;",           # 1  TensorFlow        — lightning
    "&#x1F525;",          # 2  PyTorch            — fire
    "&#x1F504;",          # 3  Model Translation  — arrows
    "&#x2699;&#xFE0F;",   # 4  Model Convert      — gear
    "&#x1F3D7;&#xFE0F;",  # 5  Custom Model       — building construction
    "&#x1F4DD;",          # 6  Paper Writing      — memo
    "&#x1F52C;",          # 7  Research Impl      — microscope
    "&#x1F319;",          # 8  Low Light          — crescent moon
    "&#x1F33E;",          # 9  Agricultural       — sheaf of rice
    "&#x1F3E5;",          # 10 Medical            — hospital
    "&#x1F680;",          # 11 Spacecraft         — rocket
    "&#x1F30C;",          # 12 NASA               — milky way
]

TEMPLATE = """\
<!-- WEEKLY:START -->
<div align="center">
<table width="90%">
<tr>
<td valign="top" width="60%">
<h3>{icon} {title}</h3>
<p>
&#127919; <b>Quest:</b> {quest}<br/>
&#128296; <b>Stack:</b> {stack}<br/>
&#128218; <b>Topics:</b> {topics}<br/>
&#128202; <b>Difficulty:</b> {diff}<br/>
&#128172; <i>&quot;{quote}&quot;</i>
</p>
<p>
<img src="https://img.shields.io/badge/Week-{week}%20%2F%2052-ff6b6b?style=for-the-badge&amp;labelColor=161b22"/>
&nbsp;
<img src="https://img.shields.io/badge/Status-Active%20%F0%9F%94%A5-success?style=for-the-badge&amp;labelColor=161b22"/>
</p>
</td>
<td valign="middle" width="40%" align="center">
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
    title, quest, stack, topics, quote, diff, gif = mission
    return TEMPLATE.format(
        icon=icon, title=title, quest=quest, stack=stack,
        topics=topics, quote=quote, diff=diff, gif=gif, week=week_num,
    )


def update_readme():
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
