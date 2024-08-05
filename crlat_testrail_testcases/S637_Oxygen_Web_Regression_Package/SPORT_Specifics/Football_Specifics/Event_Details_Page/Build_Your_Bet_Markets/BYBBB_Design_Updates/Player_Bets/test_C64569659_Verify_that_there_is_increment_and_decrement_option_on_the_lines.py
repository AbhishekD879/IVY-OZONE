import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@vtest
class Test_C64569659_Verify_that_there_is_increment_and_decrement_option_on_the_lines(Common):
    """
    TR_ID: C64569659
    NAME: Verify that there is increment and decrement option on the lines
    DESCRIPTION: Verify that there is increment and decrement option on the lines
    PRECONDITIONS: 1: In CMS &gt; BYB &gt; BYB Markets -Markets should be Configure in CMS
    PRECONDITIONS: Goals
    PRECONDITIONS: Goals inside the box
    PRECONDITIONS: Goals outside the box
    PRECONDITIONS: Offsides
    PRECONDITIONS: Passes
    PRECONDITIONS: Shots
    PRECONDITIONS: Shots on target
    PRECONDITIONS: Shots outside the box
    PRECONDITIONS: 2: Banach events should be available with all or ANY of the Markets
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral application
        EXPECTED: User should be able to launch the application successfully
        """
        pass

    def test_002_navigate_to_football_edp(self):
        """
        DESCRIPTION: Navigate to Football EDP
        EXPECTED: EDP should be displayed with BYB/BB tab
        """
        pass

    def test_003_click_on_bybbb_tab(self):
        """
        DESCRIPTION: Click on BYB/BB tab
        EXPECTED: BYB/BB tab should be displayed with all the Markets
        """
        pass

    def test_004_expand_the_player_name_by_clicking_on_the_chevron(self):
        """
        DESCRIPTION: Expand the Player name by clicking on the chevron
        EXPECTED: * Player Name should be Expanded
        EXPECTED: * Stats Increment should be displayed
        EXPECTED: * Increments of 1 should be displayed
        EXPECTED: * ADD TO BET BUILDER/ ADD TO BETSLIP CTA should be displayed
        """
        pass

    def test_005_select_stats___increase__decrease__click_on_plus___(self):
        """
        DESCRIPTION: Select Stats - Increase / Decrease -Click on (+) / (-)
        EXPECTED: * User should be able to click on (+) / (-)
        EXPECTED: * Depending on the Min /Max Stats (+) / (-) should be disabled after crossing the increments
        """
        pass

    def test_006_click_on_add_to_bet_builder_add_to_betslip(self):
        """
        DESCRIPTION: Click on ADD TO BET BUILDER/ ADD TO BETSLIP
        EXPECTED: * User should be able to click and selection should be added BYB/BB betslip
        EXPECTED: * ADDED should be displayed
        """
        pass
