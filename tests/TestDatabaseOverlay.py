import unittest

from dbmysql.dbmysql.mysqldb import DatabaseOverlay



class TestDatabaseOverlay(unittest.TestCase):
    def setUp(self):
        # Mettez en place votre objet DatabaseOverlay pour les tests
        self.db = DatabaseOverlay()

    def tearDown(self):
        # Fermez la connexion après les tests
        self.db.close()

    def test_connection(self):
        # Testez la connexion à la base de données
        state, con = self.db.get_connect()
        self.assertTrue(state)
        self.assertIsNotNone(con)


    # Ajoutez d'autres méthodes de test selon vos besoins

if __name__ == '__main__':
    unittest.main()
