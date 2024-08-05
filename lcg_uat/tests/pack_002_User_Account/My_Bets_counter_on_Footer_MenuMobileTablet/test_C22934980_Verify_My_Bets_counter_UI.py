import pytest
import datetime
import tests
from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.login
@pytest.mark.my_bets
@pytest.mark.footer
@pytest.mark.mobile_only
@pytest.mark.bet_history_open_bets
@vtest
class Test_C22934980_Verify_My_Bets_counter_UI(BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C22934980
    VOL_ID: C58637904
    NAME: Verify My Bets counter UI
    DESCRIPTION: This test case verifies counter displaying when there are one, two and three symbols ( 20+) to display
    PRECONDITIONS: * Load Oxygen/Roxanne Application
    PRECONDITIONS: * Make sure 'BetsCounter' config is turned on in CMS > System configurations
    PRECONDITIONS: * 'My Bets' option is present and active in the top 5 list in Menus > Footer menus in CMS
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    """
    keep_browser_open = True
    selection_ids = []
    now = datetime.datetime.now()
    expiry_year = str(now.year)
    expiry_month = f'{now.month:02d}'

    def get_my_bets_from_footer(self):
        menu_items = self.site.navigation_menu.items_as_ordered_dict
        self.assertTrue(menu_items, msg='Footer menu items are not found')

        my_bets = menu_items.get(vec.sb.MY_BETS_FOOTER_ITEM)
        self.assertTrue(my_bets, msg=f'"{vec.sb.MY_BETS_FOOTER_ITEM}" is not found in {menu_items.keys()}')
        return my_bets

    def test_000_preconditions(self):
        """
        DESCRIPTION: Make sure 'BetsCounter' config is turned on in CMS > System configurations
        DESCRIPTION: 'My Bets' option is present and active in the top 5 list in Menus > Footer menus in CMS
        DESCRIPTION: Get events with available 22 selections
        """
        self.__class__.expected_background_color = 'red' if self.brand == 'ladbrokes' else 'yellow'
        self.check_my_bets_counter_enabled_in_cms()

        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                         all_available_events=True)
            for event in events:
                outcomes = []
                for market in event['event']['children']:
                    if market['market']['templateMarketName'] == 'Win or Each Way':
                        outcomes.extend(market['market']['children'])
                if outcomes is None:
                    raise SiteServeException('There are no available outcomes')

                event_selection_ids = [i['outcome']['id'] for i in outcomes]

                self._logger.info(f'*** Found Horse race event with selection ids:"{event_selection_ids}"')
                self.selection_ids.extend(event_selection_ids)
                if len(self.selection_ids) >= 22:
                    break

            if len(self.selection_ids) < 22:
                raise SiteServeException('There are no enough active events')

        else:
            for item in range(3):
                event_params = self.ob_config.add_UK_racing_event(number_of_runners=8)
                self.selection_ids.extend(event_params.selection_ids.values())

        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        self.gvc_wallet_user_client.add_new_payment_card_and_deposit(username=self.username,
                                                                     amount=str(tests.settings.min_deposit_amount),
                                                                     card_number=tests.settings.master_card,
                                                                     card_type='mastercard',
                                                                     expiry_month=self.expiry_month,
                                                                     expiry_year=self.expiry_year,
                                                                     cvv=tests.settings.master_card_cvv)
        self.site.login(username=self.username)

        section_id = self.selection_ids[0]
        self.selection_ids.remove(section_id)
        self.open_betslip_with_selections(selection_ids=section_id)
        self.place_single_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.done_button.click()
        self.site.logout()

    def test_001__log_in_with_user_with_one_open_bet__unsettled_bet_available_verify_my_bets_counter_displaying(self):
        """
        DESCRIPTION: * Log in with user with one open bet ( unsettled bet) available
        DESCRIPTION: * Verify My Bets counter displaying
        EXPECTED: Coral: BetsCounter is displayed as a yellow round circle in top right corner of My Bets Footer Menu item with 1 digit ( 12 px)
        EXPECTED: Ladbrokes: BetsCounter is displayed as a red round circle in top right corner of My Bets Footer Menu item with 1 digit ( 12 px)
        """
        self.site.login(username=self.username)

        my_bets = self.get_my_bets_from_footer()

        self.__class__.actual_indicator = my_bets.indicator
        self.assertEqual(self.actual_indicator, '1',
                         msg=f'Actual value indicator "{self.actual_indicator}" is not equal to expected "1"')

        actual_background_color = my_bets.indicator_content.background_color_name
        self.assertEqual(actual_background_color, self.expected_background_color,
                         msg=f'My bets counter background color is not "{self.expected_background_color}", '
                             f'actual result "{actual_background_color}"')

        actual_font_size = my_bets.indicator_content.css_property_value('font-size')
        self.assertEqual(actual_font_size, '12px', msg=f'My bets counter font size is not equal to "12px", '
                                                       f'actual result "{actual_font_size}"')

    def test_002_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: My Bets counter is not displayed anymore
        """
        section_ids = self.selection_ids[:10 - int(self.actual_indicator)]
        del(self.selection_ids[:len(section_ids)])
        self.expected_betslip_counter_value = len(section_ids)
        self.open_betslip_with_selections(selection_ids=section_ids)
        self.place_single_bet(number_of_stakes=len(section_ids))
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.done_button.click()
        self.site.logout()

        my_bets = self.get_my_bets_from_footer()
        self.assertFalse(my_bets.has_indicator(expected_result=False), msg=f'My bets counter is displayed')

    def test_003__log_in_with_user_with_10_open_bet__unsettled_bet_available_verify_my_bets_counter_displaying(self):
        """
        DESCRIPTION: * Log in with user with 10 open bet ( unsettled bet) available
        DESCRIPTION: * Verify My Bets counter displaying
        EXPECTED: Coral: BetsCounter is displayed as a yellow round circle in top right corner of My Bets Footer Menu item with '10' digit ( 12 px)
        EXPECTED: Ladbrokes: BetsCounter is displayed as a red round circle in top right corner of My Bets Footer Menu item with '10' digit ( 12 px)
        """
        self.site.login(username=self.username)

        my_bets = self.get_my_bets_from_footer()

        self.__class__.actual_indicator = my_bets.indicator
        self.assertEqual(self.actual_indicator, '10',
                         msg=f'Actual value indicator "{self.actual_indicator}" is not equal to expected "10"')

        actual_background_color = my_bets.indicator_content.background_color_name
        self.assertEqual(actual_background_color, self.expected_background_color,
                         msg=f'My bets counter background color is not "{self.expected_background_color}", '
                             f'actual result "{actual_background_color}"')

        actual_font_size = my_bets.indicator_content.css_property_value('font-size')
        self.assertEqual(actual_font_size, '12px', msg=f'My bets counter font size is not equal to "12px", '
                                                       f'actual result "{actual_font_size}"')

    def test_004__log_out(self):
        """
        DESCRIPTION: * Log out
        EXPECTED: My Bets counter is not displayed anymore
        """
        section_ids = self.selection_ids[:22 - int(self.actual_indicator)]
        del (self.selection_ids[:len(section_ids)])
        self.expected_betslip_counter_value = len(section_ids)
        self.open_betslip_with_selections(selection_ids=section_ids)
        self.place_single_bet(number_of_stakes=len(section_ids))
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.done_button.click()
        self.site.logout()

        my_bets = self.get_my_bets_from_footer()
        self.assertFalse(my_bets.has_indicator(expected_result=False), msg=f'My bets counter is displayed')

    def test_005__log_in_with_user_with_22_open_bet__unsettled_bet_available_verify_my_bets_counter_displaying(self):
        """
        DESCRIPTION: * Log in with user with 22 open bet ( unsettled bet) available
        DESCRIPTION: * Verify My Bets counter displaying
        EXPECTED: Coral: BetsCounter is displayed as a yellow round circle in top right corner of My Bets Footer Menu item with '20+' digit ( 8 px)
        EXPECTED: Ladbrokes: BetsCounter is displayed as a red round circle in top right corner of My Bets Footer Menu item with '20+' digit ( 10 px)
        """
        self.site.login(username=self.username)

        my_bets = self.get_my_bets_from_footer()
        actual_indicator = my_bets.indicator
        self.assertEqual(actual_indicator, '20+',
                         msg=f'Actual value indicator "{actual_indicator}" is not equal to expected "20+"')

        actual_background_color = my_bets.indicator_content.background_color_name
        self.assertEqual(actual_background_color, self.expected_background_color,
                         msg=f'My bets counter background color is not "{self.expected_background_color}", '
                             f'actual result "{actual_background_color}"')

        actual_font_size = my_bets.indicator_content.css_property_value('font-size')
        expected_font_size = '10px' if self.brand == 'ladbrokes' else '8px'
        self.assertEqual(actual_font_size, expected_font_size,
                         msg=f'My bets counter font size is not equal to "{expected_font_size}", '
                             f'actual result "{actual_font_size}"')

    def test_006__log_out(self):
        """
        DESCRIPTION: * Log out
        EXPECTED: My Bets counter is not displayed anymore
        """
        self.site.logout()

        my_bets = self.get_my_bets_from_footer()
        self.assertFalse(my_bets.has_indicator(expected_result=False), msg=f'My bets counter is displayed')
