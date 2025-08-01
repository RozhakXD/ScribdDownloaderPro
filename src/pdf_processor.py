import io
import os
import re
import shutil
import subprocess
import sys
import warnings
import tempfile
from PyPDF2 import PdfReader, PdfWriter
import pdfplumber

class StderrRedirect:
    def __init__(self):
        self._stderr = sys.stderr
        self._devnull = open(os.devnull, 'w')

    def __enter__(self):
        sys.stderr = self._devnull
        warnings.filterwarnings("ignore")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stderr = self._stderr
        self._devnull.close()
        warnings.resetwarnings()

class PDFProcessor:
    """Menangani operasi PDF dengan deteksi halaman kosong."""
    def __init__(self, logger):
        self.logger = logger

    def is_page_blank(self, page, page_number):
        """Deteksi halaman kosong dengan redirect stderr."""
        try:
            with io.BytesIO() as temp_pdf:
                writer = PdfWriter()
                writer.add_page(page)
                writer.write(temp_pdf)
                temp_pdf.seek(0)
                with StderrRedirect():
                    with pdfplumber.open(temp_pdf, laparams={
                        'line_margin': 0.1,
                        'char_margin': 0.1,
                        'boxes_flow': None
                    }) as pdf:
                        p = pdf.pages[0]
                        text = p.extract_text(x_tolerance=2, y_tolerance=2) or ""
                        text = re.sub(r'\s+', '', text)
                        has_images = bool(p.images)
                        has_vector = bool(p.curves) or bool(p.lines)
                        if not text and not has_images and not has_vector:
                            self.logger.debug(f"Halaman {page_number+1} terdeteksi kosong")
                            return True
                        return False
        except Exception as e:
            self.logger.warning(f"Gagal memeriksa halaman {page_number+1}: {e}")
            return False

    def remove_blank_pages(self, pdf_bytes):
        """Menghapus halaman kosong dengan redirect stderr."""
        try:
            reader = PdfReader(io.BytesIO(pdf_bytes))
            writer = PdfWriter()
            removed_count = 0
            for i, page in enumerate(reader.pages):
                if not self.is_page_blank(page, i):
                    writer.add_page(page)
                else:
                    removed_count += 1
            msg = f"Berhasil menghapus {removed_count} halaman kosong." if removed_count else "Tidak ada halaman kosong yang terdeteksi."
            self.logger.info(msg)
            output = io.BytesIO()
            writer.write(output)
            return output.getvalue()
        except Exception as e:
            self.logger.error(f"Gagal saat membersihkan halaman kosong: {e}")
            return pdf_bytes

    def compress_pdf(self, pdf_bytes):
        """Mengompres PDF menggunakan Ghostscript jika tersedia, jika tidak fallback ke PyPDF2."""
        gs_path = shutil.which('gs') or shutil.which('gswin64c.exe')
        if gs_path:
            self.logger.info(f"Ghostscript ditemukan di '{gs_path}'. Memulai kompresi canggih.")
            return self._compress_with_ghostscript(pdf_bytes, gs_path)
        self.logger.warning("Ghostscript tidak ditemukan. Menggunakan metode kompresi fallback (kurang efektif).")
        return self._compress_with_pypdf(pdf_bytes)

    def _compress_with_ghostscript(self, pdf_bytes, gs_path):
        """Kompresi menggunakan Ghostscript."""
        temp_input = temp_output = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as f_in:
                f_in.write(pdf_bytes)
                temp_input = f_in.name
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as f_out:
                temp_output = f_out.name
            command = [
                gs_path,
                '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
                '-dPDFSETTINGS=/ebook', '-dNOPAUSE', '-dQUIET',
                '-dBATCH', f'-sOutputFile={temp_output}', temp_input
            ]
            subprocess.run(command, check=True, capture_output=True, text=True)
            with open(temp_output, "rb") as f:
                compressed_bytes = f.read()
            self.logger.info("Kompresi dengan Ghostscript berhasil.")
            return compressed_bytes
        except subprocess.CalledProcessError as e:
            self.logger.error("Gagal menjalankan Ghostscript.")
            self.logger.error(f"Stderr: {e.stderr}")
            return pdf_bytes
        except Exception as e:
            self.logger.error(f"Terjadi kesalahan saat kompresi dengan Ghostscript: {e}")
            return pdf_bytes
        finally:
            for f in (temp_input, temp_output):
                if f and os.path.exists(f):
                    os.remove(f)

    def _compress_with_pypdf(self, pdf_bytes):
        """Kompresi fallback menggunakan PyPDF2."""
        try:
            reader = PdfReader(io.BytesIO(pdf_bytes))
            writer = PdfWriter()
            for page in reader.pages:
                page.compress_content_streams()
                writer.add_page(page)
            output = io.BytesIO()
            writer.write(output)
            self.logger.info("Kompresi fallback dengan PyPDF2 selesai.")
            return output.getvalue()
        except Exception as e:
            self.logger.error(f"Gagal saat kompresi dengan PyPDF2: {e}")
            return pdf_bytes

    def save_pdf(self, pdf_bytes, path):
        """Menyimpan bytes PDF ke file."""
        try:
            with open(path, "wb") as f:
                f.write(pdf_bytes)
            self.logger.debug(f"File berhasil disimpan di: {path}")
        except IOError as e:
            self.logger.error(f"Gagal menyimpan file ke '{path}': {e}")