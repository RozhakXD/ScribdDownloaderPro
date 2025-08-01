import time
import base64
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BrowserHandler:
    """
    Mengelola interaksi dengan browser (Chrome) menggunakan Selenium untuk
    meng-scrape halaman dan mencetaknya ke PDF.
    """
    def __init__(self, logger):
        self.logger = logger
        self.driver = None

    def _setup_driver(self):
        """Mengkonfigurasi dan menginisialisasi instance Chrome WebDriver."""
        self.logger.debug("Mempersiapkan opsi untuk Chrome WebDriver...")
        options = Options()

        #options.add_argument("--headless") # Menjalankan Chrome di background
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-dev-shm-usage")

        app_state = {
            "recentDestinations": [{"id": "Save as PDF", "origin": "local", "account": ""}],
            "selectedDestinationId": "Save as PDF",
            "version": 2
        }
        options.add_experimental_option("prefs", {
            "printing.print_preview_sticky_settings.appState": base64.b64encode(str(app_state).encode()).decode('utf-8'),
        })

        try:
            self.logger.debug("Membuat instance Chrome WebDriver...")
            self.driver = webdriver.Chrome(options=options)
        except Exception as e:
            self.logger.error("Gagal memulai WebDriver. Pastikan ChromeDriver sudah terinstall dan cocok dengan versi Chrome Anda.")
            self.logger.error(f"Detail Error: {e}")
            self.driver = None

    def _scroll_all_pages(self):
        """
        Menggulir setiap halaman dokumen satu per satu, meniru logika andal
        dari skrip run.py asli untuk memastikan semua konten dirender.
        """
        self.logger.info("Memulai proses menggulir halaman...")
        try:
            self.logger.debug("Memberi jeda 5 detik untuk inisialisasi halaman...")
            time.sleep(5)

            page_elements = self.driver.find_elements(By.CSS_SELECTOR, "[class*='page']")

            if not page_elements:
                self.logger.error("KRITIS: Tidak ada elemen halaman yang ditemukan dengan selector '[class*=\"page\"]'. Proses unduh tidak akan lengkap.")
                return
            
            total_pages = len(page_elements)
            self.logger.info(f"Ditemukan {total_pages} elemen halaman. Memulai proses gulir...")

            for i, page in enumerate(page_elements):
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView();", page)
                    self.logger.debug(f"Menggulir ke halaman {i + 1}/{total_pages}")

                    time.sleep(3)  # Memberi jeda untuk memastikan halaman dirender
                except Exception as e:
                    self.logger.warning(f"Gagal menggulir ke elemen halaman {i+1}: {e}")
            
            self.logger.info("Selesai menggulir semua halaman.")
        except Exception as e:
            self.logger.error(f"Terjadi kesalahan tak terduga saat proses scrolling: {e}")

    def _clean_ui_elements(self):
        """Menghapus elemen UI yang tidak diinginkan dari halaman."""
        self.logger.debug("Menghapus elemen UI yang mengganggu (toolbar, etc)...")
        scripts_to_run = [
            "var el = document.querySelector('.toolbar_top'); if (el) el.parentNode.removeChild(el);",
            "var el = document.querySelector('.toolbar_bottom'); if (el) el.parentNode.removeChild(el);",
            "var els = document.querySelectorAll('.document_scroller'); for (var i = 0; i < els.length; i++) { els[i].setAttribute('class', ''); }"
        ]
        for script in scripts_to_run:
            try:
                self.driver.execute_script(script)
            except Exception as e:
                self.logger.warning(f"Gagal menjalankan skrip pembersihan: {e}")

    def _print_to_pdf(self):
        """Mencetak halaman saat ini ke format PDF (dalam bentuk bytes)."""
        self.logger.info("Membuat PDF dari konten browser...")
        try:
            pdf_data = self.driver.execute_cdp_cmd("Page.printToPDF", {
                "landscape": False,
                "displayHeaderFooter": False,
                "printBackground": True,
                "preferCSSPageSize": True,
            })
            return base64.b64decode(pdf_data['data'])
        except Exception as e:
            self.logger.error(f"Gagal saat menjalankan perintah Page.printToPDF: {e}")
            return None

    def get_pdf_from_url(self, url):
        """
        Fungsi utama untuk membuka URL, melakukan scraping, dan menghasilkan PDF.
        """
        self._setup_driver()
        if not self.driver:
            return None
        
        pdf_bytes = None
        try:
            self.logger.info(f"Mengakses URL: {url}")
            self.driver.get(url)

            self._scroll_all_pages()

            self._clean_ui_elements()
            time.sleep(1)
            pdf_bytes = self._print_to_pdf()
        except Exception as e:
            self.logger.error(f"Terjadi kesalahan pada proses browser: {e}")
        
        finally:
            if self.driver:
                self.logger.debug("Menutup WebDriver...")
                self.driver.quit()

        return pdf_bytes