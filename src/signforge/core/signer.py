"""
Core PDF signing module - Add signature images to PDF documents.
核心PDF签名模块 - 在PDF文档指定位置添加签名图片
"""

import os
import io
from typing import Optional, Tuple, List

try:
    from PyPDF2 import PdfReader, PdfWriter
    from PyPDF2.generic import RectangleObject, NameObject, ArrayObject, NumberObject
except ImportError:
    raise ImportError("PyPDF2 is required. Install with: pip install PyPDF2")

try:
    from PIL import Image
except ImportError:
    raise ImportError("Pillow is required. Install with: pip install Pillow")

try:
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter, A4
except ImportError:
    raise ImportError("reportlab is required. Install with: pip install reportlab")


class PDFSigner:
    """PDF document signer - adds signature images to PDF pages."""

    # Common page sizes (width, height) in points (1/72 inch)
    PAGE_SIZES = {
        "letter": letter,      # 612 x 792
        "a4": A4,              # 595.27 x 841.89
        "a3": (841.89, 1190.55),
        "a5": (419.53, 595.28),
        "legal": (612, 1008),
    }

    def __init__(self):
        self._signatures = {}  # name -> image_path cache

    def register_signature(self, name: str, image_path: str) -> bool:
        """Register a signature image by name for reuse.

        Args:
            name: Signature template name
            image_path: Path to signature image (PNG recommended, transparent background)

        Returns:
            True if registered successfully
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Signature image not found: {image_path}")

        # Validate image
        try:
            with Image.open(image_path) as img:
                if img.mode == 'RGBA':
                    pass  # Transparent background is ideal
                elif img.mode in ('RGB', 'L'):
                    pass  # Acceptable
                else:
                    img = img.convert('RGBA')
        except Exception as e:
            raise ValueError(f"Invalid signature image: {e}")

        self._signatures[name] = image_path
        return True

    def sign_pdf(
        self,
        input_pdf: str,
        output_pdf: str,
        signature_image: str,
        page: int = -1,
        x: float = 100,
        y: float = 100,
        width: Optional[float] = None,
        height: Optional[float] = None,
        opacity: float = 1.0,
    ) -> str:
        """Add a signature image to a PDF page.

        Args:
            input_pdf: Path to input PDF file
            output_pdf: Path to output PDF file
            signature_image: Path to signature image
            page: Page number (1-based, -1 for last page)
            x: X position in points from left
            y: Y position in points from bottom
            width: Signature width (auto-calculated if None)
            height: Signature height (auto-calculated if None)
            opacity: Signature opacity (0.0 - 1.0)

        Returns:
            Path to the signed PDF file
        """
        if not os.path.exists(input_pdf):
            raise FileNotFoundError(f"Input PDF not found: {input_pdf}")
        if not os.path.exists(signature_image):
            raise FileNotFoundError(f"Signature image not found: {signature_image}")

        # Read the original PDF
        reader = PdfReader(input_pdf)
        writer = PdfWriter()

        # Determine target page
        if page == -1:
            page_idx = len(reader.pages) - 1
        else:
            page_idx = page - 1

        if page_idx < 0 or page_idx >= len(reader.pages):
            raise ValueError(f"Invalid page number: {page}. PDF has {len(reader.pages)} pages.")

        # Get page dimensions
        target_page = reader.pages[page_idx]
        page_rect = target_page.mediabox
        page_width = float(page_rect.width)
        page_height = float(page_rect.height)

        # Load and prepare signature image
        sig_img = Image.open(signature_image)
        if sig_img.mode != 'RGBA':
            sig_img = sig_img.convert('RGBA')

        # Calculate dimensions
        if width is None and height is None:
            # Default: 150 points wide, maintain aspect ratio
            width = 150
            aspect = sig_img.height / sig_img.width
            height = width * aspect
        elif width is not None and height is None:
            aspect = sig_img.height / sig_img.width
            height = width * aspect
        elif width is None and height is not None:
            aspect = sig_img.width / sig_img.height
            width = height * aspect

        # Apply opacity
        if opacity < 1.0:
            alpha = sig_img.split()[3]
            alpha = alpha.point(lambda p: int(p * opacity))
            sig_img.putalpha(alpha)

        # Create overlay PDF with signature
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=(page_width, page_height))

        # Save signature as temp PNG for reportlab
        img_buffer = io.BytesIO()
        sig_img.save(img_buffer, format='PNG')
        img_buffer.seek(0)

        can.drawImage(
            ImageReader(img_buffer),
            x, y,
            width=width,
            height=height,
            mask='auto',
            preserveAspectRatio=True,
        )
        can.save()

        # Merge overlay with original page
        packet.seek(0)
        overlay_reader = PdfReader(packet)
        overlay_page = overlay_reader.pages[0]

        # Copy all pages, merging the target page
        for i, p in enumerate(reader.pages):
            if i == page_idx:
                p.merge_page(overlay_page)
            writer.add_page(p)

        # Copy metadata
        if reader.metadata:
            writer.add_metadata(reader.metadata)

        # Write output
        os.makedirs(os.path.dirname(output_pdf) or '.', exist_ok=True)
        with open(output_pdf, 'wb') as f:
            writer.write(f)

        return output_pdf

    def sign_multiple_pages(
        self,
        input_pdf: str,
        output_pdf: str,
        signature_image: str,
        pages: Optional[List[int]] = None,
        x: float = 100,
        y: float = 100,
        width: Optional[float] = None,
        height: Optional[float] = None,
        opacity: float = 1.0,
    ) -> str:
        """Add signature to multiple pages of a PDF.

        Args:
            input_pdf: Path to input PDF
            output_pdf: Path to output PDF
            signature_image: Path to signature image
            pages: List of page numbers (1-based), None for all pages
            x: X position
            y: Y position
            width: Signature width
            height: Signature height
            opacity: Opacity

        Returns:
            Path to the signed PDF
        """
        reader = PdfReader(input_pdf)
        total_pages = len(reader.pages)

        if pages is None:
            pages = list(range(1, total_pages + 1))

        # Use sign_pdf for the first page to create the output
        self.sign_pdf(input_pdf, output_pdf, signature_image, pages[0], x, y, width, height, opacity)

        # Sign remaining pages
        for page_num in pages[1:]:
            self.sign_pdf(output_pdf, output_pdf, signature_image, page_num, x, y, width, height, opacity)

        return output_pdf

    def list_signatures(self) -> List[str]:
        """List all registered signature templates.

        Returns:
            List of signature names
        """
        return list(self._signatures.keys())

    def get_signature_info(self, name: str) -> Optional[dict]:
        """Get information about a registered signature.

        Args:
            name: Signature template name

        Returns:
            Dict with signature info or None
        """
        if name not in self._signatures:
            return None

        path = self._signatures[name]
        with Image.open(path) as img:
            return {
                "name": name,
                "path": path,
                "width": img.width,
                "height": img.height,
                "mode": img.mode,
                "format": img.format,
            }
