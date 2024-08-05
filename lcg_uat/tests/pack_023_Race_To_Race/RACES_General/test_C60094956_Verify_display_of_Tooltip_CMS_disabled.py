import pytest
import tests
from time import sleep
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Events cannot be created on prod & beta
@pytest.mark.medium
@pytest.mark.slow
@pytest.mark.desktop
@pytest.mark.horseracing
@pytest.mark.races
@pytest.mark.races_negative_p1  # Marker for testcases having negativing scenario like disabling a functionality
@vtest
class Test_C60094956_Verify_display_of_Tooltip_CMS_disabled(BaseRacing):
    """
    TR_ID: C60094956
    NAME: Verify display of Tooltip: CMS disabled
    DESCRIPTION: Verify that User is not able to view the Tooltip when Tooltip is disabled in CMS although the event has additional markets that need scrolling
    PRECONDITIONS: 1: Tooltip should be disabled in CMS
    PRECONDITIONS: 2: HR/GH event should be available with additional markets that needs scrolling
    PRECONDITIONS: 3: Tooltip for the device is not shown previously
    """
    keep_browser_open = True
    section_skip_list = ['VIRTUAL RACING', 'VIRTUAL RACE CAROUSEL', 'ENHANCED RACES', 'NEXT RACES',
                         'OFFERS & FEATURED RACES']
    event_markets = [('win_only',),
                     ('betting_without',),
                     ('to_finish_second',),
                     ('top_2_finish',),
                     ('insurance_2_places',),
                     ('antepost',)]

    @classmethod
    def custom_tearDown(cls):
        if tests.settings.cms_env != 'prd0':
            cls.get_cms_config().update_system_configuration_structure(
                config_item='SecondaryMarketsTooltip', field_name='enabled', field_value=True)

    def test_000_preconditions(self):
        if self.get_initial_data_system_configuration().get('SecondaryMarketsTooltip', {}).get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='SecondaryMarketsTooltip',
                                                                  field_name='enabled', field_value=False)
        event_params_hr = self.ob_config.add_UK_racing_event(markets=self.event_markets,
                                                             forecast_available=True, tricast_available=True)
        self.__class__.eventID_hr = event_params_hr.event_id
        event_params_gr = self.ob_config.add_UK_greyhound_racing_event(markets=self.event_markets,
                                                                       forecast_available=True, tricast_available=True)
        self.__class__.eventID_gr = event_params_gr.event_id

    def test_001_launch_coral_ladbrokes_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: Launch Coral/ Ladbrokes URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        self.cms_horse_tab_name = self.get_sport_title(category_id=21)
        sport = self.cms_horse_tab_name if self.device_type == 'mobile' and self.brand == 'ladbrokes' else self.cms_horse_tab_name.upper()
        if self.device_type == 'desktop':
            self.site.sport_menu.click_item(sport)
        else:
            self.site.home.menu_carousel.click_item(sport)

    def test_002_navigate_to_sports_menuhorse_racingfrom_a_z_all_sports_horse_racing(self):
        """
        DESCRIPTION: Navigate to Sports Menu(Horse Racing)/From A-Z all Sports->Horse Racing
        EXPECTED: Horse Racing Landing page should be displayed
        """
        # covered in step 1

    def test_003_click_on_any_horse_racing_event_that_has_additional_markets_that_needs_scrolling(self):
        """
        DESCRIPTION: Click on any horse racing event that has additional markets that needs scrolling
        EXPECTED: User should be navigated to event details page (race card)
        """
        self.site.wait_splash_to_hide()
        sleep(5)
        self.navigate_to_edp(event_id=self.eventID_hr, sport_name='horse-racing')

    def test_004_validate_tooltip_display(self):
        """
        DESCRIPTION: Validate Tooltip display
        EXPECTED: User should not be able to view the Tooltip
        """
        self.cms_config.update_system_configuration_structure(config_item='SecondaryMarketsTooltip',
                                                              field_name='enabled', field_value=False)
        self.delete_cookies()
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        sleep(5)
        racing_details = self.site.racing_event_details
        self.assertFalse(racing_details.has_tooltip_container, msg=f'Tooltip is Displayed for the event')

    def test_005_repeat_step_2_to_step_4_and_validate_for_grey_hound_racing(self):
        """
        DESCRIPTION: Repeat Step 2 to Step 4 and Validate for Grey Hound racing
        EXPECTED: User should not be able to view the Tooltip
        """
        self.navigate_to_edp(event_id=self.eventID_gr, sport_name='greyhound-racing')
        self.cms_config.update_system_configuration_structure(config_item='SecondaryMarketsTooltip',
                                                              field_name='enabled', field_value=False)
        self.delete_cookies()
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        sleep(5)
        self.assertFalse(self.site.greyhound_event_details.tab_content.has_tooltip_container, msg=f'Tooltip is Displayed for the event')
