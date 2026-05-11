"""
Core PDF stamping module - Create and apply official stamps/seals to PDF documents.
核心PDF盖章模块 - 创建并应用公章/印章到PDF文档
"""

import os
import io
import math
from typing import Optional, Tuple, List

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    raise ImportError("Pillow is required. Install with: pip install Pillow")

try:
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfgen import canvas
except ImportError:
    raise ImportError("reportlab is required. Install with: pip install reportlab")

from PyPDF2 import PdfReader, PdfWriter


class StampStyle:
    """Predefined stamp styles."""

    # Color presets (R, G, B)
    RED = (220, 50, 50)
    BLUE = (50, 50, 220)
    BLACK = (30, 30, 30)
    GREEN = (50, 150, 50)
    PURPLE = (128, 0, 128)

    # Stamp types
    CIRCLE = "circle"
    OVAL = "oval"
    RECTANGLE = "rectangle"
    SQUARE = "square"


class PDFStamper:
    """PDF document stamper - creates and applies official stamps/seals."""

    def __init__(self):
        self._stamps = {}  # name -> image_bytes cache

    def create_stamp(
        self,
        text: str,
        sub_text: str = "",
        style: str = StampStyle.CIRCLE,
        size: int = 200,
        color: Tuple[int, int, int] = StampStyle.RED,
        font_size: Optional[int] = None,
        border_width: int = 4,
        inner_ring: bool = True,
        star: bool = True,
    ) -> Image.Image:
        """Create a stamp/seal image.

        Args:
            text: Main text (company/org name)
            sub_text: Sub text (e.g., "SEAL" or department name)
            style: Stamp shape (circle, oval, rectangle, square)
            size: Stamp size in pixels
            color: Stamp color (R, G, B)
            font_size: Font size (auto-calculated if None)
            border_width: Border line width
            inner_ring: Whether to draw inner ring
            star: Whether to draw center star

        Returns:
            PIL Image of the stamp
        """
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Calculate font size
        if font_size is None:
            font_size = max(12, size // 10)

        # Try to load a suitable font
        font = self._get_font(font_size)
        small_font = self._get_font(max(8, font_size // 2))

        center_x, center_y = size // 2, size // 2
        radius = size // 2 - border_width

        if style == StampStyle.CIRCLE:
            self._draw_circle_stamp(
                draw, center_x, center_y, radius, color,
                border_width, inner_ring, star, text, sub_text, font, small_font, size
            )
        elif style == StampStyle.OVAL:
            self._draw_oval_stamp(
                draw, center_x, center_y, radius, color,
                border_width, inner_ring, star, text, sub_text, font, small_font, size
            )
        elif style == StampStyle.RECTANGLE:
            self._draw_rect_stamp(
                draw, center_x, center_y, radius, color,
                border_width, text, sub_text, font, small_font, size
            )
        elif style == StampStyle.SQUARE:
            self._draw_square_stamp(
                draw, center_x, center_y, radius, color,
                border_width, inner_ring, star, text, sub_text, font, small_font, size
            )

        return img

    def _get_font(self, size: int) -> ImageFont.FreeTypeFont:
        """Get a suitable font, falling back to default if needed."""
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
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

        # Fallback to default font
        try:
            return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
        except Exception:
            return ImageFont.load_default()

    def _draw_circle_stamp(
        self, draw, cx, cy, radius, color, border_width,
        inner_ring, star, text, sub_text, font, small_font, size
    ):
        """Draw a circular stamp."""
        # Outer circle
        draw.ellipse(
            [cx - radius, cy - radius, cx + radius, cy + radius],
            outline=color, width=border_width
        )

        # Inner ring
        if inner_ring:
            inner_radius = radius - border_width * 3
            draw.ellipse(
                [cx - inner_radius, cy - inner_radius, cx + inner_radius, cy + inner_radius],
                outline=color, width=border_width // 2
            )

        # Center star
        if star:
            self._draw_star(draw, cx, cy, radius // 5, color)

        # Draw curved text along the top arc
        self._draw_curved_text(draw, text, cx, cy, radius - border_width * 2, color, font, start_angle=-90, end_angle=90)

        # Draw sub text at bottom
        if sub_text:
            bbox = draw.textbbox((0, 0), sub_text, font=small_font)
            tw = bbox[2] - bbox[0]
            draw.text((cx - tw // 2, cy + radius // 3), sub_text, fill=color, font=small_font)

    def _draw_oval_stamp(
        self, draw, cx, cy, radius, color, border_width,
        inner_ring, star, text, sub_text, font, small_font, size
    ):
        """Draw an oval stamp."""
        draw.ellipse(
            [cx - radius, cy - int(radius * 0.7), cx + radius, cy + int(radius * 0.7)],
            outline=color, width=border_width
        )
        if star:
            self._draw_star(draw, cx, cy, radius // 5, color)
        if sub_text:
            bbox = draw.textbbox((0, 0), sub_text, font=small_font)
            tw = bbox[2] - bbox[0]
            draw.text((cx - tw // 2, cy + radius // 4), sub_text, fill=color, font=small_font)

        # Draw text in center
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        draw.text((cx - tw // 2, cy - radius // 4), text, fill=color, font=font)

    def _draw_rect_stamp(
        self, draw, cx, cy, radius, color, border_width,
        text, sub_text, font, small_font, size
    ):
        """Draw a rectangular stamp."""
        margin = border_width
        draw.rectangle(
            [cx - radius, cy - int(radius * 0.6), cx + radius, cy + int(radius * 0.6)],
            outline=color, width=border_width
        )
        # Main text
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        draw.text((cx - tw // 2, cy - font.size // 2), text, fill=color, font=font)
        # Sub text
        if sub_text:
            bbox = draw.textbbox((0, 0), sub_text, font=small_font)
            tw = bbox[2] - bbox[0]
            draw.text((cx - tw // 2, cy + font.size // 2), sub_text, fill=color, font=small_font)

    def _draw_square_stamp(
        self, draw, cx, cy, radius, color, border_width,
        inner_ring, star, text, sub_text, font, small_font, size
    ):
        """Draw a square stamp."""
        draw.rectangle(
            [cx - radius, cy - radius, cx + radius, cy + radius],
            outline=color, width=border_width
        )
        if inner_ring:
            inner_r = radius - border_width * 3
            draw.rectangle(
                [cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r],
                outline=color, width=border_width // 2
            )
        if star:
            self._draw_star(draw, cx, cy, radius // 5, color)
        if sub_text:
            bbox = draw.textbbox((0, 0), sub_text, font=small_font)
            tw = bbox[2] - bbox[0]
            draw.text((cx - tw // 2, cy + radius // 3), sub_text, fill=color, font=small_font)

    def _draw_star(self, draw, cx, cy, size, color):
        """Draw a 5-pointed star."""
        points = []
        for i in range(10):
            angle = math.pi / 2 + i * math.pi / 5
            r = size if i % 2 == 0 else size * 0.4
            x = cx + r * math.cos(angle)
            y = cy - r * math.sin(angle)
            points.append((x, y))
        draw.polygon(points, fill=color)

    def _draw_curved_text(self, draw, text, cx, cy, radius, color, font, start_angle=-90, end_angle=90):
        """Draw text curved along an arc."""
        if not text:
            return

        # Calculate angle per character
        total_angle = end_angle - start_angle
        char_angle = total_angle / max(len(text), 1)

        for i, char in enumerate(text):
            angle_deg = start_angle + char_angle * (i + 0.5)
            angle_rad = math.radians(angle_deg)

            x = cx + radius * math.cos(angle_rad)
            y = cy + radius * math.sin(angle_rad)

            # Draw character
            draw.text((x, y), char, fill=color, font=font)

    def stamp_pdf(
        self,
        input_pdf: str,
        output_pdf: str,
        stamp_image: str,
        page: int = -1,
        x: float = 350,
        y: float = 200,
        width: float = 150,
        height: float = 150,
        opacity: float = 0.85,
    ) -> str:
        """Apply a stamp image to a PDF page.

        Args:
            input_pdf: Path to input PDF
            output_pdf: Path to output PDF
            stamp_image: Path to stamp image (PNG with transparency)
            page: Page number (1-based, -1 for last page)
            x: X position in points
            y: Y position in points
            width: Stamp width
            height: Stamp height
            opacity: Stamp opacity

        Returns:
            Path to the stamped PDF
        """
        if not os.path.exists(input_pdf):
            raise FileNotFoundError(f"Input PDF not found: {input_pdf}")
        if not os.path.exists(stamp_image):
            raise FileNotFoundError(f"Stamp image not found: {stamp_image}")

        reader = PdfReader(input_pdf)
        writer = PdfWriter()

        if page == -1:
            page_idx = len(reader.pages) - 1
        else:
            page_idx = page - 1

        if page_idx < 0 or page_idx >= len(reader.pages):
            raise ValueError(f"Invalid page: {page}. PDF has {len(reader.pages)} pages.")

        target_page = reader.pages[page_idx]
        page_rect = target_page.mediabox
        page_width = float(page_rect.width)
        page_height = float(page_rect.height)

        # Load stamp image
        stamp_img = Image.open(stamp_image)
        if stamp_img.mode != 'RGBA':
            stamp_img = stamp_img.convert('RGBA')

        # Apply opacity
        if opacity < 1.0:
            alpha = stamp_img.split()[3]
            alpha = alpha.point(lambda p: int(p * opacity))
            stamp_img.putalpha(alpha)

        # Create overlay
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=(page_width, page_height))

        img_buffer = io.BytesIO()
        stamp_img.save(img_buffer, format='PNG')
        img_buffer.seek(0)

        can.drawImage(
            ImageReader(img_buffer),
            x, y,
            width=width,
            height=height,
            mask='auto',
        )
        can.save()

        packet.seek(0)
        overlay_reader = PdfReader(packet)
        overlay_page = overlay_reader.pages[0]

        for i, p in enumerate(reader.pages):
            if i == page_idx:
                p.merge_page(overlay_page)
            writer.add_page(p)

        if reader.metadata:
            writer.add_metadata(reader.metadata)

        os.makedirs(os.path.dirname(output_pdf) or '.', exist_ok=True)
        with open(output_pdf, 'wb') as f:
            writer.write(f)

        return output_pdf

    def save_stamp_template(self, name: str, stamp_image: Image.Image, directory: str = "./templates") -> str:
        """Save a stamp as a reusable template.

        Args:
            name: Template name
            stamp_image: PIL Image of the stamp
            directory: Directory to save templates

        Returns:
            Path to saved template
        """
        os.makedirs(directory, exist_ok=True)
        path = os.path.join(directory, f"{name}.png")
        stamp_image.save(path, format='PNG')
        self._stamps[name] = path
        return path

    def list_templates(self) -> List[str]:
        """List all saved stamp templates."""
        return list(self._stamps.keys())
