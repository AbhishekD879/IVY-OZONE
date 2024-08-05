import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Cannot create events in prod/beta (req: Additional markets)
@pytest.mark.slow
@pytest.mark.horseracing
@pytest.mark.greyhounds
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C60094960_Verify_Tool_Tip_Close(Common):
    """
    TR_ID: C60094960
    NAME: Verify Tool Tip Close
    DESCRIPTION: Verify that on clicking anywhere on screen Tooltip is closed
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
        PRECONDITIONS: 1: Tooltip should be enabled in CMS
        PRECONDITIONS: 2: HR/GH events should be available with additional markets that needs scrolling
        PRECONDITIONS: 3: Tooltip for the device is not shown previously
        """
        tooltip_status = self.cms_config.update_secondary_market_tooltip(enabled=True)
        self.assertTrue(tooltip_status, msg='tooltip is not enabled')
        event_params = self.ob_config.add_UK_racing_event(markets=self.event_markets, forecast_available=True,
                                                          tricast_available=True)
        self.__class__.HR_eventID = event_params.event_id
        event_params1 = self.ob_config.add_UK_greyhound_racing_event(markets=self.event_markets,
                                                                     forecast_available=True,
                                                                     tricast_available=True)
        self.__class__.GH_eventID = event_params1.event_id

    def test_001_launch_coral_ladbrokes_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: Launch Coral/ Ladbrokes URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        # covered in step 2

    def test_002_navigate_to_sports_menuhorse_racingfrom_a_z_all_sports_horse_racing(self):
        """
        DESCRIPTION: Navigate to Sports Menu(Horse Racing)/From A-Z all Sports->Horse Racing
        EXPECTED: Horse Racing Landing page should be displayed
        """
        self.sport_navigation(tabname=self.ob_config.horseracing_config.category_id)
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

    def test_004_validate_tooltip_displaytext_that_is_configured_in_cmsindexphpattachmentsget120878235indexphpattachmentsget120878237indexphpattachmentsget120878236indexphpattachmentsget120878238(
            self, sport='HR'):
        """
        DESCRIPTION: Validate Tooltip display
        DESCRIPTION: (Text that is configured in CMS)
        DESCRIPTION: ![](index.php?/attachments/get/120878235)
        DESCRIPTION: ![](index.php?/attachments/get/120878237)
        DESCRIPTION: ![](index.php?/attachments/get/120878236)
        DESCRIPTION: ![](index.php?/attachments/get/120878238)
        EXPECTED: User should be able to view the Tooltip "There are more markets for you to view below"
        EXPECTED: "Look below to find out what other markets are available"
        EXPECTED: (Text that is configured in CMS)
        """
        if sport == 'HR':
            has_tooltip = self.site.racing_event_details.tab_content.additional_markets_tooltip
            actual_tooltip_text = self.site.racing_event_details.tab_content.additional_markets_tooltip.text
        else:
            has_tooltip = self.site.greyhound_event_details.tab_content.additional_markets_tooltip
            actual_tooltip_text = self.site.greyhound_event_details.tab_content.additional_markets_tooltip.text
        self.assertTrue(has_tooltip, msg='tooltip for additional markets is not displayed')
        cms_tooltip_text = self.cms_config.get_system_configuration_item('SecondaryMarketsTooltip').get('title')
        self.assertEqual(actual_tooltip_text, cms_tooltip_text,
                         msg=f'Actual tooltip "{actual_tooltip_text}" is not same as in CMS configuration "{cms_tooltip_text}"')

    def test_005_click_anywhere_on_screen_and_validate_that_tooltip_is_closed(self, sport='HR'):
        """
        DESCRIPTION: Click anywhere on screen and Validate that Tooltip is closed
        EXPECTED: Tooltip should be closed
        """
        if sport == 'HR':
            tooltip = self.site.racing_event_details.tab_content.additional_markets_tooltip.click()
        else:
            tooltip = self.site.greyhound_event_details.tab_content.additional_markets_tooltip.click()
        self.assertFalse(tooltip, msg='tooltip for additional markets is displayed')

    def test_006_repeat_step_2_to_step_5_and_validate_for_grey_hound_racing_on_a_new_device(self):
        """
        DESCRIPTION: Repeat Step 2 to Step 5 and Validate for Grey Hound racing (On a new device)
        EXPECTED: Tooltip should be closed
        """
        self.sport_navigation(tabname=self.ob_config.greyhound_racing_config.category_id)
        self.site.wait_content_state('greyhound-racing')
        self.navigate_to_edp(event_id=self.GH_eventID, sport_name='greyhound-racing')
        self.clear_cookies()
        self.device.refresh_page()
        self.site.wait_content_state(state_name='GreyHoundEventDetails')
        self.test_004_validate_tooltip_displaytext_that_is_configured_in_cmsindexphpattachmentsget120878235indexphpattachmentsget120878237indexphpattachmentsget120878236indexphpattachmentsget120878238(
            sport='GR')
        self.test_005_click_anywhere_on_screen_and_validate_that_tooltip_is_closed(sport='GR')