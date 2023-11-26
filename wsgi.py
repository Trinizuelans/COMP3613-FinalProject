import click, pytest, sys
from flask import Flask
from datetime import datetime

from flask.cli import with_appcontext, AppGroup
from App.controllers.admin import create_admin
from App.controllers.competitor import create_competitor
from App.controllers.competition import create_competition, remove_competition, get_all_competitions, get_all_competitions_json, modify_competition

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import (
                             get_all_competitors_json
                             )



# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()
    create_competitor("rick","rick@mail.com","rickpass")
    create_admin("rick","rick@mail.com","rickpass")
    print(get_all_competitors_json())
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

# test = AppGroup('test', help='Testing commands') 

# @test.command("user", help="Run User tests")
# @click.argument("type", default="all")
# def user_tests_command(type):
#     if type == "unit":
#         sys.exit(pytest.main(["-k", "UserUnitTests"]))
#     elif type == "int":
#         sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
#     else:
#         sys.exit(pytest.main(["-k", "App"]))





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
@click.argument("id", default = 1)
def remove_comp(id):
    comp = remove_competition(id)
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




app.cli.add_command(comps)