import sys


def fail_with_message(msg: str):
    print(f'❌  {msg}', file=sys.stderr)
    sys.exit(1)


def progress_with_message(title: str, percent: float):
    print(f' 🔄  {title} ({percent * 100:.0f}%)', end='\r')


def success_with_message(msg: str):
    print(f'✅  {msg}')
