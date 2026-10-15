import datetime, getpass, os, platform,socket

def print_student_header():
    # 1. Ask for Student ID
    student_id = input('Enter Your Matric Number: ').strip()

    # 2. Get system information
    username = getpass.getuser()
    hostname = socket.gethostname()
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 3. Detect OS name
    os_name = platform.system()
    if os_name == "Linux":
        if os.path.exists("/etc/os-release") and "ubuntu" in open("/etc/os-release").read().lower():
            os_name = "Ubuntu"
    elif os_name == "Darwin":
        os_name = "macOS"

    # 4. Print Verification Card
    print("=======================================================")
    print(f" VERIFICATION: MATRIC NUMBER: {student_id}")
    print(f" USER: {username}@{hostname} | OS: {os_name}")
    print(f" TIME: {current_time}")
    print("=======================================================\n")


if __name__ == '__main__':
    print_student_header()