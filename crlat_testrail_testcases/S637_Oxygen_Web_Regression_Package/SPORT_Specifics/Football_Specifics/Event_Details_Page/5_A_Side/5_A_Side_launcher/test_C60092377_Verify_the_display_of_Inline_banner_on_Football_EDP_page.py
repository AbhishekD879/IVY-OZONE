import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.5_a_side
@vtest
class Test_C60092377_Verify_the_display_of_Inline_banner_on_Football_EDP_page(Common):
    """
    TR_ID: C60092377
    NAME: Verify the display of Inline banner on Football EDP page
    DESCRIPTION: This test cases verifies the display of Inline banner on Football EDP page.
    PRECONDITIONS: 1: User should have access to CMS to enable/disable Inline banner for 5 A side
    PRECONDITIONS: 2: Title, description should be added for Inline banner in CMS
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

    def test_001_login_to_cms_and_enable_the_inline_banner_set_the_position_and_text_to_be_displayed_on_the_banner(self):
        """
        DESCRIPTION: Login to CMS and enable the Inline banner, set the position and text to be displayed on the banner
        EXPECTED: User should be able to enable edit the text and position and save the change successfully
        """
        pass

    def test_002_launch_ladbrokes_url_app(self):
        """
        DESCRIPTION: Launch Ladbrokes URL/ app
        EXPECTED: User should be able to launch the app/URL successfully
        """
        pass

    def test_003_navigate_to_football_edp_which_has_5_a_side_available__check_pre_conditions_for_5_a_side(self):
        """
        DESCRIPTION: Navigate to Football EDP which has 5 A side available ( Check Pre-conditions for 5 A side)
        EXPECTED: User should be able to view Football EDP
        """
        pass

    def test_004_validate_the_inline_banner_display(self):
        """
        DESCRIPTION: Validate the Inline banner display
        EXPECTED: User should be able to view the Inline banner in All markets tab depending on the position set in CMS (Inline Banner should be displayed below All Markets tab and above the first market in that tab when position is set to '0'  and if we set Position=3 then it will sit below market number 3. )
        """
        pass

    def test_005_validate_the_title_and_description_for_inline_banner(self):
        """
        DESCRIPTION: Validate the title and description for Inline banner
        EXPECTED: User should be able to view the title and description as configured in CMS
        """
        pass

    def test_006_login_to_cms_and_disable_the_inline_banner(self):
        """
        DESCRIPTION: Login to CMS and disable the Inline banner
        EXPECTED: User should be able to disable the Inline banner and save the changes successfully
        """
        pass

    def test_007_repeat_the_steps_234(self):
        """
        DESCRIPTION: Repeat the steps 2,3&4
        EXPECTED: User should not be able to see the Inline banner on any Football EDP
        """
        pass
