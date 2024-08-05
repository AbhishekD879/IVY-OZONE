import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone
@vtest
class Test_C65304969_To_verify_if_user_clicks_on_Remind_me_later_the_overlay_should_disappear_and_user_should_be_on_the_same_page(Common):
    """
    TR_ID: C65304969
    NAME: To verify if user clicks on "Remind me later" the overlay should disappear and user should be on the same page
    DESCRIPTION: To verify if user clicks on "Remind me later" the overlay should disappear and user should be on the same page
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in cms
    PRECONDITIONS: 3)Featured events are present to be displayed for competition for the particular team in OB
    PRECONDITIONS: 4)SYC page is created in cms with all required data in Fanzone SYC section
    PRECONDITIONS: 5)User has not performed any action on SYC overlay
    PRECONDITIONS: 6)User has FE url and Valid credentials to Login Lads FE and user has successfully logged into application
    """
    keep_browser_open = True

    def test_001_navigate_to_football_page(self):
        """
        DESCRIPTION: Navigate to Football page
        EXPECTED: User should be navigated to Football page
        """
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username, timeout=15)
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football")

    def test_002_verify_if_syc_overlay_is_shown_in_football_page(self):
        """
        DESCRIPTION: Verify if SYC overlay is shown in Football page
        EXPECTED: SYC overlay is shown to the user in Football Landing page
        """
        self.__class__.dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                                             verify_name=False)
        self.assertTrue(self.dialog_fb, msg='"SYC overlay"is not displayed on Football landing page')

    def test_003_click_on_remind_me_later__button_in_the_overlay(self):
        """
        DESCRIPTION: Click on "Remind Me Later " BUTTON in the overlay
        EXPECTED: The overlay should disappear and user should be on Football landing page
        """
        remind_later_btn = self.dialog_fb.has_remind_later_button(timeout=15)
        self.assertTrue(remind_later_btn, msg='Remind later button is not present')
        self.dialog_fb.remind_later_button.click()
        self.site.wait_content_state("football")
