import pytest
import re
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Cannot create events in prod/beta (req: Additional markets)
@pytest.mark.mobile_only
@pytest.mark.slow
@pytest.mark.horseracing
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C60094961_Verify_display_of_Tooltip_only_once_for_a_device(Common):
    """
    TR_ID: C60094961
    NAME: Verify display of Tooltip: only once for a device
    DESCRIPTION: Verify that ToolTip is displayed only once for a device
    PRECONDITIONS: 1: Tooltip should be enabled in CMS
    PRECONDITIONS: 2: HR/GH events should be available with additional markets that needs scrolling
    PRECONDITIONS: 3: Tooltip for the device is not shown previously
    """
    keep_browser_open = True

    event_markets = [('win_only',),
                     ('betting_without',),
                     ('to_finish_second',),
                     ('top_2_finish',),
                     ('insurance_2_places',),
                     ('antepost',)]

    def clear_cookies(self):
        """
        DESCRIPTION: Clear local storage and Download the app.
        PRECONDITIONS: Clear all the cookies for WEB
        """
        self.delete_cookies()
        self.device.driver.execute_script('localStorage.clear();')
        self.device.driver.implicitly_wait(5)

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1: Tooltip should be enabled in CMS
        PRECONDITIONS: 2: HR/GH events should be available with additional markets that needs scrolling
        PRECONDITIONS: 3: Tooltip for the device is not shown previously
        """
        tooltip_status = self.cms_config.update_secondary_market_tooltip(enabled=True)
        self.assertTrue(tooltip_status, msg='tooltip is not enabled')
        event_params = self.ob_config.add_UK_racing_event(markets=self.event_markets, forecast_available=True,
                                                          tricast_available=True)
        self.__class__.HR_eventID = event_params.event_id

    def test_001_launch_coral_ladbrokes_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: Launch Coral/ Ladbrokes URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        self.site.wait_content_state('Homepage')

    def test_002_navigate_to_sports_menuhorse_racingfrom_a_z_all_sports_horse_racing(self):
        """
        DESCRIPTION: Navigate to Sports Menu(Horse Racing)/From A-Z all Sports->Horse Racing
        EXPECTED: Horse Racing Landing page should be displayed
        """
        cms_horse_tab_name = self.get_sport_title(category_id=self.ob_config.horseracing_config.category_id)
        cms_horse_tab_name = cms_horse_tab_name if self.device_type == 'mobile' and self.brand == 'ladbrokes' else cms_horse_tab_name.upper()
        if self.device_type == 'mobile':
            all_items = self.site.home.menu_carousel.items_as_ordered_dict
        else:
            all_items = self.site.header.sport_menu.items_as_ordered_dict
        all_items.get(cms_horse_tab_name).click()
        self.site.wait_content_state('horse-racing')

    def test_003_click_on_any_horse_racing_event_that_has_additional_markets_that_needs_scrolling(self):
        """
        DESCRIPTION: Click on any horse racing event that has additional markets that needs scrolling
        EXPECTED: User should be navigated to event details page (race card)
        """
        self.navigate_to_edp(event_id=self.HR_eventID, sport_name='horse-racing')
        self.clear_cookies()
        self.device.refresh_page()
        self.site.wait_content_state(state_name='RacingEventDetails', timeout=10)

    def test_004_validate_that_there_are_more_markets_for_you_to_view_below_tooltip_is_displayed(self):
        """
        DESCRIPTION: Validate that "There are more markets for you to view below" Tooltip is displayed
        EXPECTED: User should be able to see the Tooltip "There are more markets for you to view below" which is displayed is same as that is Configured in CMS
        """
        has_tooltip = self.site.racing_event_details.tab_content.has_additional_markets_tooltip
        self.assertTrue(has_tooltip, msg='Tooltip for Additional Markets is not displayed')
        actual_tooltip_text = self.site.racing_event_details.tab_content.additional_markets_tooltip.text
        cms_tooltip = self.cms_config.get_system_configuration_item('SecondaryMarketsTooltip').get('title')
        cms_tooltip_text = re.sub(' +', ' ', cms_tooltip)
        self.assertEqual(actual_tooltip_text, cms_tooltip_text,
                         msg=f'Actual tooltip "{actual_tooltip_text}" is not same as in CMS configuration "{cms_tooltip_text}"')

    def test_005_click_anywhere_on_screen_and_validate_that_tooltip_is_closed(self):
        """
        DESCRIPTION: Click anywhere on screen and Validate that Tooltip is closed
        EXPECTED: Tooltip should be closed
        """
        self.site.racing_event_details.tab_content.additional_markets_tooltip.click()
        has_tooltip = self.site.racing_event_details.tab_content.has_additional_markets_tooltip
        self.assertFalse(has_tooltip, msg='tooltip for additional markets is displayed')

    def test_006_click_on_back_button(self):
        """
        DESCRIPTION: Click on Back button
        EXPECTED: User should be navigated back to racing landing page
        """
        self.site.back_button_click()
        self.site.wait_content_state_changed()

    def test_007_navigate_back_to_the_same_event_and_validate_tooltip_display(self):
        """
        DESCRIPTION: Navigate back to the same event and validate Tooltip display
        EXPECTED: 1: User should be navigated to Event details page
        EXPECTED: 2: User should not be displayed any tooltip
        """
        self.navigate_to_edp(event_id=self.HR_eventID, sport_name='horse-racing')
        self.site.wait_content_state(state_name='RacingEventDetails')
        has_tooltip = self.site.racing_event_details.tab_content.has_additional_markets_tooltip
        self.assertFalse(has_tooltip, msg='tooltip for additional markets is displayed')

    def test_008_repeat_the_same_by_logging_out_or_re_launching_the_app(self):
        """
        DESCRIPTION: Repeat the same by logging out or re-launching the App
        EXPECTED: 1: No Tooltip should be displayed
        """
        self.device.open_new_tab()
        tabs = self.device.driver.window_handles
        self.device.driver.switch_to.window(tabs[1])
        self.navigate_to_page('Homepage')
        self.site.wait_content_state('homepage')
        self.test_007_navigate_back_to_the_same_event_and_validate_tooltip_display()
