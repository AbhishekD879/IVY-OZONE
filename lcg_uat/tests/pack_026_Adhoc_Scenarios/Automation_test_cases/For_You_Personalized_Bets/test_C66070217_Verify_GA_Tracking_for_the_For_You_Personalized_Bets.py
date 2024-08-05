import pytest
from crlat_cms_client.utils.exceptions import CMSException
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from voltron.pages.shared import get_driver
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.for_you
@pytest.mark.adhoc_suite
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C66070217_Verify_GA_Tracking_for_the_For_You_Personalized_Bets(BaseDataLayerTest):
    """
    TR_ID: C66070217
    NAME: Verify GA Tracking for the For You Personalized Bets
    DESCRIPTION: This test case is to verify the GA Tracking for the For You Personalized Bets

    """
    keep_browser_open = True

    def verify_ga_tracking(self, category_event, label_event, action_event, position_event, event_details, event='Event.Tracking'):
        expected_resp = {
            "event": event,
            "component.CategoryEvent": category_event,
            "component.LabelEvent": label_event,
            "component.ActionEvent": action_event,
            "component.PositionEvent": position_event,
            "component.LocationEvent": self.tab_name.lower(),
            "component.EventDetails": event_details,
            "component.URLClicked": "not applicable",
        }
        actual_response = self.get_data_layer_specific_object(object_key='event', object_value=event)
        self.assertTrue(expected_resp, actual_response)

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. For you sub section is configured under the Insights tab in CMS.
        PRECONDITIONS: 2. Navigation to go CMS>Sports pages>Insights>For You
        """
        all_sub_tabs_for_football = self.cms_config.get_sport_tabs(sport_id=self.ob_config.football_config.category_id)

        tab = next((tab for tab in all_sub_tabs_for_football if
                    tab['enabled'] and tab['name'] == 'popularbets'), None)

        if not tab:
            raise CMSException('Insights/Popular Bets tab is not enabled in CMS!!')

        self.__class__.tab_name = tab['displayName'].upper()

        self.__class__.for_you_tab_name = next(
            (sub_tab['trendingTabName'] for sub_tab in tab['trendingTabs'] for inner_sub_tab in sub_tab['popularTabs']
             if inner_sub_tab['popularTabName'] == 'for-you-personalized-bets' and inner_sub_tab['enabled'] and sub_tab['enabled']), None)

        if not self.for_you_tab_name:
            raise CMSException('"Insights >> For You" or '
                               '"Insights >> For You >> Personalised Bets" is not enabled in CMS!!')

    def test_001_launch_the_application_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch the Application and Login with valid credentials
        EXPECTED: User should launch the Application and login Successfully
        """
        self.site.login()

    def test_002_navigate_to_the_football_insights_tab_and_click_on_the_for_you_tab(self):
        """
        DESCRIPTION: Navigate to the football insights tab and click on the For You tab
        EXPECTED: Able to navigate to the Football Insights page and can able to click on the For You tab
        """
        self.site.open_sport(vec.sb.FOOTBALL)
        self.site.football.tabs_menu.click_button(button_name=self.tab_name, timeout=10)
        self.__class__.url_before_clicking_on_for_you = self.device.get_current_url()
        self.site.football.tab_content.grouping_buttons.click_button(button_name=self.for_you_tab_name.upper())

    def test_003_verify_the_ga_tracking_when_user_clicks_on_the_for_you_tab(self):
        """
        DESCRIPTION: Verify the GA Tracking When user clicks on the For You tab
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'pageView',
        EXPECTED: [{
        EXPECTED: page.host:"sports.coral.co.uk",
        EXPECTED: page.name : "sport/football/competitions",
        EXPECTED: page.pathQueryAndFragment :"en/sport/football/competitions",
        EXPECTED: page.referrer: "https://sports.coral.co.uk/sport/football/matches/today",
        EXPECTED: page.url :"https://sports.coral.co.uk/sport/football/competitions"
        EXPECTED: });
        """
        host_name = tests.HOSTNAME
        expected_response = {
                                "event": "pageView",
                                "page.referrer": self.url_before_clicking_on_for_you,
                                "page.url": self.device.get_current_url(),
                                "page.host": host_name,
                                "page.pathQueryAndFragment": self.device.get_current_url().replace('https://' + host_name, 'en'),
                                "page.name": self.device.get_current_url().replace('https://' + host_name + '/', ''),
                            }
        raw_response = self.get_data_layer_specific_object(object_key='event', object_value='pageView')
        actual_response = {key: value for key, value in raw_response.items() if key not in ['eventTimeout', 'performance.nav']}
        self.assertTrue(expected_response, actual_response)

    def test_004_verify_the_display_of_for_you_description_message(self):
        """
        DESCRIPTION: Verify the Display of For You Description Message
        EXPECTED: Able to see the For You Description Message
        """
        description_container_status = self.site.football.tab_content.has_description_container()
        self.assertTrue(description_container_status, 'Description Container is not displayed')
        description = self.site.football.tab_content.description_container.description
        self.assertTrue(description, 'Description is not displayed')

    def test_005_verify_the_ga_tracking_for_the_for_you_description_info_message_load(self):
        """
        DESCRIPTION: Verify the GA Tracking for the For You Description Info Message Load
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'contentView',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'betting',
        EXPECTED: component.LabelEvent: 'personalised bets',
        EXPECTED: component.ActionEvent: 'load',
        EXPECTED: component.PositionEvent: 'for you bet',
        EXPECTED: component.LocationEvent: '{tab name} ex: insights',
        EXPECTED: component.EventDetails: 'info message',
        EXPECTED: component.URLClicked: 'not applicable'
        EXPECTED: }]
        EXPECTED: });
        """
        self.verify_ga_tracking(event='contentView', category_event='betting', label_event='for you',
                                action_event='load', position_event='not applicable', event_details='info message')

    def test_006_verify_the_display_of_for_you_description_message_info_close__icon(self):
        """
        DESCRIPTION: Verify the Display of For You Description Message info close  icon
        EXPECTED: Able to see the For You Description Message info close icon
        """
        self.__class__.close_btn = None
        try:
            self.__class__.close_btn = self.site.football.tab_content.description_container.close
        except:
            raise VoltronException('Close Button is not displayed in description container')

    def test_007_click_on_the_close_button(self):
        """
        DESCRIPTION: Click on the close button
        EXPECTED: For You description should close
        """
        self.close_btn.click()
        description_container_status = self.site.football.tab_content.has_description_container(expected_result=False)
        self.assertFalse(description_container_status, 'Description Still Displaying Front End')

    def test_008_verify_the_ga_tracking_for_the_for_you_description_info_message_close_icon(self):
        """
        DESCRIPTION: Verify the GA Tracking for the For You Description Info Message Close icon
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'Event.Tracking',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'betting',
        EXPECTED: component.LabelEvent: 'personalised bets',
        EXPECTED: component.ActionEvent: 'close',
        EXPECTED: component.PositionEvent: 'for you bet',
        EXPECTED: component.LocationEvent: '{tab name} ex: insights',
        EXPECTED: component.EventDetails: 'info message',
        EXPECTED: component.URLClicked: 'not applicable'
        EXPECTED: }]
        EXPECTED: });
        """
        self.verify_ga_tracking(category_event='betting', label_event='personalised bets',
                                action_event='close', position_event='for you bet', event_details='info message')

    def test_009_click_on_show_more(self):
        """
        DESCRIPTION: Click on Show More
        EXPECTED: Able to click on Show More and could see the more bets
        """
        show_more_status = self.site.football.tab_content.accordions_list.has_show_more_less()
        self.assertTrue(show_more_status, '"SHOW MORE" is not displayed.')
        self.site.football.tab_content.accordions_list.show_more_less.click()

    def test_010_verify_the_ga_tracking_when_user_clicks_on_show_more(self):
        """
        DESCRIPTION: Verify the GA Tracking When user clicks on Show More
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'Event.Tracking',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'betting',
        EXPECTED: component.LabelEvent: 'personalised bets',
        EXPECTED: component.ActionEvent: 'click',
        EXPECTED: component.PositionEvent: 'for you bet',
        EXPECTED: component.LocationEvent: '{tab name} ex: insights',
        EXPECTED: component.EventDetails: 'show more',
        EXPECTED: component.URLClicked: 'not applicable'
        EXPECTED: }]
        EXPECTED: });
        """
        self.verify_ga_tracking(category_event='betting', label_event='personalised bets',
                                action_event='click', position_event='for you bet', event_details='show more')

    def test_011_click_on_show_less(self):
        """
        DESCRIPTION: Click on Show Less
        EXPECTED: Able to click on Show Less and could see only 5 bets
        """
        show_more_less_btn = self.site.football.tab_content.accordions_list.show_more_less
        while show_more_less_btn.name.upper() == 'SHOW MORE':
            show_more_less_btn.click()
            show_more_less_btn = self.site.football.tab_content.accordions_list.show_more_less

        show_more_less_btn.click()

    def test_012_verify_the_ga_tracking_when_user_clicks_on_show_less(self):
        """
        DESCRIPTION: Verify the GA Tracking When user clicks on Show Less
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'Event.Tracking',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'betting',
        EXPECTED: component.LabelEvent: 'personalised bets',
        EXPECTED: component.ActionEvent: 'click',
        EXPECTED: component.PositionEvent: 'for you bet',
        EXPECTED: component.LocationEvent: '{tab name} ex: insights',
        EXPECTED: component.EventDetails: 'show less',
        EXPECTED: component.URLClicked: 'not applicable'
        EXPECTED: }]
        EXPECTED: });
        """
        self.verify_ga_tracking(category_event='betting', label_event='personalised bets', action_event='click',
                                position_event='for you bet', event_details='show less')

    def test_013_click_on_refresh_buttonicon(self):
        """
        DESCRIPTION: Click on Refresh button/icon
        EXPECTED: Able to click on Refresh button/icon
        """
        # descoped this refresh button

    def test_014_verify_the_ga_tracking_when_user_clicks_on_the_refresh_buttonicon(self):
        """
        DESCRIPTION: Verify the GA Tracking When user clicks on the refresh button/icon
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'Event.Tracking',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'betting',
        EXPECTED: component.LabelEvent: 'personalised bets',
        EXPECTED: component.ActionEvent: 'click',
        EXPECTED: component.PositionEvent: 'for you bet',
        EXPECTED: component.LocationEvent: '{tab name} ex: insights',
        EXPECTED: component.EventDetails: 'refresh icon',
        EXPECTED: component.URLClicked: 'not applicable'
        EXPECTED: }]
        EXPECTED: });
        """
        # descoped this refresh button
