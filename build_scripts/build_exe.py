# Скрипт для сборки в .exe приложение

import os
import sys
import subprocess
from pathlib import Path

def build_exe():
    """Собирает игру в .exe файл используя PyInstaller."""
    
    # Путь к корню проекта
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Проверяем, установлен ли PyInstaller
    try:
        import PyInstaller
        print("PyInstaller найден.")
    except ImportError:
        print("PyInstaller не установлен. Устанавливаю...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller установлен.")
    
    # Параметры для PyInstaller
    main_script = project_root / "main.py"
    name = "Tetris"
    icon = None  # Можно добавить иконку, если есть
    
    # Собираем команду
    cmd = [
        "pyinstaller",
        "--name", name,
        "--onefile",  # Один файл .exe
        "--windowed",  # Без консоли (для GUI приложения)
        "--clean",  # Очистить временные файлы
        str(main_script)
    ]
    
    # Добавляем иконку, если она есть
    icon_path = project_root / "icon.ico"
    if icon_path.exists():
        cmd.extend(["--icon", str(icon_path)])
    
    print(f"Начинаю сборку {name}.exe...")
    print(f"Команда: {' '.join(cmd)}")
    
    try:
        # Запускаем PyInstaller
        subprocess.check_call(cmd)
        
        exe_path = project_root / "dist" / f"{name}.exe"
        if exe_path.exists():
            print(f"\n✓ Сборка завершена успешно!")
            print(f"✓ Исполняемый файл: {exe_path}")
            print(f"✓ Размер файла: {exe_path.stat().st_size / (1024*1024):.2f} MB")
        else:
            print("\n✗ Файл .exe не найден. Проверьте вывод PyInstaller выше.")
            
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Ошибка при сборке: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Неожиданная ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    build_exe()
