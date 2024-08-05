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
class Test_C2779915_Verify_displaying_odds_boost_button_in_the_betslip_for_logged_out_user(Common):
    """
    TR_ID: C2779915
    NAME: Verify displaying odds boost button in the betslip for logged out user
    DESCRIPTION: Verify displaying odds boost button in the betslip (Single selections) for logged out user
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Load application
    PRECONDITIONS: Do NOT login
    PRECONDITIONS: Add a single selection with added Stake to the Betslip
    """
    keep_browser_open = True

    def test_001_navigate_to_betslipverify_that_odds_boost_button_is_not_shown_in_betslip(self):
        """
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that odds boost button is NOT shown in Betslip
        EXPECTED: 'BOOST' button is NOT shown in Betslip
        """
        pass

    def test_002_add_one_more_selection_and_navigate_to_betslipverify_that_odds_boost_button_is_not_shown_in_betslip(self):
        """
        DESCRIPTION: Add one more selection and navigate to Betslip
        DESCRIPTION: Verify that odds boost button is NOT shown in Betslip
        EXPECTED: 'BOOST' button is NOT shown in Betslip
        """
        pass
