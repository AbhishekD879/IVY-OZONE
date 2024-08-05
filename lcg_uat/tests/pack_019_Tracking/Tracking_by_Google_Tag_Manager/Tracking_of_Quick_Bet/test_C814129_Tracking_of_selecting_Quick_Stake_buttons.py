import re

import pytest

import tests
from tests.base_test import BaseTest
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.google_analytics
@pytest.mark.quick_stake
@pytest.mark.quick_bet
@pytest.mark.mobile_only
@pytest.mark.other
@pytest.mark.low
@pytest.mark.login
@vtest
class Test_C814129_Tracking_of_selecting_Quick_Stake_buttons(BaseDataLayerTest, BaseSportTest, BaseRacing, BaseTest):
    """
    TR_ID: C814129
    VOL_ID: C9698242
    NAME: Tracking of selecting Quick Stake buttons
    DESCRIPTION: This test case verifies selecting Quick Stake buttons
    PRECONDITIONS: * Test case should be run on Mobile Only
    PRECONDITIONS: * Browser console should be opened
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: * User is logged out
    """
    keep_browser_open = True

    def verify_tracking(self, value):
        expected_response = {
            'event': 'trackEvent',
            'eventCategory': 'quickbet',
            'eventAction': 'quick stake',
            'eventLabel': value
        }
        actual_response = self.get_data_layer_specific_object(object_key='eventCategory', object_value='quickbet')
        self.compare_json_response(actual_response, expected_response)

    def test_001_create_events(self):
        """
        DESCRIPTION: Create event
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.selection_ids, self.__class__.event_id = event_params.selection_ids, event_params.event_id

    def test_002_add_sport_selection_to_quick_bet(self):
        """
        DESCRIPTION: Navigate to Event Details page
        DESCRIPTION: Add <Sport> selection to Quick Bet
        EXPECTED: Quick bet appears at the bottom of the page
        """
        self.navigate_to_edp(self.event_id)
        self.add_selection_from_event_details_to_quick_bet()
        self.assertTrue(self.site.wait_for_quick_bet_panel(expected_result=True), msg='Quick Bet is not present')

    def test_003_tap_quick_stake_button(self):
        """
        DESCRIPTION: Tap each quick stake  button
        DESCRIPTION: Type in console **'dataLayer'**, tap 'Enter' and check the response
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'quickbet',
        EXPECTED: 'eventAction' : 'quick stake',
        EXPECTED: 'eventLabel' : '<button value>
        EXPECTED: });
        """
        quick_bet = self.site.quick_bet_panel.selection
        quick_stakes = quick_bet.quick_stakes.items_as_ordered_dict
        self.assertTrue(quick_stakes, msg='Quick stake buttons not present')

        for quick_stake_name, quick_stake in quick_stakes.items():
            quick_stake.click()
            self.verify_tracking(re.search('(\d+)', quick_stake_name).groups()[0])

        self.site.quick_bet_panel.header.close_button.click()
        self.site.wait_quick_bet_overlay_to_hide(timeout=15)

    def test_004_log_in_with_user_with_any_currency(self):
        """
        DESCRIPTION: Log in with user with any currency
        """
        self.site.login(username=tests.settings.user_with_usd_currency_and_card)
