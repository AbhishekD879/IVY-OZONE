import pytest
import voltron.environments.constants as vec
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
class Test_C65305153_Verify_Logged_out_user_will_not_be_see_both_entry_points_and_Fanzone_page_even_through_Fanzone_checkbox_is_checked_in_System_configuration_and_all_entry_points_toggles_are_ON_in_Fanzone_Configuration(Common):
    """
    TR_ID: C65305153
    NAME: Verify Logged out user will not be see both entry points and Fanzone page even through Fanzone checkbox is checked in System configuration and all entry points toggle's are ON in Fanzone Configuration
    DESCRIPTION: Verify Logged out user will not be see both entry points and Fanzone page even through Fanzone checkbox is checked in System configuration and all entry points toggle's are ON in Fanzone Configuration
    PRECONDITIONS: 1) Fanzone should be enabled in System Configuration
    PRECONDITIONS: CMS--> System Configuration--> Structure-->Fanzone
    PRECONDITIONS: 2) Fanzone records should be created
    PRECONDITIONS: 3) Toggle should be On for all the listed items in Fanzone Configuration(CMS)
    PRECONDITIONS: CMS-->Fanzone-->Fanzone Configurations
    """
    keep_browser_open = True

    def test_000_precondition(self):
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)

    def test_001_launch_the_lads_application(self):
        """
        DESCRIPTION: Launch the lads application
        EXPECTED: Application should be launched successfully
        """
        self.site.wait_content_state(state_name='Homepage', timeout=10)
        self.assertFalse(self.site.home.fanzone_banner(), msg="Fanzone banner is not displayed")

    def test_002_verify_below_entry_points_are_displayed(self):
        """
        DESCRIPTION: Verify below entry points are displayed
        DESCRIPTION: a. Launch Banner in home page
        DESCRIPTION: b. Fanzone in A-Z menu
        DESCRIPTION: c. Fanzone in Sports Ribbon(mobile)
        DESCRIPTION: d. Launch Banner in Football landing page
        EXPECTED: None of the entry points should be displayed for logged out user
        """
        self.assertFalse(self.site.home.menu_carousel.items_as_ordered_dict.get('Fanzone'),
                         msg='Fanzone is present under sports ribbon')
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.SB.ALL_SPORTS).click()
            self.site.wait_content_state(state_name='AllSports')
            self.assertNotIn('Fanzone', self.site.all_sports.a_z_sports_section.items_as_ordered_dict,
                             msg='Fanzone is present under A-Z menu')
            self.site.back_button.click()
            self.site.wait_content_state_changed()
        else:
            self.assertNotIn('Fanzone', self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict.keys(),
                             msg='Fanzone is present under A-Z menu')
        self.site.open_sport('football', fanzone=True)
        self.site.wait_content_state("football")
        self.assertFalse(self.site.home.fanzone_banner(), msg="Fanzone banner is not displayed")
