from typing import List

import requests

from models import User


class Api:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, params=params)
        return response

    def post(self, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, json=data)
        return response

    def update(self, endpoint, user_id, data=None):
        url = f"{self.base_url}/{endpoint}/{user_id}"
        response = requests.put(url, json=data)
        return response

    def delete(self, endpoint, user_id):
        url = f"{self.base_url}/{endpoint}/{user_id}"
        response = requests.delete(url)
        return response


class ExampleApi(Api):

    def __init__(self, base_url="https://example.com/api"):
        super().__init__(base_url)

    def get_all_users(self) -> List[User]:
        endpoint = f"{self.base_url}/users"
        response = requests.get(endpoint)
        return [User(**user) for user in response.json().get("users")]

    def get_user_by_id(self, user_id):
        endpoint = f"{self.base_url}/user/{user_id}"
        response = requests.get(endpoint)
        return response


# Usage example:
if __name__ == "__main__":
    # Replace 'https://example.com/api' with the actual base URL of your API
    api = Api("https://example.com/api")
    api2 = ExampleApi()

    # Example: Get all users directly
    response_all_users = api.get("users")
    if response_all_users.status_code == 200:
        print("All Users:")
        print(response_all_users.json())
    else:
        print(f"Failed to fetch all users. Status code: {response_all_users.status_code}")

    # Example: Get all users
    response_all_users = api2.get_all_users()
    if response_all_users.status_code == 200:
        print("All Users:")
        print(response_all_users.json())
    else:
        print(f"Failed to fetch all users. Status code: {response_all_users.status_code}")

    # Example: Create a new user
    new_user_data = {"name": "John Doe", "email": "john.doe@example.com"}
    response_create_user = api.post("users", data=new_user_data)
    if response_create_user.status_code == 201:
        created_user_id = response_create_user.json()["id"]
        print(f"User created with ID: {created_user_id}")
    else:
        print(f"Failed to create user. Status code: {response_create_user.status_code}")

    # Example: Update user information
    user_id_to_update = 1
    updated_user_data = {"name": "Updated Name"}
    response_update_user = api.update("users", user_id_to_update, data=updated_user_data)
    if response_update_user.status_code == 200:
        print(f"User {user_id_to_update} updated successfully")
    else:
        print(f"Failed to update user. Status code: {response_update_user.status_code}")

    # Example: Delete a user
    user_id_to_delete = 2
    response_delete_user = api.delete("users", user_id_to_delete)
    if response_delete_user.status_code == 204:
        print(f"User {user_id_to_delete} deleted successfully")
    else:
        print(f"Failed to delete user. Status code: {response_delete_user.status_code}")
