import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone
@vtest
class Test_C65304965_To_verify_SYC_overlay_shouldnt_be_displayed_for_Logged_Out_users(Common):
    """
    TR_ID: C65304965
    NAME: To verify SYC overlay shouldn't be displayed for Logged Out users
    DESCRIPTION: To verify SYC overlay shouldn't be displayed for Logged Out users
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in cms
    PRECONDITIONS: 3)Featured events are present to be displayed for competition for the particular team in OB
    PRECONDITIONS: 4)SYC page is created in cms with all required data in Fanzone SYC section
    PRECONDITIONS: 5)User has not performed any action on SYC overlay
    PRECONDITIONS: 6)User has FE url and is on Lads homepage
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1)User has access to CMS
        PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in cms
        PRECONDITIONS: 3)Featured events are present to be displayed for competition for the particular team in OB
        PRECONDITIONS: 4)SYC page is created in cms with all required data in Fanzone SYC section
        PRECONDITIONS: 5)User has not performed any action on SYC overlay
        PRECONDITIONS: 6)User has FE url and is on Lads homepage
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

    def test_001_navigate_to_football_page(self):
        """
        DESCRIPTION: Navigate to Football page
        EXPECTED: User should be navigated to Football page
        """
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football")

    def test_002_verify_if_syc_overlay_is_shown_in_football_page(self):
        """
        DESCRIPTION: Verify if SYC overlay is shown in Football page
        EXPECTED: SYC overlay should not be shown to the user in Football Landing page
        """
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS)
        self.assertFalse(dialog_fb, msg='"SYC overlay"is displayed on Football landing page')
