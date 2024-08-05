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
class Test_C59498785_Verify_appearance_of_on_boarding_free_bet_screen_once_Static_Block_is_created_in_CMS(Common):
    """
    TR_ID: C59498785
    NAME: Verify appearance of on-boarding/free bet screen once Static Block is created in CMS
    DESCRIPTION: Test case verifies appearance of on-boarding/free bet screen on the event details page with 5-a-side market once all required CMS static blocks are created.
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: - Formations are added in CMS -> BYB -> 5 A Side
    PRECONDITIONS: Event linking(Banach to Openbet TI) is done through an email - see following article: https://confluence.egalacoral.com/display/SPI/Request+Banach+%28BYB%2C+5-A-Side%2C+Player+Bets%29+Test+Events+Mapping
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Football event details page that has all 5-A-Side configs
    PRECONDITIONS: 3. Switch to 5-A-Side tab
    PRECONDITIONS: 4. Click/Tap 'BUILD TEAM' button
    """
    keep_browser_open = True

    def test_001_verify_on_boarding_screen_availability(self):
        """
        DESCRIPTION: Verify 'on-boarding' screen availability
        EXPECTED: 'On-boarding' screen is NOT displayed within the 5-A-Side overlay
        EXPECTED: ![](index.php?/attachments/get/115915618)
        """
        pass

    def test_002__in_cms_go_to_byb__byb_static_blocks__create_new_static_block_in_the_opened_pop_up_fill_in_the_byb_static_block_title_field_with__five_a_side_journey_step_1_and_click_save_html_markup_field_fill_with_any_text_and_click_save_changes_refresh_the_page_on_front_end(self):
        """
        DESCRIPTION: * In CMS, go to 'BYB' > 'BYB Static Blocks' > 'Create New Static Block'
        DESCRIPTION: * In the opened pop-up, fill in the 'BYB Static Block Title' field with  'five-a-side-journey-step-1' and click 'Save'
        DESCRIPTION: * 'Html Markup' field fill with any text and click 'Save Changes'
        DESCRIPTION: * Refresh the page on front-end
        EXPECTED: 'On-boarding' screen is displayed within the 5-A-Side overlay (configured slide only)
        """
        pass

    def test_003_repeat_step_2_but_fill_the_byb_static_block_title_field_with_five_a_side_journey_step_2_input(self):
        """
        DESCRIPTION: Repeat step 2, but fill the 'BYB Static Block Title' field with 'five-a-side-journey-step-2' input
        EXPECTED: 'On-boarding' screen is displayed within the 5-A-Side overlay (configured slides only)
        """
        pass

    def test_004_repeat_step_2_but_fill_the_c_field_with_five_a_side_journey_step_3_input(self):
        """
        DESCRIPTION: Repeat step 2, but fill the 'c' field with 'five-a-side-journey-step-3' input
        EXPECTED: 'On-boarding' screen IS displayed at the bottom of 5-A-Side overlay (configured slides only)
        EXPECTED: ![](index.php?/attachments/get/115916684)
        """
        pass

    def test_005__close_the_5_a_side_overlay_login_with_a_user_that_has_a_free_bet_which_is_applicable_for_bet_placement_for_5_a_side_clicktap_build_team_button(self):
        """
        DESCRIPTION: * Close the '5-A-Side' overlay
        DESCRIPTION: * Login with a user that has a free bet which is applicable for bet placement for 5-A-Side
        DESCRIPTION: * Click/Tap 'BUILD TEAM' button
        EXPECTED: 'On-boarding' screen is NOT displayed within the 5-A-Side overlay
        """
        pass

    def test_006_repeat_step_2_but_fill_the_byb_static_block_title_field_with_five_a_side_free_bet_input(self):
        """
        DESCRIPTION: Repeat step 2, but fill the 'BYB Static Block Title' field with 'five-a-side-free-bet' input
        EXPECTED: 'Free Bet' screen IS displayed at the bottom of 5-A-Side overlay
        EXPECTED: ![](index.php?/attachments/get/115917777)
        """
        pass
