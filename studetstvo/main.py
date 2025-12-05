from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from data.database import get_overall_table_data
app = Flask(__name__)

@app.route("/")
def hello_world():

    html = f"""
    <html>
      <head>
        <title>Students</title>
        <meta charset=\"utf-8\">
        <style>
          table {{ border-collapse: collapse; }}
          th, td {{ border: 1px solid #ccc; padding: 6px 10px; }}
          th {{ background: #f5f5f5; }}
        </style>
      </head>
      <body>
        <h2>Students</h2>
        </table>
      </body>
    </html>
    """
    return html

if __name__ == "__main__":
    get_overall_table_data()