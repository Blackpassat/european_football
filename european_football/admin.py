from django.contrib import admin

# Register your models here.
import european_football.models as models

@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
	fields = ['country_name']
	list_display = ['country_name']
	ordering = ['country_name']

@admin.register(models.Season)
class SeasonAdmin(admin.ModelAdmin):
	fields = ['season_name']
	list_display = ['season_name']
	ordering = ['season_name']

@admin.register(models.PreferredFoot)
class PreferredFootAdmin(admin.ModelAdmin):
	fields = ['preferred_foot_name']
	list_display = ['preferred_foot_name']
	ordering = ['preferred_foot_name']

@admin.register(models.League)
class LeagueAdmin(admin.ModelAdmin):
	fields = ['league_name', 'country']
	list_display = ['league_name', 'country']
	ordering = ['league_name']

@admin.register(models.PlayerAttributes)
class PlayerAttributesAdmin(admin.ModelAdmin):
	fields = [
		'player',
		'overall_rating',
		'potential',
		'preferred_foot',
		'crossing',
		'finishing',
		'heading_accuracy',
		'short_passing',
		'volleys',
		'marking',
		'standing_tackle',
		'sliding_tackle',
		'diving',
		'handling',
		'kicking',
		'positioning',
		'reflexes'
	]

	list_display = [
		'player',
		'overall_rating',
		'potential',
		'preferred_foot',
		'crossing',
		'finishing',
		'heading_accuracy',
		'short_passing',
		'volleys',
		'marking',
		'standing_tackle',
		'sliding_tackle',
		'diving',
		'handling',
		'kicking',
		'positioning',
		'reflexes'
	]

	list_filter = ['preferred_foot']

@admin.register(models.TeamAttributes)
class TeamAttributesAdmin(admin.ModelAdmin):
	fields = [
		'team',
		'play_speed',
		'play_passing',
		'chance_creation_passing',
		'chance_creation_crossing',
		'chance_creation_shooting',
		'defence_pressure',
		'defence_aggression',
		'defence_team_width'
	]

	list_display = [
		'team',
		'play_speed',
		'play_passing',
		'chance_creation_passing',
		'chance_creation_crossing',
		'chance_creation_shooting',
		'defence_pressure',
		'defence_aggression',
		'defence_team_width'
	]

@admin.register(models.MatchTable)
class MatchTableAdmin(admin.ModelAdmin):
	fields = ['season', 'date', 'home_team_goal', 'away_team_goal']
	list_display = ['season', 'date', 'home_team_goal', 'away_team_goal']
	ordering = ['season']

@admin.register(models.Player)
class PlayerAdmin(admin.ModelAdmin):
	fields = ['player_name', 'birthday', 'height', 'weight']
	list_display = ['player_name', 'birthday', 'height', 'weight', 'match_display']
	ordering = ['player_name']

@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
	fields = ['team_long_name', 'team_short_name', 'league']
	list_display = ['team_long_name', 'team_short_name', 'league', 'match_display', 'player_display']
	ordering = ['team_long_name']