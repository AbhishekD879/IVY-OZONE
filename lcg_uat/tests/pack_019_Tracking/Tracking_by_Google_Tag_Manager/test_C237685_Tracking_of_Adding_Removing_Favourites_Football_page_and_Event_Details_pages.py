import pytest

import tests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.helpers import normalize_name


# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.crl_tst2  # Coral Only
@pytest.mark.crl_stg2
@pytest.mark.google_analytics
@pytest.mark.favourites
@pytest.mark.other
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-33439')
@pytest.mark.login
@vtest
class Test_C237685_Tracking_Of_Adding_Removing_Favourites_Football_Page_and_Event_Details_Page(BaseSportTest, BaseDataLayerTest):
    """
    TR_ID: C237685
    VOL_ID: C9697713
    NAME: Tracking of Adding/Removing Favourites on Football page and Event Details page
    """
    keep_browser_open = True
    event = None

    def test_000_create_test_event(self):
        """
        DESCRIPTION: Create event
        EXPECTED: Event is created
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID, self.__class__.selection_ids = event_params.event_id, event_params.selection_ids

        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        self.__class__.event_name = normalize_name(event_resp[0]['event']['name'])
        self._logger.info(f'*** Created Football event "{self.event_name}"')
        self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0])

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
        self.navigate_to_page(name='sport/football')

    def test_003_find_event_and_add_it_to_favourites(self):
        """
        DESCRIPTION: Find created event on Football page and click on 'star' icon
        EXPECTED: 'Star' icon is highlighted
        """
        self.__class__.event = self.get_event_from_league(event_id=self.eventID, section_name=self.section_name)
        self.event.favourite_icon.click()
        self.assertTrue(self.event.favourite_icon.is_selected(),
                        msg=f'Favourites icon is not highlighted for event "{self.event_name}"')

    def test_004_check_data_layer_response_for_adding_to_favourites_on_football_page(self):
        """
        DESCRIPTION: Check data layer response for adding to favourites on football page
        EXPECTED: 'action' must be 'add', 'location' must be 'football matches'
        """
        self.check_data_layer_favourites_response(object_key='eventAction', action='add', location='football matches')

    def test_005_remove_event_from_favourites(self):
        """
        DESCRIPTION: Remove event from Favourites
        EXPECTED: Star icon is not highlighted
        """
        self.event.favourite_icon.click()
        self.assertFalse(self.event.favourite_icon.is_selected(expected_result=False),
                         msg=f'Favourites icon is still highlighted for event "{self.event_name}"')

    def test_006_check_data_layer_response_for_removing_from_favourites_on_football_page(self):
        """
        DESCRIPTION: Check data layer response for removing from favourites on football page
        EXPECTED: 'action' must be 'remove', 'location' must be 'football matches'
        """
        self.check_data_layer_favourites_response(object_key='eventAction', action='remove', location='football matches')

    def test_007_go_to_event_details_page(self):
        """
        DESCRIPTION: Go to Event Details page
        EXPECTED: Event Details page is opened
        """
        if self.brand != 'ladbrokes':
            self.event.click()
            self.site.wait_content_state(state_name='EventDetails')

    def test_008_add_event_to_favourites(self):
        """
        DESCRIPTION: Click on 'star' icon on Event Details page
        EXPECTED: 'Star' icon is highlighted
        """
        if self.brand != 'ladbrokes':
            self.site.sport_event_details.favourite_icon.click()
            self.assertTrue(self.site.sport_event_details.favourite_icon.is_selected(),
                            msg=f'Favourites icon is not highlighted for event "{self.event_name}"')

    def test_009_check_data_layer_response_for_adding_to_favourites_on_event_details_page(self):
        """
        DESCRIPTION: Check data layer response on event details page
        EXPECTED: 'action' must be 'add', 'location' must be 'event page'
        """
        if self.brand != 'ladbrokes':
            self.check_data_layer_favourites_response(object_key='eventAction', action='add', location='event page')

    def test_010_remove_event_from_favourites(self):
        """
        DESCRIPTION: Click on 'star' icon again
        EXPECTED: 'Star' icon is not highlighted - event is removed from favourites
        """
        if self.brand != 'ladbrokes':
            self.site.contents.favourite_icon.click()
            self.assertFalse(self.site.contents.favourite_icon.is_selected(expected_result=False),
                             msg=f'Favourites icon is highlighted for event "{self.event_name}"')

    def test_011_check_data_layer_response_for_removing_from_favourites_on_event_details_page(self):
        """
        DESCRIPTION: Check data layer response on football page
        EXPECTED: 'action' must be 'remove', 'location' must be 'event page'
        """
        if self.brand != 'ladbrokes':
            self.check_data_layer_favourites_response(object_key='eventAction', action='remove', location='event page')
