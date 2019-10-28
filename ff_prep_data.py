import json
import pandas as pd

#TODO: update this auto get max

PRO_TEAM_MAP = {
    0 : 'None',
    1 : 'ATL',
    2 : 'BUF',
    3 : 'CHI',
    4 : 'CIN',
    5 : 'CLE',
    6 : 'DAL',
    7 : 'DEN',
    8 : 'DET',
    9 : 'GB',
    10: 'TEN',
    11: 'IND',
    12: 'KC',
    13: 'OAK',
    14: 'LAR',
    15: 'MIA',
    16: 'MIN',
    17: 'NE',
    18: 'NO',
    19: 'NYG',
    20: 'NYJ',
    21: 'PHI',
    22: 'ARI',
    23: 'PIT',
    24: 'LAC',
    25: 'SF',
    26: 'SEA',
    27: 'TB',
    28: 'WSH',
    29: 'CAR',
    30: 'JAX',
    33: 'BAL',
    34: 'HOU'
}

POSITION_MAP = {
    0: 'QB',
    1: 'TQB',
    2: 'RB',
    3: 'RB/WR',
    4: 'WR',
    5: 'WR/TE',
    6: 'TE',
    7: 'OP',
    8: 'DT',
    9: 'DE',
    10: 'LB',
    11: 'DL',
    12: 'CB',
    13: 'S',
    14: 'DB',
    15: 'DP',
    16: 'D/ST',
    17: 'K',
    18: 'P',
    19: 'HC',
    20: 'BE',
    21: 'IR',
    22: '',
    23: 'RB/WR/TE',
    24: 'ER',
    25: 'Rookie',
    'QB': 0,
    'RB': 2,
    'WR': 4,
    'TE': 6,
    'D/ST': 16,
    'K': 17,
    'FLEX': 23
}

def create_roster(max_period):
    list_roster = []
    max_period = max_period

    #iterate through each .json and populate the roster in memory.
    for period in range(1, max_period+1):    
        with open('./ff_data/ff_view_mMatchup_'+str(period)+'.json') as f:
            data_matchups = json.load(f)

        scoring_period_id = data_matchups['scoringPeriodId']
        matchup_teams = data_matchups['teams']

        for mteam in matchup_teams:

            roster_team_id = mteam['id']
            roster_entries = mteam['roster']['entries']
            
            for entry in roster_entries:
                
                roster_lineup_slot_id = entry['lineupSlotId']
                roster_entry_id = entry['playerPoolEntry']['id']
                roster_player_id = entry['playerId']
                player_injury_status = entry['injuryStatus']
                roster_on_team_id = entry['playerPoolEntry']['onTeamId']
                player_score = entry['playerPoolEntry']['appliedStatTotal']

                list_roster.append({'scoring_period_id':scoring_period_id,
                                    'team_id':roster_team_id,
                                    'roster_lineup_slot_id':roster_lineup_slot_id,
                                    'roster_entry_id':roster_entry_id,
                                    'player_id':roster_player_id,
                                    'roster_on_team_id':roster_on_team_id,
                                    'player_injury_status':player_injury_status,
                                    'player_score':player_score})

    df_roster = pd.DataFrame(list_roster)
    df_roster.to_pickle('./ff_data/roster.pkl')
    print('pickled data to ./ff_data/roster.pkl')

    return df_roster

def create_scoreboard(max_period):
    #the scoreboard is updated each week with a new row appended. we can treat this as a type-1 update where we keep the most recent scores
    df_schedule = []

    with open('./ff_data/ff_view_mMatchup_'+str(max_period)+'.json') as f:
            data_matchups = json.load(f)
        
    matchup_schedule = data_matchups['schedule']

    for sch in matchup_schedule :
        winner = sch['winner'] #HOME/AWAY/!UNDECIDED / TODO:ties??
        if winner == 'UNDECIDED':
            next
        else:
                game_id = sch['id']
                matchup_period_id = sch['matchupPeriodId']
                
                away = sch['away']
                away_team_id = away['teamId']
                away_total_score = away['totalPoints']
                
                home = sch['home']
                home_team_id = home['teamId']
                home_total_score = home['totalPoints']
                
                df_schedule.append({'game_id':game_id, 
                                    'winner':winner,
                                    'matchup_period_id':matchup_period_id, 
                                    'away_team_id':away_team_id, 
                                    'away_total_score':away_total_score,
                                    'home_team_id':home_team_id,
                                    'home_total_score':home_total_score
                                })
    df_schedule = pd.DataFrame(df_schedule)
    df_schedule.to_pickle('./ff_data/schedule.pkl')
    print('pickled data to ./ff_data/schedule.pkl')
    return pd.DataFrame(df_schedule)


def map_players(max_period):
    df_players = []

    for period in range(1, max_period+1):

        with open('./ff_data/ff_view_players_wl_'+str(period)+'.json') as f:
            data_players = json.load(f)

        for player in data_players['players']:

            p = player['player'] #playa playa      
            scoring_period_id = period      
            player_id = p['id']
            player_default_position_id = p['defaultPositionId']
            player_eligible_slots = p['eligibleSlots']
            player_first_name = p['firstName']
            player_last_name = p['lastName']
            player_full_name = p['fullName']
            player_proteam_id = p['proTeamId']
            
            df_players.append({'scoring_period_id':scoring_period_id, 
                                'player_id':player_id,
                                'player_default_position_id':player_default_position_id,
                                'player_eligible_slots':player_eligible_slots,
                                'player_first_name':player_first_name,
                                'player_last_name':player_last_name,
                                'player_full_name':player_full_name,
                                'player_proteam_id':player_proteam_id})

    df_players = pd.DataFrame(df_players)
    df_players.replace({'player_proteam_id': PRO_TEAM_MAP})
    
    return df_players
        
def teams(maxPeriod):
    df_teams = []
    max_period = maxPeriod
    for period in range(1, max_period+1):
        with open('./ff_data/ff_view_mTeam_'+str(period)+'.json') as f:
            data_teams = json.load(f)

        scoring_period_id = period
        for team in data_teams['teams']:
            team_abbrev = team['abbrev']
            team_cur_proj_rank = team['currentProjectedRank']
            team_draft_proj_rank = team['draftDayProjectedRank']
            team_div_id = team['divisionId']
            team_points = team['points']
            team_points_adj = team['pointsAdjusted'] #val of adjustment points: e.g. 0 is no adjustment

            df_teams.append({'scoring_period_id':scoring_period_id, 
                            'team_abbrev':team_abbrev,
                            'team_cur_proj_rank':team_cur_proj_rank,
                            'team_draft_proj_rank':team_draft_proj_rank,
                            'team_div_id':team_div_id,
                            'team_points':team_points,
                            'team_points_adj':team_points_adj})
    df_teams = pd.DataFrame(df_teams)
    return df_teams

if __name__ == '__main__':
    max_period = 8
    roster = create_roster(max_period)
    scoreboard = create_scoreboard(max_period)
    players = map_players(max_period)
    teams = teams(max_period)

    full_roster = pd.merge(roster, players, how='left', on=['scoring_period_id', 'player_id'])

    print(full_roster)
    print(scoreboard)