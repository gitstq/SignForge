"""
Core PDF watermark module - Add text/image watermarks to PDF documents.
核心PDF水印模块 - 为PDF文档添加文字/图片水印
"""

import os
import io
import math
from typing import Optional, List, Tuple

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    raise ImportError("Pillow is required. Install with: pip install Pillow")

try:
    from reportlab.lib.utils import ImageReader
    from reportlab.lib.colors import Color
    from reportlab.pdfgen import canvas
except ImportError:
    raise ImportError("reportlab is required. Install with: pip install reportlab")

from PyPDF2 import PdfReader, PdfWriter


class WatermarkStyle:
    """Watermark style presets."""

    # Text watermark styles
    DIAGONAL = "diagonal"
    HORIZONTAL = "horizontal"
    TILED = "tiled"

    # Color presets
    GRAY = (128, 128, 128)
    LIGHT_GRAY = (200, 200, 200)
    RED = (200, 50, 50)
    BLUE = (50, 50, 200)
    GREEN = (50, 150, 50)
    CUSTOM = "custom"


class PDFWatermarker:
    """PDF document watermarker - adds text/image watermarks."""

    def __init__(self):
        pass

    def _get_font(self, size: int) -> ImageFont.FreeTypeFont:
        """Get a suitable font."""
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/TTF/DejaVuSans.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "C:\\Windows\\Fonts\\arial.ttf",
            "C:\\Windows\\Fonts\\msyh.ttc",
        ]

        for path in font_paths:
            if os.path.exists(path):
                try:
                    return ImageFont.truetype(path, size)
                except Exception:
                    continue

        try:
            return ImageFont.truetype("DejaVuSans.ttf", size)
        except Exception:
            return ImageFont.load_default()

    def create_text_watermark(
        self,
        text: str,
        width: int = 800,
        height: int = 600,
        font_size: int = 48,
        color: Tuple[int, int, int] = WatermarkStyle.LIGHT_GRAY,
        opacity: float = 0.3,
        rotation: float = -30,
        style: str = WatermarkStyle.DIAGONAL,
    ) -> Image.Image:
        """Create a text watermark image.

        Args:
            text: Watermark text
            width: Image width
            height: Image height
            font_size: Font size
            color: Text color (R, G, B)
            opacity: Opacity (0.0 - 1.0)
            rotation: Rotation angle in degrees
            style: Watermark style (diagonal, horizontal, tiled)

        Returns:
            PIL Image of the watermark
        """
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        font = self._get_font(font_size)

        # Calculate alpha from opacity
        alpha = int(255 * opacity)
        fill_color = (*color, alpha)

        if style == WatermarkStyle.TILED:
            self._draw_tiled_text(draw, text, width, height, font, fill_color, font_size)
        elif style == WatermarkStyle.HORIZONTAL:
            bbox = draw.textbbox((0, 0), text, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            draw.text(((width - tw) // 2, (height - th) // 2), text, fill=fill_color, font=font)
        else:  # DIAGONAL
            bbox = draw.textbbox((0, 0), text, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            draw.text(((width - tw) // 2, (height - th) // 2), text, fill=fill_color, font=font)

        # Rotate
        if rotation != 0:
            img = img.rotate(rotation, expand=False, center=(width // 2, height // 2))

        return img

    def _draw_tiled_text(self, draw, text, width, height, font, fill_color, font_size):
        """Draw tiled watermark text."""
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]

        x_spacing = tw + int(tw * 0.5)
        y_spacing = th + int(th * 1.5)

        y = -th
        while y < height + th:
            x = -tw
            while x < width + tw:
                draw.text((x, y), text, fill=fill_color, font=font)
                x += x_spacing
            y += y_spacing

    def add_watermark(
        self,
        input_pdf: str,
        output_pdf: str,
        watermark_text: str = "",
        watermark_image: str = "",
        pages: Optional[List[int]] = None,
        opacity: float = 0.3,
        rotation: float = -30,
        font_size: int = 48,
        color: Tuple[int, int, int] = WatermarkStyle.LIGHT_GRAY,
        style: str = WatermarkStyle.DIAGONAL,
        x: float = 0,
        y: float = 0,
        width: Optional[float] = None,
        height: Optional[float] = None,
    ) -> str:
        """Add watermark to PDF pages.

        Args:
            input_pdf: Path to input PDF
            output_pdf: Path to output PDF
            watermark_text: Text watermark content
            watermark_image: Path to watermark image (alternative to text)
            pages: Page numbers to watermark (None for all)
            opacity: Watermark opacity
            rotation: Rotation angle
            font_size: Font size for text watermark
            color: Color for text watermark
            style: Watermark style
            x: X position for image watermark
            y: Y position for image watermark
            width: Width for image watermark
            height: Height for image watermark

        Returns:
            Path to the watermarked PDF
        """
        if not os.path.exists(input_pdf):
            raise FileNotFoundError(f"Input PDF not found: {input_pdf}")

        reader = PdfReader(input_pdf)
        writer = PdfWriter()
        total_pages = len(reader.pages)

        if pages is None:
            pages = list(range(1, total_pages + 1))

        for page_num in pages:
            page_idx = page_num - 1
            if page_idx < 0 or page_idx >= total_pages:
                continue

            page = reader.pages[page_idx]
            page_rect = page.mediabox
            page_width = float(page_rect.width)
            page_height = float(page_rect.height)

            # Create watermark overlay
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=(page_width, page_height))

            if watermark_image and os.path.exists(watermark_image):
                # Image watermark
                wm_img = Image.open(watermark_image)
                if wm_img.mode != 'RGBA':
                    wm_img = wm_img.convert('RGBA')

                if opacity < 1.0:
                    alpha = wm_img.split()[3]
                    alpha = alpha.point(lambda p: int(p * opacity))
                    wm_img.putalpha(alpha)

                img_buffer = io.BytesIO()
                wm_img.save(img_buffer, format='PNG')
                img_buffer.seek(0)

                wm_width = width or page_width * 0.8
                wm_height = height or (wm_width * wm_img.height / wm_img.width)

                can.drawImage(
                    ImageReader(img_buffer),
                    x, y,
                    width=wm_width,
                    height=wm_height,
                    mask='auto',
                )
            elif watermark_text:
                # Text watermark
                wm_img = self.create_text_watermark(
                    text=watermark_text,
                    width=int(page_width),
                    height=int(page_height),
                    font_size=font_size,
                    color=color,
                    opacity=opacity,
                    rotation=rotation,
                    style=style,
                )

                img_buffer = io.BytesIO()
                wm_img.save(img_buffer, format='PNG')
                img_buffer.seek(0)

                can.drawImage(
                    ImageReader(img_buffer),
                    0, 0,
                    width=page_width,
                    height=page_height,
                    mask='auto',
                )

            can.save()

            packet.seek(0)
            overlay_reader = PdfReader(packet)
            overlay_page = overlay_reader.pages[0]

            page.merge_page(overlay_page)

        for page in reader.pages:
            writer.add_page(page)

        if reader.metadata:
            writer.add_metadata(reader.metadata)

        os.makedirs(os.path.dirname(output_pdf) or '.', exist_ok=True)
        with open(output_pdf, 'wb') as f:
            writer.write(f)

        return output_pdf

    def batch_watermark(
        self,
        input_dir: str,
        output_dir: str,
        watermark_text: str = "",
        watermark_image: str = "",
        pattern: str = "*.pdf",
        opacity: float = 0.3,
        rotation: float = -30,
        font_size: int = 48,
        color: Tuple[int, int, int] = WatermarkStyle.LIGHT_GRAY,
        style: str = WatermarkStyle.DIAGONAL,
    ) -> List[str]:
        """Batch add watermarks to all PDFs in a directory.

        Args:
            input_dir: Input directory
            output_dir: Output directory
            watermark_text: Watermark text
            watermark_image: Watermark image path
            pattern: File glob pattern
            opacity: Watermark opacity
            rotation: Rotation angle
            font_size: Font size
            color: Color
            style: Style

        Returns:
            List of output file paths
        """
        import glob

        os.makedirs(output_dir, exist_ok=True)
        pdf_files = glob.glob(os.path.join(input_dir, pattern))

        results = []
        for pdf_path in pdf_files:
            filename = os.path.basename(pdf_path)
            output_path = os.path.join(output_dir, f"watermarked_{filename}")

            try:
                self.add_watermark(
                    pdf_path, output_path,
                    watermark_text=watermark_text,
                    watermark_image=watermark_image,
                    opacity=opacity,
                    rotation=rotation,
                    font_size=font_size,
                    color=color,
                    style=style,
                )
                results.append(output_path)
            except Exception as e:
                print(f"Warning: Failed to watermark {filename}: {e}")

        return results
