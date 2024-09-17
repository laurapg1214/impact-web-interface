import owb_module_base.owb_module.database as db


def main():
    # connect to owb database
    connection = db.create_db_connection(
        "localhost", 
        "laurapg1214", 
        "0bjectDataba$3",
        "owb"
    )

    # create tables
    create_participants_table = """
    CREATE TABLE participants (
        id INT NOT NULL AUTO_INCREMENT,
        username VARCHAR(40) NOT NULL,
        age INT,
        gender ENUM('Female','Male','Nonbinary','Other','Prefer not to say'),
        PRIMARY KEY (id)
        );
    """

    create_questions_table = """
    CREATE TABLE questions (
        id INT NOT NULL AUTO_INCREMENT,
        question1 VARCHAR(255) NOT NULL,
        question2 VARCHAR(255),
        question3 VARCHAR(255),
        PRIMARY KEY (id)
        );
    """

    create_responses_table = """
    CREATE TABLE responses (
        id INT NOT NULL AUTO_INCREMENT,
        question_id INT NOT NULL,
        participant_id INT NOT NULL,
        response1 VARCHAR(255),
        response2 VARCHAR(255),
        response3 VARCHAR(255),
        PRIMARY KEY (id),
        FOREIGN KEY (question_id) REFERENCES questions(id),
        FOREIGN KEY (participant_id) REFERENCES participants(id)
        );
    """

    db.execute_query(connection, create_participants_table)
    db.execute_query(connection, create_questions_table)
    db.execute_query(connection, create_responses_table)


if __name__ == "__main__":
    main()