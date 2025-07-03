import os
os.environ['DATABASE_URL'] = 'sqlite://'

from datetime import datetime, timezone, timedelta
import unittest
from app import app, db
from app.models import User, Post


class UserModelCase(unittest.TestCase):
    def setUp(self):
        """Initialise la base de données du test.

        Cette méthode est appelée avant chaque test et 
        crée une base de données SQLite vide en mémoire. 
        La base de données est supprimée après chaque test."""
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Nettoie la base de données apres chaque test.

        Cette methode est appellee apres chaque test et supprime 
        toutes les donnees de la base de données.
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        """Test la fonction de hachage du mot de passe.

        Cette fonction s'assure que le mechanisme de hachage du mot de passe est correct
        et que celui ci fonctionne correctement. Il verifie que le hachage du mot de passe
        correct renvoie True et que celui du mot de passe incorrect renvoie False.
        """
        # Creation d'un utilisateur
        u = User(username='susan', email='susan@example.com')
        u.set_password('cat')

        # Verification du hachage du mot de passe avec un mot de passe correct et un autre incorrect
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))


    def test_avatar(self):
        """Test la fonction d'avatar.

        Cette fonction verifie que la methode User.avatar() 
        renvoie l'URL de l'avatar correspondant au mail de l'utilisateur.
        L'URL est formee en utilisant l'adresse email de l'utilisateur
        et en ajoutant le parametre 's' egal a la taille de l'avatar
        souhaitee. Le parametre 'd' est egal a 'identicon' pour que le service
        Gravatar renvoie une image par defaut si l'utilisateur n'a pas
        d'avatar.
        """
        # Creation d'un utilisateur
        u = User(username='john', email='john@example.com')
        u.set_password('cat')

        # Verification de si l'URL de l'avatar correspond a l'URL attendue
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))


    def test_follow(self):
        """
        Test la fonctionalité de suivi (follow) et de ne plus suivre (unfollow).

        Ce test verifie que l'utilisateur peut suivre et ne plus suivre un autre utilisateur.
        Il s'assure que les listes de suiveurs et de suivis sont mises a jour correctement,
        ainsi que que les comptes de suiveurs et de suivis sont correctement mis a jour.
        Apres avoir suivi et non plus suivre (unfollow) un utilisateur, le test verifie que les listes
        et les comptes sont correctement mis a jour.
        """
        # Creation de deux utilisateurs
        u1 = User(username='john', email='john@example.com')
        u1.set_password('123456')
        u2 = User(username='susan', email='susanf@example.com')
        u2.set_password('123456')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        # Verification initiale de si les champs suiveurs (followers) et suivis (following) sont vides
        following = u1.following.all()
        followers = u2.followers.all()
        self.assertEqual(following, [])
        self.assertEqual(followers, [])

        # ----- Verification de si l'utilisateur 1 peut suivre un autre utilisateur et si les comptes sont correctement mis a jour -----

        u1.follow(u2)
        db.session.commit()
        # Verifier si l'utilisateur 1 suit l'utilisateur 2, 
        # si le compte de suiveur (followers) de l'utilisateur 1 est correct et 
        # si le compte de suivis (following) de l'utilisateur 2 est correct
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.following_count(), 1)
        self.assertEqual(u2.followers_count(), 1)

        # Verification de si les noms des utilisateurs suiveurs (followers) et suivis (following) sont corrects
        u1_following = u1.following.all()
        u2_followers = u2.followers.all()
        self.assertEqual(u1_following[0].username, 'susan')
        self.assertEqual(u2_followers[0].username, 'john')

        # ----- Verification de si l'utilisateur 1 peut ne plus suivre un autre utilisateur et si les comptes sont correctement mis a jour -----
        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.following_count(), 0)
        self.assertEqual(u2.followers_count(), 0)

    def test_follow_posts(self):
        """
        Test la fonctionalité d'affichage des posts
        des utilisateurs(following) que l'utilisateur suivi (following_users_posts).

        Ce test verifie que l'utilisateur peut voir les posts des utilisateurs qu'il suit.
        Il cree quatre utilisateurs, quatre posts et installe les relations de suivi.
        Ensuite, il verifie que chaque utilisateur voit les posts des utilisateurs qu'il suit.
        """

        u1 = User(username='john', email='johnf@example.com')
        u2 = User(username='susan', email='susanfp@example.com')
        u3 = User(username='mary', email='mary@example.com')
        u4 = User(username='david', email='david@example.com')
        u1.set_password('123456')
        u2.set_password('123456')
        u3.set_password('123456')
        u4.set_password('123456')
        db.session.add_all([u1, u2, u3, u4])

        # create four posts
        now = datetime.now(timezone.utc)
        p1 = Post(body="post from john", author=u1,
                  timestamp=now + timedelta(seconds=1))
        p2 = Post(body="post from susan", author=u2,
                  timestamp=now + timedelta(seconds=4))
        p3 = Post(body="post from mary", author=u3,
                  timestamp=now + timedelta(seconds=3))
        p4 = Post(body="post from david", author=u4,
                  timestamp=now + timedelta(seconds=2))
        
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # setup the followers
        u1.follow(u2)  # john follows susan
        u1.follow(u4)  # john follows david
        u2.follow(u3)  # susan follows mary
        u3.follow(u4)  # mary follows david
        db.session.commit()

        # check the following posts of each user
        f1 = u1.following_users_post().all()
        f2 = u2.following_users_post().all()
        f3 = u3.following_users_post().all()
        f4 = u4.following_users_post().all()

        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])


if __name__ == '__main__':
    unittest.main(verbosity=2)