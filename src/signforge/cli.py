"""
SignForge CLI - Command Line Interface
SignForge 命令行界面

Usage:
    signforge sign <input> --sig <image> [options]
    signforge stamp <input> --text <text> [options]
    signforge watermark <input> --text <text> [options]
    signforge verify <input>
    signforge info <input>
    signforge batch <command> <input_dir> [options]
"""

import argparse
import sys
import os

from . import __version__
from .core import PDFSigner, PDFStamper, StampStyle, PDFWatermarker, WatermarkStyle, PDFVerifier
from .utils import (
    print_header, print_success, print_error, print_info, print_warning,
    print_result_json, check_pdf_file, check_image_file, generate_output_path,
    ensure_output_dir, get_timestamp,
)


def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser."""
    parser = argparse.ArgumentParser(
        prog="signforge",
        description="🔐 SignForge - Lightweight PDF Document Intelligent Signing & Stamping Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Sign a PDF with a signature image
  signforge sign document.pdf --sig signature.png --page 1 --x 100 --y 100

  # Create and apply a circular stamp
  signforge stamp document.pdf --text "ACME Corp" --style circle --page -1

  # Add a diagonal watermark
  signforge watermark document.pdf --text "CONFIDENTIAL" --style diagonal --opacity 0.2

  # Verify PDF integrity
  signforge verify document.pdf

  # Get PDF info
  signforge info document.pdf

  # Batch watermark all PDFs in a directory
  signforge batch watermark ./docs --text "DRAFT" --output ./output
        """,
    )

    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # === Sign command ===
    sign_parser = subparsers.add_parser("sign", help="Sign a PDF with a signature image")
    sign_parser.add_argument("input", help="Input PDF file path")
    sign_parser.add_argument("--sig", required=True, help="Signature image path (PNG recommended)")
    sign_parser.add_argument("-o", "--output", help="Output PDF path (default: <input>_signed.pdf)")
    sign_parser.add_argument("--page", type=int, default=-1, help="Page number (1-based, -1 for last)")
    sign_parser.add_argument("--x", type=float, default=100, help="X position in points")
    sign_parser.add_argument("--y", type=float, default=100, help="Y position in points")
    sign_parser.add_argument("--width", type=float, default=None, help="Signature width")
    sign_parser.add_argument("--height", type=float, default=None, help="Signature height")
    sign_parser.add_argument("--opacity", type=float, default=1.0, help="Opacity (0.0-1.0)")
    sign_parser.add_argument("--all-pages", action="store_true", help="Sign all pages")

    # === Stamp command ===
    stamp_parser = subparsers.add_parser("stamp", help="Create and apply a stamp/seal to PDF")
    stamp_parser.add_argument("input", help="Input PDF file path")
    stamp_parser.add_argument("--text", required=True, help="Main stamp text (org/company name)")
    stamp_parser.add_argument("--sub-text", default="", help="Sub text (e.g., 'SEAL')")
    stamp_parser.add_argument("-o", "--output", help="Output PDF path")
    stamp_parser.add_argument("--style", choices=["circle", "oval", "rectangle", "square"],
                              default="circle", help="Stamp shape")
    stamp_parser.add_argument("--size", type=int, default=200, help="Stamp size in pixels")
    stamp_parser.add_argument("--color", default="red", help="Stamp color (red/blue/black/green/purple)")
    stamp_parser.add_argument("--page", type=int, default=-1, help="Page number")
    stamp_parser.add_argument("--x", type=float, default=350, help="X position")
    stamp_parser.add_argument("--y", type=float, default=200, help="Y position")
    stamp_parser.add_argument("--stamp-width", type=float, default=150, help="Stamp width on PDF")
    stamp_parser.add_argument("--stamp-height", type=float, default=150, help="Stamp height on PDF")
    stamp_parser.add_argument("--opacity", type=float, default=0.85, help="Stamp opacity")
    stamp_parser.add_argument("--save-template", help="Save stamp template with this name")
    stamp_parser.add_argument("--stamp-image", help="Use existing stamp image instead of creating")

    # === Watermark command ===
    wm_parser = subparsers.add_parser("watermark", help="Add watermark to PDF")
    wm_parser.add_argument("input", help="Input PDF file path")
    wm_parser.add_argument("--text", default="", help="Watermark text")
    wm_parser.add_argument("--image", default="", help="Watermark image path")
    wm_parser.add_argument("-o", "--output", help="Output PDF path")
    wm_parser.add_argument("--style", choices=["diagonal", "horizontal", "tiled"],
                           default="diagonal", help="Watermark style")
    wm_parser.add_argument("--opacity", type=float, default=0.3, help="Opacity (0.0-1.0)")
    wm_parser.add_argument("--rotation", type=float, default=-30, help="Rotation angle")
    wm_parser.add_argument("--font-size", type=int, default=48, help="Font size")
    wm_parser.add_argument("--color", default="light_gray", help="Color (gray/light_gray/red/blue/green)")
    wm_parser.add_argument("--pages", help="Comma-separated page numbers (default: all)")

    # === Verify command ===
    verify_parser = subparsers.add_parser("verify", help="Verify PDF integrity")
    verify_parser.add_argument("input", help="PDF file path")
    verify_parser.add_argument("--compare", help="Compare with another PDF")
    verify_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # === Info command ===
    info_parser = subparsers.add_parser("info", help="Get PDF information")
    info_parser.add_argument("input", help="PDF file path")
    info_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # === Batch command ===
    batch_parser = subparsers.add_parser("batch", help="Batch process PDFs")
    batch_subparsers = batch_parser.add_subparsers(dest="batch_command")

    # Batch watermark
    batch_wm = batch_subparsers.add_parser("watermark", help="Batch add watermarks")
    batch_wm.add_argument("input_dir", help="Input directory")
    batch_wm.add_argument("--text", default="", help="Watermark text")
    batch_wm.add_argument("--image", default="", help="Watermark image")
    batch_wm.add_argument("-o", "--output", required=True, help="Output directory")
    batch_wm.add_argument("--pattern", default="*.pdf", help="File pattern")
    batch_wm.add_argument("--opacity", type=float, default=0.3)
    batch_wm.add_argument("--style", choices=["diagonal", "horizontal", "tiled"], default="diagonal")

    return parser


def _get_color(color_str: str) -> tuple:
    """Parse color string to RGB tuple."""
    colors = {
        "red": (220, 50, 50),
        "blue": (50, 50, 220),
        "black": (30, 30, 30),
        "green": (50, 150, 50),
        "purple": (128, 0, 128),
        "gray": (128, 128, 128),
        "light_gray": (200, 200, 200),
    }
    return colors.get(color_str.lower(), (128, 128, 128))


def cmd_sign(args):
    """Handle sign command."""
    print_header("🔐 PDF Signing")

    if not check_pdf_file(args.input):
        print_error(f"Invalid PDF file: {args.input}")
        return 1

    if not check_image_file(args.sig):
        print_error(f"Invalid signature image: {args.sig}")
        return 1

    output = args.output or generate_output_path(args.input, "_signed")

    signer = PDFSigner()
    try:
        if args.all_pages:
            print_info(f"Signing all pages of: {args.input}")
            result = signer.sign_multiple_pages(
                args.input, output, args.sig,
                x=args.x, y=args.y,
                width=args.width, height=args.height,
                opacity=args.opacity,
            )
        else:
            print_info(f"Signing page {args.page} of: {args.input}")
            result = signer.sign_pdf(
                args.input, output, args.sig,
                page=args.page, x=args.x, y=args.y,
                width=args.width, height=args.height,
                opacity=args.opacity,
            )
        print_success(f"Signed PDF saved to: {result}")
        return 0
    except Exception as e:
        print_error(f"Signing failed: {e}")
        return 1


def cmd_stamp(args):
    """Handle stamp command."""
    print_header("🔴 PDF Stamping")

    if not check_pdf_file(args.input):
        print_error(f"Invalid PDF file: {args.input}")
        return 1

    output = args.output or generate_output_path(args.input, "_stamped")
    color = _get_color(args.color)

    stamper = PDFStamper()

    if args.stamp_image:
        # Use existing stamp image
        stamp_path = args.stamp_image
        if not check_image_file(stamp_path):
            print_error(f"Invalid stamp image: {stamp_path}")
            return 1
    else:
        # Create stamp
        print_info(f"Creating {args.style} stamp: {args.text}")
        stamp_img = stamper.create_stamp(
            text=args.text,
            sub_text=args.sub_text,
            style=args.style,
            size=args.size,
            color=color,
        )

        # Save template if requested
        if args.save_template:
            stamp_path = stamper.save_stamp_template(args.save_template, stamp_img)
            print_success(f"Stamp template saved: {stamp_path}")
        else:
            # Save to temp
            import tempfile
            tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
            stamp_img.save(tmp.name, format='PNG')
            stamp_path = tmp.name

    try:
        print_info(f"Applying stamp to page {args.page} of: {args.input}")
        result = stamper.stamp_pdf(
            args.input, output, stamp_path,
            page=args.page, x=args.x, y=args.y,
            width=args.stamp_width, height=args.stamp_height,
            opacity=args.opacity,
        )
        print_success(f"Stamped PDF saved to: {result}")
        return 0
    except Exception as e:
        print_error(f"Stamping failed: {e}")
        return 1


def cmd_watermark(args):
    """Handle watermark command."""
    print_header("💧 PDF Watermarking")

    if not check_pdf_file(args.input):
        print_error(f"Invalid PDF file: {args.input}")
        return 1

    if not args.text and not args.image:
        print_error("Either --text or --image is required")
        return 1

    output = args.output or generate_output_path(args.input, "_watermarked")
    color = _get_color(args.color)

    pages = None
    if args.pages:
        pages = [int(p.strip()) for p in args.pages.split(",")]

    watermarker = PDFWatermarker()
    try:
        print_info(f"Adding watermark to: {args.input}")
        result = watermarker.add_watermark(
            args.input, output,
            watermark_text=args.text,
            watermark_image=args.image,
            pages=pages,
            opacity=args.opacity,
            rotation=args.rotation,
            font_size=args.font_size,
            color=color,
            style=args.style,
        )
        print_success(f"Watermarked PDF saved to: {result}")
        return 0
    except Exception as e:
        print_error(f"Watermarking failed: {e}")
        return 1


def cmd_verify(args):
    """Handle verify command."""
    print_header("🔍 PDF Verification")

    if not check_pdf_file(args.input):
        print_error(f"Invalid PDF file: {args.input}")
        return 1

    verifier = PDFVerifier()
    try:
        result = verifier.verify_integrity(args.input)

        if args.json:
            print_result_json(result)
            return 0

        if result["valid"]:
            print_success(f"PDF is valid: {args.input}")
        else:
            print_error(f"PDF has issues: {args.input}")

        print_info(f"Pages: {result['checks'].get('page_count', 'N/A')}")
        print_info(f"Size: {result['file_size']} bytes")
        print_info(f"MD5: {result['checks'].get('md5', 'N/A')}")
        print_info(f"SHA-256: {result['checks'].get('sha256', 'N/A')}")
        print_info(f"Encrypted: {result['checks'].get('encrypted', False)}")
        print_info(f"Has signatures: {result['checks'].get('has_signatures', False)}")

        if result['checks'].get('metadata'):
            meta = result['checks']['metadata']
            print()
            print("  Metadata:")
            for k, v in meta.items():
                if v and v != "N/A":
                    print(f"    {k}: {v}")

        if args.compare:
            print()
            print_info(f"Comparing with: {args.compare}")
            cmp = verifier.compare_pdfs(args.input, args.compare)
            if cmp["identical"]:
                print_success("Files are identical")
            else:
                print_warning("Files differ:")
                for diff in cmp["differences"]:
                    print(f"    - {diff}")

        return 0
    except Exception as e:
        print_error(f"Verification failed: {e}")
        return 1


def cmd_info(args):
    """Handle info command."""
    print_header("📄 PDF Information")

    if not check_pdf_file(args.input):
        print_error(f"Invalid PDF file: {args.input}")
        return 1

    verifier = PDFVerifier()
    try:
        info = verifier.extract_info(args.input)

        if args.json:
            print_result_json(info)
            return 0

        print(f"  File: {info['file']}")
        print(f"  Size: {info['size_human']} ({info['size_bytes']} bytes)")
        print(f"  Pages: {info['pages']}")
        print(f"  Encrypted: {info['encrypted']}")

        if info['metadata']:
            print()
            print("  Metadata:")
            for k, v in info['metadata'].items():
                print(f"    {k}: {v}")

        print()
        print("  Page Details:")
        for p in info['page_details']:
            print(f"    Page {p['page']}: {p['width']:.0f}x{p['height']:.0f}pt, "
                  f"text: {p['text_length']} chars, annotations: {p['has_annotations']}")

        return 0
    except Exception as e:
        print_error(f"Failed to extract info: {e}")
        return 1


def cmd_batch(args):
    """Handle batch command."""
    if args.batch_command == "watermark":
        print_header("💧 Batch Watermarking")

        if not args.text and not args.image:
            print_error("Either --text or --image is required")
            return 1

        if not os.path.isdir(args.input_dir):
            print_error(f"Directory not found: {args.input_dir}")
            return 1

        color = _get_color("light_gray")
        watermarker = PDFWatermarker()

        try:
            results = watermarker.batch_watermark(
                args.input_dir, args.output,
                watermark_text=args.text,
                watermark_image=args.image,
                pattern=args.pattern,
                opacity=args.opacity,
                style=args.style,
            )
            print_success(f"Processed {len(results)} files")
            for r in results:
                print_info(f"  → {r}")
            return 0
        except Exception as e:
            print_error(f"Batch watermarking failed: {e}")
            return 1
    else:
        print_error(f"Unknown batch command: {args.batch_command}")
        return 1


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    # Banner
    print()
    print(f"\033[96m  🔐 SignForge v{__version__}\033[0m")
    print(f"\033[90m  Lightweight PDF Signing & Stamping Engine\033[0m")
    print(f"\033[90m  {get_timestamp()}\033[0m")

    # Route to command handler
    handlers = {
        "sign": cmd_sign,
        "stamp": cmd_stamp,
        "watermark": cmd_watermark,
        "verify": cmd_verify,
        "info": cmd_info,
        "batch": cmd_batch,
    }

    handler = handlers.get(args.command)
    if handler:
        return handler(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
