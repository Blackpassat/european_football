from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views import generic
from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django_filters.views import FilterView

from .models import Team
from .models import TeamAttributes
from .models import Player
from .models import MatchSquad
from .forms import TeamForm
from .filters import TeamFilter


def index(request):
	return HttpResponse("Hello, world. You're at the UNESCO Heritage Sites index page.")


class AboutPageView(generic.TemplateView):
	template_name = 'european_football/about.html'


class HomePageView(generic.TemplateView):
	template_name = 'european_football/home.html'


@method_decorator(login_required, name='dispatch')
class TeamListView(generic.ListView):
	model = Team
	context_object_name = 'teams'
	template_name = 'european_football/team.html'
	paginate_by = 50

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def get_queryset(self):
		return Team.objects.all()

@method_decorator(login_required, name='dispatch')
class TeamDetailView(generic.DetailView):
	model = Team
	context_object_name = 'team'
	template_name = 'european_football/team_detail.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

@method_decorator(login_required, name='dispatch')
class PlayerDetailView(generic.DetailView):
	model = Player
	context_object_name = 'player'
	template_name = 'european_football/player_detail.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

@method_decorator(login_required, name='dispatch')
class TeamCreateView(generic.View):
	model = Team
	form_class = TeamForm
	success_message = "Team created successfully"
	template_name = 'european_football/team_new.html'
	# fields = '__all__' <-- superseded by form_class
	# success_url = reverse_lazy('heritagesites/site_list')

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def post(self, request):
		form = TeamForm(request.POST)
		if form.is_valid():
			team = form.save(commit=False)
			team.save()
			for player in form.cleaned_data['player']:
				for match in form.cleaned_data['match_table']:
					MatchSquad.objects.create(match=match, team=team, player=player, is_home_team=2)
			return redirect(team) # shortcut to object's get_absolute_url()
			# return HttpResponseRedirect(site.get_absolute_url())
		return render(request, 'european_football/team_new.html', {'form': form})

	def get(self, request):
		form = TeamForm()
		return render(request, 'european_football/team_new.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class TeamUpdateView(generic.UpdateView):
	model = Team
	form_class = TeamForm
	# fields = '__all__' <-- superseded by form_class
	context_object_name = 'team'
	# pk_url_kwarg = 'site_pk'
	success_message = "Team updated successfully"
	template_name = 'european_football/team_update.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def form_valid(self, form):
		team = form.save(commit=False)
		# site.updated_by = self.request.user
		# site.date_updated = timezone.now()
		team.save()

		# Current country_area_id values linked to site
		old_player_ids = MatchSquad.objects\
			.values_list('player_id', flat=True)\
			.filter(team_id=team.team_id)

		old_match_ids = MatchSquad.objects\
			.values_list('match_id', flat=True)\
			.filter(team_id=team.team_id)

		# New countries list
		new_players = form.cleaned_data['player']

		new_matches = form.cleaned_data['match_table']

		# TODO can these loops be refactored?

		# New ids
		new_player_ids = []
		new_match_ids = []

		# Insert new unmatched country entries
		for player in new_players:
			for match in new_matches:
				new_player_id = player.player_id
				new_player_ids.append(new_player_id)
				new_match_id = match.match_table_id
				new_match_ids.append(new_match_id)
				if new_player_id in old_player_ids and new_match_id in old_match_ids:
					continue
				else:
					MatchSquad.objects \
						.create(match=match, team=team, player=player, is_home_team=2)

		# Delete old unmatched country entries
		for old_player_id in old_player_ids:
			for old_match_id in old_match_ids:
				if old_player_id in new_player_ids and old_match_id in new_match_ids:
					continue					
				else:
					MatchSquad.objects \
						.filter(match_id=old_match_id, team_id=team.team_id, player_id=old_player_id) \
						.delete()

		return HttpResponseRedirect(team.get_absolute_url())
		# return redirect('heritagesites/site_detail', pk=site.pk)

@method_decorator(login_required, name='dispatch')
class TeamDeleteView(generic.DeleteView):
	model = Team
	success_message = "Team deleted successfully"
	success_url = reverse_lazy('teams')
	context_object_name = 'team'
	template_name = 'european_football/team_delete.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()

		# Delete HeritageSiteJurisdiction entries
		MatchSquad.objects \
			.filter(team_id=self.object.team_id) \
			.delete()

		Team.objects.filter(team_id=self.object.team_id).delete()

		self.object.delete()

		return HttpResponseRedirect(self.get_success_url())

class TeamFilterView(FilterView):
	filterset_class = TeamFilter
	template_name = 'european_football/team_filter.html'