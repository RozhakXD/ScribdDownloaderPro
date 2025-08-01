import os
from .metadata_fetcher import MetadataFetcher
from .browser_handler import BrowserHandler
from .pdf_processor import PDFProcessor
from .utils import get_document_id_from_url, sanitize_filename

class Downloader:
    """
    Mengorkestrasi proses pengunduhan dokumen dari Scribd, mulai dari
    pengambilan metadata, interaksi browser, hingga pemrosesan PDF.
    """
    def __init__(self, url_or_id, compress, clean, logger):
        self.url_or_id = url_or_id
        self.compress = compress
        self.clean = clean
        self.logger = logger
        self.output_dir = "downloads"

    def run(self):
        """
        Menjalankan seluruh alur kerja pengunduhan.
        """
        self.logger.info("="*50)
        self.logger.info("Memulai Proses Unduh Dokumen Scribd")
        self.logger.info("="*50)

        doc_id = get_document_id_from_url(self.url_or_id)
        if not doc_id:
            self.logger.error(f"URL atau ID tidak valid: '{self.url_or_id}'")
            return
        self.logger.info(f"Berhasil mengekstrak ID Dokumen: {doc_id}")

        metadata_fetcher = MetadataFetcher(doc_id, self.logger)
        metadata = metadata_fetcher.fetch()

        doc_title = metadata.get("title", f"scribd_document_{doc_id}")
        self.logger.info(f"Judul Dokumen: {doc_title}")
        self.logger.info(f"Jumlah Halaman: {metadata.get('page_count', 'N/A')}")

        browser_handler = BrowserHandler(self.logger)

        embed_url = f"https://www.scribd.com/embeds/{doc_id}/content"

        pdf_bytes = browser_handler.get_pdf_from_url(embed_url)

        if not pdf_bytes:
            self.logger.error("Gagal menghasilkan PDF dari browser. Proses dihentikan.")
            return
        self.logger.info("Berhasil membuat file PDF dari browser.")

        pdf_processor = PDFProcessor(self.logger)
        processed_pdf = pdf_bytes

        if self.clean:
            self.logger.info("Memulai proses pembersihan halaman kosong...")
            processed_pdf = pdf_processor.remove_blank_pages(processed_pdf)
        else:
            self.logger.info("Melewati proses pembersihan halaman kosong.")

        if self.compress:
            self.logger.info("Memulai proses kompresi PDF...")
            processed_pdf = pdf_processor.compress_pdf(processed_pdf)
        else:
            self.logger.info("Melewati proses kompresi PDF.")

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            self.logger.info(f"Direktori '{self.output_dir}' berhasil dibuat.")
        
        safe_filename = sanitize_filename(doc_title) + ".pdf"
        output_path = os.path.join(self.output_dir, safe_filename)

        pdf_processor.save_pdf(processed_pdf, output_path)

        file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
        self.logger.info("="*50)
        self.logger.info("🎉 PROSES SELESAI 🎉")
        self.logger.info(f"File berhasil disimpan di: {output_path}")
        self.logger.info(f"Ukuran File: {file_size_mb:.2f} MB")
        self.logger.info("="*50)