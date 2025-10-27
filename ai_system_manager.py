#!/usr/bin/env python3
"""
AI-менеджер системы - интеллектуальное управление компьютером
"""

import json
import os
from typing import Dict, Any, List
from mac_client import MacSystemClient

class AISystemManager:
    def __init__(self):
        self.client = MacSystemClient()
        self.context = {}
    
    def analyze_system_health(self) -> Dict[str, Any]:
        """Анализ здоровья системы"""
        print("🔍 Анализирую состояние системы...")
        
        # Получаем системную информацию
        system_info = self.client.get_system_info()
        
        # Анализируем дисковое пространство
        disk_info = self.client.execute_command("disk_space")
        
        # Анализируем память
        memory_info = self.client.execute_command("memory_usage")
        
        # Формируем отчет
        health_report = {
            "system": system_info,
            "disk": disk_info,
            "memory": memory_info,
            "recommendations": []
        }
        
        # Анализируем и даем рекомендации
        if disk_info.get("success"):
            disk_output = disk_info.get("output", "")
            if "90%" in disk_output or "95%" in disk_output:
                health_report["recommendations"].append(
                    "⚠️ Дисковое пространство заканчивается! Рекомендуется очистить временные файлы."
                )
        
        if memory_info.get("success"):
            memory_output = memory_info.get("output", "")
            if "90%" in memory_output:
                health_report["recommendations"].append(
                    "⚠️ Высокое использование памяти! Рекомендуется перезагрузить систему."
                )
        
        return health_report
    
    def optimize_development_environment(self) -> Dict[str, Any]:
        """Оптимизация среды разработки"""
        print("⚙️ Оптимизирую среду разработки...")
        
        # Анализируем текущий проект
        project_analysis = self.client.analyze_project(".")
        
        # Проверяем Python зависимости
        pip_list = self.client.execute_command("pip_list")
        
        # Проверяем Git статус
        git_status = self.client.execute_command("git_status")
        
        optimization_report = {
            "project": project_analysis,
            "dependencies": pip_list,
            "git_status": git_status,
            "actions": []
        }
        
        # Рекомендации по оптимизации
        if git_status.get("success") and "Untracked files" in git_status.get("output", ""):
            optimization_report["actions"].append(
                "📝 Есть неотслеживаемые файлы. Рекомендуется добавить их в Git."
            )
        
        if pip_list.get("success"):
            deps_output = pip_list.get("output", "")
            if "outdated" in deps_output or "WARNING" in deps_output:
                optimization_report["actions"].append(
                    "📦 Есть устаревшие пакеты. Рекомендуется обновить зависимости."
                )
        
        return optimization_report
    
    def install_development_tools(self, tools: List[str]) -> Dict[str, Any]:
        """Установка инструментов разработки"""
        print(f"🛠️ Устанавливаю инструменты: {', '.join(tools)}")
        
        results = {}
        for tool in tools:
            print(f"📦 Устанавливаю {tool}...")
            result = self.client.install_package(tool)
            results[tool] = result
            
            if result.get("success"):
                print(f"✅ {tool} установлен успешно")
            else:
                print(f"❌ Ошибка установки {tool}: {result.get('error')}")
        
        return results
    
    def create_project_structure(self, project_name: str, project_type: str = "python") -> Dict[str, Any]:
        """Создание структуры проекта"""
        print(f"📁 Создаю структуру проекта: {project_name}")
        
        # Определяем структуру в зависимости от типа проекта
        if project_type == "python":
            structure = {
                "folders": [
                    f"{project_name}",
                    f"{project_name}/src",
                    f"{project_name}/tests",
                    f"{project_name}/docs",
                    f"{project_name}/data"
                ],
                "files": [
                    f"{project_name}/README.md",
                    f"{project_name}/requirements.txt",
                    f"{project_name}/setup.py",
                    f"{project_name}/src/__init__.py",
                    f"{project_name}/tests/__init__.py"
                ]
            }
        elif project_type == "web":
            structure = {
                "folders": [
                    f"{project_name}",
                    f"{project_name}/frontend",
                    f"{project_name}/backend",
                    f"{project_name}/static",
                    f"{project_name}/templates"
                ],
                "files": [
                    f"{project_name}/README.md",
                    f"{project_name}/package.json",
                    f"{project_name}/requirements.txt"
                ]
            }
        else:
            return {"error": f"Неизвестный тип проекта: {project_type}"}
        
        # Создаем структуру
        try:
            for folder in structure["folders"]:
                os.makedirs(folder, exist_ok=True)
                print(f"📁 Создана папка: {folder}")
            
            for file in structure["files"]:
                with open(file, 'w') as f:
                    f.write(f"# {project_name}\n\nАвтоматически создано AI-менеджером системы.\n")
                print(f"📄 Создан файл: {file}")
            
            return {
                "success": True,
                "project_name": project_name,
                "structure": structure
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def run_diagnostic(self) -> Dict[str, Any]:
        """Полная диагностика системы"""
        print("🔬 Запускаю полную диагностику системы...")
        
        diagnostic = {
            "system_health": self.analyze_system_health(),
            "development_environment": self.optimize_development_environment(),
            "available_commands": [
                "system_info", "disk_space", "memory_usage", 
                "process_list", "network_status", "file_list",
                "git_status", "python_version", "pip_list", "brew_list"
            ]
        }
        
        return diagnostic

def main():
    """Демонстрация работы AI-менеджера системы"""
    manager = AISystemManager()
    
    print("🤖 AI-менеджер системы запущен!")
    print("=" * 50)
    
    # Полная диагностика
    diagnostic = manager.run_diagnostic()
    
    print("\n📊 РЕЗУЛЬТАТЫ ДИАГНОСТИКИ:")
    print(json.dumps(diagnostic, indent=2, ensure_ascii=False))
    
    # Создание тестового проекта
    print("\n📁 СОЗДАНИЕ ТЕСТОВОГО ПРОЕКТА:")
    project_result = manager.create_project_structure("test_ai_project", "python")
    print(json.dumps(project_result, indent=2, ensure_ascii=False))
    
    print("\n✅ Диагностика завершена!")

if __name__ == "__main__":
    main()