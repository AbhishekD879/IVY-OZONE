import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C9608480_Races_displaying_ODDS_in_fractional_decimal_formats_on_resulted_event_details_page(Common):
    """
    TR_ID: C9608480
    NAME: <Races>: displaying ODDS in fractional/decimal formats on resulted event details page
    DESCRIPTION: This test cases verifies displaying ODDS on <Race> results page in different formats
    PRECONDITIONS: - To see what TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - You should have resulted <Race> events
    PRECONDITIONS: - You should be logged in
    PRECONDITIONS: - You should have enabled 'Fractional' format for your account (Right Menu > Settings)
    PRECONDITIONS: - You should be on <Race> result details page
    PRECONDITIONS: NOTE: Horse Racing and Greyhounds should be verified separately
    """
    keep_browser_open = True

    def test_001_verify_format_of_displayed_odds(self):
        """
        DESCRIPTION: Verify format of displayed ODDS
        EXPECTED: ODDS are displayed in 'Fractional' format (e.g. '1/2')
        """
        pass

    def test_002___switch_format_to_decimal_in_user_menu__settings__tap_back_button_and_verify_format_of_displayed_odds(self):
        """
        DESCRIPTION: - Switch format to 'Decimal' in User Menu > Settings
        DESCRIPTION: - Tap 'Back' button and verify format of displayed ODDS
        EXPECTED: ODDS are displayed in 'Decimal' format (e.g. '0.5')
        """
        pass
