import pytest
import tests
import voltron.environments.constants as vec
from random import choice
from datetime import datetime
from tests.base_test import vtest
from collections import OrderedDict
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from tests.pack_009_SPORT_Specifics.Football_Specifics.Football_Coupons.BaseCouponsTest import BaseCouponsTest
from voltron.utils.waiters import wait_for_result
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@pytest.mark.coupon
@pytest.mark.login
@pytest.mark.bet_placement
@pytest.mark.desktop
@pytest.mark.safari
@pytest.mark.sanity
@pytest.mark.soc
@vtest
class Test_C874317_Verify_placing_Trixies_bet_on_Football_Coupon_Selections(BaseBetSlipTest, BaseCouponsTest):
    """
    TR_ID: C874317
    NAME: Verify placing Trixies bet on Football Coupon Selections
    DESCRIPTION: Bet Placement - Verify that the customer can place a Trixie bet on Football Coupon selections
    PRECONDITIONS: **CMS Configuration:**
    PRECONDITIONS: Football Coupon ->Coupon Segments -> Create New Segment - 'Featured Coupon' section
    PRECONDITIONS: NOTE:  **Popular coupon** section contains all the rest of available coupons EXCEPT coupons are present in *Featured section*
    PRECONDITIONS: **COUPONS** for Coral (CMS configurable)
    PRECONDITIONS: **ACCAS** for Ladbrokes (CMS configurable)
    PRECONDITIONS: 1. In order to create coupons use the following instruction https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    PRECONDITIONS: 2. List of Coupons depends on TI tool configuration data for Coupons. All available Coupons from OB response will be displayed on the page
    PRECONDITIONS: Preconditions:
    PRECONDITIONS: 1. Login to Oxygen app
    """
    keep_browser_open = True
    sport_name = vec.sb.FOOTBALL
    autotest_coupon = vec.siteserve.EXPECTED_COUPON_NAME

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create/Get football enhanced multiples events
        """
        self.__class__.category_id = self.ob_config.football_config.category_id
        self.__class__.expected_sport_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.coupons,
                                                                    self.category_id,
                                                                    raise_exceptions=False)
        if not self.expected_sport_tab:
            raise CmsClientException(f'"{self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.coupons}" is not configured for "{self.category_id}"')

        if tests.settings.backend_env != 'prod':
            tomorrow_start_time = self.get_date_time_formatted_string(days=1)
            event_matches_params = self.ob_config.add_autotest_premier_league_football_event(start_time=tomorrow_start_time)
            event_matches_params2 = self.ob_config.add_football_event_to_autotest_league2(start_time=tomorrow_start_time)
            event_matches_params3 = self.ob_config.add_football_event_to_england_premier_league(start_time=tomorrow_start_time)
            # coupons
            market_short_name = self.ob_config.football_config. \
                autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
            event_coupons_id = self.ob_config.market_ids[event_matches_params.event_id][market_short_name]
            event_coupons_id2 = self.ob_config.market_ids[event_matches_params2.event_id][market_short_name]
            event_coupons_id3 = self.ob_config.market_ids[event_matches_params3.event_id][market_short_name]
            self.ob_config.add_event_to_coupon(market_id=event_coupons_id, coupon_name=self.autotest_coupon)
            self.ob_config.add_event_to_coupon(market_id=event_coupons_id2, coupon_name=self.autotest_coupon)
            self.ob_config.add_event_to_coupon(market_id=event_coupons_id3, coupon_name=self.autotest_coupon)
        self.site.login()
        self.site.toggle_quick_bet()

    def test_001_navigate_to_football_page(self):
        """
        DESCRIPTION: Navigate to Football page
        EXPECTED: The Football page is opened. 'Matches' tab is opened by default and highlighted
        """
        self.site.open_sport(name=self.get_sport_title(self.ob_config.football_config.category_id))
        current_tab_name = self.site.football.tabs_menu.current
        self.assertEqual(current_tab_name, self.expected_sport_tabs.matches,
                         msg=f'Default tab is not "{self.expected_sport_tabs.matches}", it is "{current_tab_name}"')

    def test_002_navigate_to_the_coupons_tab(self):
        """
        DESCRIPTION: Navigate to the Coupons tab
        EXPECTED: Coupons tab is displayed
        """
        self.navigate_to_page(name='sport/football/coupons')
        self.site.wait_content_state('Football')
        coupon_categories = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(coupon_categories, msg='Can not find any coupon category')

    def test_003_add_3_selections_from_3_different_events_to_the_betslip(self):
        """
        DESCRIPTION: Add 3 selections from 3 different events to the betslip
        EXPECTED: Selections are added to the betslip
        """
        if tests.settings.backend_env == 'prod':
            coupon_categories = self.site.football.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(coupon_categories, msg='Can not find any coupon category')
            coupons_list = coupon_categories.get(vec.coupons.POPULAR_COUPONS.upper()).items_as_ordered_dict
            self.assertTrue(coupons_list, msg='Can not find any coupon')
            exclude_coupons_list = ["Todays Correct Scores", "Correct Score Coupon"]
            while True:
                coupon_name, coupon = choice(list(coupons_list.items()))
                if coupon_name not in exclude_coupons_list:
                    break
            coupon.click()
            sleep(3)
            try:
                wait_for_result(lambda: coupon.coupon_dialog.close_button.click(), timeout=5)
            except Exception:
                pass
            self.site.wait_content_state('CouponPage')
        else:
            self.find_coupon_and_open_it(coupon_section=vec.coupons.POPULAR_COUPONS.upper(),
                                         coupon_name=self.autotest_coupon)
        sections = self.site.coupon.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Sections not found on coupon page')
        number_of_selections = 3
        if len(sections) < 1:
            raise SiteServeException('There are no enough leagues on Coupons page')
        items = sections.items()
        self.__class__.events_names = []
        for section_name, section in items:
            if not section.is_expanded:
                section.expand()
            self.assertTrue(section.is_expanded(), msg=f'"{section} is not expanded"')
            date_groups = section.items_as_ordered_dict
            self.assertTrue(date_groups, msg=f'No date groups found on Coupon section "{section_name}"')
            for name, date_group in date_groups.items():
                events = date_group.items_as_ordered_dict
                self.assertTrue(events, msg=f'No events found on Coupon details page in date group "{name}"')
                for event_name, event in events.items():
                    time_format = self.event_card_coupon_and_competition_future_time_format_pattern
                    event_time = event.event_time.replace(' ', ', ').replace(',,', ',') if 'Today' in event.event_time else self.get_date_time_formatted_string(
                        date_time_obj=datetime.strptime(event.event_time, time_format), time_format=self.my_bets_event_future_time_format_pattern)
                    prices = event.get_available_prices()
                    button_name, button = list(prices.items())[0]
                    button.click()
                    self.assertTrue(button.is_enabled(), msg=f'Bet button "{button_name}" is not selected')
                    self.events_names.append(f'{event_name} {event_time}')
                    if len(self.events_names) == number_of_selections:
                        return
        if len(self.events_names) < number_of_selections:
            raise SiteServeException('Cannot collect enough events on Coupons page')

    def test_004_navigate_to_betslip(self):
        """
        DESCRIPTION: Navigate to betslip
        EXPECTED: Betslip is loaded
        """
        self.site.open_betslip()

    def test_005_add_a_stake_in_the_trixie_stake_box_and_click_on_bet_now_button_from_ox_99___place_bet_button(self):
        """
        DESCRIPTION: Add a stake in the Trixie stake box and click on "Bet Now" button (From OX 99 - "Place Bet" button)
        EXPECTED: The bet is successfully placed and bet confirmation is displayed.
        EXPECTED: The currency is in £.(Currency should be the same as it was set during registration)
        """
        self.__class__.user_balance = self.site.header.user_balance
        singles = self.get_betslip_sections().Singles
        self.assertTrue(singles, msg='No Single stakes found')
        multiples_section = self.get_betslip_sections(multiples=True).Multiples
        self.assertTrue(multiples_section, msg='No Multiple stakes found')
        self.__class__.bet_info = OrderedDict()
        stake = self.zip_available_stakes(section=multiples_section).get(vec.betslip.TRX)
        self.assertTrue(stake, msg=f'No "{vec.betslip.TRX}" stake found')
        self.enter_stake_amount(stake=(stake.name, stake))
        params = self.collect_stake_info(stake=(vec.betslip.TRX, stake), multiples=True)
        self.bet_info[stake.name] = params
        self.bet_info[stake.name]['market_name'] = []
        for event_name, event in singles.items():
            self.bet_info[stake.name]['market_name'].append(event.market_name)
            self.bet_info[event.outcome_name] = dict()
            self.bet_info[event.outcome_name]['odds'] = event.odds
            self.bet_info[event.outcome_name]['market_name'] = event.market_name
        betslip = self.get_betslip_content()
        self.bet_info['total_stake'] = float(betslip.total_stake)
        self.assertTrue(betslip.bet_now_button.is_enabled(), msg='Bet Now Button is disabled')
        betslip.bet_now_button.click()
        self.check_bet_receipt_is_displayed()

    def test_006_verify_the_bet_confirmation(self):
        """
        DESCRIPTION: Verify the Bet Confirmation
        EXPECTED: The currency is in £.
        EXPECTED: **The bet type is displayed: (e.g: Trixie(n));
        EXPECTED: Same Selection and Market is displayed where the bet was placed;
        EXPECTED: **Unique Bet ID is displayed;
        EXPECTED: The balance is correctly updated;
        EXPECTED: **Odds are exactly the same as when bet has been placed;
        EXPECTED: **Stake is correctly displayed;
        EXPECTED: **Total Stake is correctly displayed;
        EXPECTED: **Estimated Returns is exactly the same as when bet has been placed;
        EXPECTED: "Reuse Selection" and "Done" buttons are displayed.
        """
        self.__class__.bet_receipt = self.site.bet_receipt.footer
        self.check_bet_receipt(betslip_info=self.bet_info, stake_name=vec.betslip.TRX)
        self.assertTrue(self.bet_receipt.has_reuse_selections_button(),
                        msg=f'"Reuse Selection" is not displayed')
        self.assertTrue(self.bet_receipt.has_done_button(),
                        msg=f'"Done" is not displayed')
        self.verify_user_balance(expected_user_balance=(float(self.user_balance) - self.bet_info['total_stake']))

        betreceipt_section = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertEqual(len(betreceipt_section), 1, msg='There is more than one item in Bet Receipt')
        for section_name, section in betreceipt_section.items():
            bet_id = section.bet_id
        self.assertTrue(bet_id, msg='Bet ID os not displayed')

    def test_007_click_on_done_button(self):
        """
        DESCRIPTION: Click on Done button
        EXPECTED: Football Coupons page is loading
        """
        self.bet_receipt.click_done()
        self.site.wait_content_state('CouponPage')

    def test_008_click_on_my_bets_button_from_the_header(self):
        """
        DESCRIPTION: Click on My Bets button from the header
        EXPECTED: My Bets page is opened
        """
        self.site.open_my_bets_open_bets()
        self.device.driver.implicitly_wait(5)

    def test_009_go_to_the_bet_that_was_just_placed_and_verify_that_the_bet_receipt_fields_are_correct(self):
        """
        DESCRIPTION: Go to the bet that was just placed and Verify that the Bet Receipt fields are correct.
        EXPECTED: The currency is in £.
        EXPECTED: **The bet type , Selection Name and odds are displayed
        EXPECTED: Event Name is displayed
        EXPECTED: **Bet Receipt unique ID
        EXPECTED: Selection Details:
        EXPECTED: Selection Name where the bet has been placed
        EXPECTED: Event name
        EXPECTED: **Time and Date
        EXPECTED: **Market where the bet has been placed
        EXPECTED: **E/W Terms: (None for bets where E/W is not valid)
        EXPECTED: **Correct Stake is correctly displayed;
        """
        if self.device_type == 'mobile':
            self.site.wait_content_state(state_name='OpenBets', timeout=20)
        _, trixie_bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=vec.betslip.TRX.upper(), event_names=self.events_names, number_of_stakes=1)

        for _, betleg in trixie_bet.items_as_ordered_dict.items():
            market_name = self.bet_info[betleg.outcome_name]['market_name']
            self.assertEqual(betleg.market_name, market_name,
                             msg=f'Market name: "{betleg.market_name}" '
                             f'is not as expected: "{market_name}"')
            self.assertEqual(betleg.odds_value, self.bet_info[betleg.outcome_name]['odds'],
                             msg=f'Actual Odds value: "{betleg.odds_value}" '
                             f'is not as expected: "{self.bet_info[betleg.outcome_name]["odds"]}"')
        actual_stake = trixie_bet.stake.value
        expected_stake = f'£{self.bet_info["total_stake"]:.2f}'
        self.assertEqual(actual_stake, expected_stake,
                         msg=f'Actual stake: "{actual_stake} '
                         f'is not as expected: "{expected_stake}"')
