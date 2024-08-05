import pytest
import tests
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Events cannot be created on prod & beta
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.horseracing
@pytest.mark.greyhounds
@pytest.mark.races
@pytest.mark.races_negative_p2  # Marker for testcases having blank market description
@vtest
class Test_C60094946_Verify_market_description_display_Blank_in_CMS(Common):
    """
    TR_ID: C60094946
    NAME: Verify market description display- Blank in CMS
    DESCRIPTION: Verify that description is not displayed below the Market tab when left blank in CMS -Horse racing/ Greyhounds market description table
    PRECONDITIONS: 1. Horse racing event should be available
    PRECONDITIONS: 2. User should have admin role for CMS
    PRECONDITIONS: 3: Market description table should have description blank for atleast one Market Template
    """
    keep_browser_open = True
    event_markets = [('win_only',),
                     ('betting_without',)]

    @classmethod
    def custom_tearDown(cls):
        if tests.settings.cms_env != 'prd0':
            cls.get_cms_config().create_and_update_markets_with_description(name='Win or Each Way',
                                                                            description=cls.desc1)
            cls.get_cms_config().create_and_update_markets_with_description(name='Win Only', description=cls.desc2)
            cls.get_cms_config().create_and_update_markets_with_description(name='Betting Without',
                                                                            description=cls.desc3)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Horseracing/Greyhounds Events
        EXPECTED: Horseracing/Greyhounds Events created successfully
        """
        event_params_hr = self.ob_config.add_UK_racing_event(markets=self.event_markets, forecast_available=False,
                                                             tricast_available=False)
        self.__class__.eventID_hr = event_params_hr.event_id
        event_params_gr = self.ob_config.add_UK_greyhound_racing_event(markets=self.event_markets,
                                                                       forecast_available=False, tricast_available=False)
        self.__class__.eventID_gr = event_params_gr.event_id

    def test_001_login_to_cms(self):
        """
        DESCRIPTION: Login to CMS
        EXPECTED: User should be logged into CMS
        """
        if not (self.get_initial_data_system_configuration().get('RacingEDPMarketsDescription', {}).get('enabled')):
            self.cms_config.update_system_configuration_structure(config_item='RacingEDPMarketsDescription',
                                                                  field_name='enabled', field_value=True)

    def test_002_navigate_to_system_configuration__structure_and_enable_market_description_table(self):
        """
        DESCRIPTION: Navigate to System configuration > Structure and enable Market Description table
        EXPECTED: User should be able to disable Market Description table successfully
        """
        # Covered in step 1

    def test_003_navigate_to_racing_edp_template_and_leave_the_description_blank_for_one_of_the_market_template(self):
        """
        DESCRIPTION: Navigate to Racing EDP template and leave the description blank for one of the market template
        EXPECTED: User should be able to save the changes in CMS
        """
        racing_edp_market_list = self.cms_config.get_markets_with_description()
        for item in racing_edp_market_list:
            if item.get('name') == 'Win or Each Way':
                self.__class__.desc1 = item.get('description')
            elif item.get('name') == 'Win Only':
                self.__class__.desc2 = item.get('description')
            elif item.get('name') == 'Betting Without':
                self.__class__.desc3 = item.get('description')
        self.cms_config.create_and_update_markets_with_description(name='Win or Each Way', description='')
        self.cms_config.create_and_update_markets_with_description(name='Win Only', description='')
        self.cms_config.create_and_update_markets_with_description(name='Betting Without', description='')

    def test_004_launch_coral_ladbrokes_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: Launch Coral /Ladbrokes URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        self.site.wait_content_state("Homepage")

    def test_005_navigate_to_sports_menuhorse_racingfrom_a_z_all_sports_horse_racing(self):
        """
        DESCRIPTION: Navigate to Sports Menu(Horse Racing)/From A-Z all Sports->Horse Racing
        EXPECTED: User should be navigated Horse racing landing page
        """
        if self.device_type == 'desktop':
            sports = self.site.header.sport_menu.items_as_ordered_dict
            self.assertIn(vec.sb.HORSERACING.upper(), sports.keys(), msg=f'"{vec.sb.HORSERACING.upper()}" is not found in the header sport menu')
            sports.get(vec.sb.HORSERACING.upper()).click()
        else:
            self.navigate_to_page('horse-racing')
        self.site.wait_content_state(state_name='Horseracing', timeout=50)

    def test_006_click_on_any_race_which_has_the_market_templates_available_for_which_description_is_left_blank_in_cms(self):
        """
        DESCRIPTION: Click on any race which has the Market templates available for which description is left blank in CMS
        EXPECTED: User should be navigated to EDP page
        """
        self.delete_cookies()
        self.device.refresh_page()
        self.site.wait_splash_to_hide(timeout=10)
        self.navigate_to_edp(event_id=self.eventID_hr, sport_name='horse-racing')

    def test_007_validate_the_description_below_the_market_tab(self):
        """
        DESCRIPTION: Validate the description below the Market tab
        EXPECTED: User should not be displayed description
        """
        sleep(5)
        self.__class__.market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertTrue(self.market_tabs, msg='No market tabs found on EDP')
        racing_edp_market_list = self.cms_config.get_markets_with_description()
        self.assertTrue(racing_edp_market_list, msg='"racing edp markets" is not displayed in CMS')
        self.__class__.new_markets = [market['name'] for market in racing_edp_market_list]
        for index, item in enumerate(self.new_markets):
            if item.upper() == vec.racing.RACING_EDP_WIN_OR_EACH_WAY_FULL_NAME:
                self.new_markets[index] = 'WIN OR E/W'

        for market_name, market in self.market_tabs.items():
            for exp_market in self.new_markets:
                if market_name == exp_market.upper():
                    market.click()
                    edp = self.site.racing_event_details
                    market_description = edp.has_market_description_text(expected_result=False)
                    self.assertFalse(market_description, msg='Market description is not displayed')

    def test_008_navigate_to_grey_hounds_and_repeat_67_steps(self):
        """
        DESCRIPTION: Navigate to Grey Hounds and Repeat 6,7 steps
        EXPECTED: User should not be displayed description
        """
        self.navigate_to_page("greyhound-racing")
        self.delete_cookies()
        self.device.refresh_page()
        self.site.wait_splash_to_hide(timeout=10)
        sleep(5)
        self.navigate_to_edp(event_id=self.eventID_gr, sport_name='greyhound-racing')
        self.site.wait_content_state_changed()

        self.market_tabs = self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertTrue(self.market_tabs, msg='No market tabs found on EDP')
        for market_name, market in self.market_tabs.items():
            for exp_market in self.new_markets:
                if market_name == exp_market.upper():
                    market.click()
                    edp = self.site.greyhound_event_details
                    market_description = edp.has_market_description_text(expected_result=False)
                    self.assertFalse(market_description, msg='Market description is not displayed')

    def test_009_repeat_step_3_for_different_market_templates(self):
        """
        DESCRIPTION: Repeat Step 3 for different market templates
        EXPECTED: User should be able to save the changes in CMS
        """
        # Covered in Step 3

    def test_010_repeat_67_steps_for_both_grey_hounds_and_horse_racing(self):
        """
        DESCRIPTION: Repeat 6,7 Steps for both Grey Hounds and Horse racing
        """
        # Covered in step 7 and 8
