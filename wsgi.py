import click, pytest, sys
from flask import Flask
from datetime import datetime

from flask.cli import with_appcontext, AppGroup
from App.controllers.admin import create_admin
from App.controllers.competitor import create_competitor, get_competitor_by_username
from App.controllers.competition import create_competition, remove_competition, get_all_competitions, get_all_competitions_json, modify_competition, add_team, remove_team
from App.controllers.team import create_team, get_all_teams_json, delete_team, add_competitor_to_team, remove_competitor_to_team, update_team_score

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import (
                             get_all_competitors_json,
                             create_leaderboard,
                             populate_top20_leaderboards,
                             show_competitor_leaderboard_rankings,
                             update_rank,
                             add_competitor_overall_points,
                             get_all_competitionTeams,
                             get_all_message_inbox_json,
                             create_message,
                             get_message_inbox,
                             get_latest_message,
                             get_message_inbox_by_competitor_id,
                             delete_competitor,
                             create_host,
                             get_host_by_id,
                             get_host_by_organizationName
                             
                             
                             )



# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()
    create_admin("ricky","ricky@mail.com","rickypass")

    leaderboard = create_leaderboard(1)
    for x in range (25):
         lastperson = create_competitor("rick" + str(x) ,"rick"+ str(x) + "@mail.com","rickpass")

    add_competitor_overall_points(25, 5)
    
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands')

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("createCompetitor", help="Creates a Competitor Account")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
@click.argument("email", default="rob@mail.com")
def create_user_command(username,email, password):
    create_competitor(username,email, password)
    print(f'Competitor {username} created!')

@user_cli.command("createAdmin", help="Creates a Admin Account")
@click.argument("username", default="sally")
@click.argument("password", default="sallypass")
@click.argument("email", default="sally@mail.com")
def create_user_command(username,email, password):
    create_admin(username, email, password)
    print(f'Admin {username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        # print(get_all_users())
        print("j")
    else:
        # print(get_all_users_json())
        print("j")

app.cli.add_command(user_cli) # add the group to the cli

'''
 Test Commands
 '''

test = AppGroup('test', help='Testing commands')

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit_competitor":
        sys.exit(pytest.main(["-k", "CompetitorUnitTests"]))
    elif type == "unit_admin":
        sys.exit(pytest.main(["-k", "AdminUnitTests"]))
    elif type == "unit_leaderboard":
        sys.exit(pytest.main(["-k", "LeaderboardUnitTests"]))
    elif type == "unit_rank_listener":
        sys.exit(pytest.main(["-k", "RankListenerUnitTests"]))
    elif type == "unit_message_inbox":
        sys.exit(pytest.main(["-k", "MessageInboxUnitTests"]))
    elif type == "unit_message":
        sys.exit(pytest.main(["-k", "MessageUnitTests"]))
    elif type == "integration_competitor":
        sys.exit(pytest.main(["-k", "CompetitorIntegrationTests"]))
    elif type == "integration_admin":
        sys.exit(pytest.main(["-k", "AdminIntegrationTests"]))
    elif type == "integration_leaderboard":
        sys.exit(pytest.main(["-k", "LeaderboardIntegrationTests"]))
    elif type == "integration_rank_listener":
        sys.exit(pytest.main(["-k", "RankListenerIntegrationTests"]))
    elif type == "integration_message_inbox":
        sys.exit(pytest.main(["-k", "MessageInboxIntegrationTests"]))
    elif type == "integration_message":
        sys.exit(pytest.main(["-k", "MessageIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))


app.cli.add_command(test)


# @test.command("competition", help = 'Testing Competition commands')
# @click.argument("type", default="all")
# def competition_tests_command(type):
#     if type == "unit":
#         sys.exit(pytest.main(["-k", "CompUnitTests"]))
#     elif type == "int":
#         sys.exit(pytest.main(["-k", "CompIntegrationTests"]))
#     else:
#         print("deafult input, no test ran")




# app.cli.add_command(test)


# '''
# Competition commands
# '''

comps = AppGroup('comp', help = 'commands for competition')   
app.cli.add_command(comps)

@comps.command("add", help = 'add new competition')
@click.argument("name", default = "Coding Comp")
@click.argument("host_id", default = 1)
@click.argument("location", default = "Port of Spain")
@click.argument("date", default = "26/11/2023")
@click.argument("score", default = 10)
def add_comp(name, host_id, location, date, score):
    comp = create_competition(name, host_id, location, date, score)
    if comp:
        print("Competition Created Successfully")
    else:
        print("error adding comp")

@comps.command("remove", help = 'remove competition')
@click.argument("name", default = "Comp1")
def remove_comp(name):
    comp = remove_competition(name)
    if comp:
        print("Competition Removed Successfully")
    else:
        print("error removing comp")
        
@comps.command("update", help = 'update competition')
@click.argument("id", default = 1)
@click.argument("name", default = "Coding Comp")
@click.argument("host_id", default = 1)
@click.argument("location", default = "Port of Spain")
@click.argument("date", default = "26/11/2023")
@click.argument("score", default = 10)
def update_comp(id, name, host_id, location, date, score):
    comp = modify_competition(id, name, host_id, location, date, score)
    if comp:
        print("Competition Updated Successfully")
    else:
        print("error updating comp")
        
@comps.command("add_team",help ='adds a team to a competition')
@click.argument("compname", default ="Comp")
@click.argument("teamname", default ="Team")
def add_a_team(compname, teamname):
    team = add_team(compname, teamname)
    if team:
        print("Competition Added Team Successfully")
    else:
        print("error adding team to comp")
        
@comps.command("remove_team",help ='removes a team to a competition')
@click.argument("compname", default ="Comp")
@click.argument("teamname", default ="Team")
def remove_a_team_from_comp(compname, teamname):
    team = remove_team(compname, teamname)
    if team:
        print("Competition Removed Team Successfully")
    else:
        print("error removing team to comp")


@comps.command("get", help = "list all competitions")
def get_comps():
    print(get_all_competitions())

@comps.command("get_json", help = "list all competitions")
def get_comps():
    print(get_all_competitions_json())


# @comps.command("add_user")
# @click.argument("user_id")
# @click.argument("comp_id")
# @click.argument("rank")
# def add_to_comp(user_id, comp_id, rank):
#     add_user_to_comp(user_id, comp_id, rank)
#     print("Done!")


# @comps.command("getUserComps")
# @click.argument("user_id")
# def getUserCompetitions(user_id):
#     competitions = get_user_competitions(user_id)
#     print("these are the competitions")
#     # print(competitions)

# @comps.command("findcompuser")
# @click.argument("user_id")
# @click.argument("comp_id")
# def find_comp_user(user_id, comp_id):
#     findCompUser(user_id, comp_id)

# @comps.command("getCompUsers")
# @click.argument("comp_id")
# def get_comp_users(comp_id):
#     get_competition_users(comp_id)



# '''
# Team commands
# '''

teams = AppGroup('team', help = 'commands for competition')   

app.cli.add_command(teams)

@teams.command("add", help = 'add team')
@click.argument("name", default = "Coding Geeks")
def make_team(name):
    team = create_team(name)
    if team:
        print("Team Created Successfully")
    else:
        print("error adding team")
        
@teams.command("remove", help = 'remove team')
@click.argument("id", default = 1)
def removeT_team(id):
    team = delete_team(id)
    if team:
        print("Team Removed Successfully")
    else:
        print("error removing team")
        

@teams.command("add_team_competitor", help = 'add a team memeber to a team')
@click.argument("team_name", default = "Coding Geeks")
@click.argument("name", default = "rick")
def add_team_member(team_name, name):
    competitor = get_competitor_by_username(name)
    if competitor:
        team = add_competitor_to_team(competitor, team_name)
        if team:
            print("Team Memeber Added Successfully")
        else:
            print("error adding team memeber")
    if not competitor:
       print("Competitor not found")
       
@teams.command("remove_team_competitor", help = 'remove a team memeber to a team')
@click.argument("team_name", default = "Coding Geeks")
@click.argument("name", default = "rick")
def remove_team_member(team_name, name):
    competitor = get_competitor_by_username(name)
    if competitor:
        team = remove_competitor_to_team(competitor, team_name)
        if team:
            print("Team Memeber Removed Successfully")
        else:
            print("error removing team memeber")
    if not competitor:
       print("Competitor not found")
       
@teams.command("update_team_score", help = 'update team score')
@click.argument("competition_name", default = "Competition")
@click.argument("team_name", default = "Coding Geeks")
@click.argument("score", default = 1)
def update_team_Score(competition_name ,team_name, score):
    score = update_team_score(competition_name, team_name, score)
    if score:
        print("Team Score Updated Successfully")
    else:
        print("error updating team score")
   
        
       
        
@teams.command("get", help = 'add team')
def get_teams():
     print(get_all_teams_json())


compteams = AppGroup('compteam', help = 'commands for competition')   

app.cli.add_command(compteams)


@compteams.command("get_comp_teams", help = 'get compteam info')
def get_comp_team():
    info = get_all_competitionTeams()
    print(info)