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
class Test_C44870228_Acca_Insurance__Verify_upsell_messaging_with_different_parameters(Common):
    """
    TR_ID: C44870228
    NAME: Acca Insurance - Verify upsell messaging with different parameters
    DESCRIPTION: 
    PRECONDITIONS: Football only.
    PRECONDITIONS: Preplay only.
    PRECONDITIONS: W-D-W only
    PRECONDITIONS: 5+ selections minimum.
    PRECONDITIONS: Valid on only 1st acca placed during the day.
    PRECONDITIONS: Minimum selection price 1/10.
    PRECONDITIONS: Minimum acca price 3/1.
    PRECONDITIONS: Up to Â£10 returned if 1 selection lets you down as a free bet
    """
    keep_browser_open = True

    def test_001_user_launches_the_siteapp_and_logs_in(self):
        """
        DESCRIPTION: User launches the site/app and logs in
        EXPECTED: User can able to place a bet as logged in customers
        """
        pass

    def test_002_user_adds_4_selections_in_the_bet_slip(self):
        """
        DESCRIPTION: User adds 4 selections in the bet slip
        EXPECTED: User has added 4 selections in the bet slip
        """
        pass

    def test_003_user_adds_a_fifth_selection_to_the_bet_slip_from_any_other_parametereg__take_horse_race(self):
        """
        DESCRIPTION: User adds a fifth selection to the bet slip from Any other parameter(Eg : Take Horse race)
        EXPECTED: A new selection has been selected and added to bet slip
        """
        pass

    def test_004_check_user_is_able_to_see_the_acca_insurance_or_not(self):
        """
        DESCRIPTION: Check user is able to see the Acca Insurance or not.
        EXPECTED: User should not see the Acca Insurance acca insurance qualify message' when parameters are different which is not qualify for acca insurance
        """
        pass
