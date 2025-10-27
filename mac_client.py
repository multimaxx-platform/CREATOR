#!/usr/bin/env python3
"""
Клиент для подключения к системному мосту с Mac
"""

import requests
import json
import os
from typing import Dict, Any

class MacSystemClient:
    def __init__(self, server_url: str = "http://localhost:5000"):
        self.server_url = server_url
        self.session = requests.Session()
    
    def get_system_info(self) -> Dict[str, Any]:
        """Получение информации о системе"""
        try:
            response = self.session.get(f"{self.server_url}/api/system/info")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"Ошибка подключения: {str(e)}"}
    
    def analyze_project(self, project_path: str) -> Dict[str, Any]:
        """Анализ проекта"""
        try:
            data = {"path": project_path}
            response = self.session.post(
                f"{self.server_url}/api/project/analyze",
                json=data
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"Ошибка подключения: {str(e)}"}
    
    def execute_command(self, command_name: str, args: list = None) -> Dict[str, Any]:
        """Выполнение команды"""
        try:
            data = {
                "command": command_name,
                "args": args or []
            }
            response = self.session.post(
                f"{self.server_url}/api/command/execute",
                json=data
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"Ошибка подключения: {str(e)}"}
    
    def install_package(self, package_name: str) -> Dict[str, Any]:
        """Установка пакета"""
        try:
            data = {"package": package_name}
            response = self.session.post(
                f"{self.server_url}/api/package/install",
                json=data
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"Ошибка подключения: {str(e)}"}

def main():
    """Тестирование клиента"""
    client = MacSystemClient()
    
    print("🔍 Получение информации о системе...")
    system_info = client.get_system_info()
    print(json.dumps(system_info, indent=2, ensure_ascii=False))
    
    print("\n📁 Анализ текущего проекта...")
    project_analysis = client.analyze_project(".")
    print(json.dumps(project_analysis, indent=2, ensure_ascii=False))
    
    print("\n💾 Проверка дискового пространства...")
    disk_info = client.execute_command("disk_space")
    print(json.dumps(disk_info, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()