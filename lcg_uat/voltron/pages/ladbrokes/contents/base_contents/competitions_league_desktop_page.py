from voltron.pages.shared.contents.base_contents.competitions_league_desktop_page import StandingsWidget, \
    CompetitionLeagueDesktopPage


class StandingsWidgetLadbrokes(StandingsWidget):

    def is_expanded(self, *args, **kwargs):
        return super(StandingsWidget, self).is_expanded(*args, **kwargs)


class CompetitionLeagueDesktopPageLadbrokes(CompetitionLeagueDesktopPage):

    @property
    def standings_widget(self):
        return StandingsWidgetLadbrokes(selector=self._standings_widget)
