import os
import base64
from pathlib import Path
import dotenv


def is_docker():
    cgroup = Path("/proc/self/cgroup")
    return Path("/.dockerenv").is_file() or (
        cgroup.is_file() and "docker" in cgroup.read_text()
    )


if not is_docker():
    dotenv.load_dotenv()

N_API_KEY = os.environ["NEON_API_KEY"]
N_USER = os.environ["NEON_USER"]

# Neon Account Info
N_AUTH = f"{N_USER}:{N_API_KEY}"
N_BASE_URL = "https://api.neoncrm.com"
N_SIGNATURE = base64.b64encode(bytearray(N_AUTH.encode())).decode()
N_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {N_SIGNATURE}",
}
