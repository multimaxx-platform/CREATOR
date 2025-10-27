"""
LangGraph Memory Agent для системы CREATOR
Управляет четырехуровневой системой памяти
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

class MemoryState:
    """Состояние памяти для LangGraph"""
    def __init__(self):
        self.level1_context = {}
        self.level2_dialogs = []
        self.level3_architecture = {}
        self.level4_progress = {}
        self.current_task = ""
        self.memory_path = "memory/"

class MemoryAgent:
    """Агент управления памятью"""
    
    def __init__(self):
        self.state = MemoryState()
        self.graph = self._create_graph()
        
    def _create_graph(self) -> StateGraph:
        """Создает граф обработки памяти"""
        
        # Определяем узлы
        def update_context(state):
            """Обновляет контекст (Уровень 1)"""
            context = {
                "timestamp": datetime.now().isoformat(),
                "current_task": state["current_task"],
                "system_status": "active",
                "memory_levels": ["level1", "level2", "level3", "level4"]
            }
            
            # Сохраняем в файл
            with open(f"{self.state.memory_path}level1_context/current.json", "w") as f:
                json.dump(context, f, indent=2)
            
            state["level1_context"] = context
            return state
        
        def update_dialogs(state):
            """Обновляет диалоги (Уровень 2)"""
            dialog_entry = {
                "timestamp": datetime.now().isoformat(),
                "task": state["current_task"],
                "type": "ai_action",
                "content": f"Обновление памяти: {state['current_task']}"
            }
            
            # Добавляем к существующим диалогам
            dialogs = state.get("level2_dialogs", [])
            dialogs.append(dialog_entry)
            
            # Сохраняем в файл
            with open(f"{self.state.memory_path}level2_dialogs/dialogs.json", "w") as f:
                json.dump(dialogs, f, indent=2)
            
            state["level2_dialogs"] = dialogs
            return state
        
        def update_architecture(state):
            """Обновляет архитектуру (Уровень 3)"""
            arch_entry = {
                "timestamp": datetime.now().isoformat(),
                "component": "memory_system",
                "status": "updated",
                "task": state["current_task"]
            }
            
            # Добавляем к архитектуре
            architecture = state.get("level3_architecture", {})
            architecture["memory_system"] = arch_entry
            
            # Сохраняем в файл
            with open(f"{self.state.memory_path}level3_architecture/system.json", "w") as f:
                json.dump(architecture, f, indent=2)
            
            state["level3_architecture"] = architecture
            return state
        
        def update_progress(state):
            """Обновляет прогресс (Уровень 4)"""
            progress_entry = {
                "timestamp": datetime.now().isoformat(),
                "task": state["current_task"],
                "status": "completed",
                "phase": "memory_update"
            }
            
            # Добавляем к прогрессу
            progress = state.get("level4_progress", {})
            progress[f"task_{len(progress)}"] = progress_entry
            
            # Сохраняем в файл
            with open(f"{self.state.memory_path}level4_progress/progress.json", "w") as f:
                json.dump(progress, f, indent=2)
            
            state["level4_progress"] = progress
            return state
        
        # Создаем граф
        workflow = StateGraph(MemoryState)
        
        # Добавляем узлы
        workflow.add_node("update_context", update_context)
        workflow.add_node("update_dialogs", update_dialogs)
        workflow.add_node("update_architecture", update_architecture)
        workflow.add_node("update_progress", update_progress)
        
        # Определяем поток
        workflow.set_entry_point("update_context")
        workflow.add_edge("update_context", "update_dialogs")
        workflow.add_edge("update_dialogs", "update_architecture")
        workflow.add_edge("update_architecture", "update_progress")
        workflow.add_edge("update_progress", END)
        
        return workflow.compile()
    
    def update_memory(self, task: str, data: Dict[str, Any] = None):
        """Обновляет все уровни памяти"""
        self.state.current_task = task
        
        # Запускаем граф
        result = self.graph.invoke({
            "current_task": task,
            "level1_context": self.state.level1_context,
            "level2_dialogs": self.state.level2_dialogs,
            "level3_architecture": self.state.level3_architecture,
            "level4_progress": self.state.level4_progress
        })
        
        # Обновляем состояние
        self.state.level1_context = result["level1_context"]
        self.state.level2_dialogs = result["level2_dialogs"]
        self.state.level3_architecture = result["level3_architecture"]
        self.state.level4_progress = result["level4_progress"]
        
        return result
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """Получает сводку памяти"""
        return {
            "context": self.state.level1_context,
            "dialogs_count": len(self.state.level2_dialogs),
            "architecture_components": len(self.state.level3_architecture),
            "progress_tasks": len(self.state.level4_progress)
        }

# Создаем экземпляр агента
memory_agent = MemoryAgent()

if __name__ == "__main__":
    # Тестируем агента
    result = memory_agent.update_memory("Инициализация системы памяти")
    print("Memory updated:", result)
    
    summary = memory_agent.get_memory_summary()
    print("Memory summary:", summary)