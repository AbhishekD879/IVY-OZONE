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
class Test_C59498790_Verify_that_free_bet_screen_is_shown_even_after_on_boarding_screen_was_shown(Common):
    """
    TR_ID: C59498790
    NAME: Verify that free bet screen is shown even after on-boarding screen was shown
    DESCRIPTION: Verify appearance of free bet screen for a user with an applicable free bet even after on-boarding screen was shown
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: - Formations are added in CMS -> BYB -> 5 A Side
    PRECONDITIONS: Event linking(Banach to Openbet TI) is done through an email - see following article: https://confluence.egalacoral.com/display/SPI/Request+Banach+%28BYB%2C+5-A-Side%2C+Player+Bets%29+Test+Events+Mapping
    PRECONDITIONS: Browser data(Chrome) **can be cleared** through: Dev Tools - Application - 'Clear Storage' - 'Clear site data'
    PRECONDITIONS: App data(Android) **can be cleared** through: Apps(Applications) - Coral/Ladbrokes app - Storage - 'Clear data'
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 0. 4 'Static Blocks' with 'Html Markup' content are created in CMS. URIs of Static Blocks should be: '#ONBOARD-1', '#ONBOARD-2', '#ONBOARD-3', 'FREE_BET'
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Football event details page that has all 5-A-Side configs
    PRECONDITIONS: 3. Switch to 5-A-Side tab
    PRECONDITIONS: 4. Click/Tap 'BUILD TEAM' button
    """
    keep_browser_open = True

    def test_001_verify_on_boarding_screen_availability(self):
        """
        DESCRIPTION: Verify 'on-boarding' screen availability
        EXPECTED: On-boarding screen is shown for the user without being logged in
        EXPECTED: No 'Free bets' signposting icon is shown
        EXPECTED: ![](index.php?/attachments/get/115916875)
        """
        pass

    def test_002_close_the_pitch_viewlogin_with_a_user_that_has_a_free_bet_which_is_applicable_for_bet_placement_for_5_a_sideclicktap_build_team_button(self):
        """
        DESCRIPTION: Close the 'Pitch view'
        DESCRIPTION: Login with a user that has a free bet which is applicable for bet placement for 5-A-Side
        DESCRIPTION: Click/Tap 'BUILD TEAM' button
        EXPECTED: Free bet screen is shown for logged in user
        EXPECTED: 'Free bets' signposting icon is shown
        EXPECTED: ![](index.php?/attachments/get/115917777)
        """
        pass

    def test_003_close_the_pitch_viewclear_the_site_data_for_your_browserapprefresh_the_page(self):
        """
        DESCRIPTION: Close the 'Pitch view'
        DESCRIPTION: Clear the site data for your browser/app
        DESCRIPTION: Refresh the page
        EXPECTED: User is logged out and remains on the '/5-a-side' page
        """
        pass

    def test_004_login_with_a_user_that_doesnt_have_a_free_bet_applicable_for_bet_placement_for_5_a_sideclicktap_build_team_buttonverify_on_boarding_screen_availability(self):
        """
        DESCRIPTION: Login with a user that doesn't have a free bet applicable for bet placement for 5-A-Side
        DESCRIPTION: Click/Tap 'BUILD TEAM' button
        DESCRIPTION: Verify 'on-boarding' screen availability
        EXPECTED: On-boarding screen is shown for logged in user
        EXPECTED: No 'Free bets' signposting icon is shown
        EXPECTED: ![](index.php?/attachments/get/115916875)
        """
        pass

    def test_005_close_the_pitch_viewlogout_and_login_with_a_user_that_has_a_free_bet_which_is_applicable_for_bet_placement_for_5_a_sideclicktap_build_team_button(self):
        """
        DESCRIPTION: Close the 'Pitch view'
        DESCRIPTION: Logout and Login with a user that has a free bet which is applicable for bet placement for 5-A-Side
        DESCRIPTION: Click/Tap 'BUILD TEAM' button
        EXPECTED: Free bet screen is shown for logged in user
        EXPECTED: 'Free bets' signposting icon is shown
        EXPECTED: ![](index.php?/attachments/get/115917777)
        """
        pass

    def test_006_repeat_step_3(self):
        """
        DESCRIPTION: Repeat Step #3
        EXPECTED: Expected results match those from step #3
        """
        pass

    def test_007_login_with_a_user_that_has_a_free_bet_which_is_applicable_for_bet_placement_for_5_a_sideclicktap_build_team_buttonverify_on_boarding_screen_availability(self):
        """
        DESCRIPTION: Login with a user that has a free bet which is applicable for bet placement for 5-A-Side
        DESCRIPTION: Click/Tap 'BUILD TEAM' button
        DESCRIPTION: Verify 'on-boarding' screen availability
        EXPECTED: On-boarding screen is shown for logged in user
        EXPECTED: 'Free bets' signposting icon is shown
        EXPECTED: ![](index.php?/attachments/get/115917958)
        """
        pass

    def test_008_close_the_pitch_viewclicktap_build_team_button(self):
        """
        DESCRIPTION: Close the 'Pitch view'
        DESCRIPTION: Click/Tap 'BUILD TEAM' button
        EXPECTED: Free bet screen is shown for logged in user
        EXPECTED: 'Free bets' signposting icon is shown
        EXPECTED: ![](index.php?/attachments/get/115917777)
        """
        pass
