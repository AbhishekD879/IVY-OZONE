import tests
import voltron.environments.constants as vec
import pytest
from crlat_siteserve_client.utils.exceptions import SiteServeException
from tests.Common import Common
from tests.base_test import vtest


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.fanzone
@pytest.mark.desktop
@vtest
class Test_C65304980_To_verify_SYC_popup_in_Footaball_landing_page_when_user_refresh_the_Page(Common):
    """
    TR_ID: C65304980
    NAME: To verify SYC popup in Footaball landing page when user refresh the Page
    DESCRIPTION: To verify SYC popup in Footaball landing page when user refresh the Page
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in cms
    PRECONDITIONS: 3)Featured events are present to be displayed for competition for the particular team in OB
    PRECONDITIONS: 4)SYC page is created in cms with all required data in Fanzone SYC section
    PRECONDITIONS: 5)User has not performed any action on SYC overlay
    PRECONDITIONS: 6)User has FE url and Valid credentials to Login Lads FE and user has successfully logged into application
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) In CMS-Fanzone SYC- data should be created, which will trigger SYC Entry points in front end
        PRECONDITIONS: 2) User has subscribed to Fanzone
        PRECONDITIONS: 3) User should be logged in state
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if tests.settings.backend_env == 'prod':
            if not fanzone_status.get('enabled'):
                if 'beta' in tests.HOSTNAME:
                    self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                          field_name='enabled',
                                                                          field_value=True)
                else:
                    raise SiteServeException(f'Fanzone is not enabled for "{tests.HOSTNAME}"')
        astonVilla_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        if astonVilla_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)

    def test_001_navigate_to_football_page(self):
        """
        DESCRIPTION: Navigate to Football page
        EXPECTED: User should be navigated to Football page
        """
        self.site.open_sport(name='Football', fanzone=True)

    def test_002_verify_if_syc_overlay_is_shown_in_football_page(self):
        """
        DESCRIPTION: Verify if SYC overlay is shown in Football page
        EXPECTED: SYC overlay is shown to the user in Football Landing page
        """
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        self.assertTrue(dialog_fb, msg="SYC overlay is not displayed")

    def test_003_refresh_the_page_and_verify_syc_popup_is_displayed(self):
        """
        DESCRIPTION: Refresh the Page and verify SYC popup is displayed
        EXPECTED: SYC popup should be displayed
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.test_002_verify_if_syc_overlay_is_shown_in_football_page()
