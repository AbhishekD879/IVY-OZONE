import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C14876462_Vanilla_No_Odds_Boost_available(Common):
    """
    TR_ID: C14876462
    NAME: [Vanilla] No Odds Boost available
    DESCRIPTION: This test case verifies Odds Boost menu item behaviour when there are no Odds Boost available to the user
    PRECONDITIONS: User has no Odds Boost available
    """
    keep_browser_open = True

    def test_001_login_to_the_account_with_no_odds_boost_available(self):
        """
        DESCRIPTION: Login to the account with no Odds Boost available
        EXPECTED: User is logged in
        """
        pass

    def test_002_navigate_to_offers__free_bets_menu(self):
        """
        DESCRIPTION: Navigate to 'OFFERS & FREE BETS' menu
        EXPECTED: There is no 'Odds Boost' counter next to 'ODDS BOOST'
        """
        pass
