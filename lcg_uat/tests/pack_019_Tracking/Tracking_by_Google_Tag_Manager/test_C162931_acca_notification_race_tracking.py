import pytest

from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.google_analytics
@pytest.mark.acca
@pytest.mark.other
@pytest.mark.low
@vtest
class Test_C162931_Verify_Acca_Notification_Race_Tracking(BaseDataLayerTest, BaseBetSlipTest):
    """
    TR_ID: C162931
    VOL_ID: C9697594
    NAME: This test case verifies ACCA Odds Notification Tracking for races (Mobile)
    """
    keep_browser_open = True
    selection_ids = []

    def test_000_create_racing_events(self):
        """
        DESCRIPTION: Create racing events
        EXPECTED: Racing events are created
        """
        prices = {0: '1/2', 1: '2/3'}
        selection_ids = self.ob_config.add_UK_racing_event(number_of_runners=2, time_to_start=1, lp_prices=prices).selection_ids
        self.selection_ids.append(list(selection_ids.values())[0])

        selection_ids = self.ob_config.add_UK_racing_event(number_of_runners=2, time_to_start=1, lp_prices=prices).selection_ids
        self.__class__.selection_ids.append(list(selection_ids.values())[0])

    def test_001_add_selections(self):
        """
        DESCRIPTION: Add selections to Betslip
        EXPECTED: Selections are added to Betslip
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)

    def test_002_click_acca_notification(self):
        """
        DESCRIPTION: Close betslip and click on ACCA notification
        EXPECTED: Betslip is closed, ACCA banner is shown and user is able to click on its odds
        """
        self.site.close_betslip()
        self.site.acca_notification.odds.click()

    def test_003_verify_ACCA_tracking(self):
        """
        DESCRIPTION: Verify tracking JSON
        EXPECTED: Expected response contains the following fields: 'eventAction': 'click ' and 'eventLabel': 'odds notification banner'
        """
        expected_response = {
            'event': 'trackEvent',
            'eventAction': 'click ',
            'eventLabel': 'odds notification banner'
        }
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel',
                                                              object_value='odds notification banner')
        self.compare_json_response(actual_response, expected_response)
