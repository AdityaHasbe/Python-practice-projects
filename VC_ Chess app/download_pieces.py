import os
import urllib.request
import time

def download_chess_pieces():
    # Ensure the directory exists
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pieces_dir = os.path.join(base_dir, "assets", "pieces")
    os.makedirs(pieces_dir, exist_ok=True)

    # Wikipedia URLs for standard chess SVGs
    urls = {
        'wp': 'https://upload.wikimedia.org/wikipedia/commons/4/45/Chess_plt45.svg',
        'wn': 'https://upload.wikimedia.org/wikipedia/commons/7/70/Chess_nlt45.svg',
        'wb': 'https://upload.wikimedia.org/wikipedia/commons/b/b1/Chess_blt45.svg',
        'wr': 'https://upload.wikimedia.org/wikipedia/commons/7/72/Chess_rlt45.svg',
        'wq': 'https://upload.wikimedia.org/wikipedia/commons/1/15/Chess_qlt45.svg',
        'wk': 'https://upload.wikimedia.org/wikipedia/commons/4/42/Chess_klt45.svg',
        'bp': 'https://upload.wikimedia.org/wikipedia/commons/c/c7/Chess_pdt45.svg',
        'bn': 'https://upload.wikimedia.org/wikipedia/commons/e/ef/Chess_ndt45.svg',
        'bb': 'https://upload.wikimedia.org/wikipedia/commons/9/98/Chess_bdt45.svg',
        'br': 'https://upload.wikimedia.org/wikipedia/commons/f/ff/Chess_rdt45.svg',
        'bq': 'https://upload.wikimedia.org/wikipedia/commons/4/47/Chess_qdt45.svg',
        'bk': 'https://upload.wikimedia.org/wikipedia/commons/f/f0/Chess_kdt45.svg',
    }

    print(f"Downloading pieces to: {pieces_dir}")
    
    # Tells Wikimedia we are a normal web browser
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')]
    urllib.request.install_opener(opener)

    for name, url in urls.items():
        filepath = os.path.join(pieces_dir, f"{name}.svg")
        if not os.path.exists(filepath):
            print(f"Downloading {name}.svg...")
            try:
                urllib.request.urlretrieve(url, filepath)
                time.sleep(2)  # <-- The Magic Pause! Waits 2 seconds before the next one.
            except Exception as e:
                print(f"Failed to download {name}: {e}")
        else:
            print(f"{name}.svg already exists, skipping.")
            
    print("\nAll done! You can run main.py now.")

if __name__ == "__main__":
    download_chess_pieces()