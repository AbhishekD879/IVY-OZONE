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
class Test_C237299_Logic_for_sPRICE_notification(Common):
    """
    TR_ID: C237299
    NAME: Logic for sPRICE notification
    DESCRIPTION: This test case verifies new logic of triggering getBetDetail request after sPRICE notification on My bets tab on Event Details page
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

    def test_002_change_numerator_value_in_price_field_for_selection_and_save_changes(self):
        """
        DESCRIPTION: Change **numerator** value in **'Price'** field for selection and save changes
        EXPECTED: 
        """
        pass

    def test_003_navigate_to_previously_opened_my_bets_tab_on_event_details_page_and_verify_network_tab(self):
        """
        DESCRIPTION: Navigate to previously opened My bets tab on Event Details page and verify Network tab
        EXPECTED: * sPRICE notification from Liveserve with **'lp_num'** attribute updated is received
        EXPECTED: * getBetDetail request is triggered
        """
        pass

    def test_004_navigate_to_backoffice_page_with_selection_of_event_chosen_for_testing(self):
        """
        DESCRIPTION: Navigate to backoffice page with selection of event chosen for testing
        EXPECTED: 
        """
        pass

    def test_005_change_denumerator_value_in_price_field_for_selection_and_save_changes(self):
        """
        DESCRIPTION: Change **denumerator** value in **'Price'** field for selection and save changes
        EXPECTED: 
        """
        pass

    def test_006_navigate_to_previously_opened_my_bets_tab_on_event_details_page_and_verify_network_tab(self):
        """
        DESCRIPTION: Navigate to previously opened My bets tab on Event Details page and verify Network tab
        EXPECTED: * sPRICE notification from Liveserve with **'lp_den'** attribute updated is received
        EXPECTED: * getBetDetail request is triggered
        """
        pass
