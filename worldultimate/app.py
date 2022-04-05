from os import environ
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, or_, and_
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Mgoblue2'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL') or 'sqlite:///ratingsdb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Games(db.Model):
    event = db.Column(db.String(120), index=True)
    division = db.Column(db.String(20), index=True)
    game_id = db.Column(db.Integer, primary_key=True)
    team_1 = db.Column(db.String(80), index=True)
    team_1_score = db.Column(db.Integer, index=True)
    team_2 = db.Column(db.String(80), index=True)
    team_2_score = db.Column(db.Integer, index=True)
    game_date = db.Column(db.Date, index=True)
    gender = db.Column(db.String(20), index=True)
    postseason = db.Column(db.Integer, index=True)
    season = db.Column(db.Integer, index=True)
    winner = db.Column(db.String(80), index=True)
    loser = db.Column(db.String(80), index=True)
    win_score = db.Column(db.Integer, index=True)
    lose_score = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '{} in {}'.format(self.game_id, self.season)

class ClubTeams(db.Model):
    team = db.Column(db.String(80), index=True)
    gender = db.Column(db.String(20), index=True)
    division = db.Column(db.String(20), index=True)
    city = db.Column(db.String(50), index=True)
    state = db.Column(db.String(50), index=True)
    region = db.Column(db.String(50), index=True)
    section = db.Column(db.String(50), index=True)
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '{} {} team: {}'.format(self.division, self.gender, self.id)

class CollegeTeams(db.Model):
    team = db.Column(db.String(80), index=True)
    team_name = db.Column(db.String(120), index=True)
    division = db.Column(db.String(20), index=True)
    gender = db.Column(db.String(20), index=True)
    competition = db.Column(db.String(50), index=True)
    region = db.Column(db.String(50), index=True)
    conference = db.Column(db.String(50), index=True)
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '{} {} team: {}'.format(self.division, self.gender, self.id)

class Ratings(db.Model):
    date = db.Column(db.String(20), index=True)
    rank = db.Column(db.Integer, index=True)
    team = db.Column(db.String(80), index=True)
    rating = db.Column(db.Float, index=True)
    perc_ratings = db.Column(db.Float, index=True)
    wins = db.Column(db.Integer, index=True)
    losses = db.Column(db.Integer, index=True)
    w_pct = db.Column(db.Float, index=True)
    sos = db.Column(db.Float, index=True)
    sos_rank = db.Column(db.Integer, index=True)
    division = db.Column(db.String(20), index=True)
    gender = db.Column(db.String(20), index=True)
    season = db.Column(db.Integer, index=True)
    is_final = db.Column(db.Boolean, index=True)
    key = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '{} {} rating of: {}'.format(self.team, self.season, self.rating)

class Tournaments(db.Model):
    event = db.Column(db.String(120), index=True)
    division = db.Column(db.String(20), index=True)
    season = db.Column(db.Integer, index=True)
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '{} {}'.format(self.event, self.season)

class Blogs(db.Model):
    content = db.Column(db.Text, index=True)
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), index=True)

    def __repr__(self):
        return 'Blog post {}'.format(self.id)

@app.template_filter('formatdatetime')
def format_datetime(value, format="%b %d"):
    #datetime.strptime(value, '%Y-%m-%d').strftime(format)
    if value is None:
        return ""
    return datetime.strptime(value, '%Y-%m-%d').strftime(format)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blog')
def blog():
    return render_template('ratingsBlog.html')

@app.route('/blog/1')
def introBlog():
    return render_template('introBlog.html')

@app.route('/blog/2')
def ratingsBlog():
    return render_template('ratingsBlog.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/club-men')
def clubMen():
    ratings = Ratings.query.filter_by(division='Club', gender='Men', season=2019).order_by('rank')
    seasons = [r.season for r in Ratings.query.filter_by(division='Club').values(Ratings.season)]
    seasons = list(set(seasons))
    seasons = sorted(seasons)
    return render_template('clubMen.html', ratings=ratings, year=2019, seasons=seasons)

@app.route('/club-men/<int:year>')
def clubMenRatings(year):
    ratings = Ratings.query.filter_by(division='Club', gender='Men', season=year).order_by('rank')
    seasons = [r.season for r in Ratings.query.filter_by(division='Club').values(Ratings.season)]
    seasons = list(set(seasons))
    seasons = sorted(seasons)
    return render_template('clubMen.html', ratings=ratings, seasons=seasons, year=year)

@app.route('/club-men/<int:year>/<category>')
def clubMenRatingsSorted(year, category):
    if (category == 'rank') | (category == 'sos_rank') | (category == 'team'):
        ratings = Ratings.query.filter_by(division='Club', gender='Men', season=year).order_by(category)
    else:
        ratings = Ratings.query.filter_by(division='Club', gender='Men', season=year).order_by(desc(category))

    seasons = [r.season for r in Ratings.query.filter_by(division='Club').values(Ratings.season)]
    seasons = list(set(seasons))
    seasons = sorted(seasons)
    return render_template('clubMen.html', ratings=ratings, seasons=seasons, year=year)

@app.route('/club-mixed')
def clubMixed():
    ratings = Ratings.query.filter_by(division='Club', gender='Mixed', season=2019).order_by('rank')
    seasons = [r.season for r in Ratings.query.filter_by(division='Club').values(Ratings.season)]
    seasons = list(set(seasons))
    seasons = sorted(seasons)
    return render_template('clubMixed.html', ratings=ratings, year=2019, seasons=seasons)

@app.route('/club-mixed/<int:year>')
def clubMixedRatings(year):
    ratings = Ratings.query.filter_by(division='Club', gender='Mixed', season=year).order_by('rank')
    seasons = [r.season for r in Ratings.query.filter_by(division='Club').values(Ratings.season)]
    seasons = list(set(seasons))
    seasons = sorted(seasons)
    return render_template('clubMixed.html', ratings=ratings, seasons=seasons, year=year)

@app.route('/club-mixed/<int:year>/<category>')
def clubMixedRatingsSorted(year, category):
    if (category == 'rank') | (category == 'sos_rank') | (category == 'team'):
        ratings = Ratings.query.filter_by(division='Club', gender='Mixed', season=year).order_by(category)
    else:
        ratings = Ratings.query.filter_by(division='Club', gender='Mixed', season=year).order_by(desc(category))

    seasons = [r.season for r in Ratings.query.filter_by(division='Club').values(Ratings.season)]
    seasons = list(set(seasons))
    seasons = sorted(seasons)
    return render_template('clubMixed.html', ratings=ratings, seasons=seasons, year=year)

@app.route('/club-women')
def clubWomen():
    ratings = Ratings.query.filter_by(division='Club', gender='Women', season=2019).order_by('rank')
    seasons = [r.season for r in Ratings.query.filter_by(division='Club').values(Ratings.season)]
    seasons = list(set(seasons))
    seasons = sorted(seasons)
    return render_template('clubWomen.html', ratings=ratings, year=2019, seasons=seasons)

@app.route('/club-women/<int:year>')
def clubWomenRatings(year):
    ratings = Ratings.query.filter_by(division='Club', gender='Women', season=year).order_by('rank')
    seasons = [r.season for r in Ratings.query.filter_by(division='Club').values(Ratings.season)]
    seasons = list(set(seasons))
    seasons = sorted(seasons)
    return render_template('clubWomen.html', ratings=ratings, seasons=seasons, year=year)

@app.route('/club-women/<int:year>/<category>')
def clubWomenRatingsSorted(year, category):
    if (category == 'rank') | (category == 'sos_rank') | (category == 'team'):
        ratings = Ratings.query.filter_by(division='Club', gender='Women', season=year).order_by(category)
    else:
        ratings = Ratings.query.filter_by(division='Club', gender='Women', season=year).order_by(desc(category))

    seasons = [r.season for r in Ratings.query.filter_by(division='Club').values(Ratings.season)]
    seasons = list(set(seasons))
    seasons = sorted(seasons)
    return render_template('clubWomen.html', ratings=ratings, seasons=seasons, year=year)

@app.route('/college-men')
def collegeMen():
    ratings = Ratings.query.filter_by(division='College', gender='Men', season=2020).order_by('rank')
    seasons = [r.season for r in Ratings.query.filter_by(division='College').values(Ratings.season)]
    seasons = list(set(seasons))
    seasons = sorted(seasons)
    return render_template('collegeMen.html', ratings=ratings, year=2020, seasons=seasons)

@app.route('/college-men/<int:year>')
def collegeMenRatings(year):
    ratings = Ratings.query.filter_by(division='College', gender='Men', season=year).order_by('rank')
    seasons = [r.season for r in Ratings.query.filter_by(division='College').values(Ratings.season)]
    seasons = list(set(seasons))
    seasons = sorted(seasons)
    return render_template('collegeMen.html', ratings=ratings, seasons=seasons, year=year)

@app.route('/college-men/<int:year>/<category>')
def collegeMenRatingsSorted(year, category):
    if (category == 'rank') | (category == 'sos_rank') | (category == 'team'):
        ratings = Ratings.query.filter_by(division='College', gender='Men', season=year).order_by(category)
    else:
        ratings = Ratings.query.filter_by(division='College', gender='Men', season=year).order_by(desc(category))

    seasons = [r.season for r in Ratings.query.filter_by(division='College').values(Ratings.season)]
    seasons = list(set(seasons))
    seasons = sorted(seasons)
    return render_template('collegeMen.html', ratings=ratings, seasons=seasons, year=year)

@app.route('/college-women')
def collegeWomen():
    ratings = Ratings.query.filter_by(division='College', gender='Women', season=2020).order_by('rank')
    seasons = [r.season for r in Ratings.query.filter_by(division='College').values(Ratings.season)]
    seasons = list(set(seasons))
    seasons = sorted(seasons)
    return render_template('collegeWomen.html', ratings=ratings, year=2020, seasons=seasons)

@app.route('/college-women/<int:year>')
def collegeWomenRatings(year):
    ratings = Ratings.query.filter_by(division='College', gender='Women', season=year).order_by('rank')
    seasons = [r.season for r in Ratings.query.filter_by(division='College').values(Ratings.season)]
    seasons = list(set(seasons))
    seasons = sorted(seasons)
    return render_template('collegeWomen.html', ratings=ratings, seasons=seasons, year=year)

@app.route('/college-women/<int:year>/<category>')
def collegeWomenRatingsSorted(year, category):
    if (category == 'rank') | (category == 'sos_rank') | (category == 'team'):
        ratings = Ratings.query.filter_by(division='College', gender='Women', season=year).order_by(category)
    else:
        ratings = Ratings.query.filter_by(division='College', gender='Women', season=year).order_by(desc(category))

    seasons = [r.season for r in Ratings.query.filter_by(division='College').values(Ratings.season)]
    seasons = list(set(seasons))
    seasons = sorted(seasons)
    return render_template('collegeWomen.html', ratings=ratings, seasons=seasons, year=year)

@app.route('/<division>/<team>')
def teamPage(division, team):
    # team page for 2019 or 2020
    if division == 'club':
        team_info = ClubTeams.query.filter_by(team=team)
    elif division == 'college':
        team_info = CollegeTeams.query.filter_by(team=team)
    else:
        team_info = []
    seasons = [r.season for r in Games.query.filter(or_(Games.team_1 == team, Games.team_2 == team)).values(Games.season)]
    seasons = list(set(seasons))
    seasons = sorted(seasons)
    year = seasons[-1] if len(seasons) > 1 else seasons[0]
    team_ratings = Ratings.query.filter_by(team=team, season=year)
    games = Games.query.filter(and_(Games.season == year, or_(Games.team_1 == team, Games.team_2 == team))).order_by(Games.game_date)
    teams1 = [team.team_1 for team in games.values(Games.team_1)]
    teams2 = [team.team_2 for team in games.values(Games.team_2)]
    teams = sorted(list(set(teams1 + teams2)))
    team_ratings = [ Ratings.query.filter(Ratings.team==t, Ratings.season==year)[0].rank for t in teams ]
    ratings_dict = dict(zip(teams, team_ratings))
    events = []
    for game in games:
        if game.event not in events:
            events.append(game.event)
    return render_template('teamPage.html', info=team_info, games=games, year=year, seasons=seasons, division=division, team_rating=team_ratings, events=events, ratings_dict=ratings_dict)

@app.route('/<division>/<team>/<int:year>')
def teamPagePriorSeasons(division, team, year):
    # team page for past seasons
    if division == 'club':
        info = ClubTeams.query.filter_by(team=team)
    elif division == 'college':
        info = CollegeTeams.query.filter_by(team=team)
    else:
        info = []
    seasons = [r.season for r in Games.query.filter(or_(Games.team_1 == team, Games.team_2 == team)).values(Games.season)]
    seasons = list(set(seasons))
    seasons = sorted(seasons)
    team_rating = Ratings.query.filter_by(team=team, season=year)
    games = Games.query.filter(and_(Games.season == year, or_(Games.team_1 == team, Games.team_2 == team))).order_by(Games.game_date)
    teams1 = [team.team_1 for team in games.values(Games.team_1)]
    teams2 = [team.team_2 for team in games.values(Games.team_2)]
    teams = sorted(list(set(teams1 + teams2)))
    team_ratings = [ Ratings.query.filter(Ratings.team==t, Ratings.season==year)[0].rank for t in teams ]
    ratings_dict = dict(zip(teams, team_ratings))
    events = []
    for game in games:
        if game.event not in events:
            events.append(game.event)
    return render_template('teamPage.html', info=info, games=games, year=year, seasons=seasons, division=division, team_rating=team_rating, events=events, ratings_dict=ratings_dict)

@app.route('/<division>/<team>/<gend>')
def collegeTeamPage(division, team, gend):
    # team page for 2019 or 2020
    team_info = CollegeTeams.query.filter_by(team=team, gender=gend)
    team_rating = Ratings.query.filter_by(team=team, season=year, gender=gend)
    seasons = [r.season for r in Games.query.filter(or_(Games.team_1 == team, Games.team_2 == team), Games.gender == gend).values(Games.season)]
    seasons = list(set(seasons))
    seasons = sorted(seasons)
    year = seasons[-1] if len(seasons) > 1 else seasons[0]
    games = Games.query.filter(and_(Games.season == year, or_(Games.team_1 == team, Games.team_2 == team)), Games.gender == gend).order_by(Games.game_date)
    teams1 = [team.team_1 for team in games.values(Games.team_1)]
    teams2 = [team.team_2 for team in games.values(Games.team_2)]
    teams = sorted(list(set(teams1 + teams2)))
    team_ratings = [ Ratings.query.filter(Ratings.team==t, Ratings.season==year, Ratings.gender==gend)[0].rank for t in teams ]
    ratings_dict = dict(zip(teams, team_ratings))
    events = []
    for game in games:
        if game.event not in events:
            events.append(game.event)
    return render_template('collegeTeamPage.html', info=team_info, games=games, year=year, seasons=seasons, division=division, team_rating=team_rating, events=events, gend=gend, ratings_dict=ratings_dict)

@app.route('/team/<division>/<team>/<gend>/<int:year>')
def collegeTeamPagePriorSeasons(division, team, gend, year):
    # team page for past seasons
    info = CollegeTeams.query.filter_by(team=team, gender=gend)
    seasons = [r.season for r in Games.query.filter(or_(Games.team_1 == team, Games.team_2 == team), Games.gender == gend).values(Games.season)]
    seasons = list(set(seasons))
    seasons = sorted(seasons)
    team_rating = Ratings.query.filter_by(team=team, season=year, gender=gend)
    games = Games.query.filter(and_(Games.season == year, or_(Games.team_1 == team, Games.team_2 == team)), Games.gender == gend).order_by(Games.game_date)
    teams1 = [team.team_1 for team in games.values(Games.team_1)]
    teams2 = [team.team_2 for team in games.values(Games.team_2)]
    teams = sorted(list(set(teams1 + teams2)))
    team_ratings = [ Ratings.query.filter(Ratings.team==t, Ratings.season==year, Ratings.gender==gend)[0].rank for t in teams ]
    ratings_dict = dict(zip(teams, team_ratings))
    events = []
    for game in games:
        if game.event not in events:
            events.append(game.event)
    return render_template('collegeTeamPage.html', info=info, games=games, year=year, seasons=seasons, division=division, team_rating=team_rating, events=events, gend=gend, ratings_dict=ratings_dict)

@app.route('/<event>/<int:year>/<gend>')
def eventPage(event, year, gend):
    games = Games.query.filter_by(event=event, season=year, gender=gend).order_by(Games.game_date)
    division = Tournaments.query.filter_by(event=event, season=year)[0].division
    teams1 = [team.team_1 for team in games.values(Games.team_1)]
    teams2 = [team.team_2 for team in games.values(Games.team_2)]
    teams = sorted(list(set(teams1 + teams2)))
    team_ratings = [ Ratings.query.filter(Ratings.team==t, Ratings.season==year)[0].rank for t in teams ]
    ratings_dict = dict(zip(teams, team_ratings))
    genders = [r.gender for r in Games.query.filter_by(event=event, season=year).values(Games.gender)]
    genders = sorted(list(set(genders)))
    return render_template('eventPage.html', event=event, year=year, games=games, division=division.lower(), ratings_dict=ratings_dict, genders=genders, gend=gend)

@app.route('/event/<event>/<int:year>/<gend>')
def collegeEventPage(event, year, gend):
    games = Games.query.filter_by(event=event, season=year, gender=gend).order_by(Games.game_date)
    division = Tournaments.query.filter_by(event=event, season=year)[0].division
    teams1 = [team.team_1 for team in games.values(Games.team_1)]
    teams2 = [team.team_2 for team in games.values(Games.team_2)]
    teams = sorted(list(set(teams1 + teams2)))
    team_ratings = [ Ratings.query.filter(Ratings.team==t, Ratings.season==year)[0].rank for t in teams ]
    ratings_dict = dict(zip(teams, team_ratings))
    genders = [r.gender for r in Games.query.filter_by(event=event, season=year).values(Games.gender)]
    genders = sorted(list(set(genders)))
    return render_template('collegeEventPage.html', event=event, year=year, games=games, division=division.lower(), ratings_dict=ratings_dict, genders=genders, gend=gend)

@app.route('/region/<region>/<division>/<gend>/<int:year>')
def regionStandings(region, division, gend, year):
    if division == 'college':
        teams = CollegeTeams.query.filter_by(gender=gend, region=region)
    elif division == 'club':
        teams = ClubTeams.query.filter_by(gender=gend, region=region)
    else:
        teams = []
    team_list = [t.team for t in teams]
    team_ranks = [Ratings.query.filter(Ratings.gender==gend, Ratings.team==t, Ratings.season==year, Ratings.division==division.title()) for t in team_list]
    team_ranks_list = []
    team_ratings_list = []
    teams_to_remove = []
    for i in range(len(team_ranks)):
        try:
            team_ranks_list.append(team_ranks[i][0].rank)
            team_ratings_list.append(team_ranks[i][0].rating)
        except:
            teams_to_remove.append(team_list[i])
            pass
    for team in teams_to_remove:
        team_list.remove(team)
    rankings_dict = dict(zip(team_list, team_ranks_list))
    rankings_dict = sorted(rankings_dict.items(), key=lambda x: x[1])
    ratings_dict = dict(zip(team_list, team_ratings_list))
    final_dict = {}
    for el in rankings_dict:
        final_dict[el[0]] = {'rank':el[1], 'rating':ratings_dict[el[0]]}
    seasons = [2014, 2015, 2016, 2017, 2018, 2019, 2020]

    return render_template('regions.html', region=region, gend=gend, year=year, seasons=seasons, dict=final_dict, division=division)

@app.route('/section/<section>/<division>/<gend>/<int:year>')
def sectionStandings(section, division, gend, year):
    if division == 'college':
        teams = CollegeTeams.query.filter_by(gender=gend, conference=section)
    elif division == 'club':
        teams = ClubTeams.query.filter_by(gender=gend, section=section)
    else:
        teams = []
    team_list = [t.team for t in teams]
    team_ranks = [Ratings.query.filter(Ratings.gender==gend, Ratings.team==t, Ratings.season==year, Ratings.division==division.title()) for t in team_list]
    team_ranks_list = []
    team_ratings_list = []
    teams_to_remove = []
    for i in range(len(team_ranks)):
        try:
            team_ranks_list.append(team_ranks[i][0].rank)
            team_ratings_list.append(team_ranks[i][0].rating)
        except:
            teams_to_remove.append(team_list[i])
            pass
    for team in teams_to_remove:
        team_list.remove(team)
    rankings_dict = dict(zip(team_list, team_ranks_list))
    rankings_dict = sorted(rankings_dict.items(), key=lambda x: x[1])
    ratings_dict = dict(zip(team_list, team_ratings_list))
    final_dict = {}
    for el in rankings_dict:
        final_dict[el[0]] = {'rank':el[1], 'rating':ratings_dict[el[0]]}
    seasons = [2014, 2015, 2016, 2017, 2018, 2019, 2020]

    return render_template('sections.html', section=section, gend=gend, year=year, seasons=seasons, dict=final_dict, division=division)

@app.route('/competition/<competition>/<gend>/<int:year>')
def competitionStandings(competition, gend, year):

    teams = CollegeTeams.query.filter_by(gender=gend, competition=competition)
    team_list = [t.team for t in teams]
    team_ranks = [Ratings.query.filter(Ratings.gender==gend, Ratings.team==t, Ratings.season==year) for t in team_list]
    team_ranks_list = []
    team_ratings_list = []
    teams_to_remove = []
    for i in range(len(team_ranks)):
        try:
            team_ranks_list.append(team_ranks[i][0].rank)
            team_ratings_list.append(team_ranks[i][0].rating)
        except:
            teams_to_remove.append(team_list[i])
            pass
    for team in teams_to_remove:
        team_list.remove(team)
    rankings_dict = dict(zip(team_list, team_ranks_list))
    rankings_dict = sorted(rankings_dict.items(), key=lambda x: x[1])
    ratings_dict = dict(zip(team_list, team_ratings_list))
    final_dict = {}
    for el in rankings_dict:
        final_dict[el[0]] = {'rank':el[1], 'rating':ratings_dict[el[0]]}
    seasons = [2014, 2015, 2016, 2017, 2018, 2019, 2020]

    return render_template('competitions.html', competition=competition, gend=gend, year=year, seasons=seasons, dict=final_dict, division='college')

@app.errorhandler(404) 
def not_found(e): 
  return render_template("404.html")

