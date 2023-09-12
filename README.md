# IPPT Score Calculator

#### Video Demo: https://youtu.be/JkBxwuLDOuo

## Description
The IPPT Score Calculator is a web application that allows users to calculate their Individual Physical Proficiency Test (IPPT) score. The IPPT is a standardized physical fitness test administered by the Singapore Armed Forces (SAF), the Singapore Police Force (SPF) and the Singapore Civil Defence Force (SCDF) to assess the fitness levels of their medically-eligible members on an annual basis.

Note: The current version only supports the calculator of IPPT scores for males. There is a separate scoring system for females as they take a slightly different variation of the IPPT. However, that said, majority of people who participate in the IPPT are males given that this is a standardized test used for the police, civil defence and the armed forces in Singapore where there is mandatory conscription for all medically-eligible males when they are about 18-19 years old.

## Background on IPPT
IPPT consists of 3 stations - push-ups, sit-ups and a 2.4km run.
The push-ups and sit-ups have to be completed within a time limit of 1 minute and each station has a maximum score of 25.
The 2.4km run has a maximum score of 50.
The maximum score attainable is 100.
The scoring system is age-based, where a younger person has stricter requirements to achieve the same score as an older person.
For example, for a 21 year old to get 25 points for push-ups, he has to complete 60 reps in a minute, whereas for a 47 year old to get 25 points, he only has to complete 49 reps.

Based on your total score, you are awarded one of the following:
- Pass (>= 51 points), no monetary incentive amount awarded
- Pass with Incentive (>= 61 points), $200
- Silver (>= 75 points), $300
- Gold (>= 85 points), $500
- Gold (>= 90 points), $500 for personnel in the Commando, Divers or Guards vocations

The Commando, Divers and Guards vocations have a higher requirement for their people to achieve the Gold standard as they are the elite combat units of the Singapore military.

## Features
- Age Selection: Users can choose their age to determine their age group for scoring.
- Push-Ups: Users can input their push-up rep count to calculate the score.
- Sit-Ups: Users can input their sit-up rep count to calculate the score.
- 2.4km Run: Users can input the time taken in minutes and seconds to complete the 2.4km run to calculate the score and required pace.
- To Next Point: Based on the user's input for each station's performance, the application can calculate the additional number of reps needed for the user to reach the next highest score in the case of the push-ups and sit-ups station, as well as the amount of seconds to reduce from their timing in order for the user to reach the next highest score in the case of the 2.4km run station.
- Overall Score Calculation: The application calculates the score for each component and provides an overall score.
- Award and Incentive Amount: The application uses the total score to determine which award type and corresponding amount is applicable.
- Required Pace: The application displays the required pace for the 2.4km run on a 400m basis and a 1km basis.

## Files
- `app.py`: Contains the Python code for the web application using Flask + the decorator and routes to the various pages and functions.
- `layout.html`: The base HTML template used for the layout of web pages.
- `index.html`: The main web page for the IPPT Score Calculator.
- `info.html`: An additional web page containing explanations about the IPPT.
- `script.js`: JavaScript code for the interactivity of web pages.
- `styles.css`: Contains the CSS for styling the web pages.
- 'scoring.db': The SQL database containing 4 tables: age_groups, situps, pushups and run
-- age_groups provides the index for the calculator to determine the age group, given the age of a user
-- situps and pushups provides the score, given the number of reps and the age group of a user
-- run provides the score, given the amount of time taken and the age group of a user
- 'scoring queries.sql': Contains the queries used to create and configure the 4 tables in scoring.db

## Usage
1. Select your age last birthday from the dropdown menu.
2. Input your performance for push-ups, sit-ups, and the 2.4km run.
3. The application calculates your scores and display them on the page.
4. The application also calculates what your applicable award and incentive amount is based on your total score.
5. You can also find out more about IPPT and how it works if you click on "More Information" in the navbar.

## Design Choices
- Frontend: The application uses HTML, CSS, and JavaScript for the user interface.
- Backend: Flask is used to handle HTTP requests and responses.
- Scoring Algorithm: The application uses a predefined scoring algorithm based on age and performance.

## Additional Notes
- This project was developed as a part of my submission for the CS50X 2023 Final Project assignment.

## Acknowledgments and Thanks
- Thank you to the CS50 team at Harvard University. It has been a real pleasure to have went through the entire course and a great introduction to programming.
