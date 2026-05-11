"""
Utility functions for SignForge.
"""

import os
import sys
import json
from datetime import datetime
from typing import Any, Dict


def ensure_output_dir(path: str) -> str:
    """Ensure the output directory exists."""
    dir_path = os.path.dirname(path)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)
    return path


def generate_output_path(input_path: str, suffix: str, output_dir: str = None) -> str:
    """Generate output file path with suffix.

    Args:
        input_path: Original file path
        suffix: Suffix to add (e.g., '_signed', '_stamped')
        output_dir: Output directory (default: same as input)

    Returns:
        Output file path
    """
    base, ext = os.path.splitext(input_path)
    filename = os.path.basename(base)

    if output_dir:
        return os.path.join(output_dir, f"{filename}{suffix}{ext}")
    else:
        dir_path = os.path.dirname(input_path)
        return os.path.join(dir_path or '.', f"{filename}{suffix}{ext}")


def print_success(message: str):
    """Print a success message."""
    print(f"  \033[92m✓\033[0m {message}")


def print_error(message: str):
    """Print an error message."""
    print(f"  \033[91m✗\033[0m {message}")


def print_info(message: str):
    """Print an info message."""
    print(f"  \033[94mℹ\033[0m {message}")


def print_warning(message: str):
    """Print a warning message."""
    print(f"  \033[93m⚠\033[0m {message}")


def print_header(title: str, width: int = 60):
    """Print a styled header."""
    print()
    print(f"\033[96m{'═' * width}\033[0m")
    print(f"\033[96m  {title}\033[0m")
    print(f"\033[96m{'═' * width}\033[0m")
    print()


def print_result_json(data: Dict[str, Any]):
    """Print result data as formatted JSON."""
    print(json.dumps(data, indent=2, ensure_ascii=False, default=str))


def get_timestamp() -> str:
    """Get current timestamp string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def check_pdf_file(path: str) -> bool:
    """Check if a file is a valid PDF."""
    if not os.path.exists(path):
        return False
    if not path.lower().endswith('.pdf'):
        return False
    # Check PDF magic bytes
    try:
        with open(path, 'rb') as f:
            header = f.read(5)
            return header == b'%PDF-'
    except Exception:
        return False


def check_image_file(path: str) -> bool:
    """Check if a file is a valid image."""
    if not os.path.exists(path):
        return False
    valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp')
    return path.lower().endswith(valid_extensions)
