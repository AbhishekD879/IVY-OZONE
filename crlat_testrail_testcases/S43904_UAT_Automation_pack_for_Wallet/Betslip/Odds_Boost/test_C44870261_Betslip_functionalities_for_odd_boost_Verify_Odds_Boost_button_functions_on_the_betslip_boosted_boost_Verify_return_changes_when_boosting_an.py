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
class Test_C44870261_Betslip_functionalities_for_odd_boost_Verify_Odds_Boost_button_functions_on_the_betslip_boosted_boost_Verify_return_changes_when_boosting_and_unboosting_Verify_boosting_boosted_price_appears_with_the_animation_also_shows_the_previous_price_v(Common):
    """
    TR_ID: C44870261
    NAME: "Betslip functionalities for odd boost -Verify Odds Boost button functions on the betslip (boosted/boost) -Verify return changes when boosting and unboosting -Verify boosting boosted price appears with the animation (also shows the previous price , v
    DESCRIPTION: "Betslip functionalities for odd boost
    DESCRIPTION: -Verify Odds Boost button functions on the betslip (boosted/boost)
    DESCRIPTION: -Verify return changes when boosting and unboosting
    DESCRIPTION: -Verify boosting boosted price appears with the animation (also shows the previous price , verify for decimal and fraction both)
    DESCRIPTION: -Verify Odds Boost Betslip - Info icon and tooltip ('i' icon is tappable and user sees tool tip when tapping only, verify tooltip close)"
    PRECONDITIONS: User should be logged in
    """
    keep_browser_open = True

    def test_001_verify_odds_boost_button_functions_on_the_betslip_boostedboost(self):
        """
        DESCRIPTION: Verify Odds Boost button functions on the betslip (boosted/boost)
        EXPECTED: Odds should be boosted when user clicks on the Odds
        """
        pass

    def test_002_verify_boosting_boosted_price_appears_with_the_animation_verify_for_decimal_and_fraction_both(self):
        """
        DESCRIPTION: Verify boosting boosted price appears with the animation, verify for decimal and fraction both
        EXPECTED: Boosted price appears with the animation (also shows the previous price , )
        """
        pass

    def test_003_verify_return_changes_when_boosting_and_unboosting(self):
        """
        DESCRIPTION: Verify return changes when boosting and unboosting
        EXPECTED: Boosted odds when unboosted should display the boost symbol
        """
        pass

    def test_004_verify_odds_boost_betslip(self):
        """
        DESCRIPTION: Verify Odds Boost Betslip
        EXPECTED: Odds Boost- Info icon and tooltip ('i' icon is tappable and user sees tool tip when tapping only, verify tooltip close)"
        """
        pass
