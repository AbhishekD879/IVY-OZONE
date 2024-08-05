import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C2496174_Floating_Bet_slip__Content_displaying_in_Open_bets_Bet_history_tabs_and_their_sub_tabs_eg_Regular_Lotto_etc(Common):
    """
    TR_ID: C2496174
    NAME: Floating Bet slip - Content displaying in 'Open bets', 'Bet history' tabs and their sub-tabs (e.g. 'Regular', 'Lotto', etc.)
    DESCRIPTION: This test case verifies content displaying in 'Open bets', 'Bet history' tabs and their sub-tabs (e.g. 'Regular', 'Lotto', etc.) when Bet Slip widget is anchored to the top of the page.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: 1. Oxygen app is loaded
    PRECONDITIONS: 2. The user is logged in
    PRECONDITIONS: 3. Bet Slip widget is located at the top of the last column
    PRECONDITIONS: 4. Bet Slip widget is expanded by default (CMS configurable: Widgets->Betslip->'Show Expanded' checkbox)
    PRECONDITIONS: 5. 'Bet slip locked' icon is displayed in the header of the bet slip, it's anchored to the top of the page
    PRECONDITIONS: 6. Bet Slip (selected by default), Cash Out, Open Bets, Bet History tabs are available in the widget
    """
    keep_browser_open = True

    def test_001_click_on_cash_out_tab(self):
        """
        DESCRIPTION: Click on 'Cash out' tab
        EXPECTED: The tab is opened with respective data
        """
        pass

    def test_002_scroll_the_page_down(self):
        """
        DESCRIPTION: Scroll the page down
        EXPECTED: * Bet Slip widget is anchored to the top of the page
        EXPECTED: * Bet Slip widget remains visible while scrolling
        EXPECTED: * Bet Slip widget overlays 'Favorites' and 'Offer' widgets if available
        EXPECTED: * Bet Slip widget stops before footer area
        """
        pass

    def test_003_verify_content_displaying_of_cash_out_tab(self):
        """
        DESCRIPTION: Verify content displaying of 'Cash out' tab
        EXPECTED: * Scrollbar appears within tab container in case content doesn't fit
        EXPECTED: * All content can be viewed/accessed by scrolling up/down
        """
        pass

    def test_004_click_on_bet_slip_locked_icon(self):
        """
        DESCRIPTION: Click on 'Bet slip locked' icon
        EXPECTED: * 'Bet slip locked' icon changes to 'Bet slip unlocked' icon
        EXPECTED: * Bet Slip widget appears at the top of the last column above any other available modules
        """
        pass

    def test_005_verify_content_displaying_of_cash_out_tab(self):
        """
        DESCRIPTION: Verify content displaying of 'Cash out' tab
        EXPECTED: The list of all bets is displayed and fully visible
        """
        pass

    def test_006_repeat_steps_1_4_for_open_bets_and_bet_history_tabs_and_their_sub_tabs_eg_regular_lotto_etc(self):
        """
        DESCRIPTION: Repeat steps 1-4 for 'Open bets' and 'Bet history' tabs and their sub-tabs (e.g. 'Regular', 'Lotto', etc.)
        EXPECTED: 
        """
        pass

    def test_007_verify_content_displaying_of_open_bets_and_bet_history_tabs_and_their_sub_tabs_eg_regular_lotto_etc(self):
        """
        DESCRIPTION: Verify content displaying of 'Open bets' and 'Bet history' tabs and their sub-tabs (e.g. 'Regular', 'Lotto', etc.)
        EXPECTED: * The list of bets is displayed
        EXPECTED: * If there are more than 20 sections, they are loaded after scrolling by portions (20 sections by portion)
        """
        pass
