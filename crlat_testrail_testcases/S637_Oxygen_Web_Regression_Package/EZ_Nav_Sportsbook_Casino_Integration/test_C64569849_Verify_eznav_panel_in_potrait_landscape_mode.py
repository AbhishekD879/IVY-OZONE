import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C64569849_Verify_eznav_panel_in_potrait_landscape_mode(Common):
    """
    TR_ID: C64569849
    NAME: Verify eznav panel in potrait & landscape mode.
    DESCRIPTION: Verify eznav panel in potrait & landscape mode.
    PRECONDITIONS: * User should be in Gaming window
    PRECONDITIONS: * User should be logged in.
    PRECONDITIONS: * Allow Screen rotation option in your device
    PRECONDITIONS: Note: Applies to only Mobile Web
    """
    keep_browser_open = True

    def test_001_launch_any_casino_game_page_ex_roulette_game_page_in_portrait_mode(self):
        """
        DESCRIPTION: Launch any casino game page ex: Roulette game page in portrait mode
        EXPECTED: * Casino game page is launched ex: Roulette game page
        EXPECTED: * User is in portrait mode
        EXPECTED: * Sports icon is displayed on the EZNav panel(header)
        """
        pass

    def test_002_tap_sports_icon_from_eznav_panel(self):
        """
        DESCRIPTION: Tap 'Sports' icon from eznav panel
        EXPECTED: * User navigates to 'MyBets' overlay
        """
        pass

    def test_003_rotate_mobile_into_landscape_mode(self):
        """
        DESCRIPTION: Rotate mobile into Landscape mode
        EXPECTED: * Displays message like: "Please rotate your screen back in Portrait Mode. Please ensure you have 'screen rotate' option active."
        """
        pass
