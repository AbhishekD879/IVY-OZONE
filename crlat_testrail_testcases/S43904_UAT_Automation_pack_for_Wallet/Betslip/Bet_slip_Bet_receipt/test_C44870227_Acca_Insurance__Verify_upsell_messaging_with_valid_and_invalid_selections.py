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
class Test_C44870227_Acca_Insurance__Verify_upsell_messaging_with_valid_and_invalid_selections(Common):
    """
    TR_ID: C44870227
    NAME: Acca Insurance - Verify upsell messaging with valid and invalid selections
    DESCRIPTION: 
    PRECONDITIONS: - Football only.
    PRECONDITIONS: - W-D-W only
    PRECONDITIONS: - 5+ selections minimum.
    PRECONDITIONS: - Valid on only 1st acca placed during the day.
    PRECONDITIONS: - Minimum selection price 1/10.
    PRECONDITIONS: - Minimum acca price 3/1.
    PRECONDITIONS: - Up to Â£10 returned if 1 selection lets you down as a freebet
    """
    keep_browser_open = True

    def test_001_launch_the_site_and_add_4_selections_to_the_bet_slip(self):
        """
        DESCRIPTION: Launch the site and add 4 selections to the Bet slip
        EXPECTED: 4 selections added to bet slip (User should see add 1 more selection to qualify for 5+ acca insurance prompt on bet slip)
        EXPECTED: Note: the acca price should be less than 2/1
        """
        pass

    def test_002_add_one_more_selection_with_price_is_less_than_110(self):
        """
        DESCRIPTION: Add one more selection with price is less than 1/10
        EXPECTED: Selection has been added to bet slip
        """
        pass

    def test_003_check_user_is_able_to_see_the_acca_insurance_or_not(self):
        """
        DESCRIPTION: Check user is able to see the Acca Insurance or not.
        EXPECTED: User should not see the "Your selections qualify for Acca Insurance" when 1 selection is less than 1/10
        """
        pass

    def test_004_add_one_selection_with_price_less_than_31(self):
        """
        DESCRIPTION: Add one selection with price less than 3/1
        EXPECTED: Added selection with price less than 3/1
        EXPECTED: Note: the acca price should be equal to or more than 3/1
        """
        pass

    def test_005_check_user_is_able_to_see_the_acca_insurance_or_not(self):
        """
        DESCRIPTION: Check user is able to see the Acca Insurance or not.
        EXPECTED: User should not see the "Your selections qualify for Acca Insurance"  when acca price is less than 3/1
        """
        pass
