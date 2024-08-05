import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.user_account
@vtest
class Test_C14876462_Vanilla_No_Odds_Bocoost_available(Common):
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
        self.site.login(username=tests.settings.no_odds_boost_token_user)

    def test_002_navigate_to_offers__free_bets_menu(self):
        """
        DESCRIPTION: Navigate to 'OFFERS & FREE BETS' menu
        EXPECTED: There is no 'Odds Boost' counter next to 'ODDS BOOST'
        """
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='"Right menu" is not opened')
        odds_boost_item = self.site.right_menu.items_as_ordered_dict.get(
            vec.bma.EXPECTED_RIGHT_MENU.odds_boosts)
        self.assertTrue(odds_boost_item, msg='"Odds Boost" item is not present in righrt menu.')
        self.assertEqual("", odds_boost_item.badge_text, msg='"ODDS BOOST" count is not empty as expected')
