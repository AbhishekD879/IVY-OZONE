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
class Test_C9315085_Verify_that_Sorry_one_of_the_selections_cannot_be_boosted_please_remove_the_selection_and_try_again_error_message_is_shown_in_Betslip(Common):
    """
    TR_ID: C9315085
    NAME: Verify that "Sorry, one of the selections cannot be boosted, please remove the selection and try again." error message is shown in Betslip
    DESCRIPTION: This test case verifies that "Sorry, one of the selections cannot be boosted, please remove the selection and try again." error message is shown in Betslip in case if one of selections is not allowed for boost
    PRECONDITIONS: Load application and login by User with odds boost token ANY available
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token - instruction for generating tokens
    PRECONDITIONS: Back office https://backoffice-tst2.coral.co.uk/ti
    """
    keep_browser_open = True

    def test_001_add_treble_selections_to_the_betslip(self):
        """
        DESCRIPTION: Add Treble selections to the Betslip
        EXPECTED: Selections are added
        """
        pass

    def test_002___add_stake_only_for_treble_selection__tap_boost_button(self):
        """
        DESCRIPTION: - Add stake only for Treble selection
        DESCRIPTION: - Tap 'Boost' button
        EXPECTED: Stake is added and boosted
        """
        pass

    def test_003___navigate_to_back_office_see_preconditions__open_event_for_the_first_selection_in_betslip__uncheck_enhanced_odds_available_check_box(self):
        """
        DESCRIPTION: - Navigate to Back Office (see preconditions)
        DESCRIPTION: - Open event for the first selection in Betslip
        DESCRIPTION: - Uncheck 'Enhanced Odds Available' check box
        EXPECTED: 'Enhanced Odds Available' is unchecked for the first selection in Betslip
        """
        pass

    def test_004___back_to_the_betslip_in_application__tap_bet_now_button_and_verify_that_error_message_is_displayed_on_the_betslip(self):
        """
        DESCRIPTION: - Back to the Betslip in application
        DESCRIPTION: - Tap 'Bet now' button and verify that error message is displayed on the betslip
        EXPECTED: Error message is displayed on the Betslip
        """
        pass

    def test_005_verify_content_of_error_message(self):
        """
        DESCRIPTION: Verify content of error message
        EXPECTED: Text: "Sorry, one of the selections cannot be boosted, please remove the selection and try again."
        """
        pass
