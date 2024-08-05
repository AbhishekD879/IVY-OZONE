import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.cash_out
@vtest
class Test_C237296_Logic_for_sEVENT_notification(Common):
    """
    TR_ID: C237296
    NAME: Logic for sEVENT notification
    DESCRIPTION: This test case verifies new logic of triggering getBetDetail request after sEVENT notification on My bets tab on Event Details page
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: [BMA-15775 (Logic of when to make getBetDetail requests after receiving a message from Liveserv: sEVENT)] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-15775
    DESCRIPTION: NOTE: to be archived after release of [BMA-55051 Remove support of old cashout flow][1]
    DESCRIPTION: [1]:https://jira.egalacoral.com/browse/BMA-55051
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User has placed single and multiple cashout available bets
    PRECONDITIONS: * User is on My bets tab on Event Details page of chosen event
    PRECONDITIONS: * Web console with Network tab is opened
    PRECONDITIONS: * Backoffice link for event is opened for triggering LiveServe notifications: http://backoffice-tst2.coral.co.uk/ti/hierarchy/event/<Event_ID>
    PRECONDITIONS: NOTE: Cashout microservice should be turned off in CMS (System configuration> CashOut> isV4Enabled not checked)
    """
    keep_browser_open = True

    def test_001_navigate_to_backoffice_page_with_event_chosen_for_testing(self):
        """
        DESCRIPTION: Navigate to backoffice page with event chosen for testing
        EXPECTED: 
        """
        pass

    def test_002_change_status_value_of_event_and_save_changes(self):
        """
        DESCRIPTION: Change **'Status'** value of event and save changes
        EXPECTED: 
        """
        pass

    def test_003_navigate_to_previously_opened_my_bets_tab_on_event_details_page_and_verify_network_tab(self):
        """
        DESCRIPTION: Navigate to previously opened My bets tab on Event Details page and verify Network tab
        EXPECTED: * sEVENT notification from Liveserve with **'status'** attribute updated is received
        EXPECTED: * getBetDetail request is triggered
        """
        pass

    def test_004_verify_front_end_behaviour_of_bet_line(self):
        """
        DESCRIPTION: Verify front end behaviour of bet line
        EXPECTED: Bet is shown as suspended/active
        """
        pass

    def test_005_navigate_to_backoffice_page_with_event_chosen_for_testing(self):
        """
        DESCRIPTION: Navigate to backoffice page with event chosen for testing
        EXPECTED: 
        """
        pass

    def test_006_change_displayed_value_of_event_and_save_changes(self):
        """
        DESCRIPTION: Change **'Displayed'** value of event and save changes
        EXPECTED: 
        """
        pass

    def test_007_navigate_to_previously_opened_my_bets_tab_on_event_details_page_and_verify_network_tab(self):
        """
        DESCRIPTION: Navigate to previously opened My bets tab on Event Details page and verify Network tab
        EXPECTED: * sEVENT notification from Liveserve with **'displayed'** attribute updated is received
        EXPECTED: * getBetDetail request is triggered
        """
        pass

    def test_008_navigate_to_backoffice_page_with_event_chosen_for_testing(self):
        """
        DESCRIPTION: Navigate to backoffice page with event chosen for testing
        EXPECTED: 
        """
        pass

    def test_009_change_some_values_for_event_other_than_status_or_displayedeg_disporder_or_start_time_and_save_changes(self):
        """
        DESCRIPTION: Change some value(s) for event **other than 'Status' or 'Displayed'**(e.g. Disporder or Start Time) and save changes
        EXPECTED: 
        """
        pass

    def test_010_navigate_to_previously_opened_my_bets_tab_on_event_details_page_and_verify_network_tab(self):
        """
        DESCRIPTION: Navigate to previously opened My bets tab on Event Details page and verify Network tab
        EXPECTED: * sEVENT notification from Liveserve with updated attribute(s) is received
        EXPECTED: * getBetDetail request is **NOT** triggered
        """
        pass
