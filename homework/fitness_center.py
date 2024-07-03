from flask import Flask, request, jsonify
from connection import Error

from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
from connection import connection

app = Flask(__name__)
ma = Marshmallow(app)

# Create the Member table schema, to define the structure of our data
class MemberSchema(ma.Schema):
    id = fields.Int(dump_only= True) # dump_only means we don't have to input data for this field
    member_name = fields.String(required= True) # To be valid, this needs a value
    email = fields.String()
   

    class Meta:
        fields = ("member_name", "email")

member_schema = MemberSchema()
members_schema = MemberSchema(many= True)

@app.route('/') # default landing page
def home():
    return "Welcome to the Fitness Center!"

# Views all member data via a GET request
@app.route("/members", methods = ['GET'])
def get_members():
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary= True) # returns us a dictionary of table data instead of a tuple, our schema meta class with cross check the contents of the dictionaries that are returned

            # Write our query to GET all users
            query = "SELECT * FROM members;"

            cursor.execute(query)

            members = cursor.fetchall()
        except Error as e:
            return jsonify(e.messages), 500

        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
                return members_schema.jsonify(members)
            
# Create a new member with a POST request

@app.route("/members", methods = ['POST'])
def add_member():
    try:
        member_data = member_schema.load(request.json) # request.json is the data that is sent to the server
    except ValidationError as e:
        return e.messages, 400

    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary= True)
            query = "INSERT INTO members (member_name, email) VALUES (%s, %s);"
            cursor.execute(query, (member_data['member_name'], member_data['email']))
            conn.commit()
        except Error as e:
            return jsonify(e.messages), 500
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
                return member_schema.jsonify(member_data)
            
# Update a member with a PUT request

@app.route("/members/<int:id>", methods = ['PUT'])
def update_member(id):
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary= True)
            query = "SELECT * FROM members WHERE id = %s;"
            cursor.execute(query, (id,))
            member = cursor.fetchone()
            if member is None:
                return jsonify({'Message' : 'Member not found!'}), 404
            member_data = member_schema.load(request.json)
            query = "UPDATE members SET member_name = %s, email = %s WHERE id = %s;"
            cursor.execute(query, (member_data['member_name'], member_data['email'], id))
            conn.commit()
        except Error as e:
            return jsonify(e.messages), 500
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
                return member_schema.jsonify(member_data)
            
# Delete a member with a DELETE request

@app.route("/members/<int:id>", methods = ['DELETE'])
def delete_member(id):
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary= True)
            query = "SELECT * FROM members WHERE id = %s;"
            cursor.execute(query, (id,))
            member = cursor.fetchone()
            if member is None:
                return jsonify({'Message' : 'Member not found!'}), 404
            query = "DELETE FROM members WHERE id = %s;"
            cursor.execute(query, (id,))
            conn.commit()
        except Error as e:
            return jsonify(e.messages), 500
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
                return jsonify({'Message' : 'Member deleted successfully!'})
            
# Develop routes to schedule, update, and view workout sessions

# Create the WorkoutSession table schema, to define the structure of our data

class WorkoutSessionSchema(ma.Schema):
    id = fields.Int(dump_only= True)
    session_name = fields.String(required= True)
    session_time = fields.Time(required= True)
    session_date = fields.Date(required= True)
    member_id = fields.Int()

    class Meta:
        fields = ("session_name", "session_date", "member_id")

workout_session_schema = WorkoutSessionSchema()
workout_sessions_schema = WorkoutSessionSchema(many= True)

# View all workout session data via a GET request

@app.route("/workout_sessions", methods = ['GET'])
def get_workout_sessions():
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary= True)
            query = "SELECT * FROM workout_sessions;"
            cursor.execute(query)
            workout_sessions = cursor.fetchall()
        except Error as e:
            return jsonify(e.messages), 500
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
                return workout_sessions_schema.jsonify(workout_sessions)
            
# View all workout sessions for a specific member via a GET request

@app.route("/workout_sessions/member/<int:member_id>", methods = ['GET'])
def get_member_workout_sessions(member_id):
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary= True)
            query = "SELECT * FROM workout_sessions WHERE member_id = %s;"
            cursor.execute(query, (member_id,))
            workout_sessions = cursor.fetchall()
        except Error as e:
            return jsonify(e.messages), 500
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
                return workout_sessions_schema.jsonify(workout_sessions)
            
# Schedule a new workout session with a POST request

@app.route("/workout_sessions", methods = ['POST'])
def add_workout_session():
    try:
        workout_session_data = workout_session_schema.load(request.json)
    except ValidationError as e:
        return e.messages, 400

    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary= True)
            query = "INSERT INTO workout_sessions (session_name, session_date, member_id) VALUES (%s, %s, %s);"
            cursor.execute(query, (workout_session_data['session_name'], workout_session_data['session_date'], workout_session_data['member_id']))
            conn.commit()
        except Error as e:
            return jsonify(e.messages), 500
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
                return workout_session_schema.jsonify(workout_session_data)
            
# Update a workout session with a PUT request

@app.route("/workout_sessions/<int:id>", methods = ['PUT'])
def update_workout_session(id):
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary= True)
            query = "SELECT * FROM workout_sessions WHERE id = %s;"
            cursor.execute(query, (id,))
            workout_session = cursor.fetchone()
            if workout_session is None:
                return jsonify({'Message' : 'Workout session not found!'}), 404
            workout_session_data = workout_session_schema.load(request.json)
            query = "UPDATE workout_sessions SET session_name = %s, session_date = %s, member_id = %s WHERE id = %s;"
            cursor.execute(query, (workout_session_data['session_name'], workout_session_data['session_date'], workout_session_data['member_id'], id))
            conn.commit()
        except Error as e:
            return jsonify(e.messages), 500
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
                return workout_session_schema.jsonify(workout_session_data)
            
# Delete a workout session with a DELETE request

@app.route("/workout_sessions/<int:id>", methods = ['DELETE'])
def delete_workout_session(id):
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary= True)
            query = "SELECT * FROM workout_sessions WHERE id = %s;"
            cursor.execute(query, (id,))
            workout_session = cursor.fetchone()
            if workout_session is None:
                return jsonify({'Message' : 'Workout session not found!'}), 404
            query = "DELETE FROM workout_sessions WHERE id = %s;"
            cursor.execute(query, (id,))
            conn.commit()
        except Error as e:
            return jsonify(e.messages), 500
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
                return jsonify({'Message' : 'Workout session deleted successfully!'})
            












if __name__ == '__main__':
    app.run(debug= True)

    