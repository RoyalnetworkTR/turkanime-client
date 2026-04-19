import sys
from unittest.mock import MagicMock

# Mock necessary modules that might be missing in the environment
sys.modules['yt_dlp'] = MagicMock()
sys.modules['customtkinter'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['PIL.Image'] = MagicMock()
sys.modules['PIL.ImageTk'] = MagicMock()
sys.modules['appdirs'] = MagicMock()
sys.modules['Crypto'] = MagicMock()
sys.modules['Crypto.Cipher'] = MagicMock()
sys.modules['Crypto.Cipher.AES'] = MagicMock()
sys.modules['Crypto.Util.Padding'] = MagicMock()
sys.modules['curl_cffi'] = MagicMock()
sys.modules['curl_cffi.requests'] = MagicMock()
sys.modules['prompt_toolkit'] = MagicMock()
sys.modules['prompt_toolkit.styles'] = MagicMock()
sys.modules['easygui'] = MagicMock()
sys.modules['questionary'] = MagicMock()
sys.modules['toml'] = MagicMock()
sys.modules['rich'] = MagicMock()
sys.modules['rich.panel'] = MagicMock()
sys.modules['rich.console'] = MagicMock()
sys.modules['rich.progress'] = MagicMock()

import unittest
# After mocking 'rich', indirme_task_cli will use the mock rprint
from turkanime_api.cli.cli_tools import indirme_task_cli

class TestCLIErrors(unittest.TestCase):
    def test_indirme_task_cli_no_video(self):
        # Mock bolum
        bolum = MagicMock()
        bolum.slug = "test-bolum-1"
        bolum.best_video.return_value = None

        # Mock table
        table = MagicMock()

        # Mock dosya
        dosya = MagicMock()
        dosya.ayarlar = {"max resolution": 1080}

        from turkanime_api.cli import cli_tools
        cli_tools.rprint = MagicMock()

        indirme_task_cli(bolum, table, dosya)

        # Verify rprint was called with the expected error message
        expected_msg = "[red]Hata:[/red] test-bolum-1 için uygun video bulunamadı."
        cli_tools.rprint.assert_any_call(expected_msg)

    def test_vid_search_cli_callback_error(self):
        from turkanime_api.cli.cli_tools import VidSearchCLI
        vid_cli = VidSearchCLI()

        # Mock progress update
        vid_cli.progress.update = MagicMock()
        vid_cli.progress.tasks = [MagicMock(id=1)]

        hook = {"status": "hiçbiri çalışmıyor", "total": 10, "current": 10}
        vid_cli.callback(hook)

        # Verify message was updated with error
        vid_cli.progress.update.assert_called()
        args, kwargs = vid_cli.progress.update.call_args
        self.assertEqual(kwargs['description'], "[red]Hiçbir video çalışmıyor![/red]")

    def test_download_cli_ytdl_callback_error(self):
        from turkanime_api.cli.cli_tools import DownloadCLI
        dl_cli = DownloadCLI()

        # Mock progress update
        dl_cli.progress.update = MagicMock()
        task_mock = MagicMock(id=99)
        dl_cli.progress.tasks = [task_mock]

        hook = {"status": "error", "message": "Connection timeout"}

        from turkanime_api.cli import cli_tools
        cli_tools.rprint = MagicMock()

        dl_cli.ytdl_callback(hook)

        # Verify rprint was called
        cli_tools.rprint.assert_called_with("[red]Hata:[/red] Connection timeout")

        # Verify progress bar update
        dl_cli.progress.update.assert_called_with(99, description="[red]Hata: Connection timeout[/red]")

if __name__ == '__main__':
    unittest.main()
