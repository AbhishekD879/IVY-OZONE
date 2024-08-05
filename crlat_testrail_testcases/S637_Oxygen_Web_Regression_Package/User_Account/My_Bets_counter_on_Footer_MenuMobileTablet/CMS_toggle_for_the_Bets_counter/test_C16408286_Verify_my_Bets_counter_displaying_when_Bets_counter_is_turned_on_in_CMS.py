import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C16408286_Verify_my_Bets_counter_displaying_when_Bets_counter_is_turned_on_in_CMS(Common):
    """
    TR_ID: C16408286
    NAME: Verify my Bets counter displaying when Bets counter is turned on in CMS
    DESCRIPTION: This test case verifies enabling Bet counter toggle in CMS
    PRECONDITIONS: 1. CMS-API Endpoints:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: 2. Make sure that development tool is opened once loading Oxygen/Ladbrokes app
    PRECONDITIONS: 3. Make sure to have a user with placed bets (open bets)
    """
    keep_browser_open = True

    def test_001__go_to_cms_and_navigate_to_system_configuration__structure__bet_counter_and_enable_toggle_save_changes(self):
        """
        DESCRIPTION: * Go to CMS and navigate to System configuration > Structure > Bet counter and enable toggle
        DESCRIPTION: * Save changes
        EXPECTED: - Changes are submitted successfully
        EXPECTED: - 'Bets counter' is enabled in CMS
        """
        pass

    def test_002__load_coralladbrokes_app_and_login_with_user_from_preconditions_verify_that_my_bets_counter_is_displayed_on_footer(self):
        """
        DESCRIPTION: * Load Coral/Ladbrokes app and login with user from preconditions
        DESCRIPTION: * Verify that 'My Bets' counter is displayed on Footer
        EXPECTED: 'Bet counter' is displayed on the right top corner of 'My Bets' Footer Menu
        """
        pass
