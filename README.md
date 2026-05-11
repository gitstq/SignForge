# SignForge

Lightweight PDF Document Intelligent Signing & Stamping Engine.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Installation

```bash
pip install signforge
```

## Quick Start

```bash
# Sign a PDF
signforge sign document.pdf --sig signature.png

# Create and apply a stamp
signforge stamp document.pdf --text "ACME Corp"

# Add a watermark
signforge watermark document.pdf --text "CONFIDENTIAL"

# Verify PDF integrity
signforge verify document.pdf
```

## License

MIT License
