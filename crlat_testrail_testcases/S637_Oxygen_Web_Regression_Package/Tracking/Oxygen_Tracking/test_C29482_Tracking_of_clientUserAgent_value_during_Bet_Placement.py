import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C29482_Tracking_of_clientUserAgent_value_during_Bet_Placement(Common):
    """
    TR_ID: C29482
    NAME: Tracking of clientUserAgent value during Bet Placement
    DESCRIPTION: This test case verifies tracking of **clientUserAgent **value during **Bet Placement**.
    DESCRIPTION: **Jira tickets: **
    DESCRIPTION: *   BMA-8963 Tracking bet placement for Native
    DESCRIPTION: *   BMA-9212 Tracking bet placement for Web HTML5
    PRECONDITIONS: *   Use is logged in
    PRECONDITIONS: *   User is able to place a bet (user is not suspended and has a positive balance)
    PRECONDITIONS: *   List of all supported devices should be covered
    PRECONDITIONS: *   Guide "[How to debug emulator, real iOS and Android devices][1]"
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/MOB/How+to+debug+emulator%2C+real+iOS+and+Android+devices
    """
    keep_browser_open = True

    def test_001_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip
        EXPECTED: Selection is added
        """
        pass

    def test_002_open_betslip_slideoutwidget(self):
        """
        DESCRIPTION: Open 'Betslip' slideout/widget
        EXPECTED: 'Bet Slip' slideout/widget is opened
        EXPECTED: **Note**: It's recommended to clear history in Developer tools before next step. It would be easier to find request needed.
        """
        pass

    def test_003_enter_stake_value_and_tap_bet_now_button(self):
        """
        DESCRIPTION: Enter "Stake" value and tap 'Bet Now' button
        EXPECTED: The Bet is successfully placed
        """
        pass

    def test_004_in_developer_tools_go_to_network_tab_resources_on_macbook___xhr_tab(self):
        """
        DESCRIPTION: In Developer tools: Go to 'Network' tab ('Resources' on Macbook) -> 'XHR' tab
        EXPECTED: 
        """
        pass

    def test_005_search_for_request_with_name_placebets(self):
        """
        DESCRIPTION: Search for request with name** "placeBets"**
        EXPECTED: 2 requests are shown
        """
        pass

    def test_006_in_one_of_these_2_requests_open_preview_tab_note_sometimes_page_refresh_is_needed_to_make_it_workand_check_the_clientuseragent_parameter_sent(self):
        """
        DESCRIPTION: In one of these 2 requests open '**Preview**' tab (Note: sometimes page refresh is needed to make it work) and check the  '**clientUserAgent**' parameter sent
        EXPECTED: This parameter should be present:
        EXPECTED: *   If the customer places a bet on BMA Mobile (**HTML5**), the clientUserAgent: "**6000**"​
        EXPECTED: *   If the customer places a bet on **iOS Wrapper** of BMA Mobile, the clientUserAgent: "**BMANATIVE**"
        EXPECTED: *   If the customer places a bet on **Android Wrapper** of BMA Mobile, the clientUserAgent: "**BMANATIVE**"
        EXPECTED: *   If the customer places a bet on **Windows Wrapper** of BMA Mobile, the clientUserAgent: "**BMANATIVE**"
        """
        pass
