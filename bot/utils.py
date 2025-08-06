import os


def load_dotenv(filepath: str = '.env'):
    if not os.path.exists(filepath): return

    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue

            if '=' in line:
                key, value = line.split('=')
                key = key.strip()
                value = value.strip().strip('"').strip('\'')

                if key not in os.environ:
                    os.environ[key] = value
