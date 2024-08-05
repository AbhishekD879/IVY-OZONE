import json

import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2  # Coral only
# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.low
@pytest.mark.google_analytics
@pytest.mark.event_details
@pytest.mark.bet_placement
@pytest.mark.other
@pytest.mark.login
@vtest
class Test_C237968_Tracking_Of_Viewing_My_Bets_Tab_On_Event_Details_Page(BaseBetSlipTest, BaseDataLayerTest):
    """
    TR_ID: C237968
    VOL_ID: C9698726
    NAME: Tracking of Viewing 'My Bets' tab on Event Details page
    """
    keep_browser_open = True

    def test_000_create_test_event(self):
        """
        DESCRIPTION: Create event and place bet using one of its selections
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID, self.__class__.team1, self.__class__.team2, self.__class__.selection_ids = \
            event_params.event_id, event_params.team1, event_params.team2, event_params.selection_ids

    def test_001_login(self):
        """
        DESCRIPTION: Login to application
        """
        self.site.login(username=tests.settings.betplacement_user)

    def test_002_open_betslip_via_deep_link(self):
        """
        DESCRIPTION: Open betslip via deeplink
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team1])

    def test_003_place_bet(self):
        """
        DESCRIPTION: Place single bet
        """
        self.place_single_bet()

    def test_004_check_bet_receipt_displayed(self):
        """
        DESCRIPTION: Check if user was redirected to bet receipt
        """
        self.check_bet_receipt_is_displayed()

    def test_005_go_to_event_details_page(self):
        """
        DESCRIPTION: Go to Event details page
        """
        self.navigate_to_edp(event_id=self.eventID)
        if self.brand == "ladbrokes":
            self.site.open_my_bets_open_bets()
        else:
            self.site.sport_event_details.event_user_tabs_list.open_tab(tab_name=self.my_bets_tab_name)
            self.assertEqual(self.site.sport_event_details.event_user_tabs_list.current, self.my_bets_tab_name,
                             msg=f'Current tab {self.site.sport_event_details.event_user_tabs_list.current} '
                                 f'is not the same as expected {self.my_bets_tab_name}')

    def test_006_check_dataLayer_response(self):
        """
        DESCRIPTION: Check data layer info for click on My bets tab
        """
        actual_response = self.get_data_layer_specific_object(object_key='eventID', object_value=int(self.eventID))
        expected_response = {
            'event': 'trackEvent',
            'eventCategory': 'content',
            'eventAction': 'click',
            'eventLabel': 'event page - my bets (1)',
            'eventID': int(self.eventID),
            'location': 'event page'
        }
        self._logger.debug('*** Actual data layer response \n %s' % json.dumps(actual_response, indent=2))
        self._logger.debug('*** Expected data layer response \n %s' % json.dumps(expected_response, indent=2))
        self.compare_json_response(actual_response, expected_response)
