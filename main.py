import time

def start_creator():
    print("CREATOR запущен!")
    while True:
        user_input = input("Введите команду: ")
        if user_input.lower() == "выход":
            print("CREATOR завершает работу...")
            break
        else:
            print(f"CREATOR получил команду: {user_input}")

if __name__ == "__main__":
    start_creator()
