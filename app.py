from flask import Flask, request, render_template_string, flash, redirect, url_for, render_template
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Template strings to render HTML pages
ADD_PLAYER_FORM = '''
<!doctype html>
<html lang="en">
<head>
    <title>Add Player</title>
    <!-- Include Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="container mt-5">
        <h2 class="mb-4">Add a New Tennis Player</h2>
        <form method="post" action="/add_player">
            <div class="form-group">
                <label for="firstname">First Name</label>
                <input type="text" class="form-control" name="firstname" id="firstname" required>
            </div>
            <div class="form-group">
                <label for="lastname">Last name</label>
                <input type="text" class="form-control" name="lastname" id="lastname" required>
            </div>
            <div class="form-group">
                <label for="hand">Hand</label>
                <select class="form-control" name="hand" id="hand">
                    <option value="L">Left</option>
                    <option value="R">Right</option>
                </select>
            </div>
            <div class="form-group">
                <label for="dob">DOB</label>
                <input type="date" class="form-control" name="dob" id="dob" required>
            </div>
            <div class="form-group">
                <label for="country">Country</label>
                <input type="text" class="form-control" name="country" id="country" required>
            </div>
            <div class="form-group">
                <label for="birthplace">Birthplace</label>
                <input type="text" class="form-control" name="birthplace" id="birthplace">
            </div>
            <div class="form-group">
                <label for="residence">Residence</label>
                <input type="text" class="form-control" name="residence" id="residence">
            </div>
            <div class="form-group">
                <label for="height">Height (cm)</label>
                <input type="number" class="form-control" name="height" id="height">
            </div>
            <div class="form-group">
                <label for="weight">Weight (kg)</label>
                <input type="number" class="form-control" name="weight" id="weight">
            </div>
            <div class="form-group">
                <label for="turnedPro">Turned Pro (Year)</label>
                <input type="number" class="form-control" name="turnedPro" id="turnedPro">
            </div>
            <div class="form-group">
                <label for="rankingPoints">Ranking Points</label>
                <input type="number" class="form-control" name="rankingPoints" id="rankingPoints">
            </div>
            <button type="submit" class="btn btn-primary">Add Player</button>
            
        </form>
    </div>
    <div class="container">
        <a href="/" class="btn btn-secondary my-3">Home</a>
        <!-- ... (rest of your form elements) ... -->
    </div>
    <!-- Include Bootstrap JS and its dependencies below, if you need any Bootstrap JS components -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.7.0/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
'''


DISPLAY_PLAYERS = '''
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">

    <title>List of Players</title>
  </head>
  <body>
    <div class="container mt-3">
      <h2 class="mb-3">List of Tennis Players</h2>
      <table class="table table-hover">
        <thead class="thead-dark">
          <tr>
            <th>Firstname</th>
            <th>Lastname</th>
            <th>Hand</th>
            <th>DOB</th>
            <th>Country</th>
            <th>Birthplace</th>
            <th>Residence</th>
            <th>Height</th>
            <th>Weight</th>
            <th>Turned Pro</th>
          </tr>
        </thead>
        <tbody>
          {% for player in players %}
          <tr>
            <td>{{ player.firstname }}</td>
            <td>{{ player.lastname }}</td>
            <td>{{ player.hand }}</td>
            <td>{{ player.dob }}</td>
            <td>{{ player.country }}</td>
            <td>{{ player.birthplace }}</td>
            <td>{{ player.residence }}</td>
            <td>{{ player.height }}</td>
            <td>{{ player.weight }}</td>
            <td>{{ player.turnedPro }}</td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
      <a href="/add_player" class="btn btn-primary">Add another player</a>
    </div>

    <!-- Optional JavaScript; choose one of the two! -->

    <!-- Option 1: jQuery and Bootstrap Bundle (includes Popper) -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.bundle.min.js"></script>
    <div class="container">
        <a href="/" class="btn btn-secondary my-3">Home</a>
        <!-- ... (rest of your form elements) ... -->
    </div>
  </body>
</html>
'''

ADD_TOURNAMENT_FORM = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Add Tournament</title>
    <!-- Include Bootstrap CSS for styling -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <nav class="navbar navbar-dark bg-primary">
        <a class="navbar-brand" href="/">Tennis Tracker App</a>
    </nav>
    <div class="container mt-4">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">Add a New Tennis Tournament</div>
                    <div class="card-body">
                        <form method="post" action="/add_tournament">
                            <div class="form-group">
                                <label for="name">Name</label>
                                <input type="text" class="form-control" id="name" name="name" required>
                            </div>
                            <div class="form-group">
                                <label for="surface">Surface</label>
                                <input type="text" class="form-control" id="surface" name="surface" required>
                            </div>
                            <div class="form-group">
                                <label for="draw_size">Draw Size</label>
                                <input type="number" class="form-control" id="draw_size" name="draw_size" required>
                            </div>
                            <div class="form-group">
                                <label for="country">Country</label>
                                <input type="text" class="form-control" id="country" name="country" required>
                            </div>
                            <div class="form-group">
                                <label for="city">City</label>
                                <input type="text" class="form-control" id="city" name="city" required>
                            </div>
                            <div class="form-group">
                                <label for="start_date">Start Date</label>
                                <input type="date" class="form-control" id="start_date" name="start_date" required>
                            </div>
                            <div class="form-group">
                                <label for="end_date">End Date</label>
                                <input type="date" class="form-control" id="end_date" name="end_date" required>
                            </div>
                            <button type="submit" class="btn btn-primary">Add Tournament</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Bootstrap JS and its dependencies -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.7.0/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
'''


DISPLAY_TOURNAMENTS = '''
<!doctype html>
<html lang="en">
<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">

    <title>List of Tournaments</title>
</head>
<body>
    <div class="container mt-3">
        <h2 class="mb-3">List of Tennis Tournaments</h2>
        <table class="table table-hover">
            <thead class="thead-dark">
                <tr>
                    <th>Name</th>
                    <th>Surface</th>
                    <th>Draw Size</th>
                    <th>Country</th>
                    <th>City</th>
                    <th>Start Date</th>
                    <th>End Date</th>
                </tr>
            </thead>
            <tbody>
                {% for tournament in tournaments %}
                <tr>
                    <td>{{ tournament.name }}</td>
                    <td>{{ tournament.surface }}</td>
                    <td>{{ tournament.draw_size }}</td>
                    <td>{{ tournament.country }}</td>
                    <td>{{ tournament.city }}</td>
                    <td>{{ tournament.start_date }}</td>
                    <td>{{ tournament.end_date }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        <a href="/add_tournament" class="btn btn-primary">Add a tournament</a>
        <a href="/" class="btn btn-secondary my-3">Home</a>
    </div>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.7.0/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
'''


HOME_PAGE = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tennis Tracker App</title>
    <!-- Include Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="container text-center mt-5">
        <h1>Welcome to the Tennis Tracker App</h1>
        <p class="lead mt-4">Track your favorite tennis players and their stats!</p>
        
        <div class="row justify-content-center mt-5">
            <!-- Player buttons -->
            <div class="col-sm-12 col-md-6 mb-3">
                <a href="/add_player" class="btn btn-primary btn-lg btn-block">Add Player</a>
            </div>
            <div class="col-sm-12 col-md-6 mb-3">
                <a href="/players" class="btn btn-success btn-lg btn-block">View Players</a>
            </div>
        </div>
        
        <div class="row justify-content-center">
            <!-- Tournament buttons -->
            <div class="col-sm-12 col-md-6 mb-3">
                <a href="/add_tournament" class="btn btn-warning btn-lg btn-block">Add Tournament</a>
            </div>
            <div class="col-sm-12 col-md-6 mb-3">
                <a href="/tournaments" class="btn btn-info btn-lg btn-block">View Tournaments</a>
            </div>
        </div>
        <div class="row justify-content-center">
            <!-- Tournament buttons -->
            <div class="col-sm-12 col-md-6 mb-3">
                <a href="/delete_player" class="btn btn-warning btn-lg btn-block">Delete Player</a>
            </div>
            <div class="col-sm-12 col-md-6 mb-3">
                <a href="/delete_tournament" class="btn btn-info btn-lg btn-block">Delete Tournaments</a>
            </div>
        </div>
        <div class="row justify-content-center mt-5">
            <!-- Player buttons -->
            <div class="col-sm-12 col-md-6 mb-3">
                <a href="/update_points" class="btn btn-primary btn-lg btn-block">Update points</a>
            </div>
            <div class="col-sm-12 col-md-6 mb-3">
                <a href="/rankings" class="btn btn-success btn-lg btn-block">Rankings</a>
            </div>
        </div>
    </div>
    <!-- Include Bootstrap JS and its dependencies below -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.7.0/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
'''

DELETE_PLAYER_FORM = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Delete Player</title>
    <!-- Include Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <nav class="navbar navbar-dark bg-primary">
        <a class="navbar-brand" href="/">Tennis Tracker App</a>
    </nav>
    <div class="container mt-4">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header bg-danger text-white">Delete a Tennis Player</div>
                    <div class="card-body">
                        <form method="post" action="/delete_player">
                            <div class="form-group">
                                <label for="firstname">Firstname</label>
                                <input type="text" class="form-control" id="firstname" name="firstname" required>
                            </div>
                            <div class="form-group">
                                <label for="lastname">Lastname</label>
                                <input type="text" class="form-control" id="lastname" name="lastname" required>
                            </div>
                            <button type="submit" class="btn btn-danger">Delete Player</button>
                        </form>
                    </div>
                </div>
                <div class="mt-2">
                    <a href="/" class="btn btn-secondary">Back to Home</a>
                </div>
            </div>
        </div>
    </div>
    <a href="/" class="btn btn-secondary my-3">Home</a>
    <!-- Include Bootstrap JS and its dependencies -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.7.0/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
'''

DELETE_TOURNAMENT_FORM = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Delete Tournament</title>
    <!-- Include Bootstrap CSS for styling -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <nav class="navbar navbar-dark bg-danger">
        <a class="navbar-brand" href="/">Tennis Tracker App</a>
    </nav>
    <div class="container mt-4">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header text-white bg-danger">Delete a Tennis Tournament</div>
                    <div class="card-body">
                        <form method="post" action="/delete_tournament">
                            <div class="form-group">
                                <label for="name">Tournament Name</label>
                                <input type="text" class="form-control" id="name" name="name" required>
                            </div>
                            <button type="submit" class="btn btn-danger">Delete Tournament</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <a href="/" class="btn btn-secondary my-3">Home</a>
    <!-- Include Bootstrap JS and its dependencies -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.7.0/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
'''



UPDATE_POINTS_FORM = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Update Player Points</title>
    <!-- Include Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="container mt-5">
        <h2 class="mb-4">Update Player Ranking Points</h2>
        <form method="post" action="/update_points">
            <div class="form-group">
                <label for="firstname">First Name</label>
                <input type="text" class="form-control" name="firstname" id="firstname" required>
            </div>
            <div class="form-group">
                <label for="lastname">Last Name</label>
                <input type="text" class="form-control" name="lastname" id="lastname" required>
            </div>
            <div class="form-group">
                <label for="points">New Points</label>
                <input type="number" class="form-control" name="points" id="points" required>
            </div>
            <button type="submit" class="btn btn-primary">Update Points</button>
        </form>
        <a href="/" class="btn btn-secondary my-3">Home</a>
    </div>
    <!-- Include Bootstrap JS and its dependencies -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.7.0/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
'''

RANKINGS_PAGE_TEMPLATE = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tennis Player Rankings</title>
    <!-- Include Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="container mt-5">
        <h2>Tennis Player Rankings</h2>
        <table class="table">
            <thead>
                <tr>
                    <th scope="col">#</th>
                    <th scope="col">Name</th>
                    <th scope="col">Ranking Points</th>
                </tr>
            </thead>
            <tbody>
                {% for player in rankings %}
                <tr>
                    <td>{{ player['rank'] }}</td>
                    <td>{{ player['full_name'] }}</td>
                    <td>{{ player['points'] or 'N/A' }}</td>
                </tr>
                {% else %}
                <tr>
                    <td colspan="3">No rankings available.</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        <a href="/" class="btn btn-secondary my-3">Home</a>
    </div>
    
    <!-- Include Bootstrap JS and its dependencies -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.7.0/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
'''
FIND_PLAYER_FORM = '''
<!doctype html>
<html lang="en">
<head>
    <title>Find Player</title>
    <!-- Include Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="container mt-5">
        <h2 class="mb-4">Find Tennis Player</h2>
        <form method="post" action="/find_player">
            <div class="form-group">
                <label for="lastname">Last Name</label>
                <input type="text" class="form-control" name="lastname" id="lastname">
            </div>
            <div class="form-group">
                <label for="firstname">First Name</label>
                <input type="text" class="form-control" name="firstname" id="firstname">
            </div>
            <div class="form-group">
                <label for="country">Country</label>
                <input type="text" class="form-control" name="country" id="country">
            </div>
            <button type="submit" class="btn btn-primary">Search</button>
        </form>
    </div>
    <!-- Include Bootstrap JS and its dependencies below, if you need any Bootstrap JS components -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.7.0/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
'''
SEARCH_RESULTS_TEMPLATE = '''
<!doctype html>
<html lang="en">
<head>
    <title>Search Results</title>
    <!-- Include Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="container mt-5">
        <h2>Search Results</h2>
        <table class="table">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Points</th>
                    <!-- Add other header fields if needed -->
                    <th>Country</th>
                </tr>
            </thead>
            <tbody>
                {% for player in players %}
                <tr>
                    <td>{{ player['firstname'] }} {{ player['lastname'] }}</td>
                    <td>{{ player['points'] }}</td>
                    <!-- Add other player details here -->
                    <td>{{ player['country'] }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>
'''



# Flask route for home page
@app.route('/')
def home():
    return HOME_PAGE


# Route for adding a new player (GET to display form, POST to add player)
@app.route('/add_player', methods=['GET', 'POST'])
def add_player():
    if request.method == 'POST':
        # Get form data
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        hand = request.form['hand']
        dob = request.form['dob']
        country = request.form['country']
        birthplace = request.form['birthplace']
        residence = request.form['residence']
        height = request.form['height']
        weight = request.form['weight']
        turnedPro = request.form['turnedPro']
        point = request.form['rankingPoints']
        
        # Insert player into the database
        with sqlite3.connect('tennis.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO players (playerRef, firstname, lastname, hand, dob, country,
                                     birthplace, residence, height, weight, turnedPro)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (f"{firstname.lower()}_{lastname.lower()}", firstname, lastname, hand, dob, country,
                  birthplace, residence, height, weight, turnedPro))
            player_id = cursor.lastrowid  
            cursor.execute('''
                INSERT INTO rankings (playerId, rank, points, rankingDate)
                VALUES (?, NULL, ?, NULL)
            ''', (player_id, point))
            
            conn.commit()
        
        return 'Player and ranking added successfully! <a href="/players">See all players</a>'
    return render_template_string(ADD_PLAYER_FORM)

# Route for displaying all players
@app.route('/players')
def players():
    with sqlite3.connect('tennis.db') as conn:
        conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM players')
        players = cursor.fetchall()
    return render_template_string(DISPLAY_PLAYERS, players=players)

@app.route('/add_tournament', methods=['GET', 'POST'])
def add_tournament():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        surface = request.form['surface']
        draw_size = request.form['draw_size']
        country = request.form['country']
        city = request.form['city']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        
        # Insert new tournament into the database
        with sqlite3.connect('tennis.db') as conn:
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO tournaments (name, surface, draw_size, country, city, start_date, end_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, surface, draw_size, country, city, start_date, end_date))
            conn.commit()
        
        # Redirect to view tournaments after adding
        return 'Tournament added successfully! <a href="/tournaments">See all tournaments</a>'
    
    # Render the add tournament form
    return render_template_string(ADD_TOURNAMENT_FORM)

@app.route('/tournaments')
def view_tournaments():
    # Retrieve all tournaments from the database
    with sqlite3.connect('tennis.db') as conn:
        conn.row_factory = sqlite3.Row 
        cur = conn.cursor()
        cur.execute('SELECT * FROM tournaments')
        tournaments = cur.fetchall()

    
    return render_template_string(DISPLAY_TOURNAMENTS, tournaments=tournaments)

@app.route('/delete_player', methods=['GET'])
def delete_player_form():
    return render_template_string(DELETE_PLAYER_FORM)

@app.route('/delete_player', methods=['POST'])
def delete_player():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    message = ""
    try:
        with sqlite3.connect('tennis.db') as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM players WHERE firstname=? AND lastname=?", (firstname, lastname))
            if cursor.rowcount == 0:
                message = "No player found with the provided name."
            else:
                conn.commit()
                message = "Player successfully deleted."
    except Exception as e:
        message = "An error occurred: " + str(e)
    finally:
        return f'''
        <div class="container">
            <h2>{message}</h2>
            <a href="/delete_player" class="btn btn-primary mt-2">Delete Another Player</a>
            <a href="/" class="btn btn-secondary mt-2">Back to Home</a>
        </div>
        '''
@app.route('/delete_tournament', methods=['GET'])
def delete_tournament_form():
      return render_template_string(DELETE_TOURNAMENT_FORM)

@app.route('/delete_tournament', methods=['POST'])
def delete_tournament():
    name = request.form['name']
    message = ""
    try:
        with sqlite3.connect('tennis.db') as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tournaments WHERE name=?", (name,))
            if cursor.rowcount == 0:
                message = "No tournament found with the provided name."
            else:
                conn.commit()
                message = "Tournament successfully deleted."
    except Exception as e:
        message = "An error occurred: " + str(e)
    finally:
        return f'''
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Delete Tournament Result</title>
            <!-- Include Bootstrap CSS -->
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        </head>
        <body>
            <div class="container mt-4">
                <h2>{message}</h2>
                <a href="/delete_tournament" class="btn btn-danger mt-2">Delete Another Tournament</a>
                <a href="/" class="btn btn-secondary mt-2">Back to Home</a>
            </div>
            <!-- Include Bootstrap JS and its dependencies -->
            <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.7.0/dist/umd/popper.min.js"></script>
            <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
        </body>
        </html>
        '''
@app.route('/rankings')
def show_rankings():
    with sqlite3.connect('tennis.db') as conn:
        conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
        cursor = conn.cursor()
        
        # Generate the rank based on points and concatenate first and last names
        cursor.execute('''
            SELECT ROW_NUMBER() OVER (ORDER BY r.points DESC, p.lastname ASC) AS rank,
                   p.firstname || ' ' || p.lastname AS full_name,
                   r.points
            FROM players p
            LEFT JOIN rankings r ON p.playerId = r.playerId
            ORDER BY r.points DESC, p.lastname ASC
        ''')
        rankings = cursor.fetchall()

    # Render the rankings page
    return render_template_string(RANKINGS_PAGE_TEMPLATE, rankings=rankings)

@app.route('/update_points', methods=['GET', 'POST'])
def update_points():
    if request.method == 'POST':
        # Retrieve data from form
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        new_points = request.form['points']

        with sqlite3.connect('tennis.db') as conn:
            cursor = conn.cursor()
            # Check if the player exists
            cursor.execute('SELECT playerId FROM players WHERE firstname = ? AND lastname = ?', (firstname, lastname))
            player = cursor.fetchone()
            if player:
                player_id = player[0]
                # Check if the player already has points in the rankings
                cursor.execute('SELECT points FROM rankings WHERE playerId = ?', (player_id,))
                ranking = cursor.fetchone()
                if ranking and ranking[0] is not None:  # Player has points, so update
                    cursor.execute('UPDATE rankings SET points = ? WHERE playerId = ?', (new_points, player_id))
                    message = "Points modified"
                else:  # Player has no points, so insert new points
                    cursor.execute('UPDATE rankings SET points = ? WHERE playerId = ?', (new_points, player_id))
                    message = "Points added"
                conn.commit()
            else:
                message = "Player does not exist"

        return message
    else:
        # Render form for GET request
        return render_template_string(UPDATE_POINTS_FORM)

@app.route('/find_player', methods=['GET', 'POST'])
def find_player():
    if request.method == 'POST':
        lastname = request.form['lastname']
        firstname = request.form['firstname']
        country = request.form['country']
        
        # Connect to the database
        with sqlite3.connect('tennis.db') as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Update the query to sort by points
            query = '''
            SELECT p.*, r.points
            FROM players p
            LEFT JOIN rankings r ON p.playerId = r.playerId
            WHERE (p.lastname LIKE ? OR ? = '')
            AND (p.firstname LIKE ? OR ? = '')
            AND (p.country LIKE ? OR ? = '')
            ORDER BY r.points DESC, r.rankingDate DESC  -- Sorted by points and then by the most recent ranking date
            '''
            
            # Execute the query
            cursor.execute(query, (f'%{lastname}%', lastname, f'%{firstname}%', firstname, f'%{country}%', country))
            players = cursor.fetchall()
        
        # Check if any players were found
        if players:
            return render_template_string(SEARCH_RESULTS_TEMPLATE, players=players)
        else:
            return 'No players found'
    
    # If it's a GET request, just display the search form
    return render_template_string(FIND_PLAYER_FORM)



# Run the Flask application
if __name__ == '__main__':
    app.run(port=2409, debug=True)
