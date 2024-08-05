import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone_reg_tests
@vtest
class Test_C65305001_Verify_SYC_popup_or_entry_points_should_not_display_for_a_logged_out_user(Common):
    """
    TR_ID: C65305001
    NAME: Verify SYC popup or entry points should not display for a logged out user
    DESCRIPTION: This test case is to verify  SYC popup or entry points should not display for a logged out user
    PRECONDITIONS: 1) In CMS- SYC Promotion should be configured to get SYC team selection page from promotion.
    PRECONDITIONS: 2) User should be in logged out state
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Active the fanzone in CMS
        EXPECTED: Fanzone is activated in cms
        """
        fanzone_status = self.get_initial_data_system_configuration().get(vec.sb.FANZONE)
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)

    def test_001_launch_ladbrokes_applicaion(self):
        """
        DESCRIPTION: Launch ladbrokes applicaion
        EXPECTED: Ladbrokes application should be launched and home page displayed
        """
        self.navigate_to_page("HomePage")

    def test_002_check_entry_points_fanzone(self):
        """
        DESCRIPTION: Check entry points fanzone
        EXPECTED: Entry points should not displayed
        """
        if self.device_type == 'mobile':
            self.assertNotIn(vec.sb.FANZONE, self.site.home.menu_carousel.items_names,
                             msg="Fanzone Entry Point is displayed")
            all_items = self.site.home.menu_carousel.items_as_ordered_dict
            self.assertTrue(all_items, msg='No items on MenuCarousel found')
            all_items.get(vec.SB.ALL_SPORTS).click()
            self.site.wait_content_state(state_name='AllSports')
            top_sports = self.site.all_sports.top_sports_section.items_names
            self.assertTrue(top_sports, msg='No sports found in "Top Sports" section')
            self.assertNotIn(vec.sb.FANZONE, top_sports,
                             msg="Fanzone Entry Point is displayed")
        else:
            self.assertNotIn(vec.sb.FANZONE.upper(), self.site.header.sport_menu.items_names,
                             msg="Fanzone Entry Point is displayed")
            self.assertNotIn(vec.sb.FANZONE, self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict,
                             msg="Fanzone Entry Point is displayed")
        self.assertFalse(self.site.home.fanzone_banner(timeout=3), msg="Fanzone Banner is displayed on HomePage")

    def test_003_navigate_to_football_spl_page(self):
        """
        DESCRIPTION: Navigate to football SPL page
        EXPECTED: User should navigated to football SPL page
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='Football')

    def test_004_check_syc_popup(self):
        """
        DESCRIPTION: Check SYC popup
        EXPECTED: User should not get SYC popup
        """
        self.assertFalse(self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                                   timeout=5))
