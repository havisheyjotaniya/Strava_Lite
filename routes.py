from flask import request, jsonify
from api import (
    add_user, get_user, delete_user, follow_user,
    get_followed_users, list_user_workouts, users, follows
)

def initialize_routes(app):
    # Root URL
    @app.route('/', methods=['GET'])
    def home():
        return jsonify({"message": "Welcome to Strava Lite API!"}), 200

    # API 1: Register User
    @app.route('/user', methods=['POST'])
    def register_user():
        data = request.get_json()
        if not data or 'name' not in data or 'age' not in data:
            return jsonify({'error': 'Invalid input'}), 400
        
        user_id = add_user(data['name'], data['age'])
        return jsonify({'id': user_id, 'name': data['name'], 'age': data['age']}), 200

    # API 2: Get User Info
    @app.route('/user/<user_id>', methods=['GET'])
    def get_user_info(user_id):
        user = get_user(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({'id': user_id, 'name': user['name'], 'age': user['age']}), 200

    # API 3: Remove User
    @app.route('/user/<user_id>', methods=['DELETE'])
    def remove_user(user_id):
        if not delete_user(user_id):
            return jsonify({'error': 'User not found'}), 404
        return jsonify({}), 200

    # API 4: List Users
    @app.route('/users', methods=['GET'])
    def list_users():
        return jsonify({'users': [{'id': user_id, **data} for user_id, data in users.items()]}), 200

    # API 5: Add Workout
    @app.route('/workouts/<user_id>', methods=['PUT'])
    def add_workout(user_id):
        user = get_user(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()
        if not data or 'date' not in data or 'time' not in data or 'distance' not in data:
            return jsonify({'error': 'Invalid input'}), 400

        workout = {'date': data['date'], 'time': data['time'], 'distance': data['distance']}
        user['workouts'].append(workout)
        return jsonify(workout), 200

    # API 6: List Workouts for a Specific User
    @app.route('/workouts/<user_id>', methods=['GET'])
    def list_workouts(user_id):
        workouts = list_user_workouts(user_id)
        if workouts is None:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({'workouts': workouts}), 200

    # API 7: List All Workouts for All Users (New)
    @app.route('/workouts', methods=['GET'])
    def list_all_workouts():
        all_workouts = []
        for user_id, user_data in users.items():
            for workout in user_data['workouts']:
                all_workouts.append({'user_id': user_id, **workout})
        return jsonify({'workouts': all_workouts}), 200

    # Extra Credit API 1: Follow Friend
    @app.route('/follow-list/<user_id>', methods=['PUT'])
    def follow_friend(user_id):
        user = get_user(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()
        if not data or 'follow_id' not in data:
            return jsonify({'error': 'Invalid input'}), 400

        follow_id = data['follow_id']
        if not get_user(follow_id):
            return jsonify({'error': 'Followed user not found'}), 404

        follow_user(user_id, follow_id)
        return jsonify({'following': get_followed_users(user_id)}), 200

    # Extra Credit API 2: Show Friend Workouts
    @app.route('/follow-list/<user_id>/<follow_id>', methods=['GET'])
    def show_friend_workouts(user_id, follow_id):
        user = get_user(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        followed_users = get_followed_users(user_id)
        if follow_id not in followed_users:
            return jsonify({'error': 'You do not follow this user'}), 403

        friend = get_user(follow_id)
        return jsonify({'workouts': friend['workouts']}), 200