import re
import pytest
from crlat_cms_client.utils.exceptions import CMSException
from crlat_cms_client.utils.waiters import wait_for_result
from lxml.html import fromstring
from tests.base_test import vtest
from tests.Common import Common
from fractions import Fraction

from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.pages.shared import get_driver
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import do_request
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.popular_bets
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@pytest.mark.for_you
@pytest.mark.football
@pytest.mark.other
@vtest
class Test_C66070216_Verify_the_For_You_Personilzed_Bets_end_to_end_journey(BaseBetSlipTest):
    """
    TR_ID: C66070216
    NAME: Verify the For You Personilzed Bets end to end journey
    DESCRIPTION: This test case verifies the For You Personilzed Bets end to end journey
    PRECONDITIONS: 1.  "For you" sub-section is configured under popular bets in CMS.
    PRECONDITIONS: 2. Navigation to go CMS>Sports pages>Football>Insights>For you
    PRECONDITIONS: 3. For You sub tab is created and enabled
    PRECONDITIONS: 4. Top bets for you user module is created and enabled
    """
    keep_browser_open = True
    bet_amount = 0.1
    show_less = 'Show Less'
    enable_bs_performance_log = True

    def get_response(self):
        """
        :param url: Required URl
        :return: Complete url
        """
        url = 'api/fy/tb'
        req_url = None
        perflog = self.device.get_performance_log()
        for log in list(reversed(perflog)):
            try:
                requested_url = log[1]['message']['message']['params']['request']['url']
                if url in requested_url:
                    req_url = requested_url
                    break
            except (KeyError, IndexError):
                continue
        return do_request(method='GET', url=req_url,
                          headers = {'Content-Type': 'application/json',
                                     'User-Agent':'Mozilla/5.0 (Linux; Android 9.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Mobile Safari/537.36 Frontend-Automation',
                                     'Token': self.get_local_storage_cookie_value_as_dict('OX.USER')['bppToken']})

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Configure Popular bets tab in CMS (CMS>Sports pages>Popular bets)
        """
        all_sub_tabs_for_football = self.cms_config.get_sport_tabs(sport_id=self.ob_config.football_config.category_id)
        tab = next((tab for tab in all_sub_tabs_for_football if
                    tab['enabled'] and tab['name'] == 'popularbets'), None)
        self.__class__.tab_name = tab['displayName'].upper()
        if not self.tab_name:
            raise CMSException('INSIGHTS tab is not enabled in CMS!!')
        self.__class__.foryou_tab_name = next(
            (sub_tab['trendingTabName'] for sub_tab in tab['trendingTabs']
             if sub_tab['headerDisplayName'] == 'for-you'), None)
        if not self.foryou_tab_name:
            raise CMSException('FOR YOU tab is not enabled in CMS!!')
        tab_id = self.cms_config.get_sport_tab_id(sport_id=self.ob_config.football_config.category_id,
                                                  tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.popularbets)
        tab_names = self.cms_config.get_sport_tab_data_by_tab_id(sport_tab_id=tab_id).get('trendingTabs')
        for tab_switcher in tab_names:
            if tab_switcher.get('popularTabs')[0].get('popularTabName') == 'for-you-personalized-bets':
                foryou_desc = tab_switcher.get('popularTabs')[0].get('informationTextDesc')
        # foryou_desc = self.cms_config.get_sport_tab_data_by_tab_id(sport_tab_id=tab_id).get('trendingTabs')[1].get('popularTabs')[0].get('informationTextDesc')
                text = fromstring(foryou_desc).text_content().strip('\n').strip()
                self.__class__.desc_text = re.sub(r'\{.*?\}', '', text)
                price_range = tab_switcher.get('popularTabs')[0]['priceRange']
                price_range_parts = price_range.split('-')
                self.__class__.foryou_noBettingDesc_cms = tab_switcher.get('popularTabs')[0].get('noBettingDesc')
                self.__class__.price_range_start = Fraction(price_range_parts[0])
                self.__class__.price_range_end = Fraction(price_range_parts[1])
                break
        # Popular bet tab name
        self.__class__.popular_bet_tab_name = next((sub_tab['trendingTabName'] for sub_tab in tab['trendingTabs'] for inner_sub_tab in sub_tab['popularTabs']
                                                    if inner_sub_tab['popularTabName'] == 'Popular_tab'), None)

    def test_001_launch_the_application_and_navigate_to_the_football_insights_tab(self):
        """
        DESCRIPTION: Launch the application and navigate to the football insights tab
        EXPECTED: User can launch and navigate to the football insights tab
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football')
        self.__class__.expected_tab = self.site.football.tabs_menu.current.upper()
        actual_sports_tabs = self.site.sports_page.tabs_menu.get_items(name=self.tab_name)
        insights_tab = actual_sports_tabs.get(self.tab_name)
        insights_tab.click()
        wait_for_result(lambda: self.site.football.tabs_menu.current.upper() == self.tab_name.upper())
        current_tab = self.site.football.tabs_menu.current.upper()
        self.assertEqual(current_tab, self.tab_name.upper(),
                         f'Actual Highlighted Tab : "{current_tab}" is not same as' f'Expected Highlighted Tab : "{self.tab_name}"')

    def test_002_click_on_for_you_tab_and_verify_displaying_of_just_for_you_header_and_description(self):
        """
        DESCRIPTION: Click on For you tab and verify displaying of Just for you header and description
        EXPECTED: User can navigate to For You tab and can see the Just for you header and description with info icon
        """
        self.site.football.tab_content.grouping_buttons.click_button(self.foryou_tab_name.upper())
        self.site.wait_content_state_changed()
        current_tab = self.site.football.tab_content.grouping_buttons.current.upper()
        self.assertEqual(current_tab, self.foryou_tab_name.upper(),
                         f'Actual Tab : "{current_tab}" is not same as' f'Expected Tab : "{self.foryou_tab_name}"')

    def test_003_click_on_just_for_you_description_close_icon(self):
        """
        DESCRIPTION: Click on Just for you description close icon
        EXPECTED: User can click and close the description
        """
        description_visible_status = self.site.football.tab_content.has_description_container()
        self.assertTrue(description_visible_status, msg=f' For You tab has no description')

        desc_container = self.site.football.tab_content.description_container

        description_text = desc_container.description.strip().replace('\n', ' ')
        self.assertEqual(description_text, self.desc_text,
                         msg=f'message configured in cms "{self.desc_text}" is not equal to message displayed in frontend "{description_text}"')
        desc_icon = desc_container.has_info_icon
        self.assertTrue(desc_icon, msg=f' For you tab has no description info icon')

        desc_close_btn = desc_container.close
        self.assertTrue(desc_close_btn,
                        msg=f' For You tab has no description close button for description tab')
        desc_close_btn.click()

        description_visible_status = self.site.football.tab_content.has_description_container()
        self.assertFalse(description_visible_status,
                         msg=f'For You tab has description after clicking on close button')

    def test_004_verify_the_display_of_description_by_refreshing_the_page_and_page_re_navigating(self):
        """
        DESCRIPTION: Verify the display of description by refreshing the page and page re-navigating
        EXPECTED: 1. On page refresh user can see the decription
        EXPECTED: 2. On page re-navigating user can see the description
        """
        # driver refresh
        driver = get_driver()
        driver.refresh()
        self.site.wait_content_state(state_name='football')
        self.site.football.tab_content.grouping_buttons.click_button(self.foryou_tab_name.upper())
        current_tab = self.site.football.tab_content.grouping_buttons.current.upper()
        self.assertEqual(current_tab, self.foryou_tab_name.upper(),
                         f'Actual Tab : "{current_tab}" is not same as' f'Expected Tab : "{self.foryou_tab_name}"')
        description_visible_status = self.site.football.tab_content.has_description_container()
        if description_visible_status is False:
            driver.refresh()
            self.site.wait_content_state(state_name='football')
            self.site.football.tab_content.grouping_buttons.click_button(self.foryou_tab_name.upper())
        self.assertTrue(description_visible_status, msg=f' For You tab has no description')
        desc_container = self.site.football.tab_content.description_container

        description_text = desc_container.description.strip().replace('\n', ' ')
        self.assertEqual(description_text, self.desc_text,
                         msg=f'message configured in cms "{self.desc_text}" is not equal to message displayed in frontend "{description_text}"')

    def test_005_verify_the_display_of_login_header_with_login_cta(self):
        """
        DESCRIPTION: Verify the display of Login Header with Login CTA
        EXPECTED: User could see the Login Header with Login CTA
        """
        login_button_status = self.site.football.tab_content.has_login_button()
        self.assertTrue(login_button_status, msg = 'Login button is not Display in FE')
        self.site.football.tab_content.login_button.click()

    def test_006_click_on_login_cta_and_loing_with_valid_credentials(self):
        """
        DESCRIPTION: Click on Login CTA and loing with valid credentials
        EXPECTED: User can click on Login CTA and can login
        """
        self.site.login()

    def test_007_repeat_the_steps_23_and_4(self):
        """
        DESCRIPTION: Repeat the steps 2,3 and 4
        EXPECTED: User can execute the mentioned steps successfully
        """
        self.test_002_click_on_for_you_tab_and_verify_displaying_of_just_for_you_header_and_description()

    def test_008_verify_the_display_of_top_bets_for_you_user(self):
        """
        DESCRIPTION: Verify the display of Top Bets for you user
        EXPECTED: User could see the Top Bets for you user(user name is dynamic based on the user login details)
        """
        # verifying for you tab items
        for_you_bets = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(for_you_bets, msg='For You Bets are not display in FE')

    def test_009_verify_the_display_of_last_updated_time(self):
        """
        DESCRIPTION: Verify the display of Last Updated time
        EXPECTED: User can see the Last Updated time which is in 24 hours format
        """
        position_data = []
        fe_position_data = []
        # getting response from for you bets in network call
        response_of_for_you_bets = self.get_response()
        # getting for you tab sections from Front End
        show_more_status = self.site.football.tab_content.accordions_list.has_show_more_less()
        self.assertTrue(show_more_status, msg=f'show more is not available in popuplar bets tab')
        self.site.football.tab_content.accordions_list.show_more_less.click()
        wait_for_haul(3)
        # Up to show less clicking on show more
        if self.site.football.tab_content.accordions_list.toggle_icon_name.lower() != self.show_less.lower():
            self.site.football.tab_content.accordions_list.show_more_less.click()
        sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict_inc_dup
        for section_name, section in sections.items():
            event_name = section.name
            index_of_bracket = event_name.find('(')
            if index_of_bracket != -1:  # If '(' is found in the string
                et_name = event_name[:index_of_bracket].strip()
                fe_position_data.append(et_name)
            else:
                fe_position_data.append(event_name)
        # If we didn't get response in first attempt we are trying next attempts to get response from network call
        attempts, response_of_for_you_bets = 3, None
        while attempts:
            try:
                response_of_for_you_bets = self.get_response()
                if response_of_for_you_bets:
                    break
                else:
                    wait_for_haul(1)
            except Exception:
                continue
        self.assertTrue(response_of_for_you_bets, f' Required log is not found')
        # After getting response call we are taking event names
        data = response_of_for_you_bets['positions']
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
        # Compare for you tab data in network call and Front End display
        if sorted(fe_position_data) == sorted(position_data):
            self.assertEquals(sorted(fe_position_data), sorted(position_data),
                                 msg=f' payload positions "{sorted(position_data)}" are not equal front end positions "{sorted(fe_position_data)}"')

        else:
            raise VoltronException(
                f' payload positions "{position_data}" are not equal front end positions "{fe_position_data}"')

    def test_010_verify_the_display_of_for_you_bets_and__backed_xx_times(self):
        """
        DESCRIPTION: Verify the display of For You bets and  BACKED XX TIMES
        EXPECTED: User can see the For You bets and BACKED XX TIMES
        EXPECTED: Note: Backed times will display only when it is enabled in CMS
        """
        # Covered in above step

    def test_011_verify_the_display_and_functionality_of_show_more_cta(self):
        """
        DESCRIPTION: Verify the display and functionality of Show More CTA
        EXPECTED: 1. User can see the default number of bets with Show More CTA (default number of bets is configured in the CMS)
        EXPECTED: 2. When user click on Show More CTA , the next set of bets will display (Show more number of bets is configured in the CMS)
        EXPECTED: 3. Once all the bets are displayed, user can see the Show Less CTA
        """
        # Covered in above step

    def test_012_verify_the_display_and_functionality_of_show_less_cta(self):
        """
        DESCRIPTION: Verify the display and functionality of Show Less CTA
        EXPECTED: 1. Once all the bets are displayed, user can see the Show Less CTA
        EXPECTED: 2. When user click on Show Less CTA , from last what ever the number of bets is configured for show more will be un displayed.
        EXPECTED: 3. Once all the show more bets are un displayed, user can see the default number of bets with Show More CTA
        """
        # Covered in above step

    def test_013_add_for_you_selections_to_the_betslip_and_place_bet(self):
        """
        DESCRIPTION: Add for you selections to the Betslip and place bet
        EXPECTED: For Desktop: User can add the selections to the betslip and can place a bet.
        EXPECTED: For Mobile: User can place a quick bet.
        """
        # placing bet
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

    def test_014_logout_from_the_application_and_login_with_brand_new_user_with_no_betting_history(self):
        """
        DESCRIPTION: Logout from the application and login with Brand new user with no betting history
        EXPECTED: User can logout form the application and login with Brand new user with no betting history
        """
        self.site.logout()
        self.assertTrue(self.site.wait_logged_out(),
                        msg='User has not logged out!')
        # New user creation and login with new user
        user_name = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=user_name)
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football')
        # clicking on insight tab
        actual_sports_tabs = self.site.sports_page.tabs_menu.get_items(name=self.tab_name)
        insights_tab = actual_sports_tabs.get(self.tab_name)
        insights_tab.click()
        wait_for_result(lambda: self.site.football.tabs_menu.current.upper() == self.tab_name.upper())
        current_tab = self.site.football.tabs_menu.current.upper()
        self.assertEqual(current_tab, self.tab_name.upper(),
                         f'Actual Highlighted Tab : "{current_tab}" is not same as' f'Expected Highlighted Tab : "{self.tab_name}"')
        # clicking on For you tab
        self.site.football.tab_content.grouping_buttons.click_button(self.foryou_tab_name.upper())
        self.site.wait_content_state_changed()
        current_tab = self.site.football.tab_content.grouping_buttons.current.upper()
        self.assertEqual(current_tab, self.foryou_tab_name.upper(),
                         f'Actual Tab : "{current_tab}" is not same as' f'Expected Tab : "{self.foryou_tab_name}"')

    def test_015_verify_displaying_of_we_need_more_info_description_and_go_to_football_cta(self):
        """
        DESCRIPTION: Verify displaying of We need more info description and "Go To Football" CTA
        EXPECTED: User can able to see the info description with "Go To Football" CTA
        """
        foryou_no_bets_description_visible_status = self.site.football.tab_content.has_no_foryou_bet_description()
        self.assertTrue(foryou_no_bets_description_visible_status, msg=f' For You tab has no description')

        foryou_no_bets_desc_container = self.site.football.tab_content.no_foryou_bet_description

        self.assertEqual(foryou_no_bets_desc_container, self.foryou_noBettingDesc_cms,
                         msg=f'message configured in cms "{self.foryou_noBettingDesc_cms}" is not equal to message displayed in frontend "{foryou_no_bets_desc_container}"')

    def test_016_verify_displaying_of_popular_bets_with_popular_bets_header_and_last_updated_time(self):
        """
        DESCRIPTION: Verify displaying of Popular Bets with Popular bets header and Last Updated time
        EXPECTED: 1. User can see the popular bets details with Popular bets header.
        EXPECTED: 2. user could see the Last Update time in 24hrs
        """
        self.site.football.tab_content.grouping_buttons.click_button(self.popular_bet_tab_name.upper())
        popularbet_header = self.site.football.tab_content.accordian_header
        self.site.football.tab_content.grouping_buttons.click_button(self.foryou_tab_name.upper())
        for_you_header = self.site.football.tab_content.displayname_in_foryou
        self.assertEqual(popularbet_header.upper(), for_you_header.upper(), msg='Both headers are not equal')

    def test_017_click_on_go_to_football_cta(self):
        """
        DESCRIPTION: Click on "Go To Football" CTA
        EXPECTED: User can click on the CTA and navigate to the Football Landing page
        """
        go_to_football_button_status = self.site.football.tab_content.has_go_to_football()
        self.assertTrue(go_to_football_button_status, msg='Login button is not Display in FE')
        self.site.football.tab_content.go_to_football.click()
        self.site.wait_content_state('football')
        actual_tab = self.site.football.tabs_menu.current.upper()
        self.assertEqual(self.expected_tab, actual_tab, msg = f'Expected tab is :{self.expected_tab} is not equal to actual tab: {actual_tab}, So User not in football page')

