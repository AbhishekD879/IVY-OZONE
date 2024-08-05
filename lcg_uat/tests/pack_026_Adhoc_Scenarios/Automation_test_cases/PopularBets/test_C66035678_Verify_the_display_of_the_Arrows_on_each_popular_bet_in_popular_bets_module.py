import json

import pytest
import vec

from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C66035678_Verify_the_display_of_the_Arrows_on_each_popular_bet_in_popular_bets_module(Common):
    """
    TR_ID: C66035678
    NAME: Verify the display  of the Arrows on each popular bet in popular bets module
    DESCRIPTION: This test case verifies the Display of Arrows on each popular bet in popular bets module
    PRECONDITIONS: Configure Popular bets tab in CMS (CMS>Sports pages>Popular bets)
    """
    keep_browser_open = True
    event_names_with_UP = []
    event_names_with_DOWN = []

    def bet_positions_data(self, payload):
        positions_list = list(list(json.loads(payload))[1]['positions'])
        for i in range(0,len(positions_list)):
            if positions_list[i]['position'] == 'UP':
                self.event_names_with_UP.append(positions_list[i]['event']['markets'][0]['outcomes'][0]['name'])
            elif positions_list[i]['position'] == 'DOWN':
                self.event_names_with_DOWN.append(positions_list[i]['event']['markets'][0]['outcomes'][0]['name'])

    def get_popular_bet_payload(self, brand):
        perflog = self.device.get_performance_log()
        for log in list(reversed(perflog)):
            try:
                payload = log[1]['message']['message']['params']['response']['payloadData']
                if 'positions' in payload and 'nbets' in payload and 'position' in payload and 'rank' in payload:
                    return payload
            except (KeyError, IndexError, AttributeError):
                continue
        return {}

    def test_000_launch_the_application(self):
        """
        DESCRIPTION: getting popular bet tab display name from CMS
        """
        all_sub_tabs_for_football = self.cms_config.get_sport_tabs(sport_id=self.ob_config.football_config.category_id)
        for tab in all_sub_tabs_for_football:
            if tab['enabled']==True and tab['name'] == 'popularbets':
                self.__class__.tab_name = tab['displayName'].upper()

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the Application
        EXPECTED: Application is launched Successfully
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state("football")

    def test_002_click_on_the_football_sport(self):
        """
        DESCRIPTION: Click on the Football Sport
        EXPECTED: Able to navigate to the Football landing page
        """
        # covered in above step

    def test_003_click_on_popular_bets_tab(self):
        """
        DESCRIPTION: Click on Popular bets Tab
        EXPECTED: 1. Popular bets tab is Opened.
        EXPECTED: 2. Popular bets content is loaded.
        """
        actual_sports_tabs = self.site.sports_page.tabs_menu.items_as_ordered_dict
        self.assertTrue(actual_sports_tabs, f'tabs are not available for football')
        for tab_name, tab in actual_sports_tabs.items():
            if tab_name.upper() == self.tab_name:
                tab.click()
        backed_filter = self.site.football.tab_content.backed_filter
        backed_sort_filter = backed_filter.backed_sort_filter
        backed_sort_filter.click()
        backed_time_filter_names = list(
            self.site.football.tab_content.backed_filter.backed_dropdown.items_as_ordered_dict.keys())
        for item_name in backed_time_filter_names:
            if item_name == '1 hr':
                backed_filter.backed_dropdown.select_item_with_name(item_name=item_name)
        timeline_filters = self.site.football.tab_content.timeline_filters.items_as_ordered_dict
        for time, time_obj in timeline_filters.items():
            if time == '1 hr':
                time_obj.click()

    def test_004_verify_the_display_of_arrows_on_each_popular_bet_in_popular_bets_module(self):
        """
        DESCRIPTION: Verify the Display of Arrows on each popular bet in popular bets module
        EXPECTED: User should be displayed with the arrows to display each and every bet in the list of popular bets
        """
        brand = 'ladbrokes' if self.brand == 'labrokes' else 'coral'
        prev_payload = self.get_popular_bet_payload(brand=brand)
        time, timeout, after_call_changed = 0, 48, None
        while time < timeout:
            new_payload = self.get_popular_bet_payload(brand=brand)
            if prev_payload == new_payload:
                wait_for_haul(5)
                continue
            else:
                after_call_changed = new_payload
                break

        if after_call_changed:
            self.bet_positions_data(after_call_changed)

    def test_005_verify_the_display_of_arrow_when_the_arrow_mark_is_towards_up(self):
        """
        DESCRIPTION: Verify the Display of Arrow when the arrow mark is towards up
        EXPECTED: 1. User should be displayed with the Green arrow mark towards up if the position of the popular bet is ranked higher in the list
        EXPECTED: 2. On every refresh the green arrow marks should be displayed based on the position
        """
        ws_call_UP_arrow_event_names = self.event_names_with_UP
        ws_call_DOWN_arrow_event_names = self.event_names_with_DOWN

    def test_006_verify_the_display_of_arrow_when_the_arrow_mark_is_towards_down(self):
        """
        DESCRIPTION: Verify the Display of Arrow when the arrow mark is towards down
        EXPECTED: 1. User should be displayed with the red arrow mark towards down if the position of the popular bet is ranked lower in the list.
        EXPECTED: 2. On every refresh the red arrow marks should be displayed based on the position.
        """
        pass

    def test_007_verify_the_display_of_arrow_when_there_is_no_change(self):
        """
        DESCRIPTION: Verify the Display of Arrow when there is no change
        EXPECTED: 1. User should be displayed with the No change symbol if the position of the popular bet didn't change from the last iteration.
        EXPECTED: 2. On every refresh no change should be displayed based on the position
        """
        pass
