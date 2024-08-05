import pytest
import tests
from tests.base_test import vtest
from time import sleep
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2
@pytest.mark.crl_prod
@pytest.mark.desktop
@pytest.mark.horseracing
@pytest.mark.greyhounds
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C60094962_Verify_the_display_of_header_for_selected_Market(BaseRacing):
    """
    TR_ID: C60094962
    NAME: Verify the display of header for selected Market
    DESCRIPTION: Verify the  header for selected market will be styled as per the new designs
    DESCRIPTION: 1: Bold text for selected market on light background
    DESCRIPTION: 2: Line underneath header to indicate
    PRECONDITIONS: 1: Horse Racing & Grey Hounds Racig events should be available
    PRECONDITIONS: 2: Markets should be available for the events
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Market Descriptions should be configured and enabled in CMS
        """
        if tests.settings.backend_env == 'prod':
            self.__class__.event = \
                self.get_active_events_for_category(category_id=21, expected_template_market='Win or Each Way')[0]
            self.__class__.event2 = \
                self.get_active_events_for_category(category_id=19, expected_template_market='Win or Each Way')[0]
        else:
            self.__class__.event = self.ob_config.add_UK_racing_event(number_of_runners=1)
            self.__class__.event2 = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1)

    def test_001_launch_coral_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: Launch Coral URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: URL should be launcheds
        EXPECTED: For Mobile: App should be opened
        """
        self.site.wait_content_state('Homepage')

    def test_002_navigate_to_sports_menuhorse_racingfrom_a_z_all_sports_horse_racing(self):
        """
        DESCRIPTION: Navigate to Sports Menu(Horse Racing)/From A-Z all Sports->Horse Racing
        EXPECTED: User should be navigated Horse racing landing page
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('horse-racing')

    def test_003_click_on_any_horse_racing_event_which_has_markets_available(self):
        """
        DESCRIPTION: Click on any Horse racing event which has markets available
        EXPECTED: User should be navigated to the Event details page
        """
        event_id = self.event['event']['id'] if tests.settings.backend_env == 'prod' else self.event.event_id
        self.navigate_to_edp(event_id=event_id, sport_name='horse-racing')
        self.__class__.market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertTrue(self.market_tabs, msg='No market tabs found on EDP')

    def test_004_validate_the_market_headers(self, event_type='horseracing'):
        """
        DESCRIPTION: Validate the Market Headers
        DESCRIPTION: ![](index.php?/attachments/get/120844527)
        DESCRIPTION: ![](index.php?/attachments/get/120844528)
        EXPECTED: 1: By Default first Market Header should be selected
        EXPECTED: 2: Selected Market should be in Bold on light background
        EXPECTED: 3: Blue Line underneath header to indicate
        """
        if event_type == 'horseracing':
            current_tab = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.current
        else:
            current_tab = self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list.current
        self.assertTrue(current_tab, msg=f'By default, first market "{current_tab}" is not selected as default')
        default_tab = list(self.market_tabs.values())[0]
        self.assertEqual(default_tab.background_color_name, 'transparent',
                         msg=f'Background color value"{default_tab.background_color_name}" is not same as transparent')
        font_weight = default_tab.css_property_value('font-weight')
        self.assertEqual(default_tab.css_property_value('font-weight'), '700',
                         msg=f'Selected market is not bold. Expected: 700, Actual: "{font_weight}"')

    def test_005_click_on_any_other_market_tab_in_the_edp(self):
        """
        DESCRIPTION: Click on any other Market tab in the EDP
        EXPECTED: 1: Selected Market should be in Bold on light background
        EXPECTED: 2: Blue Line underneath header to indicate
        """
        if len(self.market_tabs) > 1:
            (list(self.market_tabs.values())[1]).click()
            sleep(3)    # CSS styles to load
            self.site.wait_splash_to_hide(3)
            next_tab = list(self.market_tabs.values())[1]
            self.assertEqual(next_tab.background_color_name, 'transparent',
                             msg=f'Background color name "{next_tab.background_color_name}" is not same as transparent')
            font_weight = next_tab.css_property_value('font-weight')
            self.assertEqual(font_weight, '700',
                             msg=f'Selected market is not bold. Expected: 700, Actual: "{font_weight}"')

    def test_006_repeat_the_same_for_grey_hound(self):
        """
        DESCRIPTION: Repeat the same for Grey Hound
        EXPECTED: As per steps
        """
        self.navigate_to_page('homepage')
        self.navigate_to_page(name='greyhound-racing')
        self.site.wait_content_state('greyhound-racing')
        event_id = self.event2['event']['id'] if tests.settings.backend_env == 'prod' else self.event2.event_id
        self.navigate_to_edp(event_id=event_id, sport_name='greyhound-racing')
        self.market_tabs = self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertTrue(self.market_tabs, msg='No market tabs found on EDP')
        self.test_004_validate_the_market_headers(event_type='greyhound')
        self.test_005_click_on_any_other_market_tab_in_the_edp()
