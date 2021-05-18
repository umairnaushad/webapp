from flask import Flask, render_template, url_for

posts = [
    {
        'author': 'Author 1',
        'title': 'Title 1',
        'content': 'Content 1',
        'date_posted': '17 May 2021'
    },
    {
        'author': 'Author 2',
        'title': 'Title 2',
        'content': 'Content 2',
        'date_posted': '18 May 2021'
    }
]

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', param_posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

if __name__ == '__main__':
    app.run(debug=True)