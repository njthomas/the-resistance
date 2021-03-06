#! python3
import random

class Player:
    name = ""
    role = "rebel" # 'spy' or 'rebel' 
    teamVote = None # true = accept, false = reject
    missionVote = 0
    
    def __init__(self, name):
        self.name = name

    def mission_vote(self, vote):
        if self.role == 'rebel':
            self.missionVote = 0 #mission votes will be added and if >x fails(x=#of fails req.)
        elif self.role == 'spy':
            self.missionVote = vote

class Session:

    players = []
    
    def addPlayer(self, name):
        return Player(name)

    def addPlayerS(self, names): #optional way to make multiple players quickly
        players = []
        for name in names:
            players.append(Player(name))
        self.players = players
        return players

class Mission:
    playersM = [] # playersM represents only players currently in mission
    num_playing = 0
    fails_req = 0
    outcome = None # succeeded = True, failed = False
    team_leader = ''

    def __init__(self, playersM, fails_req, team_leader):
        self.playersM = playersM
        self.fails_req = fails_req
        self.team_leader = team_leader
        self.outcome = self.determineOutcome()

    def determineOutcome(self):
        fails = 0
        for player in self.playersM:
            fails += player.missionVote
        if fails >= self.fails_req:
            return False
        else:
            return True

class Board:
    num_players = 0
    num_spies = 0
    players = []
    curr_mission = 0 #using index-numbers for mission number
    mission_info = [] #[]false=spys won round, true=resistance won round
    mission_list = [] # use this or/and mission_info
    team_leader = 0
    
    def __init__(self, players):
        self.players = players
        self.num_players = len(players)
        self.num_spies = self.setSpies(players)
        self.team_leader = random.randint(1,len(self.players)-1) #range?
        print(players[self.team_leader].name)
        
    def setSpies(self, players):
        nsp = {5:2, 6:2, 7:3, 8:3, 9:3, 10:4}
        rands = random.sample(range(0, len(self.players)), nsp[self.num_players])
        for rand in rands:
            self.players[rand].role = 'spy'
        return len(rands)
        
    def changeLeader(self):
        self.team_leader -= 1
        return self.team_leader

    def countTeamVotes(self):
        positive = 0
        negetive = 0
        for player in self.players:
            if player.teamVote == True:
                positive += 1
            elif player.teamVote == False:
                negetive += 1
        if positive > negetive:
            print("vote passes!")
            return True
        elif negetive > positive:
            print("vote rejected!")
            return False
        elif positive == negetive:
            print("vote tie!")
            return None

    def goOnMission(self, playersM, fails_req):
        self.mission_list.append(Mission(playersM, fails_req, players[self.team_leader].name))
        return self.mission_list[-1].outcome
       


#The following is an example of how the objects would be used
s = Session()
#reminder not to allow under 5
s.addPlayerS(['person1', 'person2', 'person3','person4', 'person5', 'person6'])
b = Board(s.players)

for player in b.players:
	print(player.name + "  " + player.role)

players = b.players

team = [players[0], players[1], players[2]]

for player in players:  #vote here
    player.teamVote = True # simulating voting
b.players = players



if b.countTeamVotes() == True:
    for player in team:
        player.mission_vote(1)
    print(b.goOnMission(team, 1))
    b.curr_mission += 1
elif b.countTeamVotes() == False:
    b.changeLeader()
    print("team vote failed")

for player in team:
    print(player.missionVote)

