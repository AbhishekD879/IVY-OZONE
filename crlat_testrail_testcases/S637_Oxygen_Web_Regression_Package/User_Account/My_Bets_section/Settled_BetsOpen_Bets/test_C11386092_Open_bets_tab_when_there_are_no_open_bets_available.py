import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.user_account
@vtest
class Test_C11386092_Open_bets_tab_when_there_are_no_open_bets_available(Common):
    """
    TR_ID: C11386092
    NAME: 'Open bets' tab when there are no open bets available
    DESCRIPTION: This test case verifies text and ''Start betting'(Coral)/'Go betting'(Ladbrokes) button in Open bets tab
    DESCRIPTION: Design:
    DESCRIPTION: Coral: https://app.zeplin.io/project/5be15c714af2fc23b84d2fd3/screen/5c4f0e0920f1230172b7f095
    DESCRIPTION: Ladbrokes: https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b/screen/5c4f22d544fe0d63959b3162
    PRECONDITIONS: User is logged in;
    PRECONDITIONS: User has no open bets available
    """
    keep_browser_open = True

    def test_001_navigate_to_open_bets_tab_on_my_bets_page_bet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Open bets' tab on 'My Bets' page/ 'Bet Slip' widget
        EXPECTED: 'Open bets' tab has opened
        """
        pass

    def test_002_verify_open_bets_tab(self):
        """
        DESCRIPTION: Verify 'Open bets' tab
        EXPECTED: Text 'You currently have no open bets ' is present
        EXPECTED: Button 'Start betting'(Coral)/'Go betting'(Ladbrokes) is displayed according to design
        """
        pass

    def test_003_tap_start_bettinggo_betting_button(self):
        """
        DESCRIPTION: Tap 'Start betting'/'Go betting' button
        EXPECTED: User is redirected to the Home page
        """
        pass
