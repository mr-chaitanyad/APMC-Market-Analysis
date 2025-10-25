from dash import Dash
from app.layout import layout
from app.callbacks import register_callbacks

app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
app.title = "🌾 Maharashtra APMC Data Analysis"

app.layout = layout
register_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True)

