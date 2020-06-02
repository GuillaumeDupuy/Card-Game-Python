import MySQLdb as mdb

DBNAME = "card_game"
DBHOST = "localhost"
DBPASS = ""
DBUSER = "root"


def init_db():

    try:
        db = mdb.connect(DBHOST, DBUSER, DBPASS, DBNAME)
        print("Database Connected Successfully")

        cur = db.cursor()

        # Creer la database
        # sqlquery = """
        # CREATE DATABASE card_game CHARACTER SET 'utf8';
        # """
        # cur.execute(sqlquery)
        # print("Database card_game Created Successfully")

        # Creer table Card
        # sqlquery2 = """
        # CREATE TABLE IF NOT EXISTS card (
        # Id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
        # Name CHAR(100) NOT NULL,
        # Ressource_type CHAR(10) NOT NULL,
        # Cost INT NOT NULL,
        # Effect CHAR(100) NOT NULL,
        # Value INT NOT NULL,
        # Target CHAR(100) NOT NULL,
        # Rarity CHAR(100) NOT NULL,
        # Description CHAR(255) NOT NULL
        # )
        # """
        # cur.execute(sqlquery2)
        # print("Table card Created Successfully")
        
        # inserer info dans la table
        # sqlquery3 = """
        # INSERT TO card (Name,Ressource_type, Cost, Effect, Value, Value, Rarity, Description) VALUES
        # ('Bouliste', 'PA', '2', 'Shield', '-6', 'Enemy', 'Rare', 'Détruit le bouclier de l'ennemie'),
        # ('Bébé dragon', 'PM', '4', 'Life', '-50', 'Enemy', 'Epic', 'Fait des rototos-boules de feu qui infligent des dégâts de zone depuis les airs'),
        # ('Foudre', 'PM', '2', 'Life', '-20', 'Enemy', 'Rare', 'La foudre étourdit et inflige des dégâts au combattants ennemis dans le zone cible'),
        # ('Guérisseuse armée', 'PO', '3', 'Life', '5', 'Self', 'Epic', 'Active son aura de guérisson et restaure les points de vie'),
        # ('Le vendeur', 'PO', '3', 'Shield', '5', 'Self', 'Rare', 'Le vendeur vous vends en toute illégalité du bouclier mais chut faut pas le dire'),
        # ('Sort de Soin', 'PM', '3', 'Life', '5', 'Self', 'Rare', 'Sort de soin concocté par la guérisseuse armée'),
        # ('Sort de Poison', 'PO', '2', 'Life', '-15', 'Enemy', 'Epic', 'Recouvre l'ennemi d'une toxine mortelle qui lui inflige des dégâts'),
        # ('Sapeurs', 'PA', '2', 'Life', '-25', 'Enemy', 'Epic', 'Un audacieux duo de sapeurs sans reproche, dont la plus grande passion est de faire péter l'ennemi'),
        # ('Roquette', 'PA', '5', 'Life', '-100', 'Enemy', 'Legendary', 'Inflige d'importants dégâts et avec une classe inégalée
# Ah et aussi elle one shot xD'),
        # ('Chevalier', 'PA', '1', 'Life', '-5', 'Enemy', 'Rare', 'Un spécialiste du combat rapproché'),
        # ('Boule de feu', 'PM', '1', 'Life', '-5', 'Enemy', 'Rare', 'Et bim, une boule de feu. Incinère et inflige des dégâts sur l'ennemie'),
        # ('Gel', 'PM', '1', 'Life', '-5', 'Enemy', 'Rare', 'Immobilise et inflige des dégâts à l'ennemi. QUE PERSONNE NE BOUGE !');
        # """
        # cur.execute(sqlquery3)
        # print("Informations Inserted Successfully")

        db.close()

    except mdb.Error as e:
        print("Connexion error")


def readCards():

    final_result = []

    try:
        connection = mdb.connect(DBHOST, DBUSER, DBPASS, DBNAME)

        query = "SELECT * FROM card"

        cursor = connection.cursor()
        cursor.execute(query)

        result = cursor.fetchall()

        final_result = [list(i) for i in result]
        

    except mdb.Error as e:
        print("Connexion error")

    return final_result


def createCard(input_boxes):

    try:
        connection = mdb.connect(DBHOST, DBUSER, DBPASS, DBNAME)

        cur = connection.cursor()

        sqlquery = """
        INSERT INTO card(Name, Ressource_type, Cost, Effect, Value, Target, Rarity, Description)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        card = input_boxes[0].getInput(), input_boxes[1].getInput(), input_boxes[2].getInput(), input_boxes[3].getInput(
        ), input_boxes[4].getInput(), input_boxes[5].getInput(), input_boxes[6].getInput(), input_boxes[7].getInput()

        cur.execute(sqlquery, card)
        print("Card create successfully")

        return True

    except mdb.Error as e:
        print("Error")


def editCard(input_boxes, previous_name):

    try:
        connection = mdb.connect(DBHOST, DBUSER, DBPASS, DBNAME)

        cur = connection.cursor()

        sqlquery = """
        UPDATE card SET Name = %s, Ressource_type = %s, Cost = %s, Effect = %s, Value = %s, Target = %s, Rarity =%s,
         Description = %s WHERE Name = %s """

        card = input_boxes[0].getInput(), input_boxes[1].getInput(), input_boxes[2].getInput(), \
            input_boxes[3].getInput(), input_boxes[4].getInput(), input_boxes[5].getInput(), \
            input_boxes[6].getInput(), input_boxes[7].getInput(), previous_name

        cur.execute(sqlquery, card)
        print("Card edited successfully")

        connection.commit()

        return True

    except mdb.Error as e:
        print(e)


def deleteCard(card_name):

    try:
        connection = mdb.connect(DBHOST, DBUSER, DBPASS, DBNAME)

        cur = connection.cursor()

        sqlquery = "DELETE FROM card WHERE Name = %s"

        cur.execute(sqlquery, [card_name])
        print("Card deleted successfully")

        return True

    except mdb.Error as e:
        print(e)
