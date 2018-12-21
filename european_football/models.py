# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.db.models import Q
from django.urls import reverse


class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = False
        db_table = 'country'
        ordering = ['country_name']
        verbose_name = 'European Football Country'
        verbose_name_plural = 'European Football Country'

    def __str__(self):
        return self.country_name


class League(models.Model):
    league_id = models.AutoField(primary_key=True)
    league_name = models.CharField(unique=True, max_length=45)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)

    class Meta:
        managed = False
        db_table = 'league'
        ordering = ['league_name']
        verbose_name = 'European Football League'
        verbose_name_plural = 'European Football League'

    def __str__(self):
        return self.league_name



class MatchSquad(models.Model):
    match_squad_id = models.AutoField(primary_key=True)
    match = models.ForeignKey('MatchTable', on_delete=models.CASCADE)
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    is_home_team = models.IntegerField()
    player = models.ForeignKey('Player', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'match_squad'
        ordering = ['match', 'team', 'player']
        verbose_name = 'European Football MatchSquad'
        verbose_name_plural = 'European Football MatchSquad'


class MatchTable(models.Model):
    match_table_id = models.AutoField(primary_key=True)
    season = models.ForeignKey('Season', on_delete=models.PROTECT)
    date = models.DateTimeField()
    home_team_goal = models.IntegerField()
    away_team_goal = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'match_table'
        ordering = ['date']
        verbose_name = 'European Football MatchTable'
        verbose_name_plural = 'European Football MatchTable'

    def __str__(self):
        return str(self.match_table_id)


class Player(models.Model):
    player_id = models.AutoField(primary_key=True)
    player_name = models.CharField(max_length=45)
    birthday = models.DateTimeField()
    height = models.FloatField()
    weight = models.FloatField()

    match_table = models.ManyToManyField(MatchTable, through='MatchSquad')

    class Meta:
        managed = False
        db_table = 'player'
        ordering = ['player_name']
        verbose_name = 'European Football Player'
        verbose_name_plural = 'European Football Player'

    def __str__(self):
        return self.player_name

    def match_display(self):
        match_list = [str(match_table.match_table_id) for match_table in self.match_table.all()]
        unique_match_list = []
        for m in match_list:
            if m not in unique_match_list:
                unique_match_list.append(m)
        return ', '.join(
            m for m in unique_match_list[:25])

    match_display.short_description = 'Match Played'

    def get_absolute_url(self):
        # return reverse('site_detail', args=[str(self.id)])
        return reverse('player_detail', kwargs={'pk': self.pk})

    @property
    def object(self):
        t = PlayerAttributes.objects.filter(player_id=self.pk)[0]
        return t



class PlayerAttributes(models.Model):
    player_attributes_id = models.AutoField(primary_key=True)
    player = models.ForeignKey(Player, on_delete=models.PROTECT)
    overall_rating = models.IntegerField(blank=True, null=True)
    potential = models.IntegerField(blank=True, null=True)
    preferred_foot = models.ForeignKey('PreferredFoot', on_delete=models.PROTECT, blank=True, null=True)
    crossing = models.IntegerField(blank=True, null=True)
    finishing = models.IntegerField(blank=True, null=True)
    heading_accuracy = models.IntegerField(blank=True, null=True)
    short_passing = models.IntegerField(blank=True, null=True)
    volleys = models.IntegerField(blank=True, null=True)
    marking = models.IntegerField(blank=True, null=True)
    standing_tackle = models.IntegerField(blank=True, null=True)
    sliding_tackle = models.IntegerField(blank=True, null=True)
    diving = models.IntegerField(blank=True, null=True)
    handling = models.IntegerField(blank=True, null=True)
    kicking = models.IntegerField(blank=True, null=True)
    positioning = models.IntegerField(blank=True, null=True)
    reflexes = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'player_attributes'
        verbose_name = 'European Football PlayerAttributes'
        verbose_name_plural = 'European Football PlayerAttributes'


class PreferredFoot(models.Model):
    preferred_foot_id = models.AutoField(primary_key=True)
    preferred_foot_name = models.CharField(unique=True, max_length=10)

    class Meta:
        managed = False
        db_table = 'preferred_foot'
        ordering = ['preferred_foot_name']
        verbose_name = 'European Football PreferredFoot'
        verbose_name_plural = 'European Football PreferredFoot'

    def __str__(self):
        return self.preferred_foot_name


class Season(models.Model):
    season_id = models.AutoField(primary_key=True)
    season_name = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = False
        db_table = 'season'
        ordering = ['season_name']
        verbose_name = 'European Football Season'
        verbose_name_plural = 'European Football Season'

    def __str__(self):
        return self.season_name


class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_long_name = models.CharField(max_length=45)
    team_short_name = models.CharField(max_length=3)
    league = models.ForeignKey(League, on_delete=models.PROTECT)

    match_table = models.ManyToManyField(MatchTable, through='MatchSquad')
    player = models.ManyToManyField(Player, through='MatchSquad')

    class Meta:
        managed = False
        db_table = 'team'
        ordering = ['team_long_name']
        verbose_name = 'European Football Team'
        verbose_name_plural = 'European Football Team'

    def __str__(self):
        return self.team_long_name

    def match_display(self):
        match_list = [str(match_table.match_table_id) for match_table in self.match_table.all()]
        unique_match_list = []
        for m in match_list:
            if m not in unique_match_list:
                unique_match_list.append(m)
        return ', '.join(
            m for m in unique_match_list[:25])

    match_display.short_description = 'Match Played' 

    def player_display(self):
        player_list = [player.player_name for player in self.player.all()]
        unique_player_list = []
        for p in player_list:
            if p not in unique_player_list:
                unique_player_list.append(p)
        return ', '.join(
            p for p in unique_player_list[:25])

    player_display.short_description = 'Players'

    def get_absolute_url(self):
        # return reverse('site_detail', args=[str(self.id)])
        return reverse('team_detail', kwargs={'pk': self.pk})

    @property
    def play_speed(self):
        t = TeamAttributes.objects.filter(team_id=self.pk)
        if t:
            return t[0].play_speed
        else:
            return None

    @property
    def play_passing(self):
        t = TeamAttributes.objects.filter(team_id=self.pk)
        if t:
            return t[0].play_passing
        else:
            return None

    @property
    def chance_creation_passing(self):
        t = TeamAttributes.objects.filter(team_id=self.pk)
        if t:
            return t[0].chance_creation_passing
        else:
            return None

    @property
    def chance_creation_crossing(self):
        t = TeamAttributes.objects.filter(team_id=self.pk)
        if t:
            return t[0].chance_creation_crossing
        else:
            return None

    @property
    def chance_creation_shooting(self):
        t = TeamAttributes.objects.filter(team_id=self.pk)
        if t:
            return t[0].chance_creation_shooting
        else:
            return None

    @property
    def defence_pressure(self):
        t = TeamAttributes.objects.filter(team_id=self.pk)
        if t:
            return t[0].defence_pressure
        else:
            return None

    @property
    def defence_aggression(self):
        t = TeamAttributes.objects.filter(team_id=self.pk)
        if t:
            return t[0].defence_aggression
        else:
            return None

    @property
    def defence_team_width(self):
        t = TeamAttributes.objects.filter(team_id=self.pk)
        if t:
            return t[0].defence_team_width
        else:
            return None

    @property
    def home_wins(self):
        home_matches = MatchSquad.objects.filter(Q(team_id=self.pk) & Q(is_home_team=1))
        ids = []
        unique_ids = []
        if home_matches:
            for h in home_matches:
                ids.append(h.match.match_table_id)
            for i in ids:
                if i not in unique_ids:
                    unique_ids.append(i)
            win_num = 0
            for u in unique_ids:
                wins = MatchTable.objects.select_related('season').filter(Q(match_table_id=u))
                if wins[0].home_team_goal > wins[0].away_team_goal:
                    win_num += 1
        else:
            win_num = 0
        return win_num

    @property
    def away_wins(self):
        away_matches = MatchSquad.objects.filter(Q(team_id=self.pk) & Q(is_home_team=0))
        ids = []
        unique_ids = []
        if away_matches:
            for h in away_matches:
                ids.append(h.match.match_table_id)
            for i in ids:
                if i not in unique_ids:
                    unique_ids.append(i)
            win_num = 0
            for u in unique_ids:
                wins = MatchTable.objects.select_related('season').filter(Q(match_table_id=u))
                if wins[0].home_team_goal < wins[0].away_team_goal:
                    win_num += 1
        else:
            win_num = 0
        return win_num

    @property
    def home_ties(self):
        home_matches = MatchSquad.objects.filter(Q(team_id=self.pk) & Q(is_home_team=1))
        ids = []
        unique_ids = []
        if home_matches:
            for h in home_matches:
                ids.append(h.match.match_table_id)
            for i in ids:
                if i not in unique_ids:
                    unique_ids.append(i)
            win_num = 0
            for u in unique_ids:
                wins = MatchTable.objects.select_related('season').filter(Q(match_table_id=u))
                if wins[0].home_team_goal == wins[0].away_team_goal:
                    win_num += 1
        else:
            win_num = 0    
        return win_num

    @property
    def away_ties(self):
        away_matches = MatchSquad.objects.filter(Q(team_id=self.pk) & Q(is_home_team=0))
        ids = []
        unique_ids = []
        if away_matches:
            for h in away_matches:
                ids.append(h.match.match_table_id)
            for i in ids:
                if i not in unique_ids:
                    unique_ids.append(i)
            win_num = 0
            for u in unique_ids:
                wins = MatchTable.objects.select_related('season').filter(Q(match_table_id=u))
                if wins[0].home_team_goal == wins[0].away_team_goal:
                    win_num += 1
        else:
            win_num = 0     
        return win_num

    @property
    def home_lose(self):
        home_matches = MatchSquad.objects.filter(Q(team_id=self.pk) & Q(is_home_team=1))
        ids = []
        unique_ids = []
        if home_matches:
            for h in home_matches:
                ids.append(h.match.match_table_id)
            for i in ids:
                if i not in unique_ids:
                    unique_ids.append(i)
            win_num = 0
            for u in unique_ids:
                wins = MatchTable.objects.select_related('season').filter(Q(match_table_id=u))
                if wins[0].home_team_goal < wins[0].away_team_goal:
                    win_num += 1
        else:
            win_num = 0     
        return win_num

    @property
    def away_lose(self):
        away_matches = MatchSquad.objects.filter(Q(team_id=self.pk) & Q(is_home_team=0))
        ids = []
        unique_ids = []
        if away_matches:
            for h in away_matches:
                ids.append(h.match.match_table_id)
            for i in ids:
                if i not in unique_ids:
                    unique_ids.append(i)
            win_num = 0
            for u in unique_ids:
                wins = MatchTable.objects.select_related('season').filter(Q(match_table_id=u))
                if wins[0].home_team_goal > wins[0].away_team_goal:
                    win_num += 1
        else:
            win_num = 0     
        return win_num

    @property
    def players(self):
        players = self.player.select_related().distinct()
        return players
    
    

class TeamAttributes(models.Model):
    team_attributes_id = models.AutoField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.PROTECT)
    play_speed = models.IntegerField(blank=True, null=True)
    play_passing = models.IntegerField(blank=True, null=True)
    chance_creation_passing = models.IntegerField(blank=True, null=True)
    chance_creation_crossing = models.IntegerField(blank=True, null=True)
    chance_creation_shooting = models.IntegerField(blank=True, null=True)
    defence_pressure = models.IntegerField(blank=True, null=True)
    defence_aggression = models.IntegerField(blank=True, null=True)
    defence_team_width = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'team_attributes'
        verbose_name = 'European Football TeamAttributes'
        verbose_name_plural = 'European Football TeamAttributes'
    