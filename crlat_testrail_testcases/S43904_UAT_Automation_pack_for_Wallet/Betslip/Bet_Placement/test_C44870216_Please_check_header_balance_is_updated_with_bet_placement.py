import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C44870216_Please_check_header_balance_is_updated_with_bet_placement(Common):
    """
    TR_ID: C44870216
    NAME: Please check header balance is updated with bet placement
    DESCRIPTION: this test case verify header balance updation
    PRECONDITIONS: UserName: goldenbuild1  Password: password1
    """
    keep_browser_open = True

    def test_001_launch_oxygen_application(self):
        """
        DESCRIPTION: Launch oxygen application
        EXPECTED: HomePage opened
        """
        pass

    def test_002_add__any_selection_to_qickbetbetslip(self):
        """
        DESCRIPTION: Add  any selection to QickBet/Betslip
        EXPECTED: Selection added
        """
        pass

    def test_003_verify_the_header_balance_before_placing_bet(self):
        """
        DESCRIPTION: Verify the header balance before placing bet
        EXPECTED: Balance verified
        """
        pass

    def test_004_verify_the_header_balance_after_placing_bet(self):
        """
        DESCRIPTION: Verify the header balance after placing bet
        EXPECTED: Balance updated successfully
        """
        pass
