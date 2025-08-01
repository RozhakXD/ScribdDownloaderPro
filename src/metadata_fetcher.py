import requests
import re

class MetadataFetcher:
    """
    Mengambil metadata dokumen (seperti judul dan jumlah halaman) dari
    halaman embed Scribd menggunakan requests.
    """
    def __init__(self, doc_id, logger):
        self.doc_id = doc_id
        self.logger = logger
        self.embed_url = f"https://www.scribd.com/embeds/{self.doc_id}/content"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        }

    def fetch(self):
        """
        Mengambil konten halaman dan mengekstrak metadata.
        
        Returns:
            dict: Sebuah dictionary berisi metadata (title, page_count).
        """
        self.logger.info("Mengambil metadata dokumen...")
        try:
            response = requests.get(self.embed_url, headers=self.headers, allow_redirects=True)
            response.raise_for_status()

            content = response.text

            title_match = re.search(r'"title"\s*:\s*"(.*?)"', content)

            page_count_match = re.search(r'"page_count"\s*:\s*(\d+)', content)

            title = title_match.group(1).strip() if title_match else None
            page_count = page_count_match.group(1) if page_count_match else None

            if not page_count:
                 self.logger.warning("Jumlah halaman tidak ditemukan.")
            if not title:
                self.logger.warning("Judul dokumen tidak ditemukan, akan menggunakan nama default.")
            
            return {
                "title": title,
                "page_count": page_count
            }
        except requests.RequestException as e:
            self.logger.error(f"Gagal mengambil metadata dari {self.embed_url}: {e}")
            return {}