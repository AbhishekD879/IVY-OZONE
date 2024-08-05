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
class Test_C2844605_Verify_displaying_Odds_Boost_token_value_in_Right_menu(Common):
    """
    TR_ID: C2844605
    NAME: Verify displaying Odds Boost token value in Right menu
    DESCRIPTION: This test case verifies displaying Odds Boost token value in Right menu
    DESCRIPTION: **Autotests:**
    DESCRIPTION: Mobile - [C2990163](https://ladbrokescoral.testrail.com/index.php?/cases/view/2990163)
    PRECONDITIONS: 'Odds Boost' Feature Toggle is enabled in CMS
    PRECONDITIONS: 'Odds Boost' item is enabled in Right menu in CMS
    PRECONDITIONS: Add Odds Boost token to Any bet to the user
    PRECONDITIONS: How to add Odds boost token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Generate Upcoming token in http://backoffice-tst2.coral.co.uk/office
    PRECONDITIONS: How to create Upcoming Boosts https://confluence.egalacoral.com/display/SPI/How+to+create+Upcoming+Boosts
    PRECONDITIONS: Load application and Login into the application with user that has Odds Boost tokens available
    """
    keep_browser_open = True

    def test_001_navigate_to_the_right_menu_and_verify_that_summary_value_of_the_number_of_odds_boost_tokens_is_available(self):
        """
        DESCRIPTION: Navigate to the Right menu and verify that summary value of the number of Odds Boost tokens is available
        EXPECTED: - Right menu is expanded
        EXPECTED: - Odds Boost item is available in the menu
        EXPECTED: - Summary value of the number of Odds Boost tokens is displaying in Odds Boost item
        """
        pass

    def test_002_tap_on_odds_boost_item(self):
        """
        DESCRIPTION: Tap on Odds Boost item
        EXPECTED: User is navigated to the Odds Boost information page
        """
        pass

    def test_003_tap_on_generic_odds_boost_token_which_can_be_used_on_any_bet(self):
        """
        DESCRIPTION: Tap on generic Odds Boost token which can be used on ANY bet
        EXPECTED: User is navigated to the homepage
        """
        pass

    def test_004_add_selection_to_the_betslip_boost_it_and_place_this_boosted_bet(self):
        """
        DESCRIPTION: Add selection to the betslip, boost it and place this boosted bet
        EXPECTED: Bet is placed successfully
        """
        pass

    def test_005_navigate_to_right_menu_and_verify_that_summary_value_of_the_number_of_odds_boost_tokens_decreased_on_one_digit(self):
        """
        DESCRIPTION: Navigate to Right menu and verify that summary value of the number of Odds Boost tokens decreased on one digit
        EXPECTED: Summary value of the number of Odds Boost tokens is updated according to available number of Odds Boost tokens (decreased on one digit)
        """
        pass
