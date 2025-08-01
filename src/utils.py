import re

def get_document_id_from_url(url_or_id: str) -> str | None:
    """
    Mengekstrak ID dokumen dari berbagai format URL Scribd atau
    jika inputnya adalah ID itu sendiri.

    Args:
        url_or_id (str): URL Scribd atau ID dokumen.

    Returns:
        str: ID dokumen jika ditemukan, selain itu None.
    """
    match = re.search(r'(?:document|embeds)/(\d+)', url_or_id)
    if match:
        return match.group(1)

    if url_or_id.isdigit():
        return url_or_id
    
    return None

def sanitize_filename(filename: str) -> str:
    """
    Membersihkan string agar bisa digunakan sebagai nama file yang valid
    dengan menghapus atau mengganti karakter ilegal.

    Args:
        filename (str): Nama file asli.

    Returns:
        str: Nama file yang sudah dibersihkan.
    """
    if not filename:
        return "untitled"
    
    return re.sub(r'[\\/*?:"<>|]', "", filename).strip()