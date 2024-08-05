import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.horseracing
@pytest.mark.greyhounds
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C60094943_Verify_market_description_table_for_HR_GH_CMS_enable(BaseRacing):
    """
    TR_ID: C60094943
    NAME: Verify market description table for HR/GH -CMS enable
    DESCRIPTION: Verify that market description is displayed in the EDP page below the Market tab when Horse racing/ Greyhounds market description table toggle is ON and Market description text is configured in CMS
    PRECONDITIONS: 1.  Horse racing & Grey Hound racing event should be available
    PRECONDITIONS: 2. User should have admin role for CMS
    PRECONDITIONS: 3: Market description table should have description added for the Market
    """
    keep_browser_open = True

    def test_001_login_to_cms(self):
        """
        DESCRIPTION: Login to CMS
        EXPECTED: User should be logged into CMS
        """
        if self.cms_config.get_system_configuration_structure()['RacingEDPMarketsDescription']['enabled']:
            self.cms_config.update_system_configuration_structure(config_item='RacingEDPMarketsDescription',
                                                                  field_name='enabled', field_value=True)

    def test_002_navigate_to_system_configuration__structure_and_enable_market_description_table(self):
        """
        DESCRIPTION: Navigate to System configuration > Structure and enable Market Description table
        EXPECTED: User should be able to enable Market Description table successfully
        """
        # Covered in step 1

    def test_003_launch_coral_ladbrokes_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: Launch Coral /Ladbrokes URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        self.site.wait_content_state("Homepage")

    def test_004_navigate_to_sports_menuhorse_racingfrom_a_z_all_sports_horse_racing(self):
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
        self.site.wait_content_state(state_name='Horseracing')

    def test_005_click_on_any_race_which_has_the_market_templates_available_for_which_description_is_configured_in_cms(self):
        """
        DESCRIPTION: Click on any race which has the Market templates available for which description is configured in CMS
        EXPECTED: User should be navigated to EDP page
        """
        category_events = self.get_active_events_for_category(category_id=21)
        for event in category_events:
            try:
                if event['event']['eventStatusCode'] == 'A':
                    self.__class__.active_event_id_HR = event['event']['id']
                    break
            except Exception:
                self._logger.info(f"****{event['event']['name']} is not resulted event")
        else:
            raise Exception('Active event not found')

        self.navigate_to_edp(event_id=self.active_event_id_HR, sport_name='horse-racing')
        self.site.wait_content_state_changed()

        self.__class__.market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertTrue(self.market_tabs, msg='No market tabs found on EDP')
        racing_edp_market_list = self.cms_config.get_markets_with_description()
        self.assertTrue(racing_edp_market_list, msg='"racing edp markets" is not displayed in CMS')
        self.__class__.new_markets = [market['name'] for market in racing_edp_market_list]
        for index, item in enumerate(self.new_markets):
            if item == vec.racing.RACING_EDP_WIN_OR_EACH_WAY_FULL_NAME:
                self.new_markets[index] = 'WIN OR E/W'

    def test_006_validate_the_description_below_the_market_tab(self):
        """
        DESCRIPTION: Validate the description below the Market tab
        EXPECTED: User should be able to view the description configured for that market template in CMS
        """
        # Covered in step 7

    def test_007_validate_the_description_for_different_market_templates_available(self):
        """
        DESCRIPTION: Validate the description for different market templates available
        EXPECTED: User should be able to view the description configured for that market template in CMS
        """
        for market_name, market in self.market_tabs.items():
            for exp_market in self.new_markets:
                if market_name == exp_market.upper():
                    market.click()
                    edp = self.site.racing_event_details
                    market_description = edp.has_market_description_text(expected_result=True)
                    self.assertTrue(market_description, msg='Market description is not displayed')

    def test_008_navigate_to_grey_hounds_and_repeat_567_steps(self):
        """
        DESCRIPTION: Navigate to Grey Hounds and Repeat 5,6,7 steps
        EXPECTED:
        """
        self.navigate_to_page("greyhound-racing")
        self.site.wait_splash_to_hide(timeout=10)
        category_events = self.get_active_events_for_category(category_id=19)
        for event in category_events:
            try:
                if event['event']['eventStatusCode'] == 'A':
                    self.__class__.active_event_id_GH = event['event']['id']
                    break
            except Exception:
                self._logger.info(f"****{event['event']['name']} is not resulted event")
        else:
            raise Exception('Active event not found')

        self.navigate_to_edp(event_id=self.active_event_id_GH, sport_name='greyhound-racing')
        self.site.wait_content_state_changed()

        self.market_tabs = self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertTrue(self.market_tabs, msg='No market tabs found on EDP')
        for market_name, market in self.market_tabs.items():
            for exp_market in self.new_markets:
                if market_name == exp_market.upper():
                    market.click()
                    edp = self.site.greyhound_event_details
                    market_description = edp.has_market_description_text(expected_result=True)
                    self.assertTrue(market_description, msg='Market description is not displayed')
