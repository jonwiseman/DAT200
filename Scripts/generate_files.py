import pandas as pd
import json
import pickle
import numpy as np
from random import sample
from random import shuffle


def main():
    with open(r'../Data/Datasets/profiles.json', 'r') as f:
        data = json.load(f)

    cleaned_data = []
    for entry in data:
        cleaned_data.append({'playerID': entry['player_id'], 'name': entry['name'].strip(' '),
                             'position': entry['position'].split('-')[0],
                             'team': entry['current_team']})

    profile = pd.DataFrame(cleaned_data)
    profile.set_index('playerID', inplace=True)

    with open(r'../Data/Datasets/games.json', 'r') as f:
        games = json.load(f)

    gameframe = pd.DataFrame(games)
    gameframe = gameframe[gameframe['year'] == '2016']  # Limit to 2016 year

    offense = gameframe[['player_id', 'game_number', 'passing_yards', 'rushing_yards', 'receiving_yards',
                         'passing_touchdowns', 'receiving_touchdowns', 'rushing_touchdowns', 'passing_interceptions']]

    offense = offense.rename(
        columns={'player_id': 'playerID', 'game_number': 'gameNumber', 'passing_yards': 'passYards',
                 'rushing_yards': 'rushYards', 'receiving_yards': 'recYards',
                 'passing_interceptions': 'interceptions'})

    offense['touchdowns'] = offense['passing_touchdowns'] + offense['receiving_touchdowns'] + offense[
        'rushing_touchdowns']
    offense.drop(['passing_touchdowns', 'receiving_touchdowns', 'rushing_touchdowns'], axis=1, inplace=True)
    offense['gameNumber'] = offense['gameNumber'].astype(int)
    offense = offense[offense['gameNumber'] < 17]

    offensive_profiles = profile[(profile['position'] == 'QB') |
                                 (profile['position'] == 'WR') |
                                 (profile['position'] == 'RB') |
                                 (profile['position'] == 'TE')]

    offense = pd.merge(offense, offensive_profiles, how='inner', on='playerID')
    offense.dropna(axis=0, inplace=True)
    offense.drop(['playerID', 'team'], axis=1, inplace=True)

    offense = offense.rename(columns={'name': 'playerID'})

    with open(r'../Data/Pickles/offense.pickle', 'wb') as f:
        pickle.dump(offense, f)

    defense = gameframe[
        ['player_id', 'game_number', 'defense_sacks', 'defense_interceptions', 'defense_interception_touchdowns',
         'defense_safeties', 'punting_blocked']]

    defense = defense.rename(
        columns={'player_id': 'playerID', 'game_number': 'gameNumber', 'defense_interceptions': 'interceptions',
                 'defense_interception_touchdowns': 'touchdowns', 'defense_safeties': 'safeties',
                 'punting_blocked': 'blocks', 'defense_sacks': 'sacks'})

    defense['gameNumber'] = defense['gameNumber'].astype(int)
    defense = defense[defense['gameNumber'] < 17]

    defense_profiles = profile[(profile['position'] != 'QB') &
                               (profile['position'] != 'WR') &
                               (profile['position'] != 'RB') &
                               (profile['position'] != 'TE')]

    defense = pd.merge(defense, defense_profiles, how='inner', on='playerID')
    defense.dropna(axis=0, inplace=True)
    defense = defense.groupby(['team', 'gameNumber'], as_index=False)[
        ['sacks', 'interceptions', 'touchdowns', 'safeties', 'blocks']].sum()
    defense = defense.rename(columns={'team': 'playerID'})

    with open(r'../Data/Pickles/defense.pickle', 'wb') as f:
        pickle.dump(defense, f)

    defense.to_csv(r'../Data/CSV/defense.csv', header=False, index=False)
    offense.to_csv(r'../Data/CSV/offense.csv', header=False, index=False)

    names = pd.read_csv(r'../Data/Datasets/names.csv')
    names = names[['FirstName', 'Surname']]
    fnames = list(np.unique(names['FirstName'].to_numpy()))
    lnames = list(np.unique(names['Surname'].to_numpy()))
    sample_fnames = sample(fnames, 5)
    sample_lnames = sample(lnames, 4)

    generated_names = []
    for f in sample_fnames:
        for l in sample_lnames:
            generated_names.append(f + ' ' + l)

    shuffle(generated_names)
    league1 = generated_names[:10]
    league2 = generated_names[10:]
    league = pd.DataFrame([[1, 'family'], [2, 'competitive']], columns=['leagueID', 'leagueType'])
    league.set_index('leagueID')

    league.to_csv(r'../Data/CSV/leagues.csv', header=False, index=False)

    l1_qbs = sample(list(offense[offense['position'] == 'QB']['playerID'].unique()), len(league1))
    l1_rbs = sample(list(offense[offense['position'] == 'RB']['playerID'].unique()), 2 * len(league1))
    l1_wrs = sample(list(offense[offense['position'] == 'WR']['playerID'].unique()), 2 * len(league1))
    l1_defense = sample(list(defense['playerID'].unique()), len(league1))

    l2_qbs = sample(list(offense[offense['position'] == 'QB']['playerID'].unique()), len(league2))
    l2_rbs = sample(list(offense[offense['position'] == 'RB']['playerID'].unique()), 2 * len(league2))
    l2_wrs = sample(list(offense[offense['position'] == 'WR']['playerID'].unique()), 2 * len(league2))
    l2_defense = sample(list(defense['playerID'].unique()), len(league2))

    contract = pd.DataFrame(l1_qbs + l1_rbs + l1_wrs + l1_defense + l2_qbs + l2_rbs + l2_wrs + l2_defense,
                            columns=['playerID'])
    contract['owner'] = league1 + 2 * league1 + 2 * league1 + league1 + league2 + 2 * league2 + 2 * league2 + league2
    contract['startWeek'] = 1
    contract['endWeek'] = 16
    contract['isActive'] = 1
    contract['owner'] = contract['owner'].apply(name_to_id)

    user = pd.DataFrame(
        [(name.split(' ')[0], name.split(' ')[1], name.split(' ')[1].lower() + name.split(' ')[0].lower()[:3])
         for name in generated_names],
        columns=['nameFirst', 'nameLast', 'userID'])
    user.to_csv(r'../Data/CSV/users.csv', index=False, header=False)

    leagues1 = {name: 1 for name in league1}
    leagues2 = {name: 2 for name in league2}

    leagues1.update(leagues2)
    teams = pd.DataFrame([(f'Team{number}', name.split(' ')[1].lower() + name.split(' ')[0].lower()[:3], leagues1[name])
                          for number, name in enumerate(generated_names)],
                         columns=['teamID', 'userID', 'leagueID'])
    teams.to_csv(r'../Data/CSV/team.csv', index=False, header=False)

    real_contracts = pd.merge(contract, teams.rename({'userID': 'owner'}, axis=1), on='owner').drop(['owner', 'leagueID'], axis=1)
    real_contracts.to_csv(r'../Data/CSV/contracts.csv', index=False, header=False)


def name_to_id(name):
    return name.split(' ')[1].lower()+name.split(' ')[0].lower()[:3]


if __name__ == '__main__':
    main()
