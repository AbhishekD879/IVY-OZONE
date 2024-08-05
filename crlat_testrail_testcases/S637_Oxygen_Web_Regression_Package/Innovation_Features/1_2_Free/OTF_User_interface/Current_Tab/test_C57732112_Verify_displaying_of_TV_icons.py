import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C57732112_Verify_displaying_of_TV_icons(Common):
    """
    TR_ID: C57732112
    NAME: Verify displaying of TV icons
    DESCRIPTION: This test case verifies displaying of TV icons
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. Events created
    PRECONDITIONS: 3. User expands '1-2-Free' section in the left menu
    PRECONDITIONS: 4. User opens 'Game view'
    PRECONDITIONS: 5. User open Detail View for existing game
    """
    keep_browser_open = True

    def test_001_open_tv_icon_dropdown_for_some_event(self):
        """
        DESCRIPTION: Open 'TV Icon' dropdown for some event
        EXPECTED: Dropdown is opened with the following elements:
        EXPECTED: BBC
        EXPECTED: ITV
        EXPECTED: Sky Sports
        EXPECTED: BT Sports
        """
        pass

    def test_002_select_one_of_tv_icon_from_dropdown_and_save_the_game(self):
        """
        DESCRIPTION: Select one of TV icon from dropdown and save the game
        EXPECTED: TV icon successfully selected and saved
        """
        pass

    def test_003_open_current_tab(self):
        """
        DESCRIPTION: Open 'Current Tab'
        EXPECTED: Relevant TV icon appear alongside the relevant match
        """
        pass

    def test_004_select_option_no_tv_icon_from_dropdown_and_save_the_game_again(self):
        """
        DESCRIPTION: Select option 'No TV icon' from dropdown and save the game again
        EXPECTED: Option successfully selected and saved
        """
        pass

    def test_005_open_current_tab_again(self):
        """
        DESCRIPTION: Open 'Current Tab' again
        EXPECTED: No TV icon appear alongside the relevant match
        """
        pass
