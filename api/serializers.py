from european_football.models import Country, League, MatchSquad, MatchTable, \
	Player, PlayerAttributes, PreferredFoot, Season, Team, TeamAttributes
from rest_framework import response, serializers, status


class CountrySerializer(serializers.ModelSerializer):

	class Meta:
		model = Country
		fields = ('country_id', 'country_name')


class LeagueSerializer(serializers.ModelSerializer):
	country = CountrySerializer(many=False, read_only=True)

	class Meta:
		model = League
		fields = ('league_id', 'league_name', 'country')


class SeasonSerializer(serializers.ModelSerializer):

	class Meta:
		model = Season
		fields = ('season_id', 'season_name')


class PreferredFootSerializer(serializers.ModelSerializer):

	class Meta:
		model = PreferredFoot
		fields = ('preferred_foot_id', 'preferred_foot_name')


class MatchTableSerializer(serializers.ModelSerializer):
	season = SeasonSerializer(many=False, read_only=True)

	class Meta:
		model = MatchTable
		fields = ('match_table_id', 'season', 'date', 'home_team_goal', 'away_team_goal')


class PlayerSerializer(serializers.ModelSerializer):

	class Meta:
		model = Player
		fields = (
			'player_id',
			'player_name',
			'birthday',
			'height',
			'weight')


class PlayerAttributesSerializer(serializers.ModelSerializer):
	player = PlayerSerializer(many=False, read_only=True)
	preferred_foot = PreferredFootSerializer(many=False, read_only=True)

	class Meta:
		model = PlayerAttributes
		fields = (
			'player_attributes_id', 
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
			'reflexes')


class MatchSquadSerializer(serializers.ModelSerializer):
	team_id = serializers.ReadOnlyField(source='team.team_id')
	match_id = serializers.ReadOnlyField(source='match.match_table_id')
	player_id = serializers.ReadOnlyField(source='player.player_id')
	is_home_team = serializers.IntegerField()
	class Meta:
		model = MatchSquad
		fields = ('match_id', 'team_id', 'is_home_team', 'player_id')


class TeamSerializer(serializers.ModelSerializer):
	team_long_name = serializers.CharField(
		allow_blank=False,
		max_length=45
	)
	team_short_name = serializers.CharField(
		allow_blank=False,
		max_length=3
	)
	league = LeagueSerializer(
		many=False,
		read_only=True
	)
	league_id = serializers.PrimaryKeyRelatedField(
		allow_null=False,
		many=False,
		write_only=True,
		queryset=League.objects.all(),
		source='league'
	)

	class Meta:
		model = Team
		fields = (
			'team_id',
			'team_long_name',
			'team_short_name',
			'league',
			'league_id'
		)

	def create(self, validated_data):
		"""
		This method persists a new HeritageSite instance as well as adds all related
		countries/areas to the heritage_site_jurisdiction table.  It does so by first
		removing (validated_data.pop('heritage_site_jurisdiction')) from the validated
		data before the new HeritageSite instance is saved to the database. It then loops
		over the heritage_site_jurisdiction array in order to extract each country_area_id
		element and add entries to junction/associative heritage_site_jurisdiction table.
		:param validated_data:
		:return: site
		"""

		# print(validated_data)

		matches, homes, players = validated_data.pop('match_squad')
		team = Team.objects.create(**validated_data)

		if matches is not None and homes is not None and players is not None:
			for match in matches:
				for home in homes:
					for player in players:
						MatchSquad.objects.create(
							team_id=team.team_id,
							match_id=match.match_id,
							is_home_team=home,
							player_id=player.player_id
						)
		return team

	def update(self, instance, validated_data):
		# site_id = validated_data.pop('heritage_site_id')
		team_id = instance.team_id
		new_matches, new_is_home_team, new_players = validated_data.pop('match_squad')

		instance.team_long_name = validated_data.get(
			'team_long_name',
			instance.team_long_name
		)
		instance.team_short_name = validated_data.get(
			'team_short_name',
			instance.team_short_name
		)
		instance.league_id = validated_data.get(
			'league_id',
			instance.league_id
		)
		instance.save()

		# Current country_area_id values linked to site
		old_player_ids = MatchSquad.objects\
			.values_list('player_id', flat=True)\
			.filter(team_id=team_id)

		old_match_ids = MatchSquad.objects\
			.values_list('match_id', flat=True)\
			.filter(team_id=team_id)

		# TODO can these loops be refactored?

		# New ids
		new_player_ids = []
		new_match_ids = []

		# Insert new unmatched country entries
		for player in new_players:
			for match in new_matches:
				for home in new_is_home_team:
					new_player_id = player.player_id
					new_player_ids.append(new_player_id)
					new_match_id = match.match_table_id
					new_match_ids.append(new_match_id)
					if new_player_id in old_player_ids and new_match_id in old_match_ids:
						continue
					else:
						MatchSquad.objects \
							.create(match_id=new_match_id, team_id=team_id, player_id=new_player_id, is_home_team=home)

		# Delete old unmatched country entries
		for old_player_id in old_player_ids:
			for old_match_id in old_match_ids:
				for home in new_is_home_team:
					if old_player_id in new_player_ids and old_match_id in new_match_ids:
						continue					
					else:
						MatchSquad.objects \
							.filter(match_id=old_match_id, team_id=team_id, player_id=old_player_id, is_home_team=home) \
							.delete()

		return instance

class TeamAttributesSerializer(serializers.ModelSerializer):
	team = TeamSerializer(many=False, read_only=True)

	class Meta:
		model = TeamAttributes
		fields = (
			'team_attributes_id',
			'team',
			'play_speed',
			'play_passing',
			'chance_creation_passing',
			'chance_creation_crossing',
			'chance_creation_shooting',
			'defence_pressure',
			'defence_aggression',
			'defence_team_width')