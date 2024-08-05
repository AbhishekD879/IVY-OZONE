import pytest

import tests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.crl_tst2  # Coral Only
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.google_analytics
@pytest.mark.favourites
@pytest.mark.low
@pytest.mark.competitions
@pytest.mark.other
@pytest.mark.login
@vtest
class Test_C237685_Tracking_Of_Adding_Removing_Favourites_Football_Competitions_Page(BaseSportTest, BaseDataLayerTest):
    """
    TR_ID: C237685
    VOL_ID: C9698296
    NAME: Tracking of Adding/Removing Favourites on Football Competitions page
    NOTE: It's possible to add event to favourites not older than 12 hours from the start time of the event
    """
    keep_browser_open = True
    event = None

    def test_000_create_test_event(self):
        """
        DESCRIPTION: Create event
        EXPECTED: Event is created
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.event_name = event_params.team1 + ' v ' + event_params.team2

    def test_001_login(self):
        """
        DESCRIPTION: Login to application
        EXPECTED: User is logged in
        """
        self.site.login(username=tests.settings.betplacement_user)

    def test_002_navigate_to_football_page(self):
        """
        DESCRIPTION: Navigate to the Football Landing page
        EXPECTED: Football Landing page is shown
        """
        self.site.open_sport(name='FOOTBALL')

    def test_003_open_football_competitions_tab_and_find_event(self):
        """
        DESCRIPTION: Open Football competitions tab, find created event and add it to favourites
        EXPECTED: Event is added to favourites
        """
        expected_sport_tab = \
            self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                    self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(expected_sport_tab)
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, expected_sport_tab,
                         msg=f'Competition tab is not active, active is "{active_tab}"')
        sections = self.site.football.tab_content.all_competitions_categories.items_as_ordered_dict
        self.assertTrue(sections, msg='No Sections found')
        autotest_competition = tests.settings.football_autotest_competition
        section = sections[autotest_competition] if autotest_competition in sections.keys() else None
        self.assertTrue(section, msg=f'Could not find "{autotest_competition}" section')
        section.expand()
        wait_for_result(lambda: section.items_as_ordered_dict,
                        name='Leagues list is loaded',
                        timeout=2)
        leagues = section.items_as_ordered_dict
        self.assertTrue(leagues, msg='No Leagues found')
        autotest_league = tests.settings.football_autotest_competition_league.title()
        league = leagues[autotest_league] if autotest_league in leagues.keys() else None
        self.assertTrue(league, msg=f'Could not find "{autotest_league}" league')
        league.click()
        sections = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')
        today = 'Today' if self.brand != 'ladbrokes' else 'TODAY'
        today_section = sections[today] if today in sections.keys() else None
        self.assertTrue(today_section, msg='"Today" section is not present')
        events = today_section.items_as_ordered_dict
        self.assertTrue(events, msg='No events found')
        self.__class__.event = events[self.event_name] if self.event_name in events.keys() else None
        self.assertTrue(self.event, msg=f'Could not find event "{self.event_name}"')
        self.event.favourite_icon.click()
        self.assertTrue(self.event.favourite_icon.is_selected(),
                        msg=f'Favourites icon is not highlighted for event {self.event_name}')

    def test_004_check_data_layer_response_for_adding_to_favourites_on_football_competitions_page(self):
        """
        DESCRIPTION: Check data layer response on event details page
        EXPECTED: 'action' must be 'add', 'location' must be 'football competitions'
        """
        self.check_data_layer_favourites_response(object_key='eventAction', action='add', location='football competitions')

    def test_005_remove_event_from_favourites(self):
        """
        DESCRIPTION: Click on 'star' icon again
        EXPECTED: 'Star' icon is not highlighted - event is removed from favourites
        """
        self.event.favourite_icon.click()
        self.assertFalse(self.event.favourite_icon.is_selected(expected_result=False),
                         msg=f'Favourites icon is highlighted for event {self.event_name}')

    def test_006_check_data_layer_response_for_removing_event_from_favourites_on_football_competitions_page(self):
        """
        DESCRIPTION: Check data layer response on football competitions page
        EXPECTED: 'action' must be 'remove', 'location' must be 'football competitions'
        """
        self.check_data_layer_favourites_response(object_key='eventAction', action='add', location='football competitions')
