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
class Test_C76929_Logic_for_sSELCN_notification(Common):
    """
    TR_ID: C76929
    NAME: Logic for sSELCN notification
    DESCRIPTION: This test case verifies new logic of triggering getBetDetail request after sSELCN notification on Cash Out tab
    DESCRIPTION: NOTE: to be archived after release of [BMA-55051 Remove support of old cashout flow][1]
    DESCRIPTION: [1]:https://jira.egalacoral.com/browse/BMA-55051
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User has placed single and multiple cashout available bets
    PRECONDITIONS: * User is on Cash Out tab
    PRECONDITIONS: * Web console with Network tab is opened
    PRECONDITIONS: * Backoffice link for selection of event is opened for triggering LiveServe notifications: http://backoffice-tst2.coral.co.uk/ti/hierarchy/selection/<selection_ID>
    PRECONDITIONS: * Test case should be run for single and multiple bets
    PRECONDITIONS: NOTE: Cashout microservice should be turned off in CMS (System configuration> CashOut> isV4Enabled not checked)
    PRECONDITIONS: Should be run on:
    PRECONDITIONS: - Cash Out tab;
    PRECONDITIONS: - Open Bets tab;
    PRECONDITIONS: - Bet History;
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

    def test_003_navigate_to_previously_opened_cash_out_tab_and_verify_network_tab(self):
        """
        DESCRIPTION: Navigate to previously opened Cash Out tab and verify Network tab
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

    def test_007_navigate_to_previously_opened_cash_out_tab_and_verify_network_tab(self):
        """
        DESCRIPTION: Navigate to previously opened Cash Out tab and verify Network tab
        EXPECTED: * sSELCN notification from Liveserve with **'displayed'** attribute updated is received
        EXPECTED: * getBetDetail request is triggered
        """
        pass

    def test_008_verify_front_end_behaviour_of_bet_line(self):
        """
        DESCRIPTION: Verify front end behaviour of bet line
        EXPECTED: Bet is shown as suspended/active
        """
        pass

    def test_009_navigate_to_backoffice_page_with_selection_of_event_chosen_for_testing(self):
        """
        DESCRIPTION: Navigate to backoffice page with selection of event chosen for testing
        EXPECTED: 
        """
        pass

    def test_010_change_numerator_value_in_price_field_for_selection_and_save_changes(self):
        """
        DESCRIPTION: Change **numerator** value in **'Price'** field for selection and save changes
        EXPECTED: 
        """
        pass

    def test_011_navigate_to_previously_opened_cash_out_tab_and_verify_network_tab(self):
        """
        DESCRIPTION: Navigate to previously opened Cash Out tab and verify Network tab
        EXPECTED: * sSELCN notification from Liveserve with **'lp_num'** attribute updated is received
        EXPECTED: * getBetDetail request is triggered
        """
        pass

    def test_012_navigate_to_backoffice_page_with_selection_of_event_chosen_for_testing(self):
        """
        DESCRIPTION: Navigate to backoffice page with selection of event chosen for testing
        EXPECTED: 
        """
        pass

    def test_013_change_denominator_value_in_price_field_for_selection_and_save_changes(self):
        """
        DESCRIPTION: Change **denominator** value in **'Price'** field for selection and save changes
        EXPECTED: 
        """
        pass

    def test_014_navigate_to_previously_opened_cash_out_tab_and_verify_network_tab(self):
        """
        DESCRIPTION: Navigate to previously opened Cash Out tab and verify Network tab
        EXPECTED: * sSELCN notification from Liveserve with **'lp_den'** attribute updated is received
        EXPECTED: * getBetDetail request is triggered
        """
        pass

    def test_015_navigate_to_backoffice_page_with_selection_of_event_chosen_for_testing(self):
        """
        DESCRIPTION: Navigate to backoffice page with selection of event chosen for testing
        EXPECTED: 
        """
        pass

    def test_016_set_results_for_selection_and_save_changes(self):
        """
        DESCRIPTION: **Set results** for selection and save changes
        EXPECTED: 
        """
        pass

    def test_017_navigate_to_previously_opened_cash_out_tab_and_verify_network_tab(self):
        """
        DESCRIPTION: Navigate to previously opened Cash Out tab and verify Network tab
        EXPECTED: * sSELCN notification from Liveserve with **'settled'** attribute updated is received
        EXPECTED: * getBetDetail request is triggered
        """
        pass

    def test_018_navigate_to_backoffice_page_with_selection_of_event_chosen_for_testing(self):
        """
        DESCRIPTION: Navigate to backoffice page with selection of event chosen for testing
        EXPECTED: 
        """
        pass

    def test_019_change_some_values_for_selection_other_than_status_or_displayed_or_settled_or_lp_num_or_lp_den_eg_disporder_and_save_changes(self):
        """
        DESCRIPTION: Change some value(s) for selection **other than 'Status' or 'Displayed' or 'Settled' or 'lp_num' or lp_den** (e.g. Disporder) and save changes
        EXPECTED: 
        """
        pass

    def test_020_navigate_to_previously_opened_cash_out_tab_and_verify_network_tab(self):
        """
        DESCRIPTION: Navigate to previously opened Cash Out tab and verify Network tab
        EXPECTED: * sSELCN notification from Liveserve with updated attribute(s) is received
        EXPECTED: * getBetDetail request is **NOT** triggered
        """
        pass
