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

        # Creer table Card
        sqlquery = """
        CREATE TABLE IF NOT EXISTS card (
        Id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
        Name CHAR(100) NOT NULL,
        Ressource_type CHAR(10) NOT NULL,
        Cost INT NOT NULL,
        Effect CHAR(100) NOT NULL,
        Value INT NOT NULL,
        Target CHAR(100) NOT NULL,
        Rarity CHAR(100) NOT NULL,
        Description CHAR(255) NOT NULL
        )
        """
        cur.execute(sqlquery)
        print("Table card Created Successfully")


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
