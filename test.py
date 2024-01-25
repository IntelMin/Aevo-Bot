from database.db import get_user, add_user

if __name__ == "__main__":
    user_id = 12345678901
    user_record = get_user(user_id)
    if user_record:
        print('User exists', user_record)
    else:
        print('User does not exist', user_record)
        add_user(user_id, {'name': 'Alice Doe'})
        user_record = get_user(user_id)
        print(user_record)