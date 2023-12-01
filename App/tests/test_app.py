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
        
class CompetitionUnitTests(unittest.TestCase):
    def testA_new_competition(self):
        competition = Competition("Competition1", 1,"DCIT", "1-12-2023", 20)
        assert competition.name == "Competition1"
        assert competition.host_id == 1
        assert competition.location == "DCIT"
        assert competition.date == "1-12-2023"
        assert competition.competitionScore == 20
        
    def testB_competition_get_json(self):
        competition = Competition("Competition1", 1,"DCIT", "1-12-2023", 20)
        competition_json = competition.get_json()
        
        self.assertDictEqual(competition_json,{
           'id': None,
           'name': "Competition1",
           'host_id': 1,
           'location': "DCIT",
           'date': "1-12-2023",
           'competitionScore': 20,
           'teams': []
         })

class TeamUnitTests(unittest.TestCase):
    def testA_new_team(self):
        team = Team("Team1")
        assert team.team_name == "Team1"
        
    def testB_team_get_json(self):
        team = Team("Team1")
        team_json = team.get_json()
        
        self.assertDictEqual(team_json, {
            'team_id': None,
            'team_name':"Team1",
            'team_score': 0,
            'competitors': []     
        })

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
        
        
class CompetitionIntegrationTests(unittest.TestCase):
    def testA_new_competition(self):
        created = create_competition("Competition1", 1,"DCIT", "1-12-2023", 20)
        assert created == True
        
    def testB_competition_get_by_name(self):
        created = create_competition("Competition1", 1,"DCIT", "1-12-2023", 20)
        searched_competition = get_competition_by_name("Competition1")
        assert searched_competition.name == "Competition1"
        
    def testC_competition_remove(self):
        created = create_competition("Competition1", 1,"DCIT", "1-12-2023", 20)
        removed = remove_competition("Competition1")
        searched_competition = get_competition_by_name("Competition1")
        assert removed == True and searched_competition == None
        
    def testD_modify_compeition(self):
        created = create_competition("Competition1", 1,"CSL", "12-1-2023", 30)
        modified = modify_competition(1,"Competition2", 1,"DCIT", "1-12-2023", 20)
        search_competition = get_competition_by_name("Competition2")
        
        assert modified == True
        assert search_competition.id == 1
        assert search_competition.name == "Competition2"
        assert search_competition.host_id == 1
        assert search_competition.location == "DCIT"
        assert search_competition.date == '1-12-2023'
        assert search_competition.competitionScore == 30
        
    def testE_add_team_to_competition(self):
        createdComp = create_competition("Competition1", 1,"CSL", "12-1-2023", 30)
        createdTeam = create_team("Team1")
        added = add_team("Competition1","Team1")
        assert added == True
        
    def testF_remove_team_from_competition(self):
        createdComp = create_competition("Competition1", 1,"CSL", "12-1-2023", 30)
        createdTeam = create_team("Team1")
        added = add_team("Competition1","Team1")
        removed = remove_team("Competition1","Team1")
        assert removed == True
        
class TeamIntegrationTests(unittest.TestCase):
    def testA_new_team(self):
        created = create_team("Team2")
        assert created == True
        
    def testB_team_get_by_name(self):
        searched_team = get_team_Byname("Team1")
        assert searched_team.team_name == "Team1"
        
    def testC_remove_team(self):
        removed = delete_team("Team1")
        searched_team = get_team_Byname("Team1")
        assert removed == True and searched_team == None
        
    def testD_add_competitor_team(self):
         sally = create_competitor("Sally", "sally@mail.com", "sallypass")
         created = create_team("Team1")
         added = add_competitor_to_team(sally, "Team1")
         assert added == True
         
    def testE_remove_competitor_team(self):
         sally = get_competitor_by_username("Sally")
         searched_team = get_team_Byname("Team1")
         print(searched_team.get_json())
         print(sally)
         removed = remove_competitor_to_team(sally, "Team1")
         print(searched_team.get_json())
         assert removed == True
        
    def testF_update_team_score(self):
        createdComp = create_competition("Competition1", 1,"CSL", "12-1-2023", 30)
        addedTeam = add_team("Competition1","Team1")
        sally = get_competitor_by_username("Sally")
        addedCompetitor = add_competitor_to_team(sally, "Team1")
        addedScore = update_team_score("Competition1","Team1", 5)
        searched_team = get_team_Byname("Team1")
        assert addedScore == True and searched_team.team_score == 5

         
        
               
        

