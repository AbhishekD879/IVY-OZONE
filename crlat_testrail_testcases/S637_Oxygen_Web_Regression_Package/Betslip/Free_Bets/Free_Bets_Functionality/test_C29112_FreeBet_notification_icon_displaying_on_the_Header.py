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
class Test_C29112_FreeBet_notification_icon_displaying_on_the_Header(Common):
    """
    TR_ID: C29112
    NAME: 'FreeBet' notification icon displaying on the Header
    DESCRIPTION: This Test Case verified displaying 'FreeBet' notification icon displaying on the Header
    DESCRIPTION: AUTOTEST: [C9697747]
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. User has not Free Bets available on their account
    """
    keep_browser_open = True

    def test_001_load_oxygenapplication(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: * Homepage is opened
        EXPECTED: * 'Freebet' notification icon is NOT displayed on the header (on the Balance button/icon)
        """
        pass

    def test_002_apply_freebet_tokens_to_the_relevant_user_account(self):
        """
        DESCRIPTION: Apply Freebet tokens to the relevant user account
        EXPECTED: 
        """
        pass

    def test_003_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: * Page is reloaded
        EXPECTED: * 'Freebet' notification icon is displayed on the header
        """
        pass

    def test_004_place_a_bet_using_last_freebet(self):
        """
        DESCRIPTION: Place a bet using last Freebet
        EXPECTED: 'Freebet' notification disappeared from the header (from the Balance button/icon)
        """
        pass

    def test_005_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step 2
        EXPECTED: 
        """
        pass

    def test_006_expiration_date_and_time_of_available_freebet_has_passes(self):
        """
        DESCRIPTION: Expiration date and time of available Freebet has passes
        EXPECTED: 
        """
        pass

    def test_007_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: 'Freebet' notification icon disappeared
        """
        pass

    def test_008_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step 2
        EXPECTED: 
        """
        pass

    def test_009_log_out_from_the_oxygen_application(self):
        """
        DESCRIPTION: Log out from the Oxygen application
        EXPECTED: 'Freebet' notification icon is hidden
        """
        pass
