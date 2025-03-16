import requests
import json

BASE_URL = "https://sc22vg.pythonanywhere.com"
session = requests.Session() 

def register():
    email = input("Enter email: ")
    username = input("Enter username: ")
    password = input("Enter password: ")

    data = {"username": username, "email": email, "password": password}
    response = session.post(f"{BASE_URL}/api/register/", json=data)

    if handle_response(response):
        print("Registration successful!")


def login(url):
    global BASE_URL, session

    username = input("Enter username: ")
    password = input("Enter password: ")
    
    BASE_URL = url

    data = {"username": username, "password": password}
    response = session.post(f"{BASE_URL}/api/login/", json=data)

    if handle_response(response):
        print("Login successful!")


def logout():
    global session
    response = session.post(f"{BASE_URL}/api/logout/")
    data = handle_response(response)  
    if data:
        print("Logged out successfully!")
        session = requests.Session()

def list_iterations():
    response = session.get(f"{BASE_URL}/api/list/")
    data = handle_response(response)

    if data:
        for instance in data:
            module = instance["module"]
            professors_str = ', '.join(prof["name"] for prof in instance["professors"])

            print(
                f"Code: {module['code']}, "
                f"Name: {module['name']}, "
                f"Year: {module['year']}, "
                f"Semester: {module['semester']}, "
                f"Taught by: {professors_str if professors_str else 'No professors assigned'}"
            )


def view_ratings():
    response = session.get(f"{BASE_URL}/api/view/")
    data = handle_response(response)

    if data:
        for rating in data:
            print(f"The rating of Professor {rating['name']} ({rating['prof_code']}) is {rating['average_rating']}")


def average_rating(professor_id, module_code):
    response = session.get(f"{BASE_URL}/api/average/{professor_id}/{module_code}/")
    data = handle_response(response)

    if data:
        if data['average_rating']:
            print(f"The rating of Professor {data['professor']} ({professor_id}) in module {data['module']} ({module_code}) is {data['average_rating']}")
        else:
            print(f"No rating of Professor {data['professor']} ({professor_id}) in module {data['module']} ({module_code}).")


def rate(professor_id, module_id, year, semester, rating):
    data = {
        "professor_id": professor_id,
        "module_id": module_id,
        "year": year,
        "semester": semester,
        "rating": int(rating)
    }

    response = session.post(f"{BASE_URL}/api/rate/", json=data)
    if handle_response(response):
        print("Rating submitted")



def main():
    while True:
        print("\nAvailable commands:\n register\n login <url>\n logout\n list\n view\n average <professor_code> <module_code>\n rate <professor_code> <module_code> <year> <semester> <rating>\n exit")
        command = input("Enter command: ").strip().split() 

        if not command:
            print("Please enter a command.")
            continue

        cmd = command[0] 
        args = command[1:] 

        if cmd == "list":
            if len(args) != 0:
                print("Usage: list (no arguments required)")
            else:
                list_iterations()

        elif cmd == "view":
            if len(args) != 0:
                print("Usage: view (no arguments required)")
            else:
                view_ratings()

        elif cmd == "average":
            if len(args) != 2:
                print("Usage: average <professor_code> <module_code>")
            else:
                average_rating(args[0], args[1])

        elif cmd == "rate":
            if len(args) != 5:
                print("Usage: rate <professor_code> <module_code> <year> <semester> <rating>")
            elif not args[2].isdigit():
                print("Year must be a number.")
            elif not args[4].isdigit():
                print("Rating must be an integer.")
            elif args[3] not in ["1", "2"]:
                print("Semester must be either 1 or 2.")
            else:
                rate(args[0], args[1], args[2], args[3], args[4])

        elif cmd == "register":
            if len(args) != 0:
                print("Usage: register (no arguments required)")
            else:
                register()

        elif cmd == "login":
            if len(args) != 1:
                print("Usage: login <url>")
            elif not args[0] == BASE_URL:
                print("Incorrect URL")
            else:
                login(args[0])
        
        elif cmd == "logout":
            if len(args) != 0:
                print("Usage: logout (no arguments required)")
            else:
                logout()

        elif cmd == "exit":
            print("Exiting")
            break

        else:
            print("Invalid command")

            
def handle_response(response):
    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print(f"Unexpected response (Not JSON): {response.text}")
        return None

    if response.status_code in [200, 201]:  
        return data
    else:
        error_message = data.get("error", "An unknown error occurred") 
        print(f"Error: {error_message}")  
        return None



if __name__ == "__main__":
    main()