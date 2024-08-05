import pytest

import tests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.crl_tst2  # Coral Only
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.google_analytics
@pytest.mark.in_play
@pytest.mark.homepage
@pytest.mark.favourites
@pytest.mark.low
@pytest.mark.other
@pytest.mark.login
@vtest
class Test_C237685_Tracking_Of_Adding_Removing_Favourites_Home_Page(BaseSportTest, BaseDataLayerTest):
    """
    TR_ID: C237685
    VOL_ID: C9698096
    NAME: Tracking of Adding/Removing Favourites on Home page
    """
    keep_browser_open = True
    event = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Football live event
        EXPECTED: Event is created
        """
        self.__class__.in_play_tab = self.get_ribbon_tab_name(internal_id=self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.in_play,
                                                              raise_exceptions=False)
        if not self.in_play_tab:
            raise CmsClientException(f'Tab with internal id "{self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play}" '
                                     f'is not configured')
        start_time = self.get_date_time_formatted_string(seconds=10)
        event_params = self.ob_config.add_autotest_premier_league_football_event(is_live=True, start_time=start_time)
        self.__class__.event_name = event_params.team1 + ' v ' + event_params.team2

    def test_001_login(self):
        """
        DESCRIPTION: Login to application
        EXPECTED: User is logged in
        """
        self.site.login(username=tests.settings.betplacement_user)

    def test_002_click_on_inplay_tab_in_module_ribbon_tabs(self):
        """
        DESCRIPTION: On Home page select In Play tab
        EXPECTED: IN-PLAY tab is opened
        """
        self.site.home.get_module_content(module_name=self.in_play_tab)

    def test_003_find_event_on_home_page_inplay_tab_and_add_it_to_favourites(self):
        """
        DESCRIPTION: Find event on home page (in play tab) and add it to favourites
        EXPECTED: Event is added to favourites, star icon is highlighted
        """
        section_name = tests.settings.football_autotest_competition_league.title() if self.brand != 'ladbrokes' \
            else tests.settings.football_autotest_competition_league
        event = self.get_event_for_homepage_inplay_tab(sport_name='FOOTBALL',
                                                       league_name=section_name,
                                                       event_name=self.event_name)
        self.__class__.event = event
        self.event.favourite_icon.click()
        self.assertTrue(self.event.favourite_icon.is_selected(),
                        msg=f'Favourites icon is not highlighted for event {self.event_name}')

    def test_004_check_data_layer_response_for_adding_to_favourites_on_home_page(self):
        """
        DESCRIPTION: Check data layer response for adding to favourites on home page
        EXPECTED: 'action' must be 'add', 'location' must be 'home'
        """
        self.check_data_layer_favourites_response(object_key='eventAction', action='add', location='home')

    def test_005_remove_event_from_favourites(self):
        """
        DESCRIPTION: Remove event from Favourites
        EXPECTED: Star icon is not highlighted
        """
        self.event.favourite_icon.click()
        self.assertFalse(self.event.favourite_icon.is_selected(expected_result=False),
                         msg=f'Favourites icon is still highlighted for event "{self.event_name}"')

    def test_006_check_data_layer_response_for_removing_from_favourites_on_home_page(self):
        """
        DESCRIPTION: Check data layer response for removing from favourites on home page
        EXPECTED: 'action' must be 'remove', 'location' must be 'home'
        """
        self.check_data_layer_favourites_response(object_key='eventAction', action='remove', location='home')
