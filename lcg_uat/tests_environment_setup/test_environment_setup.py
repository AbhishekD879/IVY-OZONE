import pytest
from faker import Faker
import tests
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.hl
class TestEnvironmentSetUp(Common):
    """
    NAME: Test for environment set up
    """
    keep_browser_open = True
    f = Faker()

    def test_000_create_featured_module_by_type_id(self):
        """
        DESCRIPTION: Create featured module by type id
        """
        if tests.settings.backend_env != 'prod':
            type_id = self.ob_config.football_config.england.premier_league.type_id
            self.ob_config.add_football_event_to_england_premier_league(team1=self.f.city(),
                                                                        team2=self.f.city())
        else:
            type_id = self.get_active_events_for_category()[0]['event']['typeId']
        self.cms_config.add_featured_tab_module(select_event_by='Type',
                                                title='Featured Module By Type Id',
                                                id=type_id)

    def test_001_create_featured_module_by_race_type_id(self):
        """
        DESCRIPTION: Create featured module by race type id
        """
        if tests.settings.backend_env != 'prod':
            self.ob_config.add_UK_racing_event(number_of_runners=3)
            type_id = self.ob_config.horseracing_config.horse_racing_live.autotest_uk.type_id
        else:
            type_id = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id)[0]['event']['typeId']
        self.cms_config.add_featured_tab_module(select_event_by='RaceTypeId',
                                                title='Featured Module By Race Type Id',
                                                id=type_id)

    def test_002_create_featured_module_by_selection_id(self):
        """
        DESCRIPTION: Create featured module by selection id
        """
        if tests.settings.backend_env != 'prod':
            event = self.ob_config.add_football_event_to_england_premier_league(team1=self.f.city(),
                                                                                team2=self.f.city())
            selection = event.selection_ids[event.team1]
        else:
            selections = self.get_active_event_selections_for_category()
            selection = list(selections.values())[0]

        self.cms_config.add_featured_tab_module(select_event_by='Selection',
                                                id=selection,
                                                title='Featured module by Selection id',
                                                badge='Specials')

    def test_003_create_featured_module_by_event_id(self):
        """
        DESCRIPTION: Create featured module by event id
        """
        if tests.settings.backend_env != 'prod':
            event_id = self.ob_config.add_football_event_to_england_premier_league(team1=self.f.city(),
                                                                                   team2=self.f.city()).event_id
        else:
            event_id = self.get_active_events_for_category()[0]['event']['id']

        self.cms_config.add_featured_tab_module(select_event_by='Event',
                                                id=event_id,
                                                title='Featured module by Event')

    def test_004_create_surface_bet_on_homepage(self):
        """
        DESCRIPTION: Create Surface bet module on Homepage
        """
        if tests.settings.backend_env != 'prod':
            event = self.ob_config.add_football_event_to_england_premier_league(team1=self.f.city(),
                                                                                team2=self.f.city())
            selection_id = event.selection_ids[event.team1]
        else:
            selections = self.get_active_event_selections_for_category()
            selection_id = list(selections.values())[0]

        self.cms_config.add_surface_bet(selection_id=selection_id,
                                        categoryIDs=self.ob_config.backend.ti.football.category_id)

    def test_005_create_highlights_carousel_on_homepage(self):
        """
        DESCRIPTION: Create highlights carousel on Homepage
        """
        if tests.settings.backend_env != 'prod':
            event_id = self.ob_config.add_football_event_to_england_premier_league(team1=self.f.city(),
                                                                                   team2=self.f.city()).event_id
        else:
            event_id = self.get_active_events_for_category()[0]['event']['id']

        self.cms_config.create_highlights_carousel(title='Highlights Carousel', events=[event_id])

    def test_006_create_quick_links_module_on_homepage(self):
        """
        DESCRIPTION: Create quick links module on Homepage
        """
        self.cms_config.create_quick_link(title='Quick Links Module',
                                          sport_id=0,
                                          destination=f'https://{tests.HOSTNAME}/sport/football/matches')

    def test_007_create_surface_bet_on_sports_page(self):
        """
        DESCRIPTION: Create surface bet on sports page
        """
        if tests.settings.backend_env != 'prod':
            event = self.ob_config.add_football_event_to_england_premier_league(team1=self.f.city(),
                                                                                team2=self.f.city())
            selection_id = event.selection_ids[event.team1]
        else:
            selections = self.get_active_event_selections_for_category()
            selection_id = list(selections.values())[0]

        self.cms_config.add_surface_bet(selection_id=selection_id,
                                        categoryIDs=self.ob_config.football_config.category_id,
                                        highlightsTabOn=True)

    def test_008_create_highlights_carousel_on_sports_page(self):
        """
        DESCRIPTION: Create Highlights Carousel on Sport page
        """
        if tests.settings.backend_env != 'prod':
            event_id = self.ob_config.add_football_event_to_england_premier_league(team1=self.f.city(),
                                                                                   team2=self.f.city()).event_id
        else:
            event_id = self.get_active_events_for_category()[0]['event']['id']

        self.cms_config.create_highlights_carousel(title='Highlights Carousel',
                                                   sport_id=self.ob_config.backend.ti.football.category_id,
                                                   events=[event_id])

    def test_009_create_quick_links_module_on_sports_page(self):
        """
        DESCRIPTION: Create Quick Links Module on Sport page
        """
        self.cms_config.create_quick_link(title='Quick Link',
                                          sport_id=self.ob_config.backend.ti.football.category_id,
                                          destination=f'https://{tests.HOSTNAME}/sport/football/matches')

    @classmethod
    def tearDownClass(cls):
        pass
