import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.slow
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.portal_dependant
@vtest
class Test_C28499_Verify_Price_Odds_buttons_view_before_and_after_adding_to_betslip(BaseBetSlipTest, BaseSportTest):
    """
    TR_ID: C28499
    NAME: Verify Price/Odds buttons view before and after adding to betslip
    DESCRIPTION: This test case verifies Price/Odds buttons view before selecting them and after
    """
    keep_browser_open = True

    def select_odd_format_and_check_price_button_accordingly(self, decimal=False):
        if decimal:
            format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
            self.assertTrue(format_changed, msg='Odds format is not changed to Decimal')
        else:
            format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_FRAC)
            self.assertTrue(format_changed, msg='Odds format is not changed to fractional')
        self.site.back_button.click()
        self.site.wait_content_state_changed(timeout=10)
        self.site.open_sport(name='FOOTBALL', timeout=10)
        self.site.wait_content_state('Football')

        sections = list(self.site.football.tab_content.accordions_list.items_as_ordered_dict.values())
        self.assertTrue(sections,
                        msg='"Sections" are not available')
        for section in sections:
            events = list(section.items_as_ordered_dict.values())
            self.assertTrue(events, msg='"Events" are not available')
            for event in events:
                outputprices = list(event.template.items_as_ordered_dict.values())
                self.assertTrue(outputprices, msg='"Selections" are not available')
                for price in outputprices:
                    self._logger.info(f'Current price is: "{price.name}"')
                    if decimal:
                        self.assertRegexpMatches(price.name, self.decimal_pattern,
                                                 msg=f'Price/Odds value "{price.name}" '
                                                     f'not match decimal pattern: "{self.decimal_pattern}"')
                    else:
                        self.assertRegexpMatches(price.name, self.fractional_pattern,
                                                 msg=f'Price/Odds value "{price.name}" '
                                                     f'not match fractional pattern: "{self.fractional_pattern}"')
                break
            break

    def test_000_preconditions(self):
        """
        NAME: Verify Price/Odds buttons view before and after adding to betslip
        DESCRIPTION: This test case verifies Price/Odds buttons view before selecting them and after
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)
            self.__class__.event_id = event[0]['event']['id']
        else:
            event = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
            self.__class__.event_id = event.event_id
            start_time_upcoming = self.get_date_time_formatted_string(hours=10)
            self.ob_config.add_autotest_premier_league_football_event(is_upcoming=True, start_time=start_time_upcoming)

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Home page is opened
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_002_tap_live_icon_from_the_sports_ribbon(self):
        """
        DESCRIPTION: Tap '**LIVE**' icon from the sports ribbon
        EXPECTED: 'In-Play' Landing page is opened
        """
        if self.device_type == 'mobile':
            if self.brand == 'bma':
                self.site.home.menu_carousel.click_item(vec.siteserve.IN_PLAY_TAB)
            else:
                self.site.home.menu_carousel.click_item(vec.SB.IN_PLAY)
        else:
            menu_items = self.site.header.sport_menu.items_as_ordered_dict
            self.assertTrue(menu_items, msg='No menu items on Home page')
            in_play_tab = menu_items[vec.siteserve.IN_PLAY_TAB]
            in_play_tab.click()
        self.site.wait_content_state(state_name='in-play')

    def test_003_tap_sport_icon_from_live_sports_ribbon(self):
        """
        DESCRIPTION: Tap <Sport> icon from live sports ribbon
        EXPECTED: <Sport> In-Play page is opened
        """
        sports_categories = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
        self.assertTrue(sports_categories.keys(), msg='Categories are not displayed')
        active_tab = list(sports_categories.values())[1]
        self.assertTrue(active_tab.is_selected(), msg=f'"{active_tab.name}" is not active by default')

    def test_004_choose_live_now_sorting_type(self):
        """
        DESCRIPTION: Choose '**Live Now**' sorting type
        EXPECTED: Live Now events are displayed
        """
        if self.device_type == 'mobile':
            live_now = self.site.inplay.tab_content.live_now
            upcoming = self.site.inplay.tab_content.upcoming
            self.assertTrue(live_now.is_displayed(), msg='"LIVE_NOW" is not visible')
            self.assertTrue(upcoming.is_displayed(), msg='"UPCOMING" is not visible')
        else:
            sections = list(self.site.inplay.tab_content.grouping_buttons.items_as_ordered_dict.keys())
            expected_sections = [vec.Inplay.LIVE_NOW_SWITCHER, vec.Inplay.UPCOMING_SWITCHER]
            self.assertEqual(sections, expected_sections, msg=f'Actual sections: "{sections}" are not same as'
                                                              f'Expected sections: "{expected_sections}"')

    def test_005_verify_the_priceodds_buttons_view_of_the_events_displayed(self):
        """
        DESCRIPTION: Verify the 'Price/Odds' buttons view of the events displayed
        EXPECTED: *    'Price/Odds' buttons display price received from backend on light grey background.
        EXPECTED: *    'Price/Odds' buttons display selection type (e.gHome, Draw, Away)
        """
        if self.device_type == 'mobile':
            in_play_events = self.site.inplay.tab_content.live_now.items_as_ordered_dict
        else:
            in_play_events = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(in_play_events, msg='No events found')

        for event_name, event in in_play_events.items():
            if not event.is_expanded():
                event.expand()
            first_event = list(event.items)[0]
            self.__class__.odds = first_event.template.items_as_ordered_dict
            self.assertTrue(self.odds, msg=f'"{event_name}" event Price/Odds buttons is not displayed')

            for price, button in self.odds.items():
                self.assertEqual(bool(price), True,
                                 msg=f'\n"{event_name}" event price "{price}" actual display state: '
                                     f'"{bool(price)}" is not as expected: "{True}"')
                button_state = wait_for_result(lambda: button.is_enabled(expected_result=True, timeout=5),
                                               expected_result=True, timeout=10,
                                               name=f'Button enabled state to be: "{True}"')
                self.assertEqual(button_state, True,
                                 msg=f'\n"{event_name}" event "{price}" Bet Button actual enabled state: '
                                     f'"{button_state}" is not as expected: "{True}"')
            break

    def test_006_click_on_priceodds_button_and_check_its_displaying(self):
        """
        DESCRIPTION: Click on price/odds button and check it's displaying
        EXPECTED: Button becomes green
        """
        output_price = list(self.odds.values())[0]
        output_price.click()

        if self.device_type == 'mobile':
            self.site.add_first_selection_from_quick_bet_to_betslip()
        self.__class__.expected_betslip_counter_value = 1

    def test_007_verify_that_selection_is_added_to_bet_slip(self):
        """
        DESCRIPTION: Verify that selection is added to Bet Slip
        EXPECTED: *   Selection is shown in Betslip widget/Slide Out Betslip
        EXPECTED: *   Selection is present in Bet Slip and counter is increased on header
        """
        self.site.open_betslip()
        selections_count = self.get_betslip_content().selections_count
        self.assertEqual(int(selections_count), self.expected_betslip_counter_value,
                         msg=f'Actual Bet Slip counter value: "{int(selections_count)}" '
                             f'is not as expected: "{self.expected_betslip_counter_value}"')

    def test_008_remove_selection_from_bet_slip(self):
        """
        DESCRIPTION: Remove selection from Bet Slip
        EXPECTED: *   Selection is removed
        EXPECTED: *   Price/odds button becomes light grey
        """
        self.clear_betslip()

    def test_009_check_price_type_changing_from_decimal_to_fractional_and_vice_versa(self):
        """
        DESCRIPTION: Check Price type changing from Decimal to Fractional and vice versa
        EXPECTED: Prices format is changed on buttons depending what format was selectedDese
        """
        self.site.login(username=tests.settings.betplacement_user)
        self.select_odd_format_and_check_price_button_accordingly(decimal=True)

    def test_010_select_upcoming_sorting_type_and_repeat_steps_5_9(self):
        """
        DESCRIPTION: Select 'Upcoming' sorting type and repeat steps 5-9
        """
        self.navigate_to_page('Homepage')
        self.site.wait_content_state(state_name='Homepage')
        if self.device_type == 'mobile':
            if self.brand == 'bma':
                self.site.home.menu_carousel.click_item(vec.siteserve.IN_PLAY_TAB)
            else:
                self.site.home.menu_carousel.click_item(vec.SB.IN_PLAY)
        else:
            menu_items = self.site.header.sport_menu.items_as_ordered_dict
            self.assertTrue(menu_items, msg='No menu items on Home page')
            in_play_tab = menu_items[vec.siteserve.IN_PLAY_TAB]
            in_play_tab.click()
        self.site.wait_content_state(state_name='in-play')

        if self.device_type == 'mobile':
            upcoming = self.site.inplay.tab_content.upcoming
            self.assertTrue(upcoming.is_displayed(), msg='"UPCOMING" is not visible')
        else:
            self.site.inplay.tab_content.grouping_buttons.click_button(vec.inplay.UPCOMING_SWITCHER)
            upcoming = self.site.inplay.tab_content.accordions_list

        upcoming_list = upcoming.items_as_ordered_dict

        for event_name, event in upcoming_list.items():
            if not event.is_expanded():
                event.expand()
            first_event = list(event.items)[0]
            odds = first_event.template.items_as_ordered_dict
            self.assertTrue(odds, msg=f'"{event_name}" event Price/Odds buttons is not displayed')

            for price, button in odds.items():
                self.assertEqual(bool(price), True,
                                 msg=f'\n"{event_name}" event price "{price}" actual display state: '
                                     f'"{bool(price)}" is not as expected: "{True}"')
                button_state = wait_for_result(lambda: button.is_enabled(expected_result=True, timeout=5),
                                               expected_result=True, timeout=10,
                                               name=f'Button enabled state to be: "{True}"')
                self.assertEqual(button_state, True,
                                 msg=f'\n"{event_name}" event "{price}" Bet Button actual enabled state: '
                                     f'"{button_state}" is not as expected: "{True}"')
            break

    def test_011_repeat_steps_5_9_on_in_play_widget(self):
        """
        DESCRIPTION: Repeat steps #5-9 on 'In play' widget
        """
        # Covered in above steps

    def test_012_navigate_to_event_details_page_and_repeat_steps5_9(self):
        """
        DESCRIPTION: Navigate to Event Details Page and repeat steps#5-9
        """
        self.navigate_to_page('Homepage')
        self.site.wait_content_state(state_name='Homepage')
        self.navigate_to_edp(event_id=self.event_id)
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        if self.device_type == 'desktop' or self.brand == 'ladbrokes':
            market = markets_list.get(self.expected_market_sections.match_result.title())
        else:
            market = markets_list.get(self.expected_market_sections.match_result.upper())
        self.assertTrue(market, msg='Can not find Match Result section')
        outcomes = market.outcomes.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No outcomes are shown for Match Result market')

        for price, button in outcomes.items():
            self.assertEqual(bool(price), True,
                             msg=f'\n"Price "{price}" actual display state: '
                                 f'"{bool(price)}" is not as expected: "{True}"')
            button_state = wait_for_result(lambda: button.is_enabled(expected_result=True, timeout=5),
                                           expected_result=True, timeout=10,
                                           name=f'Button enabled state to be: "{True}"')
            self.assertEqual(button_state, True,
                             msg=f'\n"Price "{price}" Bet Button actual enabled state: '
                                 f'"{button_state}" is not as expected: "{True}"')

    def test_013_select_to_betslip_at_least_5_selections_and_check_the_price_odds_button_displaying(self):
        """
        DESCRIPTION: Select to betslip at least 5 selections and check the price odds button displaying
        EXPECTED: *   Selected Buttons becomes green
        EXPECTED: *   Selections are added to Betslip
        """
        # Covered in above steps
