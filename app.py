from cs50 import SQL
from flask import Flask, render_template, request, jsonify
from datetime import datetime

# Configure application
app = Flask(__name__)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///scoring.db")


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        age = int(request.form['age'])
        push_ups_reps = int(request.form['push_ups'])
        sit_ups_reps = int(request.form['sit_ups'])
        run_minutes = int(request.form['run_minutes'])
        run_seconds = int(request.form['run_seconds'])

        age_group = get_age_group(age)
        push_ups_score = get_pushup_score(push_ups_reps, age_group)
        sit_ups_score = get_situp_score(sit_ups_reps, age_group)
        run_score = get_run_score(run_minutes, run_seconds)

        if push_ups_score is None or sit_ups_score is None or run_score is None:
            total_score = 0

        else:
            total_score = push_ups_score + sit_ups_score + run_score
            award_type, incentive_amount = calculate_award(total_score, push_ups_score, sit_ups_score, run_score)

        return render_template('index.html', age_group=age_group,
                               push_ups_score=push_ups_score,
                               sit_ups_score=sit_ups_score,
                               run_score=run_score,
                               total_score=total_score,
                               award_type=award_type,
                               incentive_amount=incentive_amount
                               )

    return render_template('index.html', age_group="", push_ups_score=0, sit_ups_score=0, run_score=0, total_score=0)


@app.route("/calculate_age_group", methods=["POST"])
def calculate_age_group():
    age = int(request.form['age'])
    age_group = get_age_group(age)
    return jsonify({"age_group": age_group})


def get_age_group(age):
    user_age_grp = db.execute("SELECT age_grp FROM age_groups WHERE ? >= age_from AND ? <= age_to", age, age) #db.execute returns a list of dictionary
    result = user_age_grp[0]['age_grp']
    return result


@app.route("/calculate_pushup_score", methods=["POST"])
def calculate_pushup_score():
    age = None

    # Check if age is present in form data
    if 'age' in request.form and request.form['age'].strip():
        try:
            age = int(request.form['age'])
        except ValueError:
            return jsonify({"error": "Invalid age value"}), 400

    # Check if age is None
    if age is None:
        return jsonify({"error": "Age required"}), 400

    age_group = get_age_group(age)
    push_ups_reps = int(request.form['push_ups'])
    push_ups_score = get_pushup_score(push_ups_reps, age_group)
    push_ups_to_next_point = get_next_point_pushup(push_ups_reps, push_ups_score, age_group)

    response_data = {
        "push_ups_score": push_ups_score,
        "push_ups_to_next_point": push_ups_to_next_point
    }

    return jsonify(response_data)


def get_pushup_score(reps, age_group):
    score = db.execute("SELECT score FROM pushups WHERE ? = age_grp AND ? = reps", age_group, reps)
    result = score[0]['score']
    return result

# To return how many reps to the next point
def get_next_point_pushup(current_reps, current_score, age_group):
    next_score = 0
    add_reps = 0

    if current_score == 25:
        return add_reps

    elif not current_score == 25:
        next_score = current_score + 1
        next_reps = db.execute("SELECT MIN(reps) AS next_reps FROM pushups WHERE ? = age_grp AND ? = score", age_group, next_score)
        result = next_reps[0]['next_reps']

        if result is None:
            add_reps = 0
        else:
            add_reps = result - current_reps

        return add_reps


@app.route("/calculate_situp_score", methods=["POST"])
def calculate_situp_score():
    age = None

    if 'age' in request.form and request.form['age'].strip():
        try:
            age = int(request.form['age'])
        except ValueError:
            return jsonify({"error": "Invalid age value"}), 400

    if age is None:
        return jsonify({"error": "Age required"}), 400

    age_group = get_age_group(age)
    sit_ups_reps = int(request.form['sit_ups'])
    sit_ups_score = get_situp_score(sit_ups_reps, age_group)
    sit_ups_to_next_point = get_next_point_situp(sit_ups_reps, sit_ups_score, age_group)
    response_data = {
        "sit_ups_score": sit_ups_score,
        "sit_ups_to_next_point": sit_ups_to_next_point
    }
    return jsonify(response_data)


def get_situp_score(reps, age_group):
    score = db.execute("SELECT score FROM situps WHERE ? = age_grp AND ? = reps", age_group, reps)
    result = score[0]['score']
    return result

# To return how many reps to the next point
def get_next_point_situp(current_reps, current_score, age_group):
    next_score = 0
    add_reps = 0

    if current_score == 25:
        return add_reps

    elif not current_score == 25:
        next_score = current_score + 1
        next_reps = db.execute("SELECT MIN(reps) AS next_reps FROM situps WHERE ? = age_grp AND ? = score", age_group, next_score)
        result = next_reps[0]['next_reps']
        add_reps = result - current_reps
        return add_reps


@app.route("/calculate_run_score", methods=["POST"])
def calculate_run_score():
    age = None

    if 'age' in request.form and request.form['age'].strip():
        try:
            age = int(request.form['age'])
        except ValueError:
            return jsonify({"error": "Invalid age value"}), 400

    if age is None:
        return jsonify({"error": "Age required"}), 400

    age_group = get_age_group(age)
    run_minutes = int(request.form['run_minutes'])
    run_seconds = int(request.form['run_seconds'])
    run_score = get_run_score(run_minutes, run_seconds, age_group)
    secs_to_next_point = get_next_point_run(run_minutes, run_seconds, run_score, age_group)

    pace_info = calculate_pace(run_minutes, run_seconds)

    response_data = {
        "run_score": run_score,
        "secs_to_next_point": secs_to_next_point,
        "pace_400m_minutes": pace_info["pace_400m"]["minutes"],
        "pace_400m_seconds": pace_info["pace_400m"]["seconds"],
        "pace_1km_minutes": pace_info["pace_1km"]["minutes"],
        "pace_1km_seconds": pace_info["pace_1km"]["seconds"],
    }
    return jsonify(response_data)


def get_run_score(minutes, seconds, age_group):
    mins = str(minutes)

    # To accomodate for the data in run table where timing ending in 0 seconds are stylized as 00
    if seconds == 0:
        secs = str(seconds) + '0'
    else:
        secs = str(seconds)

    run_time = (mins + ":" + secs)
    score = db.execute("SELECT score FROM run WHERE ? = age_grp AND ? = time_to", age_group, run_time)
    result = score[0]['score']
    return result

# To return how many seconds to the next point
def get_next_point_run(current_minutes, current_seconds, current_score, age_group):
    next_score = 0
    add_secs = 0
    curr_min = str(current_minutes)

    if current_seconds == 0:
        curr_sec = str(current_seconds) + '0'
    else:
        curr_sec = str(current_seconds)

    curr_time_str = (curr_min + ":" + curr_sec)

    if current_score == 25:
        return add_secs

    elif not current_score == 25:
        next_score = current_score + 1
        next_time_query = db.execute("SELECT MAX(time_to) AS next_time FROM run WHERE ? = age_grp AND ? = score", age_group, next_score)

        if next_time_query[0]['next_time'] is not None:
            next_time_str = next_time_query[0]['next_time']
            curr_time = datetime.strptime(curr_time_str, '%M:%S')
            next_time = datetime.strptime(next_time_str, '%M:%S')
            add_secs = (next_time - curr_time).total_seconds()

        return add_secs


# Pace calculator for 400m track and per km for given 2.4km run time
def calculate_pace(run_minutes, run_seconds):
    total_seconds = run_minutes * 60 + run_seconds

    distance_400m = 400
    pace_400m_seconds = total_seconds / (2.4 * 1000 / distance_400m)
    pace_400m_minutes, pace_400m_seconds = divmod(pace_400m_seconds, 60)

    distance_1km = 1000
    pace_1km_seconds = total_seconds / (2.4 * 1000 / distance_1km)
    pace_1km_minutes, pace_1km_seconds = divmod(pace_1km_seconds, 60)

    return {
        "pace_400m": {
            "minutes": int(pace_400m_minutes),
            "seconds": int(pace_400m_seconds),
            },
        "pace_1km": {
            "minutes": int(pace_1km_minutes),
            "seconds": int(pace_1km_seconds),
            },
        }

@app.route("/calculate_total_score", methods=["POST"])
def calculate_total_score():
    total_score = 0

    age = int(request.form['age'])
    age_group = get_age_group(age)

    push_ups_reps = int(request.form['push_ups'])
    push_ups_score = get_pushup_score(push_ups_reps, age_group)

    sit_ups_reps = int(request.form['sit_ups'])
    sit_ups_score = get_situp_score(sit_ups_reps, age_group)

    run_minutes = int(request.form['run_minutes'])
    run_seconds = int(request.form['run_seconds'])
    run_score = get_run_score(run_minutes, run_seconds, age_group)

    total_score = push_ups_score + sit_ups_score + run_score
    award_type, incentive_amount = calculate_award(total_score, push_ups_score, sit_ups_score, run_score)

    return jsonify({
                    "total_score": total_score,
                    "award_type": award_type,
                    "incentive_amount": incentive_amount
                    })


def calculate_award(total_score, push_ups_score, sit_ups_score, run_score):
    # Check conditions and calculate award type and incentive amount
    award_type = ""
    incentive_amount = 0

    if (total_score >= 51 and push_ups_score > 0 and sit_ups_score > 0 and run_score > 0):
        award_type = "Pass (NSMen)"

    if (total_score >= 61 and push_ups_score > 0 and sit_ups_score > 0 and run_score > 0):
        award_type = "Pass with Incentive (NSMen)"
        incentive_amount = 200

    if (total_score >= 75 and push_ups_score > 0 and sit_ups_score > 0 and run_score > 0):
        award_type = "Silver"
        incentive_amount = 300

    if (total_score >= 85 and push_ups_score > 0 and sit_ups_score > 0 and run_score > 0):
        award_type = "Gold"
        incentive_amount = 500

    if (total_score >= 90 and push_ups_score > 0 and sit_ups_score > 0 and run_score > 0):
        award_type = "Gold (Commando/Diver/Guards)"
        incentive_amount = 500

    if (total_score < 51 or push_ups_score == 0 or sit_ups_score == 0 or run_score == 0):
        award_type = "Fail"

    return award_type, incentive_amount


@app.route("/info")
def info():
    return render_template("info.html")


if __name__ == '__main__':
    app.run(debug=True)
