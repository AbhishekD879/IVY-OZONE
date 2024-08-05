import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone
@vtest
class Test_C65305229_To_verify_user_could_navigate_to_any_other_page_from_SYC_page_and_get_SYC_popup_when_user_get_back_to_foot_ball_SPL(Common):
    """
    TR_ID: C65305229
    NAME: To verify user could navigate to any other page from SYC page and get SYC popup when user get back to foot ball SPL
    DESCRIPTION: To verify user could navigate to any other page from SYC page and get SYC popup when user get back to foot ball SPL
    """
    keep_browser_open = True
    all_sports_page = 'az-sports'
    aston_villa = vec.fanzone.TEAMS_LIST.aston_villa.title()

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) User is in logged in state
        PRECONDITIONS: 2) User has Not subscribed for Fanzone Previously
        PRECONDITIONS: 3) In CMS-Fanzone SYC- data should be created, which will trigger SYC popup in front end
        PRECONDITIONS: 4) User is in SYC- team selection page
        """
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                              timeout=30, verify_name=False)
        self.assertTrue(dialog_fb, msg='"SYC Pop Up"is not displayed on Football landing page')
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='I am in button is displayed',
                        timeout=5)

    def test_001_select_any_team_and_click_on_any_other_tab_like_home_page(self):
        """
        DESCRIPTION: Select any team and click on any other tab like Home page
        EXPECTED: User should be navigated back to Home Page
        """
        teams = self.site.show_your_colors.items_as_ordered_dict
        self.assertTrue(teams, msg='No teams found')
        teams[self.aston_villa].scroll_to_we()
        selected_team = teams[self.aston_villa]
        selected_team.click()

    def test_002_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Football landing page
        EXPECTED: User should be navigated to Football Landing page
        """
        self.navigate_to_page("homepage")
        self.site.wait_content_state("homepage")
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                              timeout=30, verify_name=False)
        self.assertTrue(dialog_fb, msg='"SYC Pop Up"is not displayed on Football landing page')
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='I am in button is displayed',
                        timeout=5)

    def test_003_click_on_im_in(self):
        """
        DESCRIPTION: Click on IM In
        EXPECTED: User is navigated to Show Your Colors page
        """
        # Covered in above step

    def test_004_click_on_horse_racing_page(self):
        """
        DESCRIPTION: Click on Horse Racing page
        EXPECTED: User should be navigated to Horse Racing page
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')

    def test_005_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Football landing page
        EXPECTED: User should be navigated to Football Landing page
        """
        self.test_002_navigate_to_football_landing_page()

    def test_006_click_on_im_in(self):
        """
        DESCRIPTION: Click on IM In
        EXPECTED: User is navigated to Show Your Colors page
        """
        # Covered in above step

    def test_007_repeat_step_1__step_3_by_clicking_different_tabs(self):
        """
        DESCRIPTION: Repeat Step 1- step 3 by clicking different tabs
        EXPECTED: User should be able to navigate to different pages
        """
        self.navigate_to_page(name='greyhound-racing')
        self.site.wait_content_state('Greyhoundracing', timeout=25)
        self.test_002_navigate_to_football_landing_page()

    def test_008_repeat_step_1__step_3_by_clicking_on_all_footer_menu_in_mobile(self):
        """
        DESCRIPTION: Repeat Step 1- step 3 by clicking on all footer menu in mobile
        EXPECTED: User should be able to navigate to different pages
        """
        self.navigate_to_page(name=self.all_sports_page)
        self.test_002_navigate_to_football_landing_page()

    def test_009_verify_user_will_be_prompted_with_syc_popup_in_football_landing_pagenote_as_long_as_user_is_not_subscribed_to_any_team_he_should_be_prompted_with_syc_popup_in_football_slp(self):
        """
        DESCRIPTION: Verify user will be prompted with SYC popup in football landing page
        DESCRIPTION: Note: As long as user is not subscribed to any team, he should be prompted with SYC popup in football SLP
        EXPECTED: User should be prompted with pop-up as described
        """
        self.test_002_navigate_to_football_landing_page()
