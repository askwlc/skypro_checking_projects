import subprocess


def check_file_flake8(file_path: str) -> str:
    """Функция проверки файла с помощью линтера flake8."""
    result = subprocess.run(['flake8', file_path], capture_output=True, text=True)
    return result.stdout
