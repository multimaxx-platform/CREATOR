#!/usr/bin/env python3
"""
Локальный AI-ассистент для управления системой
Работает на Mac без подключения к интернету
"""

import json
import os
import re
from typing import Dict, Any, List
from datetime import datetime
from mac_client import MacSystemClient

class LocalAIAssistant:
    def __init__(self):
        self.client = MacSystemClient()
        self.context = {}
        self.commands_history = []
        
        # Правила для анализа и принятия решений
        self.rules = {
            "disk_usage": {
                "warning": 80,
                "critical": 90,
                "actions": ["Очистить временные файлы", "Удалить ненужные файлы"]
            },
            "memory_usage": {
                "warning": 85,
                "critical": 95,
                "actions": ["Перезагрузить систему", "Закрыть лишние приложения"]
            },
            "git_status": {
                "untracked": "Добавить файлы в Git",
                "uncommitted": "Сделать коммит изменений",
                "ahead": "Отправить изменения в репозиторий"
            }
        }
    
    def analyze_system_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Анализ системных данных и принятие решений"""
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "status": "healthy",
            "issues": [],
            "recommendations": [],
            "actions": []
        }
        
        # Анализ дискового пространства
        if "disk" in data and data["disk"].get("success"):
            disk_output = data["disk"]["output"]
            usage_match = re.search(r'(\d+)%', disk_output)
            if usage_match:
                usage = int(usage_match.group(1))
                if usage > self.rules["disk_usage"]["critical"]:
                    analysis["status"] = "critical"
                    analysis["issues"].append(f"Критическое использование диска: {usage}%")
                    analysis["actions"].extend(self.rules["disk_usage"]["actions"])
                elif usage > self.rules["disk_usage"]["warning"]:
                    analysis["status"] = "warning"
                    analysis["issues"].append(f"Высокое использование диска: {usage}%")
                    analysis["recommendations"].extend(self.rules["disk_usage"]["actions"])
        
        # Анализ памяти
        if "memory" in data and data["memory"].get("success"):
            memory_output = data["memory"]["output"]
            usage_match = re.search(r'(\d+)%', memory_output)
            if usage_match:
                usage = int(usage_match.group(1))
                if usage > self.rules["memory_usage"]["critical"]:
                    analysis["status"] = "critical"
                    analysis["issues"].append(f"Критическое использование памяти: {usage}%")
                    analysis["actions"].extend(self.rules["memory_usage"]["actions"])
                elif usage > self.rules["memory_usage"]["warning"]:
                    analysis["status"] = "warning"
                    analysis["issues"].append(f"Высокое использование памяти: {usage}%")
                    analysis["recommendations"].extend(self.rules["memory_usage"]["actions"])
        
        # Анализ Git статуса
        if "git_status" in data and data["git_status"].get("success"):
            git_output = data["git_status"]["output"]
            if "Untracked files" in git_output:
                analysis["recommendations"].append(self.rules["git_status"]["untracked"])
            if "Changes not staged" in git_output:
                analysis["recommendations"].append(self.rules["git_status"]["uncommitted"])
            if "Your branch is ahead" in git_output:
                analysis["recommendations"].append(self.rules["git_status"]["ahead"])
        
        return analysis
    
    def process_user_request(self, request: str) -> Dict[str, Any]:
        """Обработка запроса пользователя"""
        request_lower = request.lower()
        response = {
            "action": "analyze",
            "message": "",
            "data": {},
            "recommendations": []
        }
        
        # Определяем тип запроса
        if any(word in request_lower for word in ["диагностика", "проверка", "статус"]):
            response["action"] = "diagnostic"
            system_data = self.client.get_system_info()
            analysis = self.analyze_system_data(system_data)
            response["data"] = analysis
            response["message"] = self.format_diagnostic_message(analysis)
            
        elif any(word in request_lower for word in ["диск", "пространство", "место"]):
            response["action"] = "disk_check"
            disk_info = self.client.execute_command("disk_space")
            response["data"] = disk_info
            response["message"] = f"💾 Информация о диске:\n{disk_info.get('output', 'Ошибка получения данных')}"
            
        elif any(word in request_lower for word in ["память", "ram", "оперативка"]):
            response["action"] = "memory_check"
            memory_info = self.client.execute_command("memory_usage")
            response["data"] = memory_info
            response["message"] = f"🧠 Информация о памяти:\n{memory_info.get('output', 'Ошибка получения данных')}"
            
        elif any(word in request_lower for word in ["проект", "git", "репозиторий"]):
            response["action"] = "project_analysis"
            project_info = self.client.analyze_project(".")
            git_status = self.client.execute_command("git_status")
            response["data"] = {"project": project_info, "git": git_status}
            response["message"] = self.format_project_message(project_info, git_status)
            
        elif any(word in request_lower for word in ["установить", "установка", "пакет"]):
            response["action"] = "install_package"
            # Извлекаем название пакета из запроса
            package_match = re.search(r'установить\s+(\w+)', request_lower)
            if package_match:
                package_name = package_match.group(1)
                install_result = self.client.install_package(package_name)
                response["data"] = install_result
                if install_result.get("success"):
                    response["message"] = f"✅ Пакет {package_name} установлен успешно!"
                else:
                    response["message"] = f"❌ Ошибка установки {package_name}: {install_result.get('error')}"
            else:
                response["message"] = "Укажите название пакета для установки"
                
        else:
            response["action"] = "help"
            response["message"] = self.get_help_message()
        
        return response
    
    def format_diagnostic_message(self, analysis: Dict[str, Any]) -> str:
        """Форматирование сообщения диагностики"""
        message = "🔍 Результаты диагностики системы:\n\n"
        
        if analysis["status"] == "healthy":
            message += "✅ Система работает нормально\n"
        elif analysis["status"] == "warning":
            message += "⚠️ Обнаружены предупреждения:\n"
            for issue in analysis["issues"]:
                message += f"  • {issue}\n"
        else:
            message += "🚨 Критические проблемы:\n"
            for issue in analysis["issues"]:
                message += f"  • {issue}\n"
        
        if analysis["recommendations"]:
            message += "\n📋 Рекомендации:\n"
            for rec in analysis["recommendations"]:
                message += f"  • {rec}\n"
        
        if analysis["actions"]:
            message += "\n⚡ Необходимые действия:\n"
            for action in analysis["actions"]:
                message += f"  • {action}\n"
        
        return message
    
    def format_project_message(self, project_info: Dict[str, Any], git_status: Dict[str, Any]) -> str:
        """Форматирование сообщения о проекте"""
        message = "📁 Анализ проекта:\n\n"
        
        if project_info.get("files"):
            message += f"📄 Найдено файлов: {len(project_info['files'])}\n"
        
        if git_status.get("success"):
            git_output = git_status["output"]
            if "working tree clean" in git_output:
                message += "✅ Git репозиторий чистый\n"
            elif "Untracked files" in git_output:
                message += "📝 Есть неотслеживаемые файлы\n"
            elif "Changes not staged" in git_output:
                message += "📝 Есть незакоммиченные изменения\n"
        else:
            message += "❌ Ошибка получения Git статуса\n"
        
        return message
    
    def get_help_message(self) -> str:
        """Сообщение помощи"""
        return """🤖 Локальный AI-ассистент

Доступные команды:
• "диагностика" - полная проверка системы
• "диск" - информация о дисковом пространстве
• "память" - информация о памяти
• "проект" - анализ текущего проекта
• "установить [пакет]" - установка пакета

Примеры:
• "Проведи диагностику системы"
• "Покажи информацию о диске"
• "Установить requests"
• "Анализируй проект"
"""

def main():
    """Демонстрация работы локального AI-ассистента"""
    assistant = LocalAIAssistant()
    
    print("🤖 Локальный AI-ассистент запущен!")
    print("=" * 50)
    
    # Тестируем различные запросы
    test_requests = [
        "Проведи диагностику системы",
        "Покажи информацию о диске",
        "Анализируй проект"
    ]
    
    for request in test_requests:
        print(f"\n📝 Запрос: {request}")
        response = assistant.process_user_request(request)
        print(f"🤖 Ответ: {response['message']}")
        print("-" * 30)

if __name__ == "__main__":
    main()