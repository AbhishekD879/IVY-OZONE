import pytest
from voltron.environments import constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.fanzone
@pytest.mark.desktop
@vtest
class Test_C65304972_To_verify_SYC_popup_when_user_login_after_navigating_directly_to_Football_Landing_Page(Common):
    """
    TR_ID: C65304972
    NAME: To verify SYC popup when user login after navigating directly to Football Landing Page
    DESCRIPTION: To verify SYC popup when user login after navigating directly to Football Landing Page
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in cms
    PRECONDITIONS: 3)Featured events are present to be displayed for competition for the particular team in OB
    PRECONDITIONS: 4)SYC page is created in cms with all required data in Fanzone SYC section and "Days to Hide Remind Me Later"- X days
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1)User has access to CMS
        PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in cms
        PRECONDITIONS: 3)Featured events are present to be displayed for competition for the particular team in OB
        PRECONDITIONS: 4)SYC page is created in cms with all required data in Fanzone SYC section and "Days to Hide Remind Me Later"- X days
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        astonVilla_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        if astonVilla_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        syc = self.cms_config.get_fanzone_syc()
        self.assertTrue(syc, msg='"SYC"is not configured in cms')

    def test_001_navigate_to_football_landing_page_httpsbeta_sportsladbrokescomsportfootballmatchestoday_without_login_to_application(self):
        """
        DESCRIPTION: Navigate to Football Landing Page "https://beta-sports.ladbrokes.com/sport/football/matches/today' without login to application
        EXPECTED: User should be navigated to Football page
        """
        self.site.wait_content_state("Homepage")
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football")

    def test_002_note_login_to_the_env_in_which_the_code_is_deployed_above_is_just_example(self):
        """
        DESCRIPTION: Note: login to the env in which the code is deployed, above is just example
        EXPECTED: 
        """
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)

    def test_003_click_on_login_and_enter_the_valid_credentials(self):
        """
        DESCRIPTION: Click on login and enter the valid credentials
        EXPECTED: User should be logged into application successfully
        """
        # Covered in above step

    def test_004_verify_syc_overlay_is_displayed_without_any_page_refresh(self):
        """
        DESCRIPTION: Verify SYC overlay is displayed without any page refresh
        EXPECTED: SYC overlay should be displayed
        """
        self.__class__.dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                                             timeout=30)
        self.assertTrue(self.dialog_fb, msg='"SYC overlay"is not displayed on Football landing page')
