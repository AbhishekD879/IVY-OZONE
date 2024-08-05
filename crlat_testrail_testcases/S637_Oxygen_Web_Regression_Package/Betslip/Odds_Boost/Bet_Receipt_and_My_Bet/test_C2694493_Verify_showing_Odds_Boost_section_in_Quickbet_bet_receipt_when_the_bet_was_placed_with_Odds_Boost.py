import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C2694493_Verify_showing_Odds_Boost_section_in_Quickbet_bet_receipt_when_the_bet_was_placed_with_Odds_Boost(Common):
    """
    TR_ID: C2694493
    NAME: Verify showing Odds Boost section in Quickbet bet receipt when the bet was placed with Odds Boost
    DESCRIPTION: This test case verifies displaying of Odds Boost section in Quickbet bet receipt when the bet was placed with odds boost
    PRECONDITIONS: 'Odds Boost' Feature Toggle is enabled in CMS
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office
    PRECONDITIONS: How to add Odds boost token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Load application and Login into the application
    PRECONDITIONS: Add selection with Odds Boost token available  to Quickbet
    PRECONDITIONS: Boost the Odds
    PRECONDITIONS: Place a Bet
    """
    keep_browser_open = True

    def test_001_verify_that_odds_boost_taken_by_the_user_is_displayed_in_quickbet_receipt(self):
        """
        DESCRIPTION: Verify that Odds Boost taken by the user is displayed in Quickbet receipt
        EXPECTED: - The boost odds taken by the user is displayed
        EXPECTED: - The bet receipt confirms the bet has been boosted through an icon and line of hardcoded text  "This bet has been boosted!"
        """
        pass
