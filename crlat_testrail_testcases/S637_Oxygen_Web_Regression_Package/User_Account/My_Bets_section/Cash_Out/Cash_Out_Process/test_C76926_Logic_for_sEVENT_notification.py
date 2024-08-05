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
class Test_C76926_Logic_for_sEVENT_notification(Common):
    """
    TR_ID: C76926
    NAME: Logic for sEVENT notification
    DESCRIPTION: This test case verifies new logic of triggering getBetDetail request after sEVENT notification on Cash Out tab
    DESCRIPTION: NOTE: to be archived after release of [BMA-55051 Remove support of old cashout flow][1]
    DESCRIPTION: [1]:https://jira.egalacoral.com/browse/BMA-55051
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User has placed single and multiple cashout available bets
    PRECONDITIONS: * User is on Cash Out tab
    PRECONDITIONS: * Web console with Network tab is opened
    PRECONDITIONS: * Backoffice link for event is opened for triggering LiveServe notifications: http://backoffice-tst2.coral.co.uk/ti/hierarchy/event/<Event_ID>
    PRECONDITIONS: * Test case should be run for single and multiple bets
    PRECONDITIONS: NOTE: Cashout microservice should be turned off in CMS (System configuration> CashOut> isV4Enabled not checked)
    PRECONDITIONS: Should be run on:
    PRECONDITIONS: - Cash Out tab;
    PRECONDITIONS: - Open Bets tab;
    PRECONDITIONS: - Bet History;
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

    def test_003_navigate_to_previously_opened_cash_out_tab_and_verify_network_tab(self):
        """
        DESCRIPTION: Navigate to previously opened Cash Out tab and verify Network tab
        EXPECTED: * sEVENT notification from Liveserve with **'status'** attribute updated is received
        EXPECTED: * getBetDetail request is triggered
        """
        pass

    def test_004_verify_front_end_behaviour_of_bet_line(self):
        """
        DESCRIPTION: Verify front end behaviour of bet line
        EXPECTED: Bet is shown as suspended/active (depends on received **cashoutStatus** in getbetDetail response)
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

    def test_007_navigate_to_previously_opened_cash_out_tab_and_verify_network_tab(self):
        """
        DESCRIPTION: Navigate to previously opened Cash Out tab and verify Network tab
        EXPECTED: * sEVENT notification from Liveserve with **'displayed'** attribute updated is received
        EXPECTED: * getBetDetail request is triggered
        """
        pass

    def test_008_verify_front_end_behaviour_of_bet_line(self):
        """
        DESCRIPTION: Verify front end behaviour of bet line
        EXPECTED: Bet is shown as suspended/active
        """
        pass

    def test_009_navigate_to_backoffice_page_with_event_chosen_for_testing(self):
        """
        DESCRIPTION: Navigate to backoffice page with event chosen for testing
        EXPECTED: 
        """
        pass

    def test_010_change_some_values_for_event_other_than_status_or_displayedeg_disporder_or_start_time_and_save_changes(self):
        """
        DESCRIPTION: Change some value(s) for event **other than 'Status' or 'Displayed'**(e.g. Disporder or Start Time) and save changes
        EXPECTED: 
        """
        pass

    def test_011_navigate_to_previously_opened_cash_out_page_and_verify_network_tab(self):
        """
        DESCRIPTION: Navigate to previously opened Cash Out page and verify Network tab
        EXPECTED: * sEVENT notification from Liveserve with updated attribute(s) is received
        EXPECTED: * getBetDetail request is **NOT** triggered
        """
        pass
