import json
import re
import pytest
import tests
from tests.base_test import vtest
from crlat_cms_client.utils.exceptions import CMSException
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result, wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.popular_bets
@pytest.mark.adhoc_suite
@pytest.mark.football
@pytest.mark.other
@pytest.mark.reg167_fix
@vtest
class Test_C66035676_Verify_the_display_of_Popular_Bets_sub_section(BaseBetSlipTest):
    """
    TR_ID: C66035676
    NAME: Verify the display of Popular Bets sub section
    DESCRIPTION: This test case verifies the display of Popular Bets sub section
    """
    enable_bs_performance_log = True
    keep_browser_open = True
    events_data = {}

    def get_requestid_for_url(self):
        """
        :param url: Required URl
        :return: Complete url
        """
        host = tests.HOSTNAME.replace('-sports', '').replace('2', '') #if beta2 it replaces to beta
        request_id = None
        url = f'wss://trending-bets.{host}/trendingbets'
        perflog = self.device.get_performance_log(preserve=False)
        for log in list(reversed(perflog)):
            try:
                requested_url = log[1]['message']['message']['params']['url']
                if url in requested_url:
                    request_id = log[1]['message']['message']['params']['requestId']
                    break
            except KeyError:
                continue
        return request_id

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Configure Popular bets tab in CMS (CMS>Sports pages>Popular bets)
        """
        all_sub_tabs_for_football = self.cms_config.get_sport_tabs(sport_id=self.ob_config.football_config.category_id)

        insights_tab_data = next((tab for tab in all_sub_tabs_for_football if tab['name'] == 'popularbets' and tab['enabled']), None)
        if not insights_tab_data:
            raise CMSException(f"Insights tab is not enabled in CMS!!")
        self.__class__.tab_name, self.__class__.popular_bets_tab_name = next(
            ([insights_tab_data['displayName'].upper(), sub_tab['trendingTabName'].upper()]
             for sub_tab in insights_tab_data['trendingTabs'] for inner_sub_tab in sub_tab['popularTabs']
             if inner_sub_tab['popularTabName'] == 'Popular_tab' and inner_sub_tab['enabled'] and sub_tab['enabled']), None)

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the Application
        EXPECTED: Application is launched Successfully
        """
        self.site.login()

    def test_002_click_on_the_football_sport(self):
        """
        DESCRIPTION: Click on the Football Sport
        EXPECTED: Able to navigate to the Football landing page
        """
        self.site.open_sport('football')

    def test_003_click_on_popular_bets_tab(self):
        """
        DESCRIPTION: Click on Popular bets Tab
        EXPECTED: Popular bets tab is loaded.
        """
        actual_sports_tabs = self.site.sports_page.tabs_menu.items_as_ordered_dict
        self.assertTrue(actual_sports_tabs, msg='tabs are not available for football')
        tab = next((tab for tab_name, tab in actual_sports_tabs.items() if tab_name.upper() == self.tab_name),
                   None)
        tab.click()
        wait_for_result(lambda: self.site.football.tabs_menu.current == self.tab_name)

        self.site.football.tab_content.grouping_buttons.click_button(self.popular_bets_tab_name.upper())

    def test_004_verify_the_display_of_backed_in_the_last_filters(self):
        """
        DESCRIPTION: Verify the display of "Backed in the last" filters
        EXPECTED: Able to see "Backed in the last filter" on top right  of the Popular bets sub section.
        """
        self.assertTrue(self.site.football.tab_content.has_backed_filter(),
                        msg=f'backed filter is not found on football popular tabs')

    def test_005_verify_the_display_of_backed_in_the_last_filters(self):
        """
        DESCRIPTION: Verify the display of Backed in the last filters
        EXPECTED: Able to see Backed in the last filter right below the Popular bets sub section to filter the list of popular bets
        """
        self.__class__.request_id_of_popular_bets = self.get_requestid_for_url()
        backed_filter = self.site.football.tab_content.backed_filter
        backed_sort_filter = backed_filter.backed_sort_filter
        backed_sort_filter.click()
        backed_time_filter_names = list(
            self.site.football.tab_content.backed_filter.backed_dropdown.items_as_ordered_dict.keys())
        backed_time_names_for_payload_dict = {item: re.search(r'\d+', item).group() + item[re.search(r'[a-zA-Z]', item).start()] for item in backed_time_filter_names}
        for item_name in backed_time_filter_names:
            backed_filter.backed_dropdown.select_item_with_name(item_name=item_name)

            attempts, performance_log = 5, None
            while attempts:
                try:
                    performance_logs = [entry for entry in self.device.get_performance_log()[::-1] if
                                        'positions' in str(entry)]
                    performance_log = next((log for log in performance_logs if
                                            self.request_id_of_popular_bets == log[1]['message']['message']['params'][
                                                'requestId'] and backed_time_names_for_payload_dict[item_name] in json.loads(log[1]['message']['message']['params']['response']['payloadData'])[0]), None)
                    if performance_log:
                        break
                    else:
                        wait_for_haul(2)
                except Exception:
                    continue
            self.assertTrue(performance_log, f' Required log is not found')
            payload = performance_log[1]['message']['message']['params']['response']['payloadData']
            data = json.loads(payload)
            payload_names_list = []
            outcome_names_from_payload = [f"{event.get('event').get('markets')[0].get('outcomes')[0].get('name')}{' (' + str(event.get('event').get('markets')[0].get('rawHandicapValue')) + ')' if event.get('event').get('markets')[0].get('rawHandicapValue') else ''}" for event
                                          in data[1]['positions']]
            for name in outcome_names_from_payload:
                event_name = ' '.join(name.split())
                payload_names_list.append(event_name)

            fe_names = list(self.site.football.tab_content.accordions_list.items_as_ordered_dict.keys())
            for item in fe_names:
                if item not in payload_names_list:
                    raise Exception(f'"{item}" is not found in payload data "{payload_names_list}"')
            backed_sort_filter.click()
        backed_sort_filter.click()

    def test_006_verify_the_drop_down_list_in_backed_in_the_last_filter(self):
        """
        DESCRIPTION: Verify the drop down list in Backed in the last filter
        EXPECTED: 1. The drop down list should have:30min, 1hr, 3hr, 12hrs, Total(48hrs).
        EXPECTED: 2. The default backed in the last filter should be displayed as 48hrs
        """
        # covered in above steps

    def test_007_select_any_of_the_filter30min_1hr_3hrs_12_hrs_48hrs(self):
        """
        DESCRIPTION: Select any of the filter(30min, 1hr, 3hrs, 12 hrs, 48hrs)
        EXPECTED: 1. Displays the list of most backed popular bets in descending order in that timeframe.
        EXPECTED: 2. Preference is remembered and should be displayed the same filter until session logouts
        """
        # covered in above steps

    def test_008_verify_the_display_of_filters_under_backed_in_the_last_filter(self):
        """
        DESCRIPTION: Verify the display of filters under 'Backed in the last' filter
        EXPECTED: Able to see the filter pills right under'Backed in the last' filter. The following filters should be displayed: 30Mins,1hr, 3hr, 12hr, 24hr, 48hr
        """
        # covered in above steps

    def test_009_verify_the_display_of_event_starts_within_timeframe_filter(self):
        """
        DESCRIPTION: Verify the display of 'Event starts within' timeframe filter
        EXPECTED: Event starts within filter should be displayed below the backed in the last filter
        """
        event_start_filter_status = self.site.football.tab_content.has_time_filters
        self.assertTrue(event_start_filter_status, msg=f' popular bets tab content doent contain time filters')

    def test_010_verify_the_display_of_filter_pills_under_event_starts_within_filter(self):
        """
        DESCRIPTION: Verify the display of filter pills under 'Event starts within' filter
        EXPECTED: Able to see the filter pills right under'Event starts within' filter. The following filter pills should be displayed: 1hr, 3hr, 12hr, 24hr, 48hr
        """
        no_bets_message = self.site.football.tab_content.has_no_bets_message
        time_filters = self.site.football.tab_content.timeline_filters
        time_pills = time_filters.items_as_ordered_dict
        time_filter_pills_dict = {item: re.search(r'\d+', item).group() + item[re.search(r'[a-zA-Z]', item).start()] for item in time_pills}
        for item_name, item in time_pills.items():
            item.click()
            current_pill = time_filters.current
            if item_name != current_pill:
                self.assertTrue(no_bets_message, msg=f'no bets message is not displayed')
                continue
            attempts, performance_log = 5, None
            while attempts:
                try:
                    performance_logs = [entry for entry in self.device.get_performance_log()[::-1] if
                                        'positions' in str(entry)]
                    performance_log = next((log for log in performance_logs if
                                            self.request_id_of_popular_bets == log[1]['message']['message']['params'][
                                                'requestId'] and '48h_'+time_filter_pills_dict[item_name] in json.loads(log[1]['message']['message']['params']['response']['payloadData'])[0]), None)
                    if performance_log:
                        break
                    else:
                        wait_for_haul(5)
                except Exception:
                    continue
            self.assertTrue(performance_log, f' Required log is not found')
            payload = performance_log[1]['message']['message']['params']['response']['payloadData']
            data = json.loads(payload)
            payload_names_list=[]
            outcome_names_from_payload = [
                f"{event.get('event').get('markets')[0].get('outcomes')[0].get('name')}{' (' + str(event.get('event').get('markets')[0].get('rawHandicapValue')) + ')' if event.get('event').get('markets')[0].get('rawHandicapValue') else ''}"
                for event
                in data[1]['positions']]
            for name in outcome_names_from_payload:
                event_name = ' '.join(name.split())
                payload_names_list.append(event_name)
            fe_names = list(self.site.football.tab_content.accordions_list.items_as_ordered_dict.keys())

            for item in fe_names:
                if item not in payload_names_list:
                    raise Exception(f'"{item}" is not found in payload data "{payload_names_list}"')

        # betplacement
        sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        for section in sections:
            sections.get(section).bet_button.click()
            break
        if self.device_type == 'mobile':
            self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')
            quick_bet = self.site.quick_bet_panel.selection.content
            quick_bet.amount_form.input.value = self.bet_amount
            self.site.quick_bet_panel.place_bet.click()
            bet_receipt = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
            self.assertTrue(bet_receipt, msg='Bet Receipt is not displayed')
            self.site.quick_bet_panel.close()
        else:
            self.place_single_bet()
            self.check_bet_receipt_is_displayed()

        # Multiple betplacement
        performance_log = next(
            (entry for entry in self.device.get_performance_log()[::-1] if 'positions' in str(entry)), None)
        payload = performance_log[1]['message']['message']['params']['response']['payloadData']
        data = json.loads(payload)[1]['positions']
        for event in data:
            event_id = event['event']['id']
            event_name = event.get('event').get('markets')[0].get('outcomes')[0].get('name')
            market_name = event['event']['markets'][0]['templateMarketName']
            if market_name.title() in ['Match Result', 'Match Betting']:
                self.events_data[event_id] = event_name
                if len(self.events_data) == 2:
                    break
        events = self.events_data.values()
        show_more_status = self.site.football.tab_content.accordions_list.has_show_more_less
        self.assertTrue(show_more_status, msg=f'show more is not available in popuplar bets tab')
        self.site.football.tab_content.accordions_list.show_more_less.click()
        self.site.football.tab_content.accordions_list.show_more_less.click()
        sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        count = 0
        for event in events:
            bet_button = wait_for_result(lambda: sections[event].bet_button, timeout=4, name="waiting for bet button")
            bet_button.click()
            if self.device_type == 'mobile' and count == 0:
                self.site.wait_for_quick_bet_panel()
                self.site.quick_bet_panel.add_to_betslip_button.click()
                self.site.wait_quick_bet_overlay_to_hide()
                count += 1
                sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.site.open_betslip()
        self.place_multiple_bet()
        self.check_bet_receipt_is_displayed()

    def test_011_click_on_any_filter_pill(self):
        """
        DESCRIPTION: Click on any filter pill
        EXPECTED: 1. It should be turned to blue color indicating that particular filter pill is selected.
        EXPECTED: 2. Able to see the list of most backed popular bets in that particular time frame.
        EXPECTED: 3. The filter pill should be displayed as preference selected by user until next login session.
        """
        # covered in above step

    def test_012_click_on_the_selected_filter_pill(self):
        """
        DESCRIPTION: Click on the selected filter pill
        EXPECTED: Selected filter should be unselected and return to its white color when user clicks on blue color selected pill.
        """
        # covered in above step

    def test_013_verify_if_there_are_no_popular_bets_to_display_when_user_choose_the_filters(self):
        """
        DESCRIPTION: Verify if there are no popular bets to display when user choose the filters
        EXPECTED: User should be displayed with the message that "Sorry there are no popular bets at this time" and it will be redirected to default filters based on cms configuration.
        """
        # covered in above step
