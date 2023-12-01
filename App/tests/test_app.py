import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import  *
from App.controllers import *


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class CompetitorUnitTests(unittest.TestCase):

    def testA_new_competitor(self):
        competitor = Competitor("bob", "bob@mail.com", "bobpass")
        assert competitor.username == "bob"

    # pure function no side effects or integrations called
    def testB_competitor_get_json(self):
        competitor = Competitor("bob", "bob@mail.com", "bobpass")
        competitor = competitor.get_json()
        print(competitor)
        self.assertDictEqual(competitor, {'id': None, 'username': 'bob', 'email': 'bob@mail.com', 'overall_points': 0, 'rank': None, 'leaderboard_id': 1, 'messageInbox': None})
    
    def testC_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        competitor = Competitor("bob","bob@mail.com", password)
        assert competitor.password != password

    def testD_check_password(self):
        password = "mypass"
        competitor = Competitor("bob","bob@mail.com", password)
        assert competitor.check_password(password)

class AdminUnitTests(unittest.TestCase):

    def testA_new_admin(self):
        admin = Admin("bob2", "bob2@mail.com", "bob2pass")
        assert admin.username == "bob2"

    # pure function no side effects or integrations called
    def testB_get_json(self):
        admin = Admin("bob2", "bob2@mail.com", "bob2pass")
        admin_json = admin.get_json()
        self.assertDictEqual(admin_json, {"id":None, "username":"bob2","email": "bob2@mail.com"})
    
    def testC_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        admin = Admin("bob2","bob2@mail.com", password)
        assert admin.password != password

    def testD_check_password(self):
        password = "mypass"
        admin = Admin("bob2", "bob2@mail.com", password)
        assert admin.check_password(password)

class LeaderboardUnitTests(unittest.TestCase):
    def testA_new_leaderboard(self):
        leaderboard = Leaderboard(1)
        assert leaderboard.leaderboard_id == 1


class RankListenerUnitTests(unittest.TestCase):
    def testA_RankSwitchInTop20(self):
        rankListener = RankSwitchInTop20(1)
        assert rankListener.leaderboard_id == 1
        assert rankListener.type == "rank_switch_in_top20"

    def testB_RankDownFromTop20(self):
        rankListener = RankDownFromTop20(1)
        assert rankListener.leaderboard_id == 1
        assert rankListener.type == 'rank_down_from_top20'

    def testC_RankUpToTop20(self):
        rankListener = RankUpToTop20(1)
        assert rankListener.leaderboard_id == 1
        assert rankListener.type == 'rank_up_to_top20'

class MessageInboxUnitTests(unittest.TestCase):
    def testA_new_messageInbox(self):
        message_inbox = MessageInbox(4)
        assert message_inbox.competitor_id == 4

class MessageUnitTests(unittest.TestCase):
    def testA_new_message(self):
        message = Message(4, "This is a test")
        assert message.message_inbox_id == 4
        assert message.content == "This is a test"



'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate_competitor():
    competition = create_competitor("sarah", "sarah@mail.com", "sarahpass")
    assert login("sarah","sarahpass") != None

def test_authenticate_admin():
    
    admin = create_admin("sarah2", "sarah2@mail.com", "sarah2pass")
    assert login("sarah2","sarah2pass",True) != None

class CompetitorIntegrationTests(unittest.TestCase):
    def testA_new_competitor(self):
        competitor = create_competitor("rob","rob@mail.com","robpass")
        assert competitor.username == "rob"

    # pure function no side effects or integrations called
    def testB_competitor_get_json(self):
        competitor = get_competitor_json(2)
        self.assertDictEqual(competitor, {'id': 2, 'username': 'rob', 'email': 'rob@mail.com', 'overall_points': 0, 'rank': 2, 'leaderboard_id': 1, 'messageInbox': {'id': 2, 'competitor_id': 2, 'messages': []}})
    
    def testC_update_competitor(self):
        original_competitor = get_competitor(1)

        # Check that the initial username is not "pikachu"
        self.assertNotEqual(original_competitor.username, "pikachu")
        
        # Update the competitor's information
        updated_competitor = update_competitor(1, "pikachu", "sarah@mail.com", "sarahpass")
        
        # Check that the updated username is "pikachu"
        self.assertEqual(updated_competitor.username, "pikachu")

    def testD_delete_competitor(self):
        competitor = create_competitor("test", "test@mail.com", "testpass")
        competitor = delete_competitor(competitor.id)
        self.assertEqual(competitor,True)

    def testE_add_competitor_points(self):
        competitor = add_competitor_overall_points(1,5)
        self.assertEqual(competitor.overall_points, 5)
    
    def testF_remove_competitor_points(self):
        competitor = remove_competitor_overall_points(1,2)
        self.assertEqual(competitor.overall_points, 3)

class AdminIntegrationTests(unittest.TestCase):
    def testA_new_admin(self):
        admin = create_admin("adi","adi@mail.com","adipass")
        assert admin.username == "adi"

    # pure function no side effects or integrations called
    def testB_admin_get_json(self):
        admin = get_admin_json(2)
        self.assertDictEqual(admin, {'id': 2, 'username': 'adi', 'email': 'adi@mail.com'})
    
    def testC_admin_competitor(self):
        original_admin = get_admin(1)
        # Check that the initial username is not "pikachu"
        self.assertNotEqual(original_admin.username, "raichu")
        
        # Update the competitor's information
        updated_competitor = update_competitor(1, "raichu", "sarah2@mail.com", "sarah2pass")
        
        # Check that the updated username is "pikachu"
        self.assertEqual(updated_competitor.username, "raichu")


class LeaderboardIntegrationTests(unittest.TestCase):
    def testA_new_leaderboard(self):
        leaderboard = create_leaderboard(1)
        assert leaderboard.leaderboard_id == 1


class RankListenerIntegrationTests(unittest.TestCase):
    def testA_RankSwitchInTop20(self):
        rankListener = create_switchListener(1)
        assert rankListener.id == 4
        assert rankListener.leaderboard_id == 1
        assert rankListener.type == "rank_switch_in_top20"

    def testB_RankDownFromTop20(self):
        rankListener = create_rankDownListener(1)
        assert rankListener.id == 5
        assert rankListener.leaderboard_id == 1
        assert rankListener.type == 'rank_down_from_top20'

    def testC_RankUpToTop20(self):
        rankListener = create_rankUpListener(1)
        assert rankListener.id == 6
        assert rankListener.leaderboard_id == 1
        assert rankListener.type == 'rank_up_to_top20'

class MessageInboxIntegrationTests(unittest.TestCase):
    def testA_new_messageInbox(self):
        message_inbox = create_message_Inbox(4)
        assert message_inbox.competitor_id == 4

class MessageIntegrationTests(unittest.TestCase):
    def testA_new_message(self):
        message = create_message(4, "This is a test")
        assert message.message_inbox_id == 4
        assert message.content == "This is a test"

