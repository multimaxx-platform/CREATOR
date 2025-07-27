"""
Letto Integration для системы CREATOR
Долгосрочное хранение и семантический поиск
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import requests

class LettoIntegration:
    """Интеграция с Letto для долгосрочной памяти"""
    
    def __init__(self, api_key: str = None, base_url: str = "https://api.letto.ai"):
        self.api_key = api_key or os.getenv("LETTO_API_KEY")
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def store_memory(self, level: str, data: Dict[str, Any], metadata: Dict[str, Any] = None):
        """Сохраняет данные в Letto"""
        try:
            payload = {
                "content": json.dumps(data, ensure_ascii=False),
                "metadata": {
                    "level": level,
                    "timestamp": datetime.now().isoformat(),
                    "project": "CREATOR",
                    **(metadata or {})
                },
                "tags": ["creator", "memory", level]
            }
            
            response = requests.post(
                f"{self.base_url}/v1/store",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Letto store error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Letto integration error: {e}")
            return None
    
    def search_memory(self, query: str, level: str = None, limit: int = 10):
        """Ищет в памяти Letto"""
        try:
            payload = {
                "query": query,
                "limit": limit,
                "filters": {
                    "tags": ["creator", "memory"]
                }
            }
            
            if level:
                payload["filters"]["metadata.level"] = level
            
            response = requests.post(
                f"{self.base_url}/v1/search",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Letto search error: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"Letto search error: {e}")
            return []
    
    def get_memory_context(self, task: str, levels: List[str] = None):
        """Получает контекст для задачи"""
        if levels is None:
            levels = ["level1", "level2", "level3", "level4"]
        
        context = {}
        
        for level in levels:
            results = self.search_memory(task, level=level, limit=5)
            context[level] = results
        
        return context
    
    def store_four_level_memory(self, memory_data: Dict[str, Any]):
        """Сохраняет четырехуровневую память"""
        results = {}
        
        # Уровень 1: Контекст
        if "level1_context" in memory_data:
            results["level1"] = self.store_memory(
                "level1", 
                memory_data["level1_context"],
                {"type": "context"}
            )
        
        # Уровень 2: Диалоги
        if "level2_dialogs" in memory_data:
            results["level2"] = self.store_memory(
                "level2",
                memory_data["level2_dialogs"],
                {"type": "dialogs"}
            )
        
        # Уровень 3: Архитектура
        if "level3_architecture" in memory_data:
            results["level3"] = self.store_memory(
                "level3",
                memory_data["level3_architecture"],
                {"type": "architecture"}
            )
        
        # Уровень 4: Прогресс
        if "level4_progress" in memory_data:
            results["level4"] = self.store_memory(
                "level4",
                memory_data["level4_progress"],
                {"type": "progress"}
            )
        
        return results
    
    def get_project_context(self, project_name: str = "CREATOR"):
        """Получает контекст проекта"""
        return self.search_memory(
            f"project:{project_name}",
            limit=20
        )

class LocalLettoMock:
    """Локальная имитация Letto для тестирования"""
    
    def __init__(self):
        self.storage = {}
        self.index = {}
    
    def store_memory(self, level: str, data: Dict[str, Any], metadata: Dict[str, Any] = None):
        """Локальное сохранение"""
        key = f"{level}_{datetime.now().isoformat()}"
        self.storage[key] = {
            "content": data,
            "metadata": metadata or {},
            "level": level,
            "timestamp": datetime.now().isoformat()
        }
        
        # Индексируем для поиска
        for word in str(data).lower().split():
            if word not in self.index:
                self.index[word] = []
            self.index[word].append(key)
        
        return {"id": key, "status": "stored"}
    
    def search_memory(self, query: str, level: str = None, limit: int = 10):
        """Локальный поиск"""
        results = []
        query_words = query.lower().split()
        
        for word in query_words:
            if word in self.index:
                for key in self.index[word]:
                    if key in self.storage:
                        item = self.storage[key]
                        if level is None or item["level"] == level:
                            results.append(item)
        
        # Убираем дубликаты и ограничиваем
        unique_results = []
        seen_keys = set()
        
        for result in results:
            if result["timestamp"] not in seen_keys:
                unique_results.append(result)
                seen_keys.add(result["timestamp"])
        
        return unique_results[:limit]
    
    def get_memory_context(self, task: str, levels: List[str] = None):
        """Получает контекст"""
        if levels is None:
            levels = ["level1", "level2", "level3", "level4"]
        
        context = {}
        
        for level in levels:
            results = self.search_memory(task, level=level, limit=5)
            context[level] = results
        
        return context

# Создаем экземпляр (используем локальную версию для тестирования)
letto_integration = LocalLettoMock()

if __name__ == "__main__":
    # Тестируем интеграцию
    test_data = {
        "level1_context": {"task": "test", "status": "active"},
        "level2_dialogs": [{"message": "test dialog"}],
        "level3_architecture": {"component": "test"},
        "level4_progress": {"task": "test progress"}
    }
    
    result = letto_integration.store_four_level_memory(test_data)
    print("Stored in Letto:", result)
    
    context = letto_integration.get_memory_context("test")
    print("Retrieved context:", context)