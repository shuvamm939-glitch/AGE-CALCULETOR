import os

from flask import Flask, render_template, request  # type: ignore
from python.newage import calculate_age

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "website", "templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "website", "static"),
)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        try:
            birth_date = request.form["birth_date"]
            present_date = request.form["present_date"]

            b_year, b_month, b_day = map(int, birth_date.split("-"))
            p_year, p_month, p_day = map(int, present_date.split("-"))

            years, months, days = calculate_age(
                b_year, b_month, b_day, p_year, p_month, p_day
            )
            result = {"years": years, "months": months, "days": days}
        except (ValueError, KeyError):
            error = "please select valid dates."

    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    app.run(debug=True)
    