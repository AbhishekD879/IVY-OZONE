import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C57732068_Verify_Show_more_button_on_previous_tab(Common):
    """
    TR_ID: C57732068
    NAME: Verify 'Show more' button on previous tab
    DESCRIPTION: This test case verifies 'Show more' button on the previous tab
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. The user is logged in to Coral/Ladbrokes test environment
    PRECONDITIONS: 3. The user is played more than 7 Previous Games
    """
    keep_browser_open = True

    def test_001_tap_on_correct_4_link(self):
        """
        DESCRIPTION: Tap on Correct 4 link
        EXPECTED: - User navigated to the end page (Results page) and it designed accordingly:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a
        EXPECTED: - All data retrieved from CMS and correctly displayed
        """
        pass

    def test_002_user_tap_on_previous_tab(self):
        """
        DESCRIPTION: User tap on Previous Tab
        EXPECTED: Previous Tab succssefuly opened and it designed accordingly:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d4d962a8847a29b543109bd
        """
        pass

    def test_003_tap_show_more_button_on_the_bottom_of_game_cards(self):
        """
        DESCRIPTION: Tap 'Show more' button on the bottom of game cards
        EXPECTED: - Next three or less games will be loaded and displayed
        EXPECTED: - 'Show more' button still present if more games are present
        """
        pass

    def test_004_tap_show_more_button_again_on_the_bottom_of_game_cards(self):
        """
        DESCRIPTION: Tap 'Show more' button again on the bottom of game cards
        EXPECTED: - Next three or less games will be loaded and displayed
        EXPECTED: - 'Show more' button NOT present if there are no more games available
        """
        pass
