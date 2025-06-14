import os
import subprocess
import requests
from dotenv import load_dotenv

# Load .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
REPO_PATHS_FILE = "repo_paths.txt"
LOG_FILE = "last_commit.txt"

def get_git_info(repo_path):
    try:
        commit_hash = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=repo_path
        ).decode().strip()
        
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=repo_path
        ).decode().strip()

        return commit_hash, branch
    except subprocess.CalledProcessError:
        return None, None

def collect_commits():
    results = []
    if not os.path.exists(REPO_PATHS_FILE):
        print(f"[ERROR] File {REPO_PATHS_FILE} tidak ditemukan.")
        return results

    with open(REPO_PATHS_FILE) as f:
        for line in f:
            path = line.strip()
            if not os.path.isdir(path):
                continue
            git_path = os.path.join(path, ".git")
            if os.path.exists(git_path):
                commit, branch = get_git_info(path)
                if commit:
                    results.append(f"[{os.path.basename(path)}] {commit} ({branch})")
                else:
                    results.append(f"[{os.path.basename(path)}] Gagal membaca commit")
    return results

def save_to_file(logs):
    with open(LOG_FILE, "w") as f:
        f.write("\n".join(logs))
    print(f"[INFO] Log ditulis ke {LOG_FILE}")

def send_as_text(logs):
    message = "📌 *Last Git Commit Log:*\n\n" + "\n".join(logs)
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    res = requests.post(url, data=payload)
    if res.status_code == 200:
        print("[INFO] Pesan berhasil dikirim ke Telegram.")
    else:
        print(f"[ERROR] Gagal kirim pesan: {res.text}")

def send_as_file():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    with open(LOG_FILE, "rb") as file:
        res = requests.post(url, data={
            "chat_id": CHAT_ID,
            "caption": "📄 Log commit Git terbaru"
        }, files={"document": file})
    if res.status_code == 200:
        print("[INFO] File berhasil dikirim ke Telegram.")
    else:
        print(f"[ERROR] Gagal kirim file: {res.text}")

def prompt_kirim_mode():
    print("\nPilih mode pengiriman ke Telegram:")
    print("1. Kirim sebagai pesan teks")
    print("2. Kirim sebagai file lampiran")
    print("3. Kirim sebagai pesan + file")
    print("4. Tidak usah kirim")
    
    pilihan = input("Masukkan pilihan [1-4]: ").strip()
    return pilihan

if __name__ == "__main__":
    logs = collect_commits()
    if logs:
        save_to_file(logs)

        mode = prompt_kirim_mode()

        if mode == "1":
            send_as_text(logs)
        elif mode == "2":
            send_as_file()
        elif mode == "3":
            send_as_text(logs)
            send_as_file()
        else:
            print("[INFO] Pengiriman ke Telegram dibatalkan.")
    else:
        print("[INFO] Tidak ada repo Git yang valid ditemukan.")
