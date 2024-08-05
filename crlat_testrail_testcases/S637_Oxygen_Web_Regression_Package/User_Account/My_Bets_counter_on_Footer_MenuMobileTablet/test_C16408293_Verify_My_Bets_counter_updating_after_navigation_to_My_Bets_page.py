import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C16408293_Verify_My_Bets_counter_updating_after_navigation_to_My_Bets_page(Common):
    """
    TR_ID: C16408293
    NAME: Verify My Bets counter updating after navigation to My Bets page
    DESCRIPTION: This test case verifies that correct My Bets counter is displayed after navigation to My Bets page
    PRECONDITIONS: - Load Oxygen/Roxanne Application
    PRECONDITIONS: - Make sure user has open (unsettled) bets
    PRECONDITIONS: - Make sure 'BetsCounter' config is turned on in CMS > System configurations
    PRECONDITIONS: - My Bets option is present and active in the top 5 list in Menus > Footer menus in CMS https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    """
    keep_browser_open = True

    def test_001_navigate_to_my_bets_page(self):
        """
        DESCRIPTION: Navigate to My Bets page
        EXPECTED: - Open bets tab is opened
        EXPECTED: - Open bets are present
        """
        pass

    def test_002_verify_displaying_correct_my_bets_counter_when_number_of_my_bets_has_changed_after_cash_out(self):
        """
        DESCRIPTION: Verify displaying correct My Bets counter when number of My bets has changed after Cash Out
        EXPECTED: - My bets badge' icon is changed the number of unsettled bets in real time for Cash-out.
        EXPECTED: - Back-end request is send to BPP if 20+ bets is still present after cash-out (verify with *count?* search in devtools XHR tab)
        EXPECTED: - Back-end request is not send to BPP if less than 20 bets is still present after cash-out (verify with *count?* search in devtools XHR tab)
        """
        pass

    def test_003_verify_displaying_correct_my_bets_counter_when_number_of_my_bets_has_changed_after_settling_of_the_users_bet(self):
        """
        DESCRIPTION: Verify displaying correct My Bets counter when number of My bets has changed after Settling of the user's bet
        EXPECTED: - My bets counter icon is changed the number of unsettled bets after navigation to other tab and back to Open bets for Settled Bets or New Bet added
        """
        pass
