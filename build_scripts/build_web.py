# Скрипт для сборки веб-версии для сайта

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_web():
    """Собирает игру в веб-версию используя pygbag."""
    
    # Путь к корню проекта
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Проверяем, установлен ли pygbag
    try:
        import pygbag
        print("pygbag найден.")
    except ImportError:
        print("pygbag не установлен. Устанавливаю...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygbag"])
        print("pygbag установлен.")
    
    main_script = project_root / "main.py"
    output_dir = project_root / "web_build"
    
    # Очищаем предыдущую сборку
    if output_dir.exists():
        print(f"Удаляю старую сборку из {output_dir}...")
        shutil.rmtree(output_dir)
    
    print(f"Начинаю сборку веб-версии...")
    print(f"Исходный файл: {main_script}")
    print(f"Выходная директория: {output_dir}")
    
    try:
        # Команда для pygbag
        # pygbag работает через python -m pygbag
        cmd = [
            sys.executable, "-m", "pygbag",
            "--title", "Тетрис",
            "--icon", "none",  # Можно добавить иконку
            "--build",
            str(main_script)
        ]
        
        print(f"Команда: {' '.join(cmd)}")
        subprocess.check_call(cmd)
        
        # pygbag создает директорию build/web
        build_web_dir = project_root / "build" / "web"
        if build_web_dir.exists():
            # Копируем в web_build
            if output_dir.exists():
                shutil.rmtree(output_dir)
            shutil.copytree(build_web_dir, output_dir)
            print(f"\n✓ Сборка завершена успешно!")
            print(f"✓ Веб-версия находится в: {output_dir}")
            print(f"\nДля запуска локально:")
            print(f"  python -m http.server 8000")
            print(f"  Затем откройте http://localhost:8000/{output_dir.name}/index.html")
            print(f"\nДля размещения на сервере:")
            print(f"  Загрузите содержимое папки {output_dir} на ваш веб-сервер")
        else:
            print("\n✗ Директория сборки не найдена. Проверьте вывод pygbag выше.")
            
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Ошибка при сборке: {e}")
        print("\nПримечание: pygbag может требовать дополнительных зависимостей.")
        print("Убедитесь, что установлены все необходимые пакеты.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Неожиданная ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    build_web()
