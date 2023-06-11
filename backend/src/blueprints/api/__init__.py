""" Blueprint for the API """
# Standard libraries
from os import getenv

# External libraries
from flask import (
    Blueprint,
    request,
    Response,
    jsonify
)

# Local imports
from src.utils import load_dataframe

# Create blueprint
api_bp = Blueprint(
    name="api_bp",
    import_name=__name__
)

# Load dataframe
dataframe = load_dataframe(getenv("DF_KIND"), getenv("DF_CONNECTION_PATH"))

# Get courses
@api_bp.route("/courses", methods=["GET", "POST"])
def api_get_courses(dataframe=dataframe) -> Response:
    """
    Route to query courses data
    """
    if request.method == "GET":
        results = list(sorted(dataframe["curso"].unique()))
    elif request.method == "POST":
        body = request.get_json()
        course_df = dataframe.loc[
            dataframe["curso"] == body.get("course")
        ].sort_values(
            by=["periodo", "codigo"],
            ascending=True
        )
        semesters = enumerate(course_df["periodo"].unique())
        results = {
            "course": body.get("course"),
            "semesters": [
                {
                    "id": i,
                    "name": semester,
                    "subjects": [
                        {
                            "name": subject["disciplina"],
                            "code": subject["codigo"],
                            "credits": subject["codigo"]
                        }
                        for _, subject in course_df.loc[
                            course_df["periodo"] == semester
                        ].drop_duplicates(["codigo"]).iterrows()
                    ]
                }
                for i, semester in semesters
            ]
        }
    return jsonify(
        results
    )

# Sample route
@api_bp.route("/", methods=["GET"])
def api_root() -> Response:
    """
    Sample route that returns the values it
    receives as query parameters
    """
    params = request.args

    results = [
        {
            "key": key,
            "value": value
        }
        for key, value
        in params.items()
    ]

    return jsonify(
        results
    )
