import os
import sys
from utils.settings import ConfigManager
from core.instance_manager import InstanceManager
from core.minecraft_runner import MinecraftRunner
from core.java_manager import JavaManager

# Колбеки для прогресу
def callback_set_status(status_text): print(f"\n[Статус]: {status_text}")
def callback_set_progress(progress_value): sys.stdout.write(f"\rПрогрес: {progress_value}%"); sys.stdout.flush()
def callback_set_max(max_value): pass

my_callbacks = {"setStatus": callback_set_status, "setProgress": callback_set_progress, "setMax": callback_set_max}

def main():
    print("=== Тестування Ядра Лаунчера + Автозавантаження Java ===")
    
    config = ConfigManager()
    instances = InstanceManager()
    runner = MinecraftRunner()
    java_manager = JavaManager()

    nickname = config.get("nickname")
    ram = config.get("ram_mb")
    print(f"Налаштування: Нік={nickname}, RAM={ram}MB")

    # ТЕСТУЄМО FORGE!
    test_instance_name = "Test_Forge_1_20_4"
    test_version = "1.20.4"
    test_loader = "Forge"
    
    existing_instances = instances.get_all_instances()
    test_instance = next((i for i in existing_instances if i["name"] == test_instance_name), None)

    if not test_instance:
        try:
            test_instance = instances.create_instance(
                name=test_instance_name, 
                version=test_version, 
                loader_type=test_loader
            )
            print(f"Інстанс '{test_instance_name}' створено!")
        except Exception as e:
            print(f"Помилка: {e}"); return
    else:
        print(f"Інстанс '{test_instance_name}' вже існує.")

    # 1. Спочатку вирішуємо питання з Java (Forge інсталятор не запрацює без неї!)
    print("\n--- Пошук/Завантаження Java ---")
    required_java = java_manager.get_required_java_version(test_version)
    print(f"Для Minecraft {test_version} потрібна Java {required_java}")
    
    java_path = java_manager.get_java_executable(required_java)
    if not java_path:
        print("КРИТИЧНА ПОМИЛКА: Не вдалося знайти або завантажити Java!")
        return

    # 2. Тепер встановлюємо гру, ПЕРЕДАЮЧИ шлях до Java
    print("\n--- Перевірка/Встановлення файлів ---")
    success = runner.install_instance(test_instance, callback_dict=my_callbacks, java_path=java_path)
    if not success:
        print("\nВстановлення не вдалося!")
        return

    # 3. Запуск
    print("\n--- Спроба запуску ---")
    success = runner.launch_instance(test_instance, nickname, ram, java_path=java_path)
    if success:
        print("Гра (Forge) запущена з автоматично визначеною Java!")
    else:
        print("Не вдалося запустити гру.")

if __name__ == "__main__":
    main()