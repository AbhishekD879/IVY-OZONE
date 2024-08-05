import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_h1
@pytest.mark.high
@pytest.mark.other
@pytest.mark.fanzone
@pytest.mark.desktop
@vtest
class Test_C65304977_To_verify_SYC_POP_in_Football_landing_page_after_start_of_new_Season_for_newly_registered_users(Common):
    """
    TR_ID: C65304977
    NAME: To verify SYC POP in Football landing page after start of new Season for newly registered users
    DESCRIPTION: To verify SYC POP in Football landing page after start of new Season for newly registered users
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in cms
    PRECONDITIONS: 3)Featured events are present to be displayed for competition for the particular team in OB
    PRECONDITIONS: 4) New user should be registered and loginto application with newly registered user with Valid credentials
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1)User has access to CMS
        PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in cms
        PRECONDITIONS: 3)Featured events are present to be displayed for competition for the particular team in OB
        PRECONDITIONS: 4) New user should be registered and loginto application with newly registered user with Valid credentials
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        syc = self.cms_config.get_fanzone_syc()
        self.assertTrue(syc, msg='"SYC"is not configured in cms')
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)

    def test_001_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Football Landing Page
        EXPECTED: User should be navigated to Football page
        """
        self.site.open_sport(name='Football', fanzone=True)
        self.site.wait_content_state("football", timeout=30)

    def test_002_verify_if_syc_overlay_is_shown_in_football_page(self):
        """
        DESCRIPTION: Verify if SYC overlay is shown in Football page
        EXPECTED: SYC overlay is shown to the user in Football Landing page
        """
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        self.assertTrue(dialog_fb, msg="SYC overlay is not displayed")
