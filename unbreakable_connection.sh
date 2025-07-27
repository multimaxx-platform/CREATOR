#!/bin/bash

# Неубиваемое соединение с Mac M4
# Использует ваши рабочие доступы

MAC_IP="195.158.67.204"
MAC_USER="olegroslavitskiy"
SSH_KEY="oleg_key_rsa"
MAC_PASS="almaz777"
LOCAL_PORT="2222"

echo "🔗 Создание неубиваемого соединения с Mac M4..."

# Функция для создания туннеля с ключом
create_tunnel_with_key() {
    echo "📡 Подключение с SSH ключом..."
    ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no \
        -o ServerAliveInterval=30 \
        -o ServerAliveCountMax=10 \
        -o TCPKeepAlive=yes \
        -o ConnectTimeout=10 \
        -N -L $LOCAL_PORT:localhost:22 \
        $MAC_USER@$MAC_IP
}

# Функция для создания туннеля с паролем
create_tunnel_with_pass() {
    echo "📡 Подключение с паролем..."
    sshpass -p "$MAC_PASS" ssh -o StrictHostKeyChecking=no \
        -o ServerAliveInterval=30 \
        -o ServerAliveCountMax=10 \
        -o TCPKeepAlive=yes \
        -o ConnectTimeout=10 \
        -N -L $LOCAL_PORT:localhost:22 \
        $MAC_USER@$MAC_IP
}

# Проверяем наличие ключа
if [ -f "$SSH_KEY" ]; then
    echo "✅ SSH ключ найден, используем его"
    TUNNEL_FUNC="create_tunnel_with_key"
else
    echo "🔑 SSH ключ не найден, используем пароль"
    TUNNEL_FUNC="create_tunnel_with_pass"
fi

# Основной цикл - неубиваемое соединение
while true; do
    echo "🚀 Запуск туннеля..."
    $TUNNEL_FUNC
    
    echo "⚠️ Соединение прервано, переподключение через 3 секунды..."
    sleep 3
done