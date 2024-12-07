import uuid

# In-memory database
users = {}
follows = {}

# Utility Functions
def generate_user_id():
    """Generate a unique UUID for each user."""
    return str(uuid.uuid4())

def get_user(user_id):
    """Retrieve a user by ID from the in-memory database."""
    return users.get(user_id)

def add_user(name, age):
    """Add a new user to the in-memory database."""
    user_id = generate_user_id()
    users[user_id] = {'name': name, 'age': age, 'workouts': []}
    return user_id

def delete_user(user_id):
    """Remove a user from the in-memory database."""
    if user_id in users:
        del users[user_id]
        follows.pop(user_id, None)  # Clean up follow relationships
        return True
    return False

def follow_user(follower_id, follow_id):
    """Add a follow relationship."""
    if follower_id not in follows:
        follows[follower_id] = set()
    follows[follower_id].add(follow_id)

def get_followed_users(user_id):
    """Get the list of users that a given user is following."""
    return list(follows.get(user_id, set()))

def list_user_workouts(user_id):
    """Retrieve all workouts for a specific user."""
    user = get_user(user_id)
    return user['workouts'] if user else None
