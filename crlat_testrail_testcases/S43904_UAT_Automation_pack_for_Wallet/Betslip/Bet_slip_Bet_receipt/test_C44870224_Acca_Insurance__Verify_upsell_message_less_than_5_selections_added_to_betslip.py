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
class Test_C44870224_Acca_Insurance__Verify_upsell_message_less_than_5_selections_added_to_betslip(Common):
    """
    TR_ID: C44870224
    NAME: Acca Insurance - Verify upsell message less than 5 selections added to betslip
    DESCRIPTION: 
    PRECONDITIONS: Football only.
    PRECONDITIONS: W-D-W only
    PRECONDITIONS: 5+ selections minimum.
    PRECONDITIONS: Valid on only 1st acca placed during the day.
    PRECONDITIONS: Minimum selection price 1/10.
    PRECONDITIONS: Minimum acca price 3/1.
    PRECONDITIONS: Up to Â£10 returned if 1 selection lets you down as a free bet
    PRECONDITIONS: - User should login
    """
    keep_browser_open = True

    def test_001_launch_the_site_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch the site and login with valid credentials.
        EXPECTED: User is logged in
        """
        pass

    def test_002_add_less_than_5_selections_to_bet_slip(self):
        """
        DESCRIPTION: Add less than 5 selections to bet slip
        EXPECTED: Selections is added to bet slip
        """
        pass

    def test_003_go_to_bet_slip_page(self):
        """
        DESCRIPTION: Go to bet slip page
        EXPECTED: User should see prompt
        EXPECTED: to'Add 1 more selection to qualify for 5+ acca insurance' .
        """
        pass
