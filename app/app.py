import simplejson as json
from flask import Blueprint, Flask, request, Response, redirect, url_for, flash
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from forms import SignupForm, LoginForm
from flask_login import current_user, login_required, logout_user, LoginManager, login_user
from flask_sqlalchemy import SQLAlchemy
from .models import User

db = SQLAlchemy()

app = Flask(__name__)

mysql = MySQL(cursorclass=DictCursor)

app.config.from_object('config.Config')

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'mlbPlayerData'
mysql.init_app(app)

# db.init_app(app)
# mysql.init_app(app)

login_manager = LoginManager()


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Michael'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mlbPlayers')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, players=result)


@app.route('/view/<int:player_id>', methods=['GET'])
def record_view(player_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mlbPlayers WHERE id=%s', player_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', player=result[0])


@app.route('/edit/<int:player_id>', methods=['GET'])
def form_edit_get(player_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mlbPlayers WHERE id=%s', player_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', player=result[0])


@app.route('/edit/<int:player_id>', methods=['POST'])
def form_update_post(player_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('plName'), request.form.get('plTeam'), request.form.get('plPosition'),
                 request.form.get('plHeight'), request.form.get('plWeight'),
                 request.form.get('plAge'), player_id)
    sql_update_query = """UPDATE mlbPlayers t SET t.plName = %s, t.plTeam = %s, t.plPosition = %s, t.plHeight = 
    %s, t.plWeight = %s, t.plAge = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/player/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New MLB Player Form')


@app.route('/player/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('plName'), request.form.get('plTeam'), request.form.get('plPosition'),
                 request.form.get('plHeight'), request.form.get('plWeight'),
                 request.form.get('plAge'))
    sql_insert_query = """INSERT INTO mlbPlayers (plName,plTeam, plPosition, plHeight, plWeight,
                        plAge) VALUES (%s,%s, %s,%s, %s,%s)"""
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:player_id>', methods=['POST'])
def form_delete_post(player_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM mlbPlayers WHERE id = %s """
    cursor.execute(sql_delete_query, player_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/players', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mlbPlayers')
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/players/<int:player_id>', methods=['GET'])
def api_retrieve(player_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM mlbPlayers WHERE id=%s', player_id)
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/players/<int:player_id>', methods=['PUT'])
def api_edit(player_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['plName'], content['plTeam'], content['plPosition'],
                 content['plHeight'], content['plWeight'],
                 content['plAge'], player_id)
    sql_update_query = """UPDATE mlbPlayers t SET t.plName = %s, t.plTeam = %s, t.plPosition = %s, t.plHeight = 
        %s, t.plWeight = %s, t.plAge = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/players', methods=['POST'])
def api_add() -> str:
    content = request.json

    cursor = mysql.get_db().cursor()
    inputData = (content['plName'], content['plTeam'], content['plPosition'],
                 content['plHeight'], content['plWeight'],
                 content['plAge'])
    sql_insert_query = """INSERT INTO mlbPlayers (plName,plTeam, plPosition, plHeight, plWeight,
                        plAge) VALUES (%s,%s, %s,%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/players/<int:player_id>', methods=['DELETE'])
def api_delete(player_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM mlbPlayers WHERE id = %s """
    cursor.execute(sql_delete_query, player_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    return render_template(
        '/signup.jinja2',
        title='Create an Account.',
        form=SignupForm(),
        template='signup-page',
        body="Sign up for a user account."
    )


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    return render_template(
        '/login.html',
        title='Create an Account.',
        form=LoginForm,
        template='login-page',
        body="Log in to your account."
    )


@app.route('/', methods=['GET'])
@login_required
def dashboard():
    """Logged-in User Dashboard."""
    return render_template(
        'dashboard.jinja2',
        title='Flask-Login Tutorial.',
        template='dashboard-template',
        current_user=current_user,
        body="You are now logged in!"
    )


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    User sign-up page.
    GET requests serve sign-up page.
    POST requests validate form & user creation.
    """
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            user = User(
                name=form.name.data,
                email=form.email.data,
                website=form.website.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()  # Create new user
            login_user(user)  # Log in as newly created user
            return redirect(url_for('main_bp.dashboard'))
        flash('A user already exists with that email address.')
    return render_template(
        'signup.jinja2',
        title='Create an Account.',
        form=form,
        template='signup-page',
        body="Sign up for a user account."
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log-in page for registered users.
    GET requests serve Log-in page.
    POST requests validate and redirect user to dashboard.
    """
    # Bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.jinja2'))

    form = LoginForm()
    # Validate login attempt
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main_bp.dashboard'))
        flash('Invalid username/password combination')
        return redirect(url_for('login.html'))
    return render_template(
        'login.jinja2',
        form=form,
        title='Log in.',
        template='login-page',
        body="Log in with your User account."
    )


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in upon page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login'))


@app.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('login.html'))


@app.errorhandler(404)
def not_found(arg):
    """Page not found."""
    return render_template('404.html', title='404 error.', message='Page Not Found')


@app.errorhandler(400)
def bad_request():
    """Bad request."""
    return render_template('400.html', title='400 error.', message='Bad request.  Page Not Found')


@app.errorhandler(500)
def server_error(arg):
    """Internal server error."""
    return render_template('500.html', message='Server Error')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
