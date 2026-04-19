import sys
from unittest.mock import MagicMock

# Comprehensive mocking of all missing dependencies
mock_modules = [
    'yt_dlp', 'appdirs', 'Crypto', 'Crypto.Cipher', 'customtkinter',
    'PIL', 'PIL.Image', 'PIL.ImageTk', 'requests', 'curl_cffi',
    'prompt_toolkit', 'prompt_toolkit.styles', 'easygui'
]

for module in mock_modules:
    sys.modules[module] = MagicMock()

class MockTask:
    def __init__(self, id, description, total, completed):
        self.id = id
        self.description = description
        self.total = total
        self.completed = completed

class MockProgress:
    def __init__(self, *args, **kwargs):
        self.tasks = []
        self.next_id = 0

    def add_task(self, description, total=None, completed=0):
        task = MockTask(self.next_id, description, total, completed)
        self.tasks.append(task)
        self.next_id += 1
        return task.id

    def update(self, task_id, description=None, total=None, completed=None):
        for task in self.tasks:
            if task.id == task_id:
                if description is not None: task.description = description
                if total is not None: task.total = total
                if completed is not None: task.completed = completed
                break

# Mock rich BEFORE importing cli_tools
rich_mock = MagicMock()
sys.modules['rich'] = rich_mock
sys.modules['rich.panel'] = MagicMock()
sys.modules['rich.console'] = MagicMock()
sys.modules['rich.live'] = MagicMock()
sys.modules['rich.table'] = MagicMock()

rich_progress_mock = MagicMock()
rich_progress_mock.Progress = MockProgress
rich_progress_mock.SpinnerColumn = MagicMock()
rich_progress_mock.TextColumn = MagicMock()
rich_progress_mock.BarColumn = MagicMock()
rich_progress_mock.DownloadColumn = MagicMock()
rich_progress_mock.TimeRemainingColumn = MagicMock()
rich_progress_mock.TaskProgressColumn = MagicMock()
rich_progress_mock.TransferSpeedColumn = MagicMock()
sys.modules['rich.progress'] = rich_progress_mock

from turkanime_api.cli.cli_tools import VidSearchCLI

def test_callback_working_player():
    cli = VidSearchCLI()
    hook = {
        "player": "YADISK",
        "status": "çalışıyor",
        "total": 5,
        "current": 1
    }
    print("\n--- Testing working player ---")
    cli.callback(hook)

    if not cli.progress.tasks:
        print("FAIL: No tasks in progress")
        sys.exit(1)

    task = cli.progress.tasks[0]
    print(f"DEBUG: final description='{task.description}', completed={task.completed}, total={task.total}")
    if task.description != "YADISK çalışıyor!":
        print(f"FAIL: Expected 'YADISK çalışıyor!', got '{task.description}'")
        sys.exit(1)
    if task.completed != 5:
        print(f"FAIL: Expected 5, got {task.completed}")
        sys.exit(1)
    if task.total != 5:
        print(f"FAIL: Expected 5, got {task.total}")
        sys.exit(1)

def test_callback_not_working_player():
    cli = VidSearchCLI()
    hook = {
        "player": "MAIL",
        "status": "çalışmıyor",
        "total": 5,
        "current": 2
    }
    print("\n--- Testing non-working player ---")
    cli.callback(hook)

    if not cli.progress.tasks:
        print("FAIL: No tasks in progress")
        sys.exit(1)

    task = cli.progress.tasks[0]
    print(f"DEBUG: final description='{task.description}', completed={task.completed}, total={task.total}")
    if task.description != "MAIL çalışmıyor.":
        print(f"FAIL: Expected 'MAIL çalışmıyor.', got '{task.description}'")
        sys.exit(1)
    if task.completed != 2:
        print(f"FAIL: Expected 2, got {task.completed}")
        sys.exit(1)
    if task.total != 5:
        print(f"FAIL: Expected 5, got {task.total}")
        sys.exit(1)

def test_callback_none_working():
    cli = VidSearchCLI()
    hook = {
        "status": "hiçbiri çalışmıyor",
        "total": 5,
        "current": 5
    }
    print("\n--- Testing none working ---")
    cli.callback(hook)

    if not cli.progress.tasks:
        print("FAIL: No tasks in progress")
        sys.exit(1)

    task = cli.progress.tasks[0]
    print(f"DEBUG: final description='{task.description}', completed={task.completed}, total={task.total}")
    # Should show error message for "hiçbiri çalışmıyor"
    expected = "[red]Hiçbiri çalışmıyor![/red]"
    if task.description != expected:
        print(f"FAIL: Expected '{expected}', got '{task.description}'")
        sys.exit(1)
    if task.completed != 5:
        print(f"FAIL: Expected 5, got {task.completed}")
        sys.exit(1)
    if task.total != 5:
        print(f"FAIL: Expected 5, got {task.total}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        test_callback_working_player()
        print("test_callback_working_player passed")
        test_callback_not_working_player()
        print("test_callback_not_working_player passed")
        test_callback_none_working()
        print("test_callback_none_working passed")
    except Exception as e:
        print(f"An error occurred: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
