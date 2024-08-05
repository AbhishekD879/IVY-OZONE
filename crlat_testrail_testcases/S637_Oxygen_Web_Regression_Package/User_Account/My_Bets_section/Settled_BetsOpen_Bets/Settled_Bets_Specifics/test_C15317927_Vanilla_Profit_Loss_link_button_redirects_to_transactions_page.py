import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C15317927_Vanilla_Profit_Loss_link_button_redirects_to_transactions_page(Common):
    """
    TR_ID: C15317927
    NAME: [Vanilla] Profit/Loss link button redirects to transactions page
    DESCRIPTION: 
    PRECONDITIONS: User logged in to the application and is on Home page.
    """
    keep_browser_open = True

    def test_001_open_my_account___history___betting_history(self):
        """
        DESCRIPTION: Open My Account -> History -> Betting History
        EXPECTED: My Bets / Settled Bets tab section is opened
        """
        pass

    def test_002_click_on_profitloss_button(self):
        """
        DESCRIPTION: Click on Profit/Loss button
        EXPECTED: /mobileportal/transactions page is opened
        """
        pass

    def test_003_desktop_mode_go_to_home_page_check_if_see_profit__loss_button_is_displayed_in_my_bets___settled_bets_tab_on_the_right(self):
        """
        DESCRIPTION: [Desktop mode] Go to Home page, check if "See Profit / Loss" button is displayed in 'My Bets' -> 'Settled Bets' tab on the right
        EXPECTED: "See Profit / Loss" button is visible
        """
        pass

    def test_004_desktop_mode_click_on_profitloss_button(self):
        """
        DESCRIPTION: [Desktop mode] Click on Profit/Loss button
        EXPECTED: /mobileportal/transactions page is opened
        """
        pass
