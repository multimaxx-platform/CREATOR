"""
Главный координатор системы CREATOR
Управляет всеми агентами и памятью
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional

# Добавляем пути к модулям
sys.path.append(os.path.join(os.path.dirname(__file__), 'langgraph'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'letto'))

from langgraph.memory_agent import MemoryAgent
from letto.letto_integration import letto_integration

class CREATORCoordinator:
    """Главный координатор системы CREATOR"""
    
    def __init__(self):
        self.memory_agent = MemoryAgent()
        self.letto = letto_integration
        self.current_task = ""
        self.session_id = datetime.now().isoformat()
        
        # Инициализируем память
        self._initialize_memory()
    
    def _initialize_memory(self):
        """Инициализирует систему памяти"""
        init_data = {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "status": "initialized",
            "components": ["memory_agent", "letto_integration", "coordinator"]
        }
        
        # Обновляем память
        self.memory_agent.update_memory("Инициализация системы", init_data)
        
        # Сохраняем в Letto
        self.letto.store_memory("system", init_data, {"type": "initialization"})
        
        print("✅ Система CREATOR инициализирована")
    
    def execute_task(self, task: str, data: Dict[str, Any] = None):
        """Выполняет задачу с обновлением памяти"""
        self.current_task = task
        
        print(f"🚀 Выполняю задачу: {task}")
        
        # Обновляем память
        memory_result = self.memory_agent.update_memory(task, data)
        
        # Сохраняем в Letto
        letto_result = self.letto.store_four_level_memory(memory_result)
        
        # Получаем контекст для задачи
        context = self.letto.get_memory_context(task)
        
        return {
            "task": task,
            "memory_result": memory_result,
            "letto_result": letto_result,
            "context": context,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_project_status(self):
        """Получает статус проекта"""
        summary = self.memory_agent.get_memory_summary()
        context = self.letto.get_project_context("CREATOR")
        
        return {
            "summary": summary,
            "context": context,
            "session_id": self.session_id,
            "current_task": self.current_task,
            "timestamp": datetime.now().isoformat()
        }
    
    def search_memory(self, query: str, level: str = None):
        """Ищет в памяти"""
        return self.letto.search_memory(query, level)
    
    def get_memory_context(self, task: str):
        """Получает контекст для задачи"""
        return self.letto.get_memory_context(task)
    
    def update_architecture(self, component: str, data: Dict[str, Any]):
        """Обновляет архитектуру"""
        arch_data = {
            "component": component,
            "data": data,
            "timestamp": datetime.now().isoformat(),
            "status": "updated"
        }
        
        return self.execute_task(f"Обновление архитектуры: {component}", arch_data)
    
    def log_progress(self, phase: str, details: Dict[str, Any]):
        """Логирует прогресс"""
        progress_data = {
            "phase": phase,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "status": "in_progress"
        }
        
        return self.execute_task(f"Прогресс: {phase}", progress_data)

class MacIntegration:
    """Интеграция с Mac M4"""
    
    def __init__(self, ip: str, user: str, ssh_key: str):
        self.ip = ip
        self.user = user
        self.ssh_key = ssh_key
        self.ssh_command = f"ssh -i {ssh_key} {user}@{ip}"
    
    def execute_remote_command(self, command: str):
        """Выполняет команду на удаленном Mac"""
        full_command = f"{self.ssh_command} '{command}'"
        
        try:
            import subprocess
            result = subprocess.run(full_command, shell=True, capture_output=True, text=True)
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def check_creator_status(self):
        """Проверяет статус CREATOR на Mac"""
        return self.execute_remote_command("ls -la ~/CREATOR")
    
    def get_mac_info(self):
        """Получает информацию о Mac"""
        return self.execute_remote_command("uname -a && df -h")

# Создаем экземпляры
coordinator = CREATORCoordinator()
mac_integration = MacIntegration(
    ip="195.158.67.204",
    user="olegroslavitskiy", 
    ssh_key="oleg_key_rsa"
)

if __name__ == "__main__":
    # Тестируем координатор
    result = coordinator.execute_task("Тестирование системы")
    print("Task executed:", result)
    
    status = coordinator.get_project_status()
    print("Project status:", status)
    
    # Тестируем интеграцию с Mac
    mac_status = mac_integration.check_creator_status()
    print("Mac CREATOR status:", mac_status)