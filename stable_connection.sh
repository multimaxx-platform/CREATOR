#!/bin/bash

# Стабильное соединение с Mac M4
# Автоматическое переподключение при разрыве

MAC_IP="195.158.67.204"
MAC_USER="olegroslavitskiy"
MAC_PASS="almaz777"
LOCAL_PORT="2222"

echo "🔗 Создание стабильного соединения с Mac M4..."

# Функция для создания туннеля
create_tunnel() {
    echo "📡 Подключение к $MAC_USER@$MAC_IP..."
    sshpass -p "$MAC_PASS" ssh -o StrictHostKeyChecking=no \
        -o ServerAliveInterval=60 \
        -o ServerAliveCountMax=3 \
        -o TCPKeepAlive=yes \
        -o ConnectTimeout=30 \
        -N -L $LOCAL_PORT:localhost:22 \
        $MAC_USER@$MAC_IP
}

# Основной цикл
while true; do
    echo "🚀 Запуск туннеля..."
    create_tunnel
    
    echo "⚠️ Соединение прервано, переподключение через 5 секунд..."
    sleep 5
done