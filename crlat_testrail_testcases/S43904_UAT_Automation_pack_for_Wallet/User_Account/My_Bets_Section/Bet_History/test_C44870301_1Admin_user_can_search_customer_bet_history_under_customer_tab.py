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
class Test_C44870301_1Admin_user_can_search_customer_bet_history_under_customer_tab(Common):
    """
    TR_ID: C44870301
    NAME: 1.Admin user can search customer bet history under customer tab
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_go_to_the_traders_interface_and_click_on_customer(self):
        """
        DESCRIPTION: Go to the Trader's Interface and click on Customer
        EXPECTED: You should be in the Customer section of TI
        """
        pass

    def test_002_type_in_a_username_and_click_on_search(self):
        """
        DESCRIPTION: Type in a username and click on Search
        EXPECTED: You should be shown a section which says Search results
        """
        pass

    def test_003_click_on_your_username(self):
        """
        DESCRIPTION: Click on your username
        EXPECTED: You should be on a page showing your user's details and the following sections:
        EXPECTED: 1. Details
        EXPECTED: 2. Notes
        EXPECTED: 3. P/L Settlement (Settled Bets Only)
        EXPECTED: 4. Annual P/L Statement
        EXPECTED: 5. Bet History
        EXPECTED: 6. Manual Adjustments
        """
        pass

    def test_004_click_on_bet_history_and_check_that_you_are_shown_you_bet_history(self):
        """
        DESCRIPTION: Click on Bet History and check that you are shown you bet history
        EXPECTED: You should be shown your bet history
        """
        pass
