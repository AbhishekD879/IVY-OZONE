import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.5_a_side
@vtest
class Test_C49328606_Verify_Add_Player_buttons_and_Player_info_location_according_to_selected_formation_on_5_A_Side_overlay(Common):
    """
    TR_ID: C49328606
    NAME: Verify  'Add Player' buttons and Player info location according to selected formation on '5-A-Side' overlay
    DESCRIPTION: This test case verifies 'Add Player' buttons and Player info location according to selected formation on '5-A-Side' overlay
    PRECONDITIONS: 1. Create 12 different unique formations (1-1-2-1, 1-2-1-1, 1-1-1-2, 1-1-0-3, 1-0-2-2, 1-0-1-3, 1-3-0-1, 0-2-1-2, 0-1-2-2, 0-1-3-1, 0-3-1-1, 0-1-1-3) in CMS -> BYB -> 5-A-Side
    PRECONDITIONS: 2. Load the app
    PRECONDITIONS: 3. Navigate to Football event details page that has all 5-A-Side configs and created formations
    PRECONDITIONS: 4. Click/Tab on '5-A-Side' tab
    PRECONDITIONS: 5. Click/Tab 'Build' button
    PRECONDITIONS: **5-A-Side config:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Formations are added in CMS -> BYB -> 5 A Side
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    """
    keep_browser_open = True

    def test_001_verify_layout_of_the_5_a_side_overlay(self):
        """
        DESCRIPTION: Verify layout of the '5-A-Side' overlay
        EXPECTED: * All created formations are in the formations carousel
        EXPECTED: * First formation is selected by default
        EXPECTED: * Selected formation is highlighted
        EXPECTED: * 'Add Player' buttons with Player info are located according to selected formation (Player position and Market name)
        """
        pass

    def test_002_select_another_formation_via_clicking_formation_icon_in_formations_carouselverify_layout_of_the_5_a_side_overlay(self):
        """
        DESCRIPTION: Select another formation via clicking formation icon in formations carousel.
        DESCRIPTION: Verify layout of the '5-A-Side' overlay.
        EXPECTED: * Selected formation is highlighted
        EXPECTED: * 'Add Player' buttons move with animation to appropriate places
        EXPECTED: * 'Add Player' buttons with Player info are located according to selected formation (Player position and Market name)
        """
        pass
