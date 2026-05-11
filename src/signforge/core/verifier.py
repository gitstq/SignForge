"""
Core PDF verification module - Verify PDF integrity and extract signature info.
核心PDF验证模块 - 验证PDF完整性和提取签名信息
"""

import os
import hashlib
from typing import Optional, Dict, List, Any
from datetime import datetime


try:
    from PyPDF2 import PdfReader
except ImportError:
    raise ImportError("PyPDF2 is required. Install with: pip install PyPDF2")


class PDFVerifier:
    """PDF document verifier - checks integrity and extracts metadata."""

    def __init__(self):
        pass

    def verify_integrity(self, pdf_path: str) -> Dict[str, Any]:
        """Verify PDF file integrity.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Dict with verification results
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        result = {
            "valid": True,
            "file_path": pdf_path,
            "file_size": os.path.getsize(pdf_path),
            "checks": {},
        }

        # Check 1: File can be read
        try:
            reader = PdfReader(pdf_path)
            result["checks"]["readable"] = True
        except Exception as e:
            result["valid"] = False
            result["checks"]["readable"] = False
            result["checks"]["readable_error"] = str(e)
            return result

        # Check 2: Page count
        result["checks"]["page_count"] = len(reader.pages)

        # Check 3: Metadata
        if reader.metadata:
            meta = reader.metadata
            result["checks"]["metadata"] = {
                "title": meta.get("/Title", "N/A"),
                "author": meta.get("/Author", "N/A"),
                "subject": meta.get("/Subject", "N/A"),
                "creator": meta.get("/Creator", "N/A"),
                "producer": meta.get("/Producer", "N/A"),
                "creation_date": str(meta.get("/CreationDate", "N/A")),
                "modification_date": str(meta.get("/ModDate", "N/A")),
            }
        else:
            result["checks"]["metadata"] = None

        # Check 4: File hash
        result["checks"]["md5"] = self._file_hash(pdf_path, "md5")
        result["checks"]["sha256"] = self._file_hash(pdf_path, "sha256")

        # Check 5: Encryption
        result["checks"]["encrypted"] = reader.is_encrypted

        # Check 6: Each page basic check
        pages_ok = True
        page_details = []
        for i, page in enumerate(reader.pages):
            try:
                page_info = {
                    "page": i + 1,
                    "width": float(page.mediabox.width),
                    "height": float(page.mediabox.height),
                    "has_text": bool(page.extract_text()),
                }
                page_details.append(page_info)
            except Exception as e:
                pages_ok = False
                page_details.append({"page": i + 1, "error": str(e)})

        result["checks"]["pages_ok"] = pages_ok
        result["checks"]["page_details"] = page_details

        # Check 7: Annotations (potential signatures)
        annotations = []
        for i, page in enumerate(reader.pages):
            if "/Annots" in page:
                annots = page["/Annots"]
                for annot in annots:
                    annot_obj = annot.get_object()
                    subtype = str(annot_obj.get("/Subtype", ""))
                    if subtype == "/Widget" or "/Sig" in str(annot_obj.get("/FT", "")):
                        annotations.append({
                            "page": i + 1,
                            "type": subtype,
                            "rect": str(annot_obj.get("/Rect", "")),
                        })

        result["checks"]["signature_annotations"] = annotations
        result["checks"]["has_signatures"] = len(annotations) > 0

        return result

    def compare_pdfs(self, pdf_path1: str, pdf_path2: str) -> Dict[str, Any]:
        """Compare two PDF files for differences.

        Args:
            pdf_path1: Path to first PDF
            pdf_path2: Path to second PDF

        Returns:
            Dict with comparison results
        """
        result = {
            "file1": pdf_path1,
            "file2": pdf_path2,
            "identical": False,
            "differences": [],
        }

        # File size comparison
        size1 = os.path.getsize(pdf_path1)
        size2 = os.path.getsize(pdf_path2)

        if size1 != size2:
            result["differences"].append(f"File size differs: {size1} vs {size2}")

        # Hash comparison
        hash1 = self._file_hash(pdf_path1, "sha256")
        hash2 = self._file_hash(pdf_path2, "sha256")

        if hash1 != hash2:
            result["differences"].append("File content differs (SHA-256 mismatch)")
        else:
            result["identical"] = True

        # Page count comparison
        try:
            reader1 = PdfReader(pdf_path1)
            reader2 = PdfReader(pdf_path2)

            if len(reader1.pages) != len(reader2.pages):
                result["differences"].append(
                    f"Page count differs: {len(reader1.pages)} vs {len(reader2.pages)}"
                )

            # Text content comparison
            for i, (p1, p2) in enumerate(zip(reader1.pages, reader2.pages)):
                text1 = (p1.extract_text() or "").strip()
                text2 = (p2.extract_text() or "").strip()
                if text1 != text2:
                    result["differences"].append(f"Page {i + 1} text content differs")

        except Exception as e:
            result["differences"].append(f"Error during comparison: {e}")

        return result

    def extract_info(self, pdf_path: str) -> Dict[str, Any]:
        """Extract comprehensive information from a PDF.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Dict with PDF information
        """
        reader = PdfReader(pdf_path)

        info = {
            "file": pdf_path,
            "size_bytes": os.path.getsize(pdf_path),
            "size_human": self._human_size(os.path.getsize(pdf_path)),
            "pages": len(reader.pages),
            "encrypted": reader.is_encrypted,
            "metadata": {},
        }

        if reader.metadata:
            meta = reader.metadata
            for key in ["/Title", "/Author", "/Subject", "/Creator", "/Producer",
                        "/CreationDate", "/ModDate", "/Keywords"]:
                val = meta.get(key)
                if val:
                    clean_key = key.lstrip("/")
                    info["metadata"][clean_key] = str(val)

        # Page details
        info["page_details"] = []
        for i, page in enumerate(reader.pages):
            rect = page.mediabox
            text = page.extract_text() or ""
            info["page_details"].append({
                "page": i + 1,
                "width": float(rect.width),
                "height": float(rect.height),
                "text_length": len(text),
                "has_annotations": "/Annots" in page,
            })

        return info

    def _file_hash(self, file_path: str, algorithm: str = "sha256") -> str:
        """Calculate file hash."""
        h = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                h.update(chunk)
        return h.hexdigest()

    def _human_size(self, size: int) -> str:
        """Convert bytes to human readable size."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
