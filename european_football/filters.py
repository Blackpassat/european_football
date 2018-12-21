import django_filters
from european_football.models import Player, Team, League, Country, Season


class TeamFilter(django_filters.FilterSet):
	team_long_name = django_filters.CharFilter(
		field_name='team_long_name',
		label='Team Full Name',
		lookup_expr='icontains'
	)

	# Add description, heritage_site_category, region, sub_region and intermediate_region filters here
	team_short_name = django_filters.CharFilter(
		field_name='team_short_name',
		label='Team Code',
		lookup_expr='icontains'
	)

	league = django_filters.ModelChoiceFilter(
		field_name='league',
		label='League',
		queryset=League.objects.all().order_by('league_name'),
		lookup_expr='exact'
	)

	country = django_filters.ModelChoiceFilter(
		field_name='league__country',
		label='Country',
		queryset=Country.objects.all().order_by('country_name'),
		lookup_expr='exact'
	)

	player = django_filters.ModelMultipleChoiceFilter(
		field_name='player',
		label='Player Name',
		queryset=Player.objects.all().order_by('player_name'),
		lookup_expr='exact'
	)


	class Meta:
		model = Team
		# form = SearchForm
		# fields [] is required, even if empty.
		fields = []