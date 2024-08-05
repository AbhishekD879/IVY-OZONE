import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C11508485_No_CTA_button_in_the_Betslip_Widget_Display_on_Desktop_and_Tablet(Common):
    """
    TR_ID: C11508485
    NAME: No CTA button in the Betslip Widget Display on Desktop and Tablet
    DESCRIPTION: This test case verifies of absence CTA button in BetSlip widget on Tablets and Desktop
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User doesn't have open bets, and bets in the history
    PRECONDITIONS: Design for MOBILE:
    PRECONDITIONS: Coral: https://app.zeplin.io/project/5be15c714af2fc23b84d2fd3/screen/5c4f0e0920f1230172b7f095
    PRECONDITIONS: Ladbrokes: https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b/screen/5c4f22d544fe0d63959b3162
    """
    keep_browser_open = True

    def test_001_load_oxygen_app_on_desktoptablet_device(self):
        """
        DESCRIPTION: Load Oxygen app on desktop/tablet device
        EXPECTED: * Homepage is opened
        EXPECTED: * Bet Slip widget is located at the top of right column
        EXPECTED: * Bet Slip widget is expanded by default
        """
        pass

    def test_002_tap_cash_out_tab(self):
        """
        DESCRIPTION: Tap 'CASH OUT' tab
        EXPECTED: * CASH OUT' tab is displayed
        EXPECTED: * "You currently have no cash out bets"(CORAL)/"You currently have no bets available for cash out"(LADBROKES) message is displayed
        EXPECTED: * CTA button "START BETTING"(CORAL)/ GO BETTING(LADBROKES) isn't displayed
        """
        pass

    def test_003_tap_open_bets_tab(self):
        """
        DESCRIPTION: Tap 'OPEN BETS' tab
        EXPECTED: * 'OPEN BETS' tab is displayed
        EXPECTED: * "You currently have no open bets" message is displayed
        EXPECTED: * CTA button "START BETTING"(CORAL)/ GO BETTING(LADBROKES) isn't displayed
        """
        pass

    def test_004_tap_settled_bets_tab(self):
        """
        DESCRIPTION: Tap 'SETTLED BETS' tab
        EXPECTED: * 'SETTLED BETS' tab is displayed
        EXPECTED: * "You have no settled bets" message is displayed
        EXPECTED: * CTA button "START BETTING"(CORAL)/ GO BETTING(LADBROKES) isn't displayed
        """
        pass
