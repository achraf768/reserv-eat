import sqlite3
import flask
import random

app = flask.Flask(__name__, template_folder='views', static_folder='views')

# Def de la route home
@app.route('/', methods=['GET', 'POST'])
def home():
    try:
        # Connection à la bdd
        connection = sqlite3.connect('data.db')

        # Création de la table Joueur si inexistante
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS users (userId INTEGER PRIMARY KEY, name VARCHAR(50), mdp VARCHAR(50), email VARCHAR(50), addresse VARCHAR(50), handicap BOOLEAN, handicapType VARCHAR(50))')
        cursor.execute('CREATE TABLE IF NOT EXISTS restaurant (restaurantId INTEGER PRIMARY KEY, restaurantType VARCHAR(50), restaurantName VARCHAR(50), address VARCHAR(50), phoneNum VARCHAR(50), handicap BOOLEAN, handicapType VARCHAR(50))')
        connection.commit()
        print("Tables created successfully")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        connection.close()
    return flask.render_template('/index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    email_existant = False  # Initialisation avec une valeur par défaut
    if flask.request.method == 'POST':
        email = flask.request.values.get('email')
        mdp = flask.request.values.get('mdp')
        name = flask.request.values.get('name')
        handicap = flask.request.values.get('handicap')
        handicapType = flask.request.values.get('handicapType')
        addresse = flask.request.values.get('addresse')

        try:
            # On vérifie si le pseudo existe déjà
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute('SELECT COUNT(*) FROM users WHERE email=?', (email,))
            email_existant = cursor.fetchone()[0] > 0
        except sqlite3.Error as e:
            print(f"An error occurred while checking existing email: {e}")
        finally:
            connection.close()

        if email_existant:
            return flask.render_template('error_page.html', message="Erreur! Cette email est déjà prise !")
        else:
            try:
                # On ajoute le nouveau player dans la bdd après vérification
                connection = sqlite3.connect('data.db')
                cursor = connection.cursor()
                cursor.execute('INSERT INTO users (email, mdp, name, handicap, handicapType, addresse) VALUES (?,?,?,?,?)', (email, mdp, name, handicap, handicapType, addresse))
                connection.commit()
                print("User registered successfully")
            except sqlite3.Error as e:
                print(f"An error occurred while inserting a new user: {e}")
            finally:
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

        try:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute('SELECT userId FROM users WHERE email=? AND mdp=?', (name, mdp))
            tuple_userId = cursor.fetchone()
        except sqlite3.Error as e:
            print(f"An error occurred during login: {e}")
        finally:
            connection.close()

        if tuple_userId is not None:
            userId = tuple_userId[0]
            flask.session['userId'] = userId
            flask.session['name'] = name
            return flask.redirect('/recherche')
        else:
            return flask.render_template('error_page.html', message="Erreur! Le pseudo ou le mot de passe est incorrect !")
    else:
        return flask.render_template('connexion.html')

@app.route('/recherche', methods=['GET', 'POST'])
def recherche():
    try:
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # Récupération du handicap de l'utilisateur s'il est spécifié
        handicap = flask.request.values.get('handicap')
        handicapType = flask.request.values.get('handicapType')

        # Construction de la requête SQL pour récupérer les restaurants en fonction du handicap
        if handicap and handicapType:
            cursor.execute('SELECT * FROM restaurant WHERE handicap=? AND handicapType=?', (True, handicapType))
        else:
            cursor.execute('SELECT * FROM restaurant')

        restaurants = cursor.fetchall()

        # Génération de la liste aléatoire de localisations pour chaque restaurant
        localisations = [random.randint(10, 500) for _ in restaurants]

        return flask.render_template('recherche.html', restaurants=restaurants, localisations=localisations)
    except sqlite3.Error as e:
        print(f"An error occurred during restaurant search: {e}")
    finally:
        connection.close()

    return flask.render_template('recherche.html', restaurants=[], localisations=[])


@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    if 'userId' in flask.session:
        if flask.request.method == 'POST':
            name = flask.request.values.get('name')
            handicap = flask.request.values.get('handicap')
            handicapType = flask.request.values.get('handicapType')
            userId = flask.session['userId']

            try:
                connection = sqlite3.connect('data.db')
                cursor = connection.cursor()
                cursor.execute('UPDATE users SET name=?, handicap=?, handicapType=? WHERE userId=?', (name, handicap, handicapType, userId))
                connection.commit()
                print("Profile updated successfully")
            except sqlite3.Error as e:
                print(f"An error occurred while updating profile: {e}")
            finally:
                connection.close()
            return flask.redirect('/home')
        else:
            userId = flask.session['userId']
            try:
                connection = sqlite3.connect('data.db')
                cursor = connection.cursor()
                cursor.execute('SELECT * FROM users WHERE userId=?', (userId,))
                user = cursor.fetchone()
            except sqlite3.Error as e:
                print(f"An error occurred while fetching user data: {e}")
            finally:
                connection.close()
            return flask.render_template('edit-profile.html', user=user)
    else:
        return flask.redirect('/login')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
