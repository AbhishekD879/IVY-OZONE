import pytest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from random import choice
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter, simple_filter, SiteServeRequests
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_018_Virtual_Sports.BaseVirtualsTest import BaseVirtualsTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.waiters import wait_for_result


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.high
@pytest.mark.virtual_sports
@pytest.mark.betslip
@pytest.mark.bet_placement
@pytest.mark.desktop
@pytest.mark.login
@pytest.mark.sanity
@pytest.mark.reg157_fix
@vtest
class Test_C874323_Place_VS_Virtual_Horses_bet_Inspired(BaseBetSlipTest, BaseVirtualsTest):
    """
    TR_ID: C874323
    NAME: Place VS Virtual Horses bet Inspired
    DESCRIPTION: Bet Placement - Verify that the customer can place a Single bet on a Virtual Sport
    PRECONDITIONS: Login to Oxygen app
    """
    keep_browser_open = True
    bet_amount = 0.10

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login to Oxygen app
        EXPECTED: User is logged in
        """
        virtuals_cms_class_ids = self.cms_virtual_sports_class_ids()
        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=self.ob_config.virtuals_config.category_id)
        sports_list = ss_req.ss_class(query_builder=self.ss_query_builder.
                                      add_filter(simple_filter(LEVELS.CLASS,
                                                               ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS,
                                                               str(self.ob_config.virtuals_config.category_id))))
        if not sports_list:
            raise SiteServeException('There are no active virtual sports')
        event = None
        events = None
        for sport_class in sports_list:
            class_id = sport_class['class']['id']
            additional_filter = exists_filter(
                LEVELS.EVENT, simple_filter(LEVELS.MARKET,
                                            ATTRIBUTES.NCAST_TYPE_CODES, OPERATORS.INTERSECTS, 'CF,TC')), exists_filter(
                LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.IS_EACH_WAY_AVAILABLE, OPERATORS.IS_TRUE))
            events = self.get_active_event_for_class(class_id=class_id, additional_filters=additional_filter,
                                                     raise_exceptions=False)
            if not events:
                continue
            event = choice(events)
            ss_class_id = event['event']['classId']
            if ss_class_id not in virtuals_cms_class_ids:
                continue
            break
        if not event or not events:
            raise SiteServeException('There are no available virtual event with Forecast tab')
        tab_name = self.cms_virtual_sport_tab_name_by_class_ids(class_ids=[ss_class_id])
        self.__class__.expected_tab = tab_name[0]

        self.site.login(username=tests.settings.betplacement_user)
        self.__class__.balance = self.site.header.user_balance

    def test_001_navigate_to_virtuals_page(self):
        """
        DESCRIPTION: Navigate to Virtuals page
        EXPECTED: The Virtuals page is loaded
        """
        self.site.open_sport(self.get_sport_title(category_id=self.ob_config.virtuals_config.category_id),
                             content_state='VirtualSports')

    def test_002_open_virtual_horses(self):
        """
        DESCRIPTION: Open Virtual Horses
        EXPECTED: Virtual Horses page is loaded
        """
        self.site.wait_content_state(state_name='VirtualSports')
        virtual_hub_home_page = self.cms_config.get_system_configuration_structure().get('VirtualHubHomePage')
        if virtual_hub_home_page.get('enabled'):
            wait_for_result(lambda: next(
                (section for section_name, section in self.site.virtual_sports_hub.items_as_ordered_dict.items() if
                 section_name.title() != "Next Events"), None) is not None, name=f'Waiting for next event section "',
                            timeout=5)
            virtual_section = next(
                section for section_name, section in self.site.virtual_sports_hub.items_as_ordered_dict.items() if
                section_name.title() != "Next Events")
            virtual_sport = list(virtual_section.items_as_ordered_dict.values())[0]
            if self.device_type == 'mobile' and self.use_browser_stack and 'iPhone' in self._device.device_args.get('device'):
                virtual_sport.link.click()
            else:
                virtual_sport.click()
        virtual_sports_list = self.site.virtual_sports
        open_tab = virtual_sports_list.sport_carousel.open_tab(self.expected_tab)
        self.assertTrue(open_tab, msg=f'Tab "{self.expected_tab}" is not opened')

    def test_003_add_a_selection_to_bet_slip(self):
        """
        DESCRIPTION: Add a selection to bet slip
        EXPECTED: The selection is added to bet slip
        """
        virtual_sports_list = self.site.virtual_sports
        event_off_times_list = virtual_sports_list.tab_content.event_off_times_list
        self.assertTrue(event_off_times_list.is_displayed(), msg=f'No events of times found')
        items_list = event_off_times_list.items_as_ordered_dict.keys()
        self.assertTrue(items_list, msg='No market tabs are present for the event')
        event_off_time_tab = choice(list(items_list)[3:8])
        event_off_times_list.select_off_time(event_off_time_tab)

        self.__class__.outcome_name = self.site.virtual_sports.tab_content.sport_event_name
        sections = virtual_sports_list.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        name, runner_buttons = list(sections.items())[0]
        self.__class__.runner_name = name
        bet_button = runner_buttons.bet_button
        bet_button.click()

        if self.device_type == 'mobile':
            self.site.wait_for_quick_bet_panel()
            self.site.quick_bet_panel.add_to_betslip_button.click()
            self.site.wait_quick_bet_overlay_to_hide()
            self.navigate_to_page(name='/virtual-sports/')

    def test_004_navigate_to_bet_slip(self):
        """
        DESCRIPTION: Navigate to bet slip
        EXPECTED: Bet slip is loaded
        """
        self.site.open_betslip()

    def test_005_add_a_stake_and_place_the_bet(self):
        """
        DESCRIPTION: Add a stake and place the bet
        EXPECTED: The bet is successfully placed and bet confirmation is displayed.
        """
        self.__class__.bet_info = self.place_and_validate_single_bet()
        # Workaround for issue of inability to click on "Place Bet" button on betslip via script
        # if betslip was opened from Virtual Sports page
        self.__class__.was_bet_receipt_displayed = self.site.is_bet_receipt_displayed()
        if self.device_type == 'mobile' and not self.was_bet_receipt_displayed:
            self.device.navigate_to(url=tests.HOSTNAME)
            self.site.wait_content_state('Homepage')
            self.site.header.scroll_to()
            self.site.open_betslip()
            self.site.betslip.bet_now_button.click()

    def test_006_verify_the_bet_confirmation(self):
        """
        DESCRIPTION: Verify the Bet Confirmation
        EXPECTED: The currency is in £.
        EXPECTED: The bet type is displayed: (e.g: double);
        EXPECTED: Same Selection and Market is displayed where the bet was placed;
        EXPECTED: Correct Time and Event is displayed;
        EXPECTED: Unique Bet ID is displayed;
        EXPECTED: The balance is correctly updated;
        EXPECTED: Odds are exactly the same as when bet has been placed;
        EXPECTED: Stake is correctly displayed;
        EXPECTED: Total Stake is correctly displayed;
        EXPECTED: Estimated Returns is exactly the same as when bet has been placed;
        EXPECTED: "Reuse Selection" and "Go betting" buttons are displayed.
        """
        self.check_bet_receipt(betslip_info=self.bet_info)
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        if self.brand == 'ladbrokes':
            self.assertTrue(self.site.bet_receipt.receipt_header.bet_datetime,
                            msg='Date and Time of event not displayed on the bet receipt')
        for section_name, section in betreceipt_sections.items():
            receipts = section.items_as_ordered_dict
            for receipt_name, receipt in receipts.items():
                receipt_type = receipt.__class__.__name__
                if receipt_type == 'ReceiptSingles':
                    self.assertIn(receipt.estimate_returns_currency, receipt.currencies,
                                  msg=f'Currency symbol "{receipt.estimate_returns_currency}" is not valid')
        bet_receipt = self.site.bet_receipt.footer
        self.assertTrue(bet_receipt.has_reuse_selections_button(),
                        msg=f'"{bet_receipt.reuse_selection_button.name}" is not displayed')
        self.assertTrue(bet_receipt.has_done_button(),
                        msg=f'"{bet_receipt.done_button.name}" is not displayed')

    def test_007_click_on_go_betting_button(self):
        """
        DESCRIPTION: Click on 'Go betting' button
        EXPECTED: The customer is redirected to Virtual sport page (ie: Virtuals Horse Racing)
        """
        self.site.bet_receipt.footer.click_done()
        if self.device_type == 'mobile' and not self.was_bet_receipt_displayed:
            # We are waiting for homepage, because Betslip was opened there
            self.site.wait_content_state('Homepage')

    def test_008_navigate_to_my_bets_page(self):
        """
        DESCRIPTION: Navigate to My Bets page
        EXPECTED: My Bets page is opened
        """
        self.site.open_my_bets_open_bets()

    def test_009_go_to_the_bet_that_was_just_placed_and_verify_that_the_bet_receipt_fields_are_correct(self):
        """
        DESCRIPTION: Go to the bet that was just placed and Verify that the Bet Receipt fields are correct.
        EXPECTED: The currency is in £.
        EXPECTED: The bet type , Selection Name and odds are displayed
        EXPECTED: Event Name is displayed
        EXPECTED: Bet Receipt unique ID
        EXPECTED: Selection Details:
        EXPECTED: Selection Name where the bet has been placed
        EXPECTED: Event name
        EXPECTED: **Time and Date
        EXPECTED: Market where the bet has been placed
        EXPECTED: E/W Terms: (None for bets where E/W is not valid)
        EXPECTED: Correct Stake is correctly displayed
        EXPECTED: Total Stake is correctly displayed (for E/W)
        """
        bet_name, single_bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.outcome_name)

        bet_info = self.bet_info.get(self.runner_name)
        self.assertEqual(single_bet.bet_type, vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
                         msg=f'Bet type: "{single_bet.bet_type}" '
                         f'is not as expected: "{vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE}"')
        self.assertEqual(single_bet.selection_name, self.runner_name,
                         msg=f'Selection Name: "{single_bet.selection_name}" '
                             f'is not as expected: "{self.runner_name}"')
        self.assertEqual(single_bet.odds_value, bet_info.get('odds'),
                         msg=f'Odds value: "{single_bet.odds_value}" '
                         f'is not as expected: "{bet_info.get("odds")}"')
        self.assertIn(self.outcome_name, single_bet.event_name,
                      msg=f'Event Name: "{single_bet.event_name}" is not as expected: "{self.outcome_name}"')
        self.assertEqual(single_bet.market_name, bet_info.get('market_name'),
                         msg=f'Bet market name: "{single_bet.market_name}" '
                         f'is not as expected: "{bet_info.get("market_name")}"')
        expected_stake = f'£{self.bet_amount:.2f}'
        self.assertEqual(single_bet.stake.value, expected_stake,
                         msg=f'Bet Stake value: "{single_bet.stake.value}" '
                         f'is not as expected: "{expected_stake}"')
