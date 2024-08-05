import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from voltron.utils.helpers import normalize_name
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.crl_tst2  # Coral Only
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.google_analytics
@pytest.mark.favourites
@pytest.mark.in_play
@pytest.mark.desktop
@pytest.mark.other
@pytest.mark.low
@pytest.mark.login
@vtest
class Test_C237685_Tracking_Of_Adding_Removing_Favourites_Inplay_and_Football_Inplay_Pages(BaseSportTest, BaseDataLayerTest):
    """
    TR_ID: C237685
    VOL_ID: C9698029
    NAME: Tracking of Adding/Removing Favourites on In-play and Football In-play pages
    """
    keep_browser_open = True
    event = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Football live event
        EXPECTED: Event is created
        """
        if not self.get_favourites_enabled_status():
            raise CmsClientException(f'"Favourites" is not enabled for device type "{self.device_type}" in CMS')

        start_time = self.get_date_time_formatted_string(seconds=10)
        event_params = self.ob_config.add_autotest_premier_league_football_event(is_live=True, start_time=start_time)
        self.__class__.eventID = event_params.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        self.__class__.event_name = normalize_name(event_resp[0]['event']['name'])
        self._logger.info(f'*** Created Football event "{self.event_name}"')

        self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0], in_play_tab_slp=True)

    def test_001_login(self):
        """
        DESCRIPTION: Login to application
        EXPECTED: User is logged in
        """
        self.site.login(username=tests.settings.betplacement_user, async_close_dialogs=False)

    def test_002_navigate_to_football_page(self):
        """
        DESCRIPTION: Navigate to the Football Landing page and open In Play tab
        EXPECTED: Football IN-PLAY page is shown
        """
        self.site.open_sport(name='FOOTBALL')
        expected_sport_tab = \
            self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play, self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(expected_sport_tab)
        self.site.wait_splash_to_hide(3)
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, expected_sport_tab,
                         msg=f'In-Play tab is not active, active is "{active_tab}"')

    def test_003_find_event_and_add_it_to_favourites(self):
        """
        DESCRIPTION: Find created event on Football in play page and click on 'star' icon
        EXPECTED: 'Star' icon is highlighted
        """
        self.__class__.event = self.get_event_from_league(event_id=self.eventID,
                                                          section_name=self.section_name)
        self.event.favourite_icon.click()
        self.assertTrue(self.event.favourite_icon.is_selected(),
                        msg=f'Favourites icon is not highlighted for event "{self.event_name}"')

    def test_004_check_data_layer_response_for_adding_to_favourites_on_football_inplay_page(self):
        """
        DESCRIPTION: Check data layer response for adding to favourites on football inplay page
        EXPECTED: 'action' must be 'add', 'location' must be 'football in play'
        """
        self.check_data_layer_favourites_response(object_key='eventAction', action='add', location='football in play')

    def test_005_remove_event_from_favourites(self):
        """
        DESCRIPTION: Remove event from Favourites
        EXPECTED: Star icon is not highlighted
        """
        self.event.favourite_icon.click()
        self.assertFalse(self.event.favourite_icon.is_selected(expected_result=False),
                         msg=f'Favourites icon is not highlighted for event "{self.event_name}"')

    def test_006_check_data_layer_response_for_removing_from_favourites_on_football_inplay_page(self):
        """
        DESCRIPTION: Check data layer response for removing from favourites on football inplay page
        EXPECTED: 'action' must be 'remove', 'location' must be 'football in play'
        """
        self.check_data_layer_favourites_response(object_key='eventAction', action='remove',
                                                  location='football in play')

    def test_007_go_to_inplay_page(self):
        """
        DESCRIPTION: Go to In Play page
        EXPECTED: In Play page is opened
        """
        self.navigate_to_page(name='/in-play/football')
        self.site.wait_content_state(state_name='in-play')

    def test_008_find_event_and_add_it_to_favourites(self):
        """
        DESCRIPTION: Find created event on In Play page and click on 'star' icon
        EXPECTED: 'Star' icon is highlighted
        """
        self.__class__.event = self.get_event_from_league(event_id=self.eventID,
                                                          section_name=self.section_name,
                                                          inplay_section=vec.inplay.LIVE_NOW_SWITCHER)
        self.event.favourite_icon.click()
        self.assertTrue(self.event.favourite_icon.is_selected(),
                        msg=f'Favourites icon is not highlighted for event "{self.event_name}"')

    def test_009_check_data_layer_response_for_adding_to_favourites_on_inplay_page(self):
        """
        DESCRIPTION: Check data layer response for adding to favourites on inplay page
        EXPECTED: 'action' must be 'add', 'location' must be 'in play'
        """
        self.check_data_layer_favourites_response(object_key='eventAction', action='add', location='in play')

    def test_010_remove_event_from_favourites(self):
        """
        DESCRIPTION: Remove event from Favourites
        EXPECTED: Star icon is not highlighted
        """
        self.event.favourite_icon.click()
        self.assertFalse(self.event.favourite_icon.is_selected(expected_result=False),
                         msg=f'Favourites icon is not highlighted for event "{self.event_name}"')

    def test_011_check_data_layer_response_for_removing_from_favourites_on_inplay_page(self):
        """
        DESCRIPTION: Check data layer response for removing from favourites on inplay page
        EXPECTED: 'action' must be 'remove', 'location' must be 'in play'
        """
        self.check_data_layer_favourites_response(object_key='eventAction', action='remove', location='in play')
