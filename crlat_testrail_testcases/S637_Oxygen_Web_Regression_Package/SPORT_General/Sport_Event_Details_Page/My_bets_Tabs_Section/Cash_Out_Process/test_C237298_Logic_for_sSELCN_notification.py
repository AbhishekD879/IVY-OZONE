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
class Test_C237298_Logic_for_sSELCN_notification(Common):
    """
    TR_ID: C237298
    NAME: Logic for sSELCN notification
    DESCRIPTION: This test case verifies new logic of triggering getBetDetail request after sSELCN notification on My bets tab on Event Details page
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: [BMA-16798 (Logic of when to make getBetDetail requests after receiving a message from Liveserv: sEVMKT, sSELCN, sPRICE)] [1]
    DESCRIPTION: [1]:https://jira.egalacoral.com/browse/BMA-16798
    DESCRIPTION: NOTE: to be archived after release of [BMA-55051 Remove support of old cashout flow][1]
    DESCRIPTION: [1]:https://jira.egalacoral.com/browse/BMA-55051
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User has placed single and multiple cashout available bets
    PRECONDITIONS: * User is on My bets tab on Event Details page of chosen event
    PRECONDITIONS: * Web console with Network tab is opened
    PRECONDITIONS: * Backoffice link for selection of event is opened for triggering LiveServe notifications: http://backoffice-tst2.coral.co.uk/ti/hierarchy/selection/<selection_ID>
    PRECONDITIONS: NOTE: Cashout microservice should be turned off in CMS (System configuration> CashOut> isV4Enabled not checked)
    """
    keep_browser_open = True

    def test_001_navigate_to_backoffice_page_with_selection_of_event_chosen_for_testing(self):
        """
        DESCRIPTION: Navigate to backoffice page with selection of event chosen for testing
        EXPECTED: 
        """
        pass

    def test_002_change_status_value_of_selection_and_save_changes(self):
        """
        DESCRIPTION: Change **'Status'** value of selection and save changes
        EXPECTED: 
        """
        pass

    def test_003_navigate_to_previously_opened_my_bets_tab_on_event_details_page_and_verify_network_tab(self):
        """
        DESCRIPTION: Navigate to previously opened My bets tab on Event Details page and verify Network tab
        EXPECTED: * sSELCN notification from Liveserve with **'status'** attribute updated is received
        EXPECTED: * getBetDetail request is triggered
        """
        pass

    def test_004_verify_front_end_behaviour_of_bet_line(self):
        """
        DESCRIPTION: Verify front end behaviour of bet line
        EXPECTED: Bet is shown as suspended/active
        """
        pass

    def test_005_navigate_to_backoffice_page_with_selection_of_event_chosen_for_testing(self):
        """
        DESCRIPTION: Navigate to backoffice page with selection of event chosen for testing
        EXPECTED: 
        """
        pass

    def test_006_change_displayed_value_of_selection_and_save_changes(self):
        """
        DESCRIPTION: Change **'Displayed'** value of selection and save changes
        EXPECTED: 
        """
        pass

    def test_007_navigate_to_previously_opened_my_bets_tab_on_event_details_page_and_verify_network_tab(self):
        """
        DESCRIPTION: Navigate to previously opened My bets tab on Event Details page and verify Network tab
        EXPECTED: * sSELCN notification from Liveserve with **'displayed'** attribute updated is received
        EXPECTED: * getBetDetail request is triggered
        """
        pass

    def test_008_navigate_to_backoffice_page_with_selection_of_event_chosen_for_testing(self):
        """
        DESCRIPTION: Navigate to backoffice page with selection of event chosen for testing
        EXPECTED: 
        """
        pass

    def test_009_set_results_for_selection_and_save_changes(self):
        """
        DESCRIPTION: **Set results** for selection and save changes
        EXPECTED: 
        """
        pass

    def test_010_navigate_to_previously_opened_my_bets_tab_on_event_details_page_and_verify_network_tab(self):
        """
        DESCRIPTION: Navigate to previously opened My bets tab on Event Details page and verify Network tab
        EXPECTED: * sSELCN notification from Liveserve with **'settled'** attribute updated is received
        EXPECTED: * getBetDetail request is triggered
        """
        pass

    def test_011_navigate_to_backoffice_page_with_selection_of_event_chosen_for_testing(self):
        """
        DESCRIPTION: Navigate to backoffice page with selection of event chosen for testing
        EXPECTED: 
        """
        pass

    def test_012_change_some_values_for_selection_other_than_status_or_displayed_or_settled_or_lp_num_or_lp_den_eg_disporder_and_save_changes(self):
        """
        DESCRIPTION: Change some value(s) for selection **other than 'Status' or 'Displayed' or 'Settled' or 'lp_num' or lp_den** (e.g. Disporder) and save changes
        EXPECTED: 
        """
        pass

    def test_013_navigate_to_previously_opened_my_bets_tab_on_event_details_page_and_verify_network_tab(self):
        """
        DESCRIPTION: Navigate to previously opened My bets tab on Event Details page and verify Network tab
        EXPECTED: * sSELCN notification from Liveserve with updated attribute(s) is received
        EXPECTED: * getBetDetail request is **NOT** triggered
        """
        pass
