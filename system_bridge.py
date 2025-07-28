#!/usr/bin/env python3
"""
Системный мост для безопасного управления компьютером через AI
"""

import os
import json
import subprocess
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class CommandResult:
    success: bool
    output: str
    error: str
    command: str

class SystemBridge:
    def __init__(self):
        self.safe_commands = {
            'system_info': ['uname', '-a'],
            'disk_space': ['df', '-h'],
            'memory_usage': ['free', '-h'],
            'process_list': ['ps', 'aux'],
            'network_status': ['netstat', '-tuln'],
            'file_list': ['ls', '-la'],
            'git_status': ['git', 'status'],
            'python_version': ['python3', '--version'],
            'pip_list': ['pip', 'list'],
            'brew_list': ['brew', 'list'],
        }
        
        self.logger = self._setup_logging()
    
    def _setup_logging(self) -> logging.Logger:
        """Настройка логирования"""
        logger = logging.getLogger('system_bridge')
        logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler('system_bridge.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def execute_safe_command(self, command_name: str, args: List[str] = None) -> CommandResult:
        """Выполнение безопасной команды"""
        if command_name not in self.safe_commands:
            return CommandResult(
                success=False,
                output="",
                error=f"Команда '{command_name}' не разрешена",
                command=command_name
            )
        
        cmd = self.safe_commands[command_name].copy()
        if args:
            cmd.extend(args)
        
        self.logger.info(f"Выполняется команда: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return CommandResult(
                success=result.returncode == 0,
                output=result.stdout,
                error=result.stderr,
                command=' '.join(cmd)
            )
            
        except subprocess.TimeoutExpired:
            return CommandResult(
                success=False,
                output="",
                error="Команда превысила лимит времени (30 сек)",
                command=' '.join(cmd)
            )
        except Exception as e:
            return CommandResult(
                success=False,
                output="",
                error=str(e),
                command=' '.join(cmd)
            )
    
    def get_system_info(self) -> Dict:
        """Получение информации о системе"""
        info = {}
        
        # Системная информация
        uname = self.execute_safe_command('system_info')
        if uname.success:
            info['system'] = uname.output.strip()
        
        # Дисковое пространство
        disk = self.execute_safe_command('disk_space')
        if disk.success:
            info['disk'] = disk.output.strip()
        
        # Использование памяти
        memory = self.execute_safe_command('memory_usage')
        if memory.success:
            info['memory'] = memory.output.strip()
        
        return info
    
    def analyze_project(self, project_path: str) -> Dict:
        """Анализ проекта"""
        analysis = {
            'path': project_path,
            'files': [],
            'git_status': None,
            'python_deps': None
        }
        
        # Проверяем Git статус
        git_result = self.execute_safe_command('git_status')
        if git_result.success:
            analysis['git_status'] = git_result.output.strip()
        
        # Список файлов
        if os.path.exists(project_path):
            try:
                for root, dirs, files in os.walk(project_path):
                    for file in files:
                        if file.endswith(('.py', '.js', '.ts', '.json', '.md')):
                            analysis['files'].append(os.path.join(root, file))
            except Exception as e:
                analysis['error'] = str(e)
        
        return analysis
    
    def install_package(self, package_name: str) -> CommandResult:
        """Установка пакета через pip"""
        self.logger.info(f"Установка пакета: {package_name}")
        
        try:
            result = subprocess.run(
                ['pip', 'install', package_name],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            return CommandResult(
                success=result.returncode == 0,
                output=result.stdout,
                error=result.stderr,
                command=f"pip install {package_name}"
            )
            
        except Exception as e:
            return CommandResult(
                success=False,
                output="",
                error=str(e),
                command=f"pip install {package_name}"
            )

# API сервер (Flask)
from flask import Flask, request, jsonify

app = Flask(__name__)
bridge = SystemBridge()

@app.route('/api/system/info', methods=['GET'])
def get_system_info():
    """Получение информации о системе"""
    info = bridge.get_system_info()
    return jsonify(info)

@app.route('/api/project/analyze', methods=['POST'])
def analyze_project():
    """Анализ проекта"""
    data = request.get_json()
    project_path = data.get('path', '.')
    
    analysis = bridge.analyze_project(project_path)
    return jsonify(analysis)

@app.route('/api/command/execute', methods=['POST'])
def execute_command():
    """Выполнение команды"""
    data = request.get_json()
    command_name = data.get('command')
    args = data.get('args', [])
    
    result = bridge.execute_safe_command(command_name, args)
    
    return jsonify({
        'success': result.success,
        'output': result.output,
        'error': result.error,
        'command': result.command
    })

@app.route('/api/package/install', methods=['POST'])
def install_package():
    """Установка пакета"""
    data = request.get_json()
    package_name = data.get('package')
    
    result = bridge.install_package(package_name)
    
    return jsonify({
        'success': result.success,
        'output': result.output,
        'error': result.error,
        'command': result.command
    })

if __name__ == '__main__':
    print("🚀 Системный мост запущен!")
    print("📡 API доступен на http://localhost:5000")
    print("🔒 Только безопасные команды разрешены")
    
    app.run(host='0.0.0.0', port=5000, debug=True)