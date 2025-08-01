import argparse
import sys
from src.downloader import Downloader
from src.logger import setup_logger

def main():
    """Fungsi utama untuk menjalankan aplikasi dari command line."""

    parser = argparse.ArgumentParser(
        description="Scribd Downloader Pro - Unduh dokumen dari Scribd dengan mudah.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "url_or_id",
        help="URL lengkap atau ID dokumen Scribd yang ingin diunduh."
    )

    parser.add_argument(
        "--compress",
        action="store_true",
        help="Aktifkan kompresi PDF setelah diunduh (memerlukan Ghostscript)."
    )

    parser.add_argument(
        "--no-clean",
        dest="clean",
        action="store_false",
        help="Nonaktifkan fitur penghapusan halaman kosong dari PDF."
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Tampilkan log yang lebih detail untuk proses debug."
    )

    args = parser.parse_args()

    log_level = "DEBUG" if args.verbose else "INFO"
    logger = setup_logger(level=log_level)

    try:
        downloader = Downloader(
            url_or_id=args.url_or_id,
            compress=args.compress,
            clean=args.clean,
            logger=logger
        )
        downloader.run()
    except Exception as e:
        logger.error(f"Terjadi kesalahan fatal yang tidak terduga: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()