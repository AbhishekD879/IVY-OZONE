import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
@pytest.mark.high
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone
@vtest
class Test_C65304975_To_verify_SYC_POP_in_Football_landing_page_after_start_of_new_Season_for_unsubscribed_users(BaseUserAccountTest):
    """
    TR_ID: C65304975
    NAME: To verify SYC POP in Football landing page after start of new Season for unsubscribed users
    DESCRIPTION: To verify SYC POP in Football landing page after start of new Season for unsubscribed users
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in cms
    PRECONDITIONS: 3)Featured events are present to be displayed for competition for the particular team in OB
    PRECONDITIONS: 4)SYC page is created in cms with all required data in Fanzone SYC section and "Days to Hide Remind Me Later"- 15days
    PRECONDITIONS: 5)User has clicked on Remind Me later previously on SYC overlay
    PRECONDITIONS: 6)User has to login from the same device and different app/browser, user shouldn't clear cache /cookies/ updating the app version
    PRECONDITIONS: 7)User has FE url and Valid credentials to Login Lads FE and user has successfully logged into application.
    """
    keep_browser_open = True

    def navigate_to_football_verify_syc(self, username):
        """
        Navigate to football and verify SYC
        """
        self.site.login(username=username, timeout=15)
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football")
        self.__class__.dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                                             verify_name=False)
        self.assertTrue(self.dialog_fb, msg='"SYC overlay"is not displayed on Football landing page')

    def test_000_preconditions(self):
        """
        1)User has access to CMS
        2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in cms
        3)Featured events are present to be displayed for competition for the particular team in OB
        4)SYC page is created in cms with all required data in Fanzone SYC section and "Days to Hide Remind Me Later"- 15days
        5)User has clicked on Remind Me later previously on SYC overlay
        6)User has to login from the same device and different app/browser, user shouldn't clear cache /cookies/ updating the app version
        7)User has FE url and Valid credentials to Login Lads FE and user has successfully logged into application.
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        syc = self.cms_config.get_fanzone_syc()
        self.assertTrue(syc, msg='"SYC"is not configured in cms')
        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        self.navigate_to_football_verify_syc(self.username)
        remind_later_btn = self.dialog_fb.has_remind_later_button(timeout=15)
        self.assertTrue(remind_later_btn, msg='Remind later button is not present')
        self.dialog_fb.remind_later_button.click()

        site2 = self.create_new_browser_instance()
        site2.wait_splash_to_hide()
        site2.wait_content_state('HomePage', timeout=10)

    def test_001_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Football Landing Page
        EXPECTED: User should be navigated to Football page
        """
        # Covered in step-2

    def test_002_verify_if_syc_overlay_is_shown_in_football_page(self):
        """
        DESCRIPTION: Verify if SYC overlay is shown in Football page
        EXPECTED: SYC overlay is shown to the user in Football Landing page
        """
        self.navigate_to_football_verify_syc(self.username)
