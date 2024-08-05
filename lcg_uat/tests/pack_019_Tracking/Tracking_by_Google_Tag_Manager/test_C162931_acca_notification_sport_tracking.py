import pytest

from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.google_analytics
@pytest.mark.acca
@pytest.mark.other
@pytest.mark.low
@vtest
class Test_C162931_Verify_Acca_Notification_Sport_Tracking(BaseDataLayerTest, BaseBetSlipTest):
    """
    TR_ID: C162931
    VOL_ID: C9697594
    NAME: Verify ACCA Odds Notification Tracking (Mobile)
    DESCRIPTION: This test case verifies ACCA Odds Notification Tracking for sport (Mobile)
    """
    keep_browser_open = True
    selection_ids = []

    def test_000_add_event(self):
        """
        DESCRIPTION: Add 'Football' events
        EXPECTED: Football events are added
        """
        start_time = self.get_date_time_formatted_string(seconds=20)
        selection_ids = self.ob_config.add_autotest_premier_league_football_event(is_live=True, start_time=start_time, timeout=30).selection_ids
        self.selection_ids.append(selection_ids['Draw'])

        selection_ids = self.ob_config.add_autotest_premier_league_football_event().selection_ids
        self.selection_ids.append(selection_ids['Draw'])

        selection_ids = self.ob_config.add_autotest_premier_league_football_event().selection_ids
        self.__class__.selection_ids.append(selection_ids['Draw'])

    def test_001_add_selections(self):
        """
        DESCRIPTION: Add selections to Betslip and open it
        EXPECTED: Betslip is opened and selections are added to Betslip
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)

    def test_002_click_acca_notification(self):
        """
        DESCRIPTION: Close betslip and click on ACCA notification
        EXPECTED: ACCA banner is shown and user is able to click on banner
        """
        self.get_betslip_content()
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
        self._logger.debug(f'Actual response is: {actual_response}')
        self.compare_json_response(actual_response, expected_response)
