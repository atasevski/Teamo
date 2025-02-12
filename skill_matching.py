from flask import Flask, request, jsonify
from difflib import get_close_matches
from fuzzywuzzy import process

app = Flask(__name__)

# Administrator's list of skills
ADMIN_SKILLS = ['Python', 'relational database', 'Software engineering',
                'data science', 'NLP', 'natural language processing']


def find_best_matches(query, skills, n=3, cutoff=0.5):
    """
    Find the best matches using simple string similarity.
    """
    return get_close_matches(query, skills, n=n, cutoff=cutoff)


def find_fuzzy_matches(query, skills, n=3):
    """
    Use fuzzy matching to find the closest skills.
    """
    matches = process.extract(query, skills, limit=n)
    return [match[0] for match in matches if match[1] > 50]


@app.route('/match', methods=['POST'])
def match_skill():
    data = request.json
    user_skill = data.get("skill")

    if not user_skill:
        return jsonify({"error": "Please provide a skill name."}), 400

    simple_matches = find_best_matches(user_skill, ADMIN_SKILLS)
    fuzzy_matches = find_fuzzy_matches(user_skill, ADMIN_SKILLS)

    return jsonify({
        "query": user_skill,
        "simple_matches": simple_matches,
        "fuzzy_matches": fuzzy_matches
    })


if __name__ == '__main__':
    app.run(debug=True)
