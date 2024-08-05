import pytest
from fractions import Fraction
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.environments import constants as vec
from tests.pack_009_SPORT_Specifics.Football_Specifics.Football_Coupons.BaseCouponsTest import BaseCouponsTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_uat  # It is applicable only for ladbrokes as "goal scorer coupon" is not available for coral
@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C44870317_Verify_Goal_scorer_coupons_detail_page_(BaseCouponsTest, BaseBetSlipTest):
    """
    TR_ID: C44870317
    NAME: "Verify  Goal scorer coupons detail page  "
    DESCRIPTION: -Verify below on the Goal scorer coupons detail page
    DESCRIPTION: - Verify user can navigate to Goal scorer coupons detail page
    DESCRIPTION: - Verify the single and multiple bet placement for Goal scorer coupons events
    """
    keep_browser_open = True
    goalscorer_coupon = vec.coupons.GOALSCORER_COUPON
    expected_market_types = ['1ST', 'LAST', 'ANYTIME']

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load oxygen application
        EXPECTED: Home Page is displayed
        """
        self.site.login()

    def test_002_go_to_football_coupons_and_select_goalscorer_coupon(self):
        """
        DESCRIPTION: Go to Football coupons and Select 'Goalscorer' coupon
        EXPECTED: Goalscorer coupon detail page opened
        """
        self.navigate_to_page(name='sport/football/coupons')
        self.site.wait_content_state('Football')
        self.site.close_all_dialogs(timeout=5)
        # TODO BMA when goal scorer coupon availble
        self.find_coupon_and_open_it(coupon_name=self.goalscorer_coupon)

    def test_003_verify_competition_section_displaying(self):
        """
        DESCRIPTION: Verify competition section displaying
        EXPECTED: First competition is expanded by default;
        EXPECTED: All competitions are collapsible & expandable.
        """
        leagues = self.site.coupon.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(leagues, msg='No competitions found on Coupon page')
        section = list(leagues.values())[0]
        comp_name, self.__class__.comp = list(section.items_as_ordered_dict.items())[0]
        self.assertTrue(self.comp.is_expanded(), msg=f'First competition "{comp_name}" is not expanded by default')
        for section_name, section in leagues.items():
            event = list(section.items_as_ordered_dict.values())[0]
            if event.is_expanded():
                self.assertTrue(event.is_expanded(), msg=f'League "{section_name}" is not expanded')
                event.collapse()
                self.assertFalse(event.is_expanded(), msg=f'League "{section_name}" is not collapsible')
                event.expand()
            else:
                self.assertFalse(event.is_expanded(), msg=f'League "{section_name}" is not collapsible')
                event.expand()
                self.assertTrue(event.is_expanded(), msg=f'League "{section_name}" is not expandable')
                event.collapse()
                self.assertFalse(event.is_expanded(), msg=f'League "{section_name}" is not collapsible')

    def test_004_verify_event_section_displaying(self):
        """
        DESCRIPTION: Verify event section displaying
        EXPECTED: First event section(2nd level of accordion) within first Competitions accordion is expanded by default
        EXPECTED: All other event sections are collapsed by default
        EXPECTED: Event section is expandable / collapsible with "Show more" button
        EXPECTED: 'SEE ALL' link is shown
        """
        # expandable, collapsible are covered in step 4
        self.assertTrue(self.comp.has_show_more_button(),
                        msg=f'"{vec.coupons.SHOW_MORE.upper()}" button is not present')
        self.assertTrue(self.comp.has_see_all_link(),
                        msg=f'"{vec.coupons.SEE_ALL.upper()}" link is not present for event')

    def test_005_click_on_the_see_all_link(self):
        """
        DESCRIPTION: Click on the 'SEE ALL' link
        EXPECTED: User is redirected to the event details page
        """
        self.comp.see_all_link.click()
        self.site.wait_content_state(state_name='EventDetails')
        self.site.back_button_click()
        self.site.wait_content_state('CouponPage')

    def test_006_verify_goalscorer_markets_collection_tab(self, pattern=r'^\d+\/\d+$'):
        """
        DESCRIPTION: Verify Goalscorer markets collection tab
        EXPECTED: -'Goalscorer' market headers are displayed:
        EXPECTED: -Date of event is displayed
        EXPECTED: '1st'
        EXPECTED: 'Last'
        EXPECTED: 'Anytime'
        EXPECTED: -Available selections are displayed in the grid, odds of each are shown in correct market section (1st, Last, Anytime)
        EXPECTED: -Selection name(footballer name), footballer team are displayed for each selection (if available)
        EXPECTED: -If some markets are not created or do not contain at least 1 available selection - their header is not displayed
        EXPECTED: -Odds on 'Odds/Prices' buttons are displayed in fractional format by default
        EXPECTED: -Maximum 5 selections are displayed within event section
        EXPECTED: -'SHOW MORE' button is present if there are more than 5 selections within events section
        """
        leagues = self.site.coupon.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(leagues, msg='No leagues found on Coupon page')
        section = list(leagues.values())[0]
        self.__class__.event = list(section.items_as_ordered_dict.values())[0]
        self.assertEqual(self.site.coupon.name, self.goalscorer_coupon,
                         msg=f'Coupon name in subheader "{self.site.coupon.name}" '
                             f'is not the same as expected "{self.goalscorer_coupon}"')
        date = self.event.fixture_header.date.text
        self.assertTrue(date, msg=f'date "{date}" is not displayed')
        actual_market_types = [self.event.fixture_header.header1, self.event.fixture_header.header2,
                               self.event.fixture_header.header3]
        self.assertEqual(actual_market_types, self.expected_market_types,
                         msg=f'Actual markets "{actual_market_types}" '
                             f'are not the same as expected "{self.expected_market_types}"')
        event_ordering = [selection for selection in self.event.table.items]
        for selection in event_ordering:
            name = selection.name
            team_name = selection.team_name
            price = selection.bet_button.name
            self.assertRegexpMatches(price, pattern,
                                     msg=f'Stake odds number "{price}" not match fractional pattern "{pattern}"')
            self.assertTrue(team_name, msg=f'Player team name "{team_name}" is not displayed')
            self.assertTrue(name, msg=f'Player name "{name}" is not displayed')
            self.assertTrue(price, msg=f'Player price "{price}" is not displayed')
        self.assertEqual(len(self.event.table.players), 5,
                         msg=f'Incorrect players count is displayed: "{len(self.event.table.players)}" '
                             f'Expected count: "5"')
        self.assertTrue(self.event.has_show_more_button(), msg=f'"{vec.coupons.SHOW_MORE.upper()}" button is not present')

    def test_007_verify_show_more_button(self):
        """
        DESCRIPTION: Verify 'SHOW MORE' button
        EXPECTED: All available selections are present after clicking / tapping 'SHOW MORE button
        """
        self.event.show_more_button.click()
        result = wait_for_result(lambda: len(self.event.table.items_as_ordered_dict) > 5, timeout=7,
                                 name=f'All available selections are present after clicking "{vec.coupons.SHOW_MORE.upper()}" button')
        self.assertTrue(result,
                        msg=f'Actual players count is displayed after click "SHOW MORE" button: '
                            f'"{len(self.event.table.items_as_ordered_dict)}". Expected count should be > 5')

    def test_008_verify_ordering_of_selections(self):
        """
        DESCRIPTION: Verify ordering of selections
        EXPECTED: -Selections are ordered by odds in first available market (e.g. 1st/Last/Anytime) in ascending order (lowest to highest)
        EXPECTED: -If odds of selections are the same -> display alphabetically by footballer name (in ascending order)
        EXPECTED: -If prices are absent for selections - display alphabetically by footballer name (in ascending order)
        """
        player_name = []
        player_price = []
        event_ordering = [selection for selection in self.event.table.items]
        for selection in event_ordering:
            name = selection.name
            price = float(Fraction(selection.bet_button.name))
            player_name.append(name)
            player_price.append(price)
        for player in range(len(player_name)):
            if player == len(player_name) - 1:
                break
            if player_price[player] < player_price[player + 1]:
                continue
            elif player_price[player] == player_price[player + 1]:
                self.assertTrue(player_name[player] <= player_name[player + 1], msg='player name is not in ascending order')
            else:
                self.assertTrue(player_price[player] <= player_price[player + 1],
                                msg=f'Player price "{player_price[player]}" is less than or equal to next Player price "{player_price[player + 1]}')

    def test_009_add_selections_to_the_quickbetbetslip(self):
        """
        DESCRIPTION: Add selection(s) to the QuickBet/Betslip
        EXPECTED: Added selection(s) is/are displayed within the 'Quick Bet' (for 1 selection)/'Betslip' (for more than 1 selection)
        """
        selections = self.event.table.items_as_ordered_dict
        selection_name, selection = list(selections.items())[1]
        selection.bet_button.click()
        self.site.open_betslip()
        self.place_and_validate_single_bet()

    def test_010_enter_stake_for_a_bet_manually_or_using_quick_stakes_buttons_tap_place_bet_in_quick_betbet_now_in_betslip(self):
        """
        DESCRIPTION: Enter 'Stake' for a bet manually or using 'Quick Stakes' buttons> Tap 'Place Bet' in 'Quick Bet'/'Bet Now' in Betslip
        EXPECTED: -Bet is successfully placed
        EXPECTED: -'Quick Bet'/Betslip is replaced with 'Bet Receipt' view, displaying bet information
        EXPECTED: -Balance is decreased accordingly
        """
        self.check_bet_receipt_is_displayed()
        self.navigate_to_page('homepage')
        expected_user_balance = self.user_balance - self.bet_amount
        self.verify_user_balance(expected_user_balance=expected_user_balance)

    def test_011_change_price_format_to_decimal_in_my_account__settings_and_repeat_steps_7___14(self):
        """
        DESCRIPTION: Change price format to Decimal in My Account > Settings and Repeat steps 7 - 14
        EXPECTED: All Prices/Odds are displayed in Decimal format
        """
        self.site.navigate_to_right_menu_item('Settings')
        self.site.right_menu.click_item(item_name='Betting Settings')
        self.site.settings.decimal_btn.click()
        self.site.close_all_dialogs(5)
        self.navigate_to_page('homepage')
        self.test_002_go_to_football_coupons_and_select_goalscorer_coupon()
        self.test_003_verify_competition_section_displaying()
        self.test_004_verify_event_section_displaying()
        self.test_005_click_on_the_see_all_link()
        self.test_006_verify_goalscorer_markets_collection_tab(pattern=r'^\d+\.\d+$')
        self.test_007_verify_show_more_button()
        self.test_008_verify_ordering_of_selections()
        self.test_009_add_selections_to_the_quickbetbetslip()
        self.test_010_enter_stake_for_a_bet_manually_or_using_quick_stakes_buttons_tap_place_bet_in_quick_betbet_now_in_betslip()
