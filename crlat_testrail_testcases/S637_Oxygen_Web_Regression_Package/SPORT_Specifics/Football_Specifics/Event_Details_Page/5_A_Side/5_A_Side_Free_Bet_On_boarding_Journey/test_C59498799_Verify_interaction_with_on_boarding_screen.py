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
class Test_C59498799_Verify_interaction_with_on_boarding_screen(Common):
    """
    TR_ID: C59498799
    NAME: Verify interaction with on-boarding screen
    DESCRIPTION: Test case verifies contents and interaction with them of the on-boarding screen of event details page with 5-a-side market.
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: - Formations are added in CMS -> BYB -> 5 A Side
    PRECONDITIONS: Event linking(Banach to Openbet TI) is done through an email - see following article: https://confluence.egalacoral.com/display/SPI/Request+Banach+%28BYB%2C+5-A-Side%2C+Player+Bets%29+Test+Events+Mapping
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 0. 3 'Static Blocks' with 'Html Markup' content are created in CMS.
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Login with a user that has a free bet which is applicable for bet placement for 5-A-Side
    PRECONDITIONS: 3. Navigate to Football event details page that has all 5-A-Side configs
    PRECONDITIONS: 4. Switch to 5-A-Side tab
    PRECONDITIONS: 5. Click/Tap 'BUILD TEAM' button
    """
    keep_browser_open = True

    def test_001_verify_contents_of_the_on_boarding_screen(self):
        """
        DESCRIPTION: Verify contents of the 'On-boarding' screen
        EXPECTED: Overlay contains:
        EXPECTED: * Close 'X' button
        EXPECTED: * 'Free Bet' Signposting icon (not shown to a user that doesn't have applicable free bet, or logged out user)
        EXPECTED: * Pagination 'Next' button
        EXPECTED: * 'Html Markup' content area(text from that CMS field is shown there)
        EXPECTED: * Pagination 'Bullet holes' element, with a first 'bullet hole' being black
        EXPECTED: ![](index.php?/attachments/get/115916685)
        """
        pass

    def test_002_mobiletabletswipe_the_screen_to_the_left_within_the_on_boarding_screen_sectiondesktop_mobile_tabletclicktap_on_next_button(self):
        """
        DESCRIPTION: [Mobile/Tablet]
        DESCRIPTION: Swipe the screen to the left, within the 'On-boarding' screen section
        DESCRIPTION: [Desktop, Mobile, Tablet]
        DESCRIPTION: Click/Tap on 'Next' button
        EXPECTED: Сontent and bullet are moved to the next slide
        EXPECTED: ![](index.php?/attachments/get/115916707)
        """
        pass

    def test_003_mobiletabletswipe_the_screen_to_the_left_and_then_back_to_right(self):
        """
        DESCRIPTION: [Mobile/Tablet]
        DESCRIPTION: Swipe the screen to the left and then back to right
        EXPECTED: Overlay change is done according to pagination
        EXPECTED: User can see third screen contents after the **left swipe** and returns to contents of the second screen on the **right swipe**
        """
        pass

    def test_004_desktop_onlyclick_on_the_third_bullet_and_then_back_on_the_second_one(self):
        """
        DESCRIPTION: [Desktop only]
        DESCRIPTION: Click on the third bullet and then back on the second one
        EXPECTED: Overlay change is done according to pagination
        EXPECTED: User can see third screen contents after **clicking on third bullet** and returns to contents of the second screen after **clicking on second bullet**
        """
        pass

    def test_005_mobiletabletswipe_the_screen_to_the_left_within_the_on_boarding_screen_sectiondesktop_mobile_tabletclicktap_on_next_button(self):
        """
        DESCRIPTION: [Mobile/Tablet]
        DESCRIPTION: Swipe the screen to the left, within the 'On-boarding' screen section
        DESCRIPTION: [Desktop, Mobile, Tablet]
        DESCRIPTION: Click/Tap on 'Next' button
        EXPECTED: Сontent and bullet are moved to the next slide
        EXPECTED: ![](index.php?/attachments/get/115916755)
        """
        pass

    def test_006_desktop_onlyhover_cursor_over_the_x_button_bullet_holes_element_nextdone_button(self):
        """
        DESCRIPTION: [Desktop only]
        DESCRIPTION: Hover cursor over the 'X' button, 'bullet holes' element, 'Next'/'Done' button
        EXPECTED: Cursor changes to 'Pointer' whenever it is hovered over the clickable element.
        """
        pass

    def test_007_tapclick_done_button(self):
        """
        DESCRIPTION: Tap/Click 'Done' button
        EXPECTED: 'On-boarding' screen is closed
        """
        pass

    def test_008_tapclick_x_buttonanother_device_is_needed_in_order_to_trigger_the_appearance_of_on_boarding_screen(self):
        """
        DESCRIPTION: Tap/Click 'X' Button
        DESCRIPTION: (Another device is needed in order to trigger the appearance of 'On-boarding' screen)
        EXPECTED: 'On-boarding' screen is closed
        """
        pass
