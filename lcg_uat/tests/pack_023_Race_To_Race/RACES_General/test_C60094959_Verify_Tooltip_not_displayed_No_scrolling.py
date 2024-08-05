import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Cannot create events in prod/beta (req: Additional markets)
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.races
@pytest.mark.greyhounds
@pytest.mark.horseracing
@vtest
class Test_C60094959_Verify_Tooltip_not_displayed_No_scrolling(Common):
    """
    TR_ID: C60094959
    NAME: Verify Tooltip not displayed: No scrolling
    DESCRIPTION: Verify that Tooltip is displayed only when all markets are visible in tool bar (No Scrolling needed)
    PRECONDITIONS: 1: Tooltip should be enabled in CMS
    PRECONDITIONS: 2: HR/GH events without any additional markets should be available
    PRECONDITIONS: 3: Tooltip for the device is not shown previously
    """
    keep_browser_open = True
    event_markets = [('win_only',),
                     ('antepost',)]

    def clear_cookies(self):
        """
        DESCRIPTION: Clear local storage
        PRECONDITIONS: Clear all the cookies for WEB
        """
        self.delete_cookies()
        self.device.driver.execute_script('localStorage.clear();')
        self.device.driver.implicitly_wait(5)

    def sport_navigation(self, tabname):

        cms_horse_tab_name = self.get_sport_title(tabname)
        cms_horse_tab_name = cms_horse_tab_name if self.device_type == 'mobile' and self.brand == 'ladbrokes' else cms_horse_tab_name.upper()
        self.navigate_to_page('Homepage')
        if self.device_type == 'desktop':
            self.device.driver.set_window_size(width=1200, height=1600)
        if self.device_type == 'mobile':
            all_items = self.site.home.menu_carousel.items_as_ordered_dict
        else:
            all_items = self.site.header.sport_menu.items_as_ordered_dict
        all_items.get(cms_horse_tab_name).click()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Enable tooltip in CMS
        EXPECTED: Tooltip should be enabled
        """
        tooltip_status = self.cms_config.update_secondary_market_tooltip(enabled=True)
        self.assertTrue(tooltip_status, msg='tooltip is not enabled')
        HR_event_params = self.ob_config.add_UK_racing_event(markets=self.event_markets, forecast_available=True,
                                                             tricast_available=True)
        GH_event_params = self.ob_config.add_UK_greyhound_racing_event(markets=self.event_markets,
                                                                       forecast_available=True,
                                                                       tricast_available=True)
        self.__class__.HR_eventID = HR_event_params.event_id
        self.__class__.GH_eventID = GH_event_params.event_id

    def test_001_launch_coral_ladbrokes_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: Launch Coral/ Ladbrokes URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        # covered in step2

    def test_002_navigate_to_sports_menuhorse_racingfrom_a_z_all_sports_horse_racing(self):
        """
        DESCRIPTION: Navigate to Sports Menu(Horse Racing)/From A-Z all Sports->Horse Racing
        EXPECTED: Horse Racing Landing page should be displayed
        """
        self.sport_navigation(tabname=self.ob_config.horseracing_config.category_id)
        self.site.wait_content_state('horse-racing')

    def test_003_click_on_any_horse_racing_event_where_all_markets_are_displayed_in_the_tool_bar_no_scrolling_needed(self):
        """
        DESCRIPTION: Click on any horse racing event where all markets are displayed in the Tool bar (No Scrolling needed)
        EXPECTED: User should be navigated to event details page (race card)
        """
        self.clear_cookies()
        self.navigate_to_edp(event_id=self.HR_eventID, sport_name='horse-racing')
        self.site.wait_content_state('RacingEventDetails')

    def test_004_validate_that_no_tooltip_displayed(self):
        """
        DESCRIPTION: Validate that no Tooltip displayed
        EXPECTED: User should not be displayed any tooltip
        """
        has_tooltip = self.site.racing_event_details.tab_content.has_additional_markets_tooltip
        self.assertFalse(has_tooltip, msg='Tooltip for Additional Markets is displayed')

    def test_005_repeat_step_2_to_step_4_and_validate_for_grey_hound_racing(self):
        """
        DESCRIPTION: Repeat Step 2 to Step 4 and Validate for Grey Hound racing
        EXPECTED: User should not be displayed any tooltip
        """
        self.sport_navigation(tabname=self.ob_config.greyhound_racing_config.category_id)
        self.site.wait_content_state('greyhound-racing')
        self.clear_cookies()
        self.navigate_to_edp(event_id=self.GH_eventID, sport_name='greyhound-racing')
        self.site.wait_content_state(state_name='GreyHoundEventDetails')
        has_tooltip = self.site.greyhound_event_details.tab_content.has_additional_markets_tooltip
        self.assertFalse(has_tooltip, msg='Tooltip for Additional Markets is displayed')
