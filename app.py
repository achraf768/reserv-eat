import sqlite3
import flask
import random 

app = flask.Flask(__name__, template_folder='views', static_folder='views')

# Def de la route home
@app.route('/', methods=['GET', 'POST'])
def home():
    # Connection à la bdd
    connection = sqlite3.connect('data.db')

    # Création de la table Joueur si inexistante
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (userId INTEGER PRIMARY KEY, name VARCHAR(50), mdp VARCHAR(50), email VARCHAR(50), handicap BOOLEAN, handicapType VARCHAR(50))')
    cursor.execute('CREATE TABLE IF NOT EXISTS restaurant (restaurantId INTEGER PRIMARY KEY, restaurantType VARCHAR(50), restaurantName VARCHAR(50), address VARCHAR(50), phoneNum VARCHAR(50), handicap BOOLEAN, handicapType VARCHAR(50))')
    connection.commit()
    connection.close()
    return flask.render_template('/index.html')

# Ajout du joueur dans la bdd
@app.route('/register', methods=['GET', 'POST'])
def register():
    if flask.request.method == 'POST':
        email = flask.request.values.get('email')
        mdp = flask.request.values.get('mdp')
        name = flask.request.values.get('name')
        handicap = flask.request.values.get('handicap')
        handicapType = flask.request.values.get('handicapType')
        
        # On vérifie si le pseudo existe déjà
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM users WHERE email=?', (email,))
        email_existant = cursor.fetchone()[0] > 0
        connection.close()
        if email_existant:
            return flask.render_template('error_page.html', message="Erreur! Cette email est déjà prise !")
        else:
            # On ajoute le nouveau player dans la bdd après vérification
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute('INSERT INTO users (email, mdp, name, handicap, handicapType) VALUES (?,?,?,?,?)', (email, mdp, name, handicap, handicapType))
            connection.commit()
            connection.close()
            return flask.redirect('/recherche')
    else:
        return flask.render_template('inscription.html')
    
# Connexion à un compte déjà existant
app.secret_key = 'secret-key'
@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        name = flask.request.form['email']
        mdp = flask.request.form['mdp']
        
        connection = sqlite3.connect('data.db')
        
        cursor = connection.cursor()
        cursor.execute('SELECT userId FROM users WHERE email=? AND mdp=?', (name, mdp))
        tuple_userId = cursor.fetchone()
        connection.close()
        
        if tuple_userId is not None:
            userId = tuple_userId[0]
            flask.session['userId'] = userId
            flask.session['name'] = name
            return flask.redirect('/home')
        else:
            return flask.render_template('error_page.html', message="Erreur! Le pseudo ou le mot de passe est incorrect !")
    else:
        return flask.render_template('connexion.html')
    
@app.route('/recherche', methods=['GET', 'POST'])
def recherche():
    if flask.request.method == 'POST':
        restaurantType = flask.request.values.get('restaurantType')
        handicap = flask.request.values.get('handicap')
        handicapType = flask.request.values.get('handicapType') if handicap == 'True' else None

        connection = sqlite3.connect('includes/data.db')
        cursor = connection.cursor()
        if handicapType:
            cursor.execute('SELECT * FROM restaurant WHERE restaurantType=? AND handicap=? AND handicapType=?', (restaurantType, True, handicapType))
        else:
            cursor.execute('SELECT * FROM restaurant WHERE restaurantType=?', (restaurantType,))
        restaurants = cursor.fetchall()
        connection.close()

        # Générer une liste de nombres aléatoires pour chaque restaurant trouvé
        localisations = [random.randint(10, 500) for _ in restaurants]

        return flask.render_template('recherche.html', restaurants=restaurants, localisations=localisations)
    else:
        return flask.render_template('recherche.html', restaurants=[], localisations=[])

@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    if 'userId' in flask.session:
        if flask.request.method == 'POST':
            name = flask.request.values.get('name')
            handicap = flask.request.values.get('handicap')
            handicapType = flask.request.values.get('handicapType')
            userId = flask.session['userId']
            
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute('UPDATE users SET name=?, handicap=?, handicapType=? WHERE userId=?', (name, handicap, handicapType, userId))
            connection.commit()
            connection.close()
            return flask.redirect('/home')
        else:
            userId = flask.session['userId']
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM users WHERE userId=?', (userId,))
            user = cursor.fetchone()
            connection.close()
            return flask.render_template('edit-profile.html', user=user)
    else:
        return flask.redirect('/login')

app.run(debug=True, port=5000)
