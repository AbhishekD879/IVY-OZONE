import pytest
from crlat_cms_client.utils.exceptions import CMSException
import tests
from tests.base_test import vtest
import re
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.waiters import wait_for_result, wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.popular_bets
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@pytest.mark.popular_bets_GA_tracking
@pytest.mark.football
@pytest.mark.reg_170_fix
@pytest.mark.other
@vtest
class Test_C65948318_Verify_GA_tracking_for_Page_View_once_the_click_on_Tabs(BaseDataLayerTest):
    """
    TR_ID: C65948318
    NAME: Verify GA tracking for Page View once the click on Tabs
    DESCRIPTION: This test case verifies GA tracking for Page View once the click on Tabs
    PRECONDITIONS: Configure Popular bets tab in CMS (CMS>Sports pages>Popular bets)
    PRECONDITIONS: Should have Football events
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Configure Popular bets tab in CMS (CMS>Sports pages>Popular bets)
        """
        # getting popular bets tab name according to the brand from cms
        all_sub_tabs_for_football = self.cms_config.get_sport_tabs(sport_id=self.ob_config.football_config.category_id)
        tab = next((tab for tab in all_sub_tabs_for_football if
                    tab['enabled'] and tab['name'] == 'popularbets'), None)
        self.__class__.tab_name = tab['displayName'].upper()
        self.__class__.label_event_tab_name = next(
            (sub_tab['trendingTabName'] for sub_tab in tab['trendingTabs'] for inner_sub_tab in sub_tab['popularTabs']
             if inner_sub_tab['popularTabName'] == 'Popular_tab'), None)
        if not self.tab_name:
            raise CMSException('Popular Bet tab is not enabled in CMS!!')

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the Application
        EXPECTED: User should launch the Application Successfully
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_002_click_on_the_football_sport(self):
        """
        DESCRIPTION: Click on the Football Sport
        EXPECTED: Able to navigate to the Football landing page
        """
        self.site.open_sport('football')

    def test_003_click_on_popular_bets_section(self):
        """
        DESCRIPTION: Click on Popular Bets section
        EXPECTED: Able to navigate to the Popular Bets section successfully
        """
        actual_sports_tabs = self.site.sports_page.tabs_menu.items_as_ordered_dict
        self.__class__.insights_tab = actual_sports_tabs.get(self.tab_name)
        self.insights_tab.click()
        wait_for_result(lambda: self.site.football.tabs_menu.current.upper() == self.tab_name.upper())
        current_tab = self.site.football.tabs_menu.current.upper()
        self.assertEqual(current_tab, self.tab_name.upper(), f'Actual Highlighted Tab : "{current_tab}" is not same as' f'Expected Highlighted Tab : "{self.tab_name}"')
        wait_for_haul(3)
        self.__class__.url = self.device.get_current_url()
        self.__class__.page_url = self.url.replace(f'https://{tests.HOSTNAME}', '').split('?')[0]

    def test_004_click_on_tab_and_observe_ga_tracking_for_page_view(self):
        """
        DESCRIPTION: Click on tab and Observe GA tracking for page view
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'pageView',
        EXPECTED: [{
        EXPECTED: page.host:"sports.coral.co.uk",
        EXPECTED: page.name : "sport/football/popularbets/popular-bets",
        EXPECTED: page.pathQueryAndFragment :"en/sport/football/popularbets/popular-bets",
        EXPECTED: page.referrer: "https://sports.coral.co.uk/sport/football/popularbets/popular-bets,
        EXPECTED: page.url :"https://sports.coral.co.uk/sport/football/matches"
        EXPECTED: });
        """
        expected_resp = {
            'event': 'pageView',
            'page.referrer': self.insights_tab.href,
            'page.url': self.url,
            'page.host': tests.HOSTNAME,
            'page.pathQueryAndFragment': 'en'+self.page_url,
            'page.name': self.page_url[1:]
        }
        actual_resp = self.get_data_layer_specific_object(object_key='event',
                                                          object_value='pageView')
        comparison_result = next((False for key, value in expected_resp.items() if actual_resp.get(key) != value), True)
        self.assertTrue(comparison_result, msg=f'{expected_resp} is not in {actual_resp}')

        #####################this step coveres testcase C65948319#####################
    def test_005_observe_ga_tracking(self):
        """
        TR_ID: C65948319
        NAME: Verify GA tracking for clicks on Tabs
        DESCRIPTION: Observe GA tracking
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'Event.Tracking',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'navigation',
        EXPECTED: component.LabelEvent: 'sub navigation',
        EXPECTED: component.ActionEvent: 'click',
        EXPECTED: component.PositionEvent: '{from tab name} ex:matches',
        EXPECTED: component.LocationEvent: '{sport name} ex:football,cricket',
        EXPECTED: component.EventDetails: '{to tab name} ex: popular bets',
        EXPECTED: component.URLClicked: '{clicked url} ex:https://sports.coral.co.uk/sport/football/popularbets'
        EXPECTED: }]
        EXPECTED: });
        """
        def verify(position_event="matches"):
            expected_resp = {
                'event': 'Event.Tracking',
                'component.CategoryEvent': 'navigation',
                'component.LabelEvent': 'sub navigation',
                'component.ActionEvent': 'click',
                'component.PositionEvent': position_event,
                'component.LocationEvent': 'football',
                'component.EventDetails': 'popular-bets',
                'component.URLClicked': self.url
            }
            actual_resp = self.get_data_layer_specific_object(object_key='event',
                                                           object_value='Event.Tracking')
            return expected_resp == actual_resp, expected_resp, actual_resp

        status, expected_resp, actual_resp = verify()
        if not status:
            status, expected_resp, actual_resp = verify('N/A')

        self.assertEqual(actual_resp, expected_resp)

        ######################this step covers testcase C65948320####################
    def test_006_observe_ga_tracking(self):
        """
        TR_ID: C65948320
        NAME: Verify GA tracking Info message load
        DESCRIPTION: Observe GA tracking
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'contentView',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'betting',
        EXPECTED: component.LabelEvent: 'popular bets',
        EXPECTED: component.ActionEvent: 'load',
        EXPECTED: component.PositionEvent: 'not applicable',
        EXPECTED: component.LocationEvent: 'popular bets',
        EXPECTED: component.EventDetails: 'info message',
        EXPECTED: component.URLClicked: 'not applicable'
        EXPECTED: }]
        EXPECTED: });
        """
        expected_resp3 = {
            'event': 'contentView',
            'component.CategoryEvent': 'betting',
            'component.LabelEvent': self.label_event_tab_name.lower(),
            'component.ActionEvent': 'load',
            'component.PositionEvent': 'not applicable',
            'component.LocationEvent': self.tab_name.lower(),
            'component.EventDetails': 'info message',
            'component.URLClicked': 'not applicable'
        }
        actual_resp3 = self.get_data_layer_specific_object(object_key='event',
                                                           object_value='contentView')

        self.assertEqual(actual_resp3, expected_resp3)


        #######################this step coveres testcase C65948321##############################
    def test_007_click_on_close_x_observe_ga_tracking(self):
        """
        TR_ID: C65948321
        NAME: Verify GA tracking for info message close icon
        DESCRIPTION: Click on close 'X' ,Observe GA tracking
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'Event.Tracking',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'betting',
        EXPECTED: component.LabelEvent: 'popular bets',
        EXPECTED: component.ActionEvent: 'close',
        EXPECTED: component.PositionEvent: 'not applicable',
        EXPECTED: component.LocationEvent: 'popular bets',
        EXPECTED: component.EventDetails: 'info message',
        EXPECTED: component.URLClicked: 'not applicable'
        EXPECTED: }]
        EXPECTED: });
        """
        actual_sports_tabs = self.site.sports_page.tabs_menu.items_as_ordered_dict
        tab = next((tab for tab_name, tab in actual_sports_tabs.items() if tab_name != self.tab_name), None)
        tab.click()
        actual_sports_tabs = self.site.sports_page.tabs_menu.items_as_ordered_dict
        pop_tab = next((tab for tab_name, tab in actual_sports_tabs.items() if tab_name == self.tab_name), None)
        pop_tab.click()
        self.site.wait_content_state_changed()
        desc_container = self.site.football.tab_content.description_container
        desc_close_btn = desc_container.close
        self.assertTrue(desc_close_btn,
                        msg=f' popular bets tab has no description close button for description tab')
        desc_close_btn.click()
        expected_resp4 = {
            'event': 'Event.Tracking',
            'component.CategoryEvent': 'betting',
            'component.LabelEvent': self.label_event_tab_name.lower(),
            'component.ActionEvent': 'close',
            'component.PositionEvent': 'not applicable',
            'component.LocationEvent': self.tab_name.lower(),
            'component.EventDetails': 'info message',
            'component.URLClicked': 'not applicable'
        }
        actual_resp4 = self.get_data_layer_specific_object(object_key='event',
                                                           object_value='Event.Tracking')

        self.assertEqual(actual_resp4, expected_resp4)

        #################################this step covers testcase C65948322###########################
    def test_008_click_on_filters_observe_ga_tracking(self):
        """
        TR_ID: C65948322
        NAME: Verify GA tracking for clicks on filters
        DESCRIPTION: Click on filters ,Observe GA tracking
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'Event.Tracking',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'betting',
        EXPECTED: component.LabelEvent: 'popular bets',
        EXPECTED: component.ActionEvent: 'click',
        EXPECTED: component.PositionEvent: 'not applicable',
        EXPECTED: component.LocationEvent: 'popular bets',
        EXPECTED: component.EventDetails: '{clicked filter} ex:30mins, 1hr etc',
        EXPECTED: component.URLClicked: 'not applicable'
        EXPECTED: }]
        EXPECTED: });
        """
        backed_filter = self.site.football.tab_content.backed_filter
        backed_sort_filter = backed_filter.backed_sort_filter
        backed_sort_filter.click()
        item_name = '30mins' if self.brand == 'ladbrokes' else '30 mins'
        backed_filter.backed_dropdown.select_item_with_name(item_name=item_name)
        expected_resp5 = {
            'event': 'Event.Tracking',
            'component.CategoryEvent': 'betting',
            'component.LabelEvent': self.label_event_tab_name,
            'component.ActionEvent': 'click',
            'component.PositionEvent': 'not applicable',
            'component.LocationEvent': self.tab_name.lower(),
            'component.EventDetails': item_name,
            'component.URLClicked': 'not applicable'
        }
        actual_resp5 = self.get_data_layer_specific_object(object_key='event',
                                                           object_value='Event.Tracking')

        self.assertEqual(actual_resp5, expected_resp5)


        ############################this step covers testcase C65948322############################
    def test_009_click_on_time_pills__observe_ga_tracking(self):
        """
        TR_ID: C65948323
        NAME: Verify GA tracking for Clicks on Time pills
        DESCRIPTION: Click on Time pills  ,Observe GA tracking
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'Event.Tracking',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'betting',
        EXPECTED: component.LabelEvent: 'popular bets',
        EXPECTED: component.ActionEvent: 'click',
        EXPECTED: component.PositionEvent: 'time filters',
        EXPECTED: component.LocationEvent: 'popular bets',
        EXPECTED: component.EventDetails: '{time} ex:1hr,3hr,5hr',
        EXPECTED: component.URLClicked: 'not applicable'
        EXPECTED: }]
        EXPECTED: });
        """
        time_filters = self.site.football.tab_content.timeline_filters.items_as_ordered_dict
        time_filters.get('24 hrs').click()
        expected_resp6 = {
            'event': 'Event.Tracking',
            'component.CategoryEvent': 'betting',
            'component.LabelEvent': self.label_event_tab_name,
            'component.ActionEvent': 'click',
            'component.PositionEvent': 'time filters',
            'component.LocationEvent': self.tab_name.lower(),
            'component.EventDetails': '24 hrs',
            'component.URLClicked': 'not applicable'
        }
        actual_resp6 = self.get_data_layer_specific_object(object_key='event',
                                                           object_value='Event.Tracking')

        self.assertEqual(actual_resp6, expected_resp6)




