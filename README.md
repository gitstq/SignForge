<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/Version-1.0.0-orange.svg" alt="v1.0.0">
  <img src="https://img.shields.io/badge/Tests-20%20Passed-brightgreen.svg" alt="Tests">
  <img src="https://img.shields.io/badge/Cross_Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg" alt="Cross Platform">
</p>

<h1 align="center">🔐 SignForge</h1>

<p align="center">
  <strong>Lightweight PDF Document Intelligent Signing & Stamping Engine</strong><br>
  轻量级PDF文档智能签名与盖章引擎
</p>

<p align="center">
  <a href="#-项目介绍">简体中文</a> ·
  <a href="#-簡介">繁體中文</a> ·
  <a href="#-introduction">English</a>
</p>

---

<a id="项目介绍"></a>

## 🎉 项目介绍

> **SignForge** 是一款纯Python实现的轻量级PDF文档智能签名与盖章命令行工具。灵感来源于DocuSeal等电子签名平台，但SignForge聚焦于**本地化、零依赖核心、CLI优先**的设计理念，为开发者提供简单高效的PDF签名、盖章、水印和验证能力。

### 🔥 解决的痛点

- **电子签名工具过于笨重**：现有方案多为Web平台，部署复杂、依赖繁多
- **本地化需求被忽视**：很多场景需要离线处理敏感PDF文档
- **批量处理能力缺失**：缺乏简单高效的批量签名/盖章/水印工具
- **印章制作门槛高**：没有简单易用的公章/印章生成工具

### ✨ 自研差异化亮点

- 🚀 **纯Python实现**：仅需PyPDF2、Pillow、reportlab三个轻量依赖
- 🎨 **印章生成器**：内置圆形/椭圆/方形/矩形印章模板，支持自定义文字和颜色
- 💧 **智能水印**：对角线/水平/平铺三种水印样式，支持透明度和旋转
- 🔍 **完整性验证**：PDF文件哈希校验、元数据提取、文件对比
- 📦 **批量处理**：一键批量添加水印，支持目录级操作
- 🌍 **跨平台**：Windows、macOS、Linux全平台兼容

---

<a id="核心特性"></a>

## ✨ 核心特性

| 功能 | 描述 | 命令 |
|---|---|---|
| 📝 **PDF签名** | 在PDF任意位置叠加手写签名图片，支持透明度和尺寸调整 | `signforge sign` |
| 🔴 **印章生成** | 一键生成圆形/椭圆/方形/矩形公章，支持自定义文字和颜色 | `signforge stamp` |
| 💧 **智能水印** | 对角线/水平/平铺水印，支持文字和图片两种模式 | `signforge watermark` |
| 🔍 **完整性验证** | PDF哈希校验、元数据提取、签名注解检测、文件对比 | `signforge verify` |
| 📄 **文档信息** | 提取PDF页数、尺寸、元数据、文本统计等详细信息 | `signforge info` |
| 📦 **批量处理** | 目录级批量添加水印，支持通配符匹配 | `signforge batch` |

---

<a id="快速开始"></a>

## 🚀 快速开始

### 📋 环境要求

- **Python** >= 3.8
- **操作系统**：Windows / macOS / Linux

### 📦 安装

```bash
# 通过pip安装（推荐）
pip install signforge

# 或从源码安装
git clone https://github.com/gitstq/SignForge.git
cd SignForge
pip install .
```

### 🛠️ 安装依赖

```bash
pip install PyPDF2 Pillow reportlab
```

### ⚡ 快速使用

```bash
# 1. 在PDF上签名
signforge sign document.pdf --sig signature.png --page 1 --x 100 --y 100

# 2. 创建并应用公章
signforge stamp document.pdf --text "某某科技有限公司" --style circle --page -1

# 3. 添加对角线水印
signforge watermark document.pdf --text "机密文件" --style diagonal --opacity 0.2

# 4. 验证PDF完整性
signforge verify document.pdf

# 5. 查看PDF信息
signforge info document.pdf

# 6. 批量添加水印
signforge batch watermark ./documents --text "草稿" --output ./output
```

---

<a id="详细使用指南"></a>

## 📖 详细使用指南

### 📝 PDF签名 (`sign`)

在PDF指定位置添加手写签名图片：

```bash
# 基本签名（最后一页）
signforge sign contract.pdf --sig my_signature.png

# 指定页码和位置
signforge sign contract.pdf --sig my_signature.png --page 1 --x 350 --y 150

# 自定义签名大小和透明度
signforge sign contract.pdf --sig my_signature.png --width 200 --height 80 --opacity 0.8

# 签名所有页面
signforge sign contract.pdf --sig my_signature.png --all-pages

# 指定输出路径
signforge sign contract.pdf --sig my_signature.png -o signed_contract.pdf
```

**参数说明：**

| 参数 | 说明 | 默认值 |
|---|---|---|
| `--sig` | 签名图片路径（推荐PNG透明背景） | 必填 |
| `--page` | 页码（1起算，-1为最后一页） | -1 |
| `--x` | X坐标（磅，从左侧算起） | 100 |
| `--y` | Y坐标（磅，从底部算起） | 100 |
| `--width` | 签名宽度（磅） | 150 |
| `--height` | 签名高度（磅） | 自动按比例 |
| `--opacity` | 透明度（0.0-1.0） | 1.0 |
| `--all-pages` | 签名所有页面 | false |

### 🔴 印章生成与盖章 (`stamp`)

```bash
# 创建圆形公章并盖章
signforge stamp contract.pdf --text "某某科技有限公司" --sub-text "合同专用章"

# 椭圆形章
signforge stamp contract.pdf --text "财务部" --style oval --color blue

# 方形审批章
signforge stamp approval.pdf --text "已审批" --style rectangle --color red --size 150

# 保存印章模板
signforge stamp contract.pdf --text "公司公章" --save-template company_seal

# 使用已有印章图片
signforge stamp contract.pdf --stamp-image ./templates/company_seal.png
```

**印章样式：**

| 样式 | 说明 | 适用场景 |
|---|---|---|
| `circle` | 圆形章（默认） | 公司公章、合同章 |
| `oval` | 椭圆形章 | 部门章、财务章 |
| `rectangle` | 矩形章 | 审批章、验讫章 |
| `square` | 方形章 | 专用章、备案章 |

### 💧 水印添加 (`watermark`)

```bash
# 对角线文字水印
signforge watermark report.pdf --text "机密" --style diagonal --opacity 0.15

# 水平居中水印
signforge watermark report.pdf --text "样本" --style horizontal --font-size 60

# 平铺水印（全页覆盖）
signforge watermark report.pdf --text "内部文件" --style tiled --opacity 0.1

# 图片水印
signforge watermark photo.pdf --image watermark_logo.png --opacity 0.3

# 仅对指定页面添加水印
signforge watermark report.pdf --text "草稿" --pages 1,3,5
```

### 🔍 PDF验证 (`verify`)

```bash
# 基本验证
signforge verify contract.pdf

# JSON格式输出
signforge verify contract.pdf --json

# 与另一文件对比
signforge verify signed.pdf --compare original.pdf
```

### 📄 PDF信息 (`info`)

```bash
# 查看PDF详细信息
signforge info document.pdf

# JSON格式输出
signforge info document.pdf --json
```

### 📦 批量处理 (`batch`)

```bash
# 批量添加水印
signforge batch watermark ./contracts --text "合同副本" --output ./watermarked

# 自定义文件匹配模式
signforge batch watermark ./docs --text "DRAFT" --pattern "*.pdf" --output ./output
```

---

<a id="设计思路与迭代规划"></a>

## 💡 设计思路与迭代规划

### 🎯 设计理念

1. **CLI优先**：命令行工具，易于集成到自动化流程和CI/CD管道
2. **零重型依赖**：仅依赖三个成熟的Python库，安装快速、环境干净
3. **本地化处理**：所有操作在本地完成，不上传任何文件到云端，保护隐私
4. **模块化架构**：签名、盖章、水印、验证四大模块独立解耦，可单独使用

### 🛠️ 技术选型

| 组件 | 选型 | 原因 |
|---|---|---|
| PDF读写 | PyPDF2 | 纯Python，轻量稳定，社区活跃 |
| 图像处理 | Pillow | Python图像处理事实标准 |
| PDF生成 | reportlab | 强大的PDF生成能力，支持图像叠加 |
| CLI框架 | argparse | Python标准库，零额外依赖 |

### 🗺️ 后续迭代计划

- [ ] **v1.1**：添加PDF页面提取、合并、拆分功能
- [ ] **v1.2**：支持数字签名（PKCS#7）和时间戳
- [ ] **v1.3**：添加TUI交互界面（基于textual）
- [ ] **v2.0**：支持Web界面（FastAPI + Vue.js）
- [ ] **v2.1**：OCR识别签名字段自动定位

---

<a id="打包与部署指南"></a>

## 📦 打包与部署指南

### 🐍 作为Python包安装

```bash
pip install signforge
```

### 📁 从源码运行

```bash
git clone https://github.com/gitstq/SignForge.git
cd SignForge
pip install -r requirements.txt
python -m signforge.cli --help
```

### 🔧 开发模式

```bash
git clone https://github.com/gitstq/SignForge.git
cd SignForge
pip install -e ".[dev]"
python -m pytest tests/
```

### 🐳 Docker部署（规划中）

```dockerfile
FROM python:3.11-slim
RUN pip install signforge
ENTRYPOINT ["signforge"]
```

---

<a id="贡献指南"></a>

## 🤝 贡献指南

欢迎贡献代码！请遵循以下规范：

1. **Fork** 本仓库
2. 创建功能分支：`git checkout -b feat/your-feature`
3. 编写代码并添加测试
4. 确保测试通过：`python -m pytest tests/`
5. 提交代码：`git commit -m "feat: 添加某功能"`
6. 推送并创建 **Pull Request**

提交规范：`feat:` / `fix:` / `docs:` / `refactor:` / `test:`

详见 [CONTRIBUTING.md](CONTRIBUTING.md)

---

<a id="开源协议"></a>

## 📄 开源协议

本项目基于 [MIT License](LICENSE) 开源，可自由使用、修改和分发。

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">SignForge Team</a>
</p>

---

<a id="簡介"></a>

## 🎉 簡介

> **SignForge** 是一款純Python實現的輕量級PDF文件智慧簽名與蓋章命令列工具。靈感來源於DocuSeal等電子簽名平台，但SignForge聚焦於**本地化、零依賴核心、CLI優先**的設計理念，為開發者提供簡單高效的PDF簽名、蓋章、浮水印和驗證能力。

### 🔥 解決的痛點

- **電子簽名工具過於笨重**：現有方案多為Web平台，部署複雜、依賴繁多
- **本地化需求被忽視**：很多場景需要離線處理敏感PDF文件
- **批次處理能力缺失**：缺乏簡單高效的批次簽名/蓋章/浮水印工具
- **印章製作門檻高**：沒有簡單易用的公章/印章生成工具

### ✨ 自研差異化亮點

- 🚀 **純Python實現**：僅需PyPDF2、Pillow、reportlab三個輕量依賴
- 🎨 **印章生成器**：內建圓形/橢圓/方形/矩形印章模板，支援自訂文字和顏色
- 💧 **智慧浮水印**：對角線/水平/平鋪三種浮水印樣式，支援透明度和旋轉
- 🔍 **完整性驗證**：PDF檔案雜湊校驗、元資料提取、檔案對比
- 📦 **批次處理**：一鍵批次新增浮水印，支援目錄級操作
- 🌍 **跨平台**：Windows、macOS、Linux全平台相容

---

<a id="核心特性-1"></a>

## ✨ 核心特性

| 功能 | 描述 | 指令 |
|---|---|---|
| 📝 **PDF簽名** | 在PDF任意位置疊加手寫簽名圖片，支援透明度和尺寸調整 | `signforge sign` |
| 🔴 **印章生成** | 一鍵生成圓形/橢圓/方形/矩形公章，支援自訂文字和顏色 | `signforge stamp` |
| 💧 **智慧浮水印** | 對角線/水平/平鋪浮水印，支援文字和圖片兩種模式 | `signforge watermark` |
| 🔍 **完整性驗證** | PDF雜湊校驗、元資料提取、簽名註解偵測、檔案對比 | `signforge verify` |
| 📄 **文件資訊** | 提取PDF頁數、尺寸、元資料、文字統計等詳細資訊 | `signforge info` |
| 📦 **批次處理** | 目錄級批次新增浮水印，支援萬用字元匹配 | `signforge batch` |

---

<a id="快速開始-1"></a>

## 🚀 快速開始

### 📋 環境要求

- **Python** >= 3.8
- **作業系統**：Windows / macOS / Linux

### 📦 安裝

```bash
# 透過pip安裝（推薦）
pip install signforge

# 或從原始碼安裝
git clone https://github.com/gitstq/SignForge.git
cd SignForge
pip install .
```

### ⚡ 快速使用

```bash
# 1. 在PDF上簽名
signforge sign document.pdf --sig signature.png --page 1 --x 100 --y 100

# 2. 建立並應用公章
signforge stamp document.pdf --text "某某科技有限公司" --style circle --page -1

# 3. 新增對角線浮水印
signforge watermark document.pdf --text "機密文件" --style diagonal --opacity 0.2

# 4. 驗證PDF完整性
signforge verify document.pdf

# 5. 查看PDF資訊
signforge info document.pdf

# 6. 批次新增浮水印
signforge batch watermark ./documents --text "草稿" --output ./output
```

---

<a id="詳細使用指南-1"></a>

## 📖 詳細使用指南

### 📝 PDF簽名 (`sign`)

```bash
# 基本簽名（最後一頁）
signforge sign contract.pdf --sig my_signature.png

# 指定頁碼和位置
signforge sign contract.pdf --sig my_signature.png --page 1 --x 350 --y 150

# 自訂簽名大小和透明度
signforge sign contract.pdf --sig my_signature.png --width 200 --height 80 --opacity 0.8

# 簽名所有頁面
signforge sign contract.pdf --sig my_signature.png --all-pages
```

### 🔴 印章生成與蓋章 (`stamp`)

```bash
# 建立圓形公章並蓋章
signforge stamp contract.pdf --text "某某科技有限公司" --sub-text "合同專用章"

# 橢圓形章
signforge stamp contract.pdf --text "財務部" --style oval --color blue

# 方形審批章
signforge stamp approval.pdf --text "已審批" --style rectangle --color red

# 儲存印章模板
signforge stamp contract.pdf --text "公司公章" --save-template company_seal
```

### 💧 浮水印新增 (`watermark`)

```bash
# 對角線文字浮水印
signforge watermark report.pdf --text "機密" --style diagonal --opacity 0.15

# 平鋪浮水印（全頁覆蓋）
signforge watermark report.pdf --text "內部文件" --style tiled --opacity 0.1

# 圖片浮水印
signforge watermark photo.pdf --image watermark_logo.png --opacity 0.3
```

### 🔍 PDF驗證 (`verify`)

```bash
# 基本驗證
signforge verify contract.pdf

# 與另一檔案對比
signforge verify signed.pdf --compare original.pdf
```

---

<a id="貢獻指南-1"></a>

## 🤝 貢獻指南

歡迎貢獻程式碼！請遵循以下規範：

1. **Fork** 本倉庫
2. 建立功能分支：`git checkout -b feat/your-feature`
3. 撰寫程式碼並新增測試
4. 確保測試通過：`python -m pytest tests/`
5. 提交程式碼：`git commit -m "feat: 新增某功能"`
6. 推送並建立 **Pull Request**

詳見 [CONTRIBUTING.md](CONTRIBUTING.md)

---

<a id="開源協議-1"></a>

## 📄 開源協議

本專案基於 [MIT License](LICENSE) 開源，可自由使用、修改和分發。

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">SignForge Team</a>
</p>

---

<a id="introduction"></a>

## 🎉 Introduction

> **SignForge** is a lightweight, pure-Python CLI tool for intelligent PDF document signing and stamping. Inspired by platforms like DocuSeal, SignForge focuses on a **local-first, minimal-dependency, CLI-first** design philosophy, providing developers with simple yet powerful PDF signing, stamping, watermarking, and verification capabilities.

### 🔥 Problems We Solve

- **Existing e-signature tools are too heavy**: Most solutions are web platforms with complex deployments and numerous dependencies
- **Local processing needs are ignored**: Many scenarios require offline processing of sensitive PDF documents
- **Batch processing is lacking**: No simple and efficient batch signing/stamping/watermarking tools
- **Seal creation has high barriers**: No easy-to-use official seal/stamp generation tools

### ✨ Differentiation Highlights

- 🚀 **Pure Python**: Only 3 lightweight dependencies (PyPDF2, Pillow, reportlab)
- 🎨 **Stamp Generator**: Built-in circle/oval/rectangle/square stamp templates with custom text and colors
- 💧 **Smart Watermarks**: Diagonal/horizontal/tiled watermark styles with opacity and rotation support
- 🔍 **Integrity Verification**: PDF hash verification, metadata extraction, file comparison
- 📦 **Batch Processing**: One-click batch watermarking with directory-level operations
- 🌍 **Cross-Platform**: Full compatibility with Windows, macOS, and Linux

---

<a id="core-features"></a>

## ✨ Core Features

| Feature | Description | Command |
|---|---|---|
| 📝 **PDF Signing** | Overlay handwritten signatures at any position with opacity and size control | `signforge sign` |
| 🔴 **Stamp Creation** | Generate circle/oval/rectangle/square official seals with custom text and colors | `signforge stamp` |
| 💧 **Smart Watermark** | Diagonal/horizontal/tiled watermarks in text or image mode | `signforge watermark` |
| 🔍 **Verification** | PDF hash check, metadata extraction, signature annotation detection, file comparison | `signforge verify` |
| 📄 **Document Info** | Extract page count, dimensions, metadata, text statistics | `signforge info` |
| 📦 **Batch Processing** | Directory-level batch watermarking with glob pattern support | `signforge batch` |

---

<a id="quick-start"></a>

## 🚀 Quick Start

### 📋 Requirements

- **Python** >= 3.8
- **OS**: Windows / macOS / Linux

### 📦 Installation

```bash
# Install via pip (recommended)
pip install signforge

# Or install from source
git clone https://github.com/gitstq/SignForge.git
cd SignForge
pip install .
```

### ⚡ Usage

```bash
# 1. Sign a PDF
signforge sign document.pdf --sig signature.png --page 1 --x 100 --y 100

# 2. Create and apply an official seal
signforge stamp document.pdf --text "ACME Corporation" --style circle --page -1

# 3. Add a diagonal watermark
signforge watermark document.pdf --text "CONFIDENTIAL" --style diagonal --opacity 0.2

# 4. Verify PDF integrity
signforge verify document.pdf

# 5. Get PDF information
signforge info document.pdf

# 6. Batch watermark
signforge batch watermark ./documents --text "DRAFT" --output ./output
```

---

<a id="usage-guide"></a>

## 📖 Usage Guide

### 📝 PDF Signing (`sign`)

```bash
# Basic signing (last page)
signforge sign contract.pdf --sig my_signature.png

# Specify page and position
signforge sign contract.pdf --sig my_signature.png --page 1 --x 350 --y 150

# Custom size and opacity
signforge sign contract.pdf --sig my_signature.png --width 200 --height 80 --opacity 0.8

# Sign all pages
signforge sign contract.pdf --sig my_signature.png --all-pages

# Specify output path
signforge sign contract.pdf --sig my_signature.png -o signed_contract.pdf
```

**Parameters:**

| Parameter | Description | Default |
|---|---|---|
| `--sig` | Signature image path (PNG with transparency recommended) | Required |
| `--page` | Page number (1-based, -1 for last) | -1 |
| `--x` | X position (points from left) | 100 |
| `--y` | Y position (points from bottom) | 100 |
| `--width` | Signature width (points) | 150 |
| `--height` | Signature height (points) | Auto aspect ratio |
| `--opacity` | Opacity (0.0-1.0) | 1.0 |
| `--all-pages` | Sign all pages | false |

### 🔴 Stamp Creation & Application (`stamp`)

```bash
# Create circular seal and stamp
signforge stamp contract.pdf --text "ACME Corporation" --sub-text "OFFICIAL SEAL"

# Oval seal
signforge stamp contract.pdf --text "Finance Dept" --style oval --color blue

# Rectangle approval stamp
signforge stamp approval.pdf --text "APPROVED" --style rectangle --color red --size 150

# Save stamp template
signforge stamp contract.pdf --text "Company Seal" --save-template company_seal

# Use existing stamp image
signforge stamp contract.pdf --stamp-image ./templates/company_seal.png
```

**Stamp Styles:**

| Style | Description | Use Case |
|---|---|---|
| `circle` | Circular seal (default) | Company seal, contract seal |
| `oval` | Oval seal | Department seal, finance seal |
| `rectangle` | Rectangle stamp | Approval stamp, verification stamp |
| `square` | Square stamp | Special purpose seal |

### 💧 Watermarking (`watermark`)

```bash
# Diagonal text watermark
signforge watermark report.pdf --text "CONFIDENTIAL" --style diagonal --opacity 0.15

# Horizontal centered watermark
signforge watermark report.pdf --text "SAMPLE" --style horizontal --font-size 60

# Tiled watermark (full page coverage)
signforge watermark report.pdf --text "INTERNAL" --style tiled --opacity 0.1

# Image watermark
signforge watermark photo.pdf --image watermark_logo.png --opacity 0.3

# Watermark specific pages only
signforge watermark report.pdf --text "DRAFT" --pages 1,3,5
```

### 🔍 PDF Verification (`verify`)

```bash
# Basic verification
signforge verify contract.pdf

# JSON output
signforge verify contract.pdf --json

# Compare with another file
signforge verify signed.pdf --compare original.pdf
```

### 📄 PDF Information (`info`)

```bash
# View detailed PDF info
signforge info document.pdf

# JSON output
signforge info document.pdf --json
```

### 📦 Batch Processing (`batch`)

```bash
# Batch watermark
signforge batch watermark ./contracts --text "COPY" --output ./watermarked

# Custom file pattern
signforge batch watermark ./docs --text "DRAFT" --pattern "*.pdf" --output ./output
```

---

<a id="design-roadmap"></a>

## 💡 Design Philosophy & Roadmap

### 🎯 Design Principles

1. **CLI First**: Command-line tool, easy to integrate into automation workflows and CI/CD pipelines
2. **Minimal Dependencies**: Only 3 mature Python libraries — fast installation, clean environment
3. **Local Processing**: All operations performed locally, no files uploaded to the cloud — privacy first
4. **Modular Architecture**: Signing, stamping, watermarking, and verification are independent modules

### 🛠️ Tech Stack

| Component | Choice | Reason |
|---|---|---|
| PDF I/O | PyPDF2 | Pure Python, lightweight, stable, active community |
| Image Processing | Pillow | De facto standard for Python image processing |
| PDF Generation | reportlab | Powerful PDF generation with image overlay support |
| CLI Framework | argparse | Python standard library, zero extra dependencies |

### 🗺️ Roadmap

- [ ] **v1.1**: PDF page extraction, merge, and split
- [ ] **v1.2**: Digital signature support (PKCS#7) and timestamps
- [ ] **v1.3**: TUI interface (based on textual)
- [ ] **v2.0**: Web interface (FastAPI + Vue.js)
- [ ] **v2.1**: OCR-based signature field auto-detection

---

<a id="packaging-deployment"></a>

## 📦 Packaging & Deployment

### 🐍 Install as Python Package

```bash
pip install signforge
```

### 📁 Run from Source

```bash
git clone https://github.com/gitstq/SignForge.git
cd SignForge
pip install -r requirements.txt
python -m signforge.cli --help
```

### 🔧 Development Mode

```bash
git clone https://github.com/gitstq/SignForge.git
cd SignForge
pip install -e ".[dev]"
python -m pytest tests/
```

---

<a id="contributing"></a>

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork** this repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Write code and add tests
4. Ensure tests pass: `python -m pytest tests/`
5. Commit: `git commit -m "feat: add some feature"`
6. Push and create a **Pull Request**

Commit convention: `feat:` / `fix:` / `docs:` / `refactor:` / `test:`

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

<a id="license"></a>

## 📄 License

This project is licensed under the [MIT License](LICENSE). Free to use, modify, and distribute.

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">SignForge Team</a>
</p>
