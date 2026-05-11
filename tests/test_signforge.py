"""Tests for SignForge core modules."""

import os
import sys
import tempfile
import shutil

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from signforge.core.signer import PDFSigner
from signforge.core.stamper import PDFStamper, StampStyle
from signforge.core.watermarker import PDFWatermarker, WatermarkStyle
from signforge.core.verifier import PDFVerifier
from signforge.utils import check_pdf_file, check_image_file, generate_output_path


class TestPDFSigner:
    """Tests for PDFSigner."""

    def test_create_signer(self):
        """Test signer creation."""
        signer = PDFSigner()
        assert signer is not None
        assert signer.list_signatures() == []

    def test_register_signature_invalid_path(self):
        """Test registering non-existent signature."""
        signer = PDFSigner()
        try:
            signer.register_signature("test", "/nonexistent/path.png")
            assert False, "Should have raised FileNotFoundError"
        except FileNotFoundError:
            pass

    def test_sign_pdf_invalid_input(self):
        """Test signing non-existent PDF."""
        signer = PDFSigner()
        try:
            signer.sign_pdf("/nonexistent.pdf", "/tmp/out.pdf", "/nonexistent/sig.png")
            assert False, "Should have raised FileNotFoundError"
        except FileNotFoundError:
            pass


class TestPDFStamper:
    """Tests for PDFStamper."""

    def test_create_stamper(self):
        """Test stamper creation."""
        stamper = PDFStamper()
        assert stamper is not None
        assert stamper.list_templates() == []

    def test_create_circle_stamp(self):
        """Test creating a circular stamp."""
        stamper = PDFStamper()
        stamp = stamper.create_stamp(
            text="Test Corp",
            sub_text="SEAL",
            style=StampStyle.CIRCLE,
            size=200,
            color=StampStyle.RED,
        )
        assert stamp is not None
        assert stamp.size == (200, 200)
        assert stamp.mode == 'RGBA'

    def test_create_oval_stamp(self):
        """Test creating an oval stamp."""
        stamper = PDFStamper()
        stamp = stamper.create_stamp(
            text="Test Corp",
            style=StampStyle.OVAL,
            size=200,
        )
        assert stamp is not None

    def test_create_rect_stamp(self):
        """Test creating a rectangular stamp."""
        stamper = PDFStamper()
        stamp = stamper.create_stamp(
            text="APPROVED",
            style=StampStyle.RECTANGLE,
            size=200,
        )
        assert stamp is not None

    def test_create_square_stamp(self):
        """Test creating a square stamp."""
        stamper = PDFStamper()
        stamp = stamper.create_stamp(
            text="Test Corp",
            style=StampStyle.SQUARE,
            size=200,
        )
        assert stamp is not None

    def test_save_template(self):
        """Test saving stamp template."""
        stamper = PDFStamper()
        stamp = stamper.create_stamp(text="Test", size=100)

        with tempfile.TemporaryDirectory() as tmpdir:
            path = stamper.save_stamp_template("test_stamp", stamp, tmpdir)
            assert os.path.exists(path)
            assert "test_stamp" in stamper.list_templates()


class TestPDFWatermarker:
    """Tests for PDFWatermarker."""

    def test_create_watermarker(self):
        """Test watermarker creation."""
        wm = PDFWatermarker()
        assert wm is not None

    def test_create_text_watermark(self):
        """Test creating text watermark."""
        wm = PDFWatermarker()
        img = wm.create_text_watermark(
            text="CONFIDENTIAL",
            width=800,
            height=600,
            font_size=48,
            opacity=0.3,
            rotation=-30,
            style=WatermarkStyle.DIAGONAL,
        )
        assert img is not None
        assert img.size == (800, 600)
        assert img.mode == 'RGBA'

    def test_create_tiled_watermark(self):
        """Test creating tiled watermark."""
        wm = PDFWatermarker()
        img = wm.create_text_watermark(
            text="DRAFT",
            style=WatermarkStyle.TILED,
        )
        assert img is not None

    def test_create_horizontal_watermark(self):
        """Test creating horizontal watermark."""
        wm = PDFWatermarker()
        img = wm.create_text_watermark(
            text="SAMPLE",
            style=WatermarkStyle.HORIZONTAL,
        )
        assert img is not None


class TestPDFVerifier:
    """Tests for PDFVerifier."""

    def test_create_verifier(self):
        """Test verifier creation."""
        verifier = PDFVerifier()
        assert verifier is not None

    def test_verify_nonexistent(self):
        """Test verifying non-existent file."""
        verifier = PDFVerifier()
        try:
            verifier.verify_integrity("/nonexistent.pdf")
            assert False, "Should have raised FileNotFoundError"
        except FileNotFoundError:
            pass

    def test_compare_nonexistent(self):
        """Test comparing non-existent files."""
        verifier = PDFVerifier()
        try:
            verifier.compare_pdfs("/nonexistent1.pdf", "/nonexistent2.pdf")
            assert False, "Should have raised FileNotFoundError"
        except FileNotFoundError:
            pass


class TestUtilities:
    """Tests for utility functions."""

    def test_check_pdf_file_nonexistent(self):
        """Test checking non-existent PDF."""
        assert check_pdf_file("/nonexistent.pdf") is False

    def test_check_image_file_nonexistent(self):
        """Test checking non-existent image."""
        assert check_image_file("/nonexistent.png") is False

    def test_generate_output_path(self):
        """Test output path generation."""
        result = generate_output_path("/path/to/document.pdf", "_signed")
        assert result == "/path/to/document_signed.pdf"

    def test_generate_output_path_with_dir(self):
        """Test output path generation with custom dir."""
        result = generate_output_path("/path/to/document.pdf", "_signed", "/output")
        assert result == "/output/document_signed.pdf"


if __name__ == "__main__":
    # Run all tests
    test_classes = [
        TestPDFSigner,
        TestPDFStamper,
        TestPDFWatermarker,
        TestPDFVerifier,
        TestUtilities,
    ]

    passed = 0
    failed = 0

    for cls in test_classes:
        instance = cls()
        for method_name in dir(instance):
            if method_name.startswith("test_"):
                try:
                    getattr(instance, method_name)()
                    passed += 1
                    print(f"  ✓ {cls.__name__}.{method_name}")
                except Exception as e:
                    failed += 1
                    print(f"  ✗ {cls.__name__}.{method_name}: {e}")

    print()
    print(f"  Results: {passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)
