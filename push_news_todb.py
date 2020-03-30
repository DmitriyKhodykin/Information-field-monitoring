# Module for Pushing parsed data into a local database

from common_parser import Parser
import MySQLdb  # pip install mysqlclient
import time
import auth


def push_information_field_db():
    """Push parsed data into a local db"""

    db_ifm = MySQLdb.connect(
        host=auth.host_ifm, user=auth.user_ifm,
        passwd=auth.passwd_ifm, db=auth.db_ifm, charset='utf8'
    )

    # Get cursor() method for operations with local db
    cursor = db_ifm.cursor()

    # Execute SQL-query
    for url in auth.urls:
        parser = Parser(url)
        refs = parser.get_parser_refs()
        # Def variables and their values
        for ref in refs:
            if 'ria' in url:
                entrydate = time.strftime("%Y-%m-%d")
                headers = parser.get_parser_body(ref)[:250]
                texts = parser.get_parser_body(ref)
                links = ref
            else:
                entrydate = time.strftime("%Y-%m-%d")
                headers = parser.get_parser_body(ref)[:250]
                texts = parser.get_parser_body(ref)
                links = f'{url}{ref}'
            # The values to be added to the table
            values = (entrydate, headers, texts, links)

            # The SQL-query to the db table with reference to the variables
            cursor.execute("""
                INSERT INTO 
                news (entrydate, headers, texts, links)
                VALUES 
                    (%s, %s, %s, %s)
            """, values)
            time.sleep(2)

    # Commit
    db_ifm.commit()
    db_ifm.close()


while True:
    push_information_field_db()
    time.sleep(86400)
