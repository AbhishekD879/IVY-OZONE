import json
from fractions import Fraction
import pytest
import time
import tests
from crlat_cms_client.utils.exceptions import CMSException
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_haul, wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.popular_bets
@pytest.mark.adhoc_suite
@pytest.mark.football
@pytest.mark.reg167_fix
@pytest.mark.other
@vtest
class Test_C66035677_Verify_the_display_and_dynamic_updates_of_Last_Update_time_for_Popular_Bets(Common):
    """
    TR_ID: C66035677
    NAME: Verify the display and dynamic updates of Last Update time for Popular Bets
    DESCRIPTION: This test case verifies the display and dynamic updates of Last Update time for Popular Bets
    PRECONDITIONS: Configure Popular bets tab in CMS (CMS>Sports pages>Popular bets)
    """
    enable_bs_performance_log = True
    keep_browser_open = True

    def get_requestid_for_url(self):
        """
        :param url: Required URl
        :return: Complete url
        """
        host = tests.HOSTNAME.replace('-sports', '').replace('3', '')
        request_id = None
        url = f'wss://trending-bets.{host}/trendingbets'
        perflog = self.device.get_performance_log()
        for log in list(reversed(perflog)):
            try:
                requested_url = log[1]['message']['message']['params']['url']
                if url in requested_url:
                    request_id = log[1]['message']['message']['params']['requestId']
                    break
            except KeyError:
                continue
        return request_id

    def wait_up_to_last_updated_time_will_change(self):
        wait_time, max_polling_time, last_updated_time = 2, 100, None
        start_time = time.time()
        while time.time() - start_time < max_polling_time:
            wait_for_haul(wait_time)
            self.device.refresh_page()
            self.site.wait_content_state_changed()
            self.site.football.tab_content.grouping_buttons.click_button(button_name=self.popular_bets_tab_name)
            last_updated_time = self.site.football.tab_content.last_updated
            if last_updated_time != self.last_updated:
                break
        self.assertNotEqual(last_updated_time, self.last_updated,
                            msg=f'even after 100 min last updated time is not updated')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Configure Popular bets tab in CMS (CMS>Sports pages>Popular bets)
        """
        all_sub_tabs_for_football = self.cms_config.get_sport_tabs(sport_id=self.ob_config.football_config.category_id)
        tab = next((tab for tab in all_sub_tabs_for_football if
                    tab['enabled'] == True and tab['name'] == 'popularbets'), None)
        self.__class__.tab_name = tab['displayName'].upper()
        sports_tab_data = self.cms_config.get_sports_tab_data(sport_id=self.ob_config.football_config.category_id,
                                                              tab_name='popularbets')
        price_range = sports_tab_data.get('trendingTabs')[0].get('popularTabs')[0]['priceRange']
        price_range_parts = price_range.split('-')
        self.__class__.price_range_start = Fraction(price_range_parts[0])
        self.__class__.price_range_end = Fraction(price_range_parts[1])

        self.__class__.popular_bets_tab_name, self.__class__.backed_text_status_cms = next(
            ([sub_tab['trendingTabName'].upper(), inner_sub_tab['enableBackedUpTimes']] for sub_tab in
             tab['trendingTabs'] for inner_sub_tab in sub_tab['popularTabs']
             if inner_sub_tab['popularTabName'] == 'Popular_tab' and inner_sub_tab['enabled'] and sub_tab[
                 'enabled']), None)

        if not self.tab_name:
            raise CMSException('Popular Bet tab is not enabled in CMS!!')

    def test_001_verify_the_display_of_last_updated_time_for_popular_bets(self):
        """
        DESCRIPTION: Verify the Display of Last Updated time for Popular Bets
        EXPECTED: 1. User should be displayed with "Last Updated time" above the popular bets list and below Events Starts Within filter.
        EXPECTED: 2. The last updated time displayed on the UI should be 24hour based format with (Hour:Minutes).
        """
        self.site.open_sport('Football')
        self.__class__.actual_sports_tabs = self.site.sports_page.tabs_menu.items_as_ordered_dict
        self.assertTrue(self.actual_sports_tabs, f'tabs are not available for football')
        tab = next((tab for tab_name, tab in self.actual_sports_tabs.items() if tab_name.upper() == self.tab_name),
                   None)
        tab.click()
        wait_for_result(lambda: self.site.football.tabs_menu.current == self.tab_name)
        self.assertEqual(self.site.football.tabs_menu.current, self.tab_name, f'not switched to "{self.tab_name}"')
        self.site.football.tab_content.grouping_buttons.click_button(button_name=self.popular_bets_tab_name)

    def test_002_verify_the_dynamic_update_of_last_updated_time_for_popular_bets(self):
        """
        DESCRIPTION: Verify the Dynamic Update of Last Updated time for Popular Bets
        EXPECTED: 1. The last updated time should be updated on real time basis whenever the list of popular bets gets updated in the payload received from the ADA team.
        EXPECTED: 2. Currently the time is set to 2mins to receive payload and popular bets to update. It can change in future.(Note: In lower env time has been set to 2mins and Higher env it is one min)
        """
        last_updated_status = self.site.football.tab_content.has_last_updated()
        self.assertTrue(last_updated_status, msg=f'popular bets tab content doesnt have last updated status')
        self.__class__.last_updated = self.site.football.tab_content.last_updated

    def test_003_verify_the_display_of_the_number_of_backed_times_on_the_popular_bets(self):
        """
        DESCRIPTION: Verify the display of the number of backed times on the popular bets
        EXPECTED: 1. User is able to see the popular bets displayed with number of times a bet has been backed as "BACKED 2380 times" for each and every popular bet in the list.
        EXPECTED: 2. The number should be updated for every 1 min , and for every page refresh.(If there is any change)
        """
        section_name, section = self.site.football.tab_content.accordions_list.first_item
        backed_text_status_cms = section.has_backed_text()
        self.assertEqual(backed_text_status_cms, self.backed_text_status_cms,
                         msg=f'Backed Text Status : "{backed_text_status_cms}" is not same as Expected Status: "{self.backed_text_status_cms}"')
        section.click()
        self.site.wait_splash_to_hide()
        self.site.wait_content_state(state_name='EventDetails')
        self.site.back_button_click()

    def test_004_click_on_any_selection_among_the_list_of_popular_bets(self):
        """
        DESCRIPTION: Click on any selection among the list of popular bets
        EXPECTED: User will be navigated to that particular selection event landing page
        """
        # covered in above step

    def test_005_verify_the_dynamically_updated_list_of_popular_bets(self):
        """
        DESCRIPTION: Verify the dynamically updated list of popular bets
        EXPECTED: Popular bets will be dynamically updated for every 1 min(list will be moving up and down based on most backed-being most backed at top)
        """
        self.site.football.tab_content.grouping_buttons.click_button(button_name=self.popular_bets_tab_name)
        self.wait_up_to_last_updated_time_will_change()

    def test_006_verify_the_display_of_popular_bets_if_2_bets_have_same_backed_times_number(self):
        """
        DESCRIPTION: Verify the Display of popular bets if 2 bets have same Backed times number
        EXPECTED: If two of the popular bets have same number of most backed times, then popular bets which starts first will be displayed first followed by the other.
        """
        position_data = []
        fe_position_data = []
        request_id_of_popular_bets = self.get_requestid_for_url()
        show_more_status = self.site.football.tab_content.accordions_list.has_show_more_less()
        self.assertTrue(show_more_status, msg=f'show more is not available in popuplar bets tab')
        show_more = self.site.football.tab_content.accordions_list.show_more_less
        while show_more.name.upper() == 'SHOW MORE':
            show_more.click()
            show_more = self.site.football.tab_content.accordions_list.show_more_less
        sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict_inc_dup
        for section_name, section in sections.items():
            event_name = section.name
            fe_position_data.append(event_name)
        attempts, performance_log = 3, None
        while attempts:
            try:
                performance_logs = [entry for entry in self.device.get_performance_log()[::-1] if
                                    'positions' in str(entry)]
                performance_log = next((log for log in performance_logs if
                                        request_id_of_popular_bets == log[1]['message']['message']['params'][
                                            'requestId']), None)
                if performance_log:
                    break
                else:
                    wait_for_haul(1)
            except Exception:
                continue
        self.assertTrue(performance_log, f' Required log is not found')
        payload = performance_log[1]['message']['message']['params']['response']['payloadData']
        data = json.loads(payload)[1]['positions']
        for event in data:
            event_name = event.get('event').get('markets')[0].get('outcomes')[0].get('name')
            event_name = ' '.join(event_name.split())
            price_numerator = event.get('event').get('markets')[0].get('outcomes')[0].get('prices')[0]['priceNum']
            price_denominator = event.get('event').get('markets')[0].get('outcomes')[0].get('prices')[0]['priceDen']
            odd_price = price_numerator / price_denominator
            price_in_fraction = Fraction(odd_price).limit_denominator()
            if self.price_range_start <= price_in_fraction <= self.price_range_end:
                position_data.append(event_name)
                if len(position_data) == 20:
                    break
        for i in range(10):
            if fe_position_data == position_data:
                self.assertListEqual(fe_position_data, position_data,
                                     msg=f' payload positions "{position_data}" are not equal front end positions "{fe_position_data}"')
                break
            position_data = []
            fe_position_data = []
            sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict_inc_dup
            for section_name, section in sections.items():
                event_name = section.name
                fe_position_data.append(event_name)
            attempts, performance_log = 3, None
            while attempts:
                try:
                    performance_logs = [entry for entry in self.device.get_performance_log()[::-1] if
                                        'positions' in str(entry)]
                    performance_log = next((log for log in performance_logs if
                                            request_id_of_popular_bets == log[1]['message']['message']['params'][
                                                'requestId']), None)
                    if performance_log:
                        break
                    else:
                        wait_for_haul(1)
                except Exception:
                    continue
            self.assertTrue(performance_log, f' Required log is not found')
            payload = performance_log[1]['message']['message']['params']['response']['payloadData']
            data = json.loads(payload)[1]['positions']
            for event in data:
                event_name = event.get('event').get('markets')[0].get('outcomes')[0].get('name')
                event_name = ' '.join(event_name.split())
                price_numerator = event.get('event').get('markets')[0].get('outcomes')[0].get('prices')[0]['priceNum']
                price_denominator = event.get('event').get('markets')[0].get('outcomes')[0].get('prices')[0]['priceDen']
                odd_price = price_numerator / price_denominator
                price_in_fraction = Fraction(odd_price).limit_denominator()
                if self.price_range_start <= price_in_fraction <= self.price_range_end:
                    position_data.append(event_name)
                    if len(position_data) == 20:
                        break
        else:
            raise VoltronException(
                f' payload positions "{position_data}" are not equal front end positions "{fe_position_data}"')

    def test_007_verify_price_updates_for_popular_bets(self):
        """
        DESCRIPTION: Verify price updates for popular bets.
        EXPECTED: User should be able to see the price updates in popular bets page whenever there is a price update in relevant EDP
        """
        # cant automate as price changes wont occur frequently in prematches

    def test_008_verify_the_suspended_bets_in_popular_bets_sub_section(self):
        """
        DESCRIPTION: Verify the suspended bets in popular bets sub section
        EXPECTED: Popular bet will be displayed with suspended status in greyed out mode as we currently display in existing production
        """
        # can not be automated because we wont be waiting until bets gets suspended.
