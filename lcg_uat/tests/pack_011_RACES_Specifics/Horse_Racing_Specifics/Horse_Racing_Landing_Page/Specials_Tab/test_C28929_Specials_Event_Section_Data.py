import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.bet_placement
@pytest.mark.quick_bet
@pytest.mark.each_way
@pytest.mark.mobile_only
@pytest.mark.races
@pytest.mark.login
@vtest
class Test_C28929_Event_Section_Data(BaseRacing):
    """
    TR_ID: C28929
    VOL_ID: C9698311
    NAME: Specials Event Section Data
    """
    keep_browser_open = True
    event_name = None
    bet_amount = 0.1
    expected_ew_terms = {"ew_places": 2, "ew_fac_num": 1, "ew_fac_den": 16}
    lp_prices = {0: '1/4', 1: '7/1'}
    ew_terms = ''
    specials_event = None
    racing_specials_name = vec.racing.RACING_SPECIALS_NAME

    def test_000_create_event_with_ew_terms(self):
        """
        DESCRIPTION: Create racing specials events with Each Way terms and SP/LP prices
        EXPECTED: Events are created in OB
        """
        event_params = self.ob_config.add_racing_specials_event(number_of_runners=2, ew_terms=self.expected_ew_terms, time_to_start=20)
        self.__class__.eventID, self.__class__.event_off_time, self.__class__.selection_ids =\
            event_params.event_id, event_params.event_off_time, event_params.selection_ids
        self.__class__.event_name = '%s %s' % (self.event_off_time, self.horseracing_autotest_specials_name_pattern)
        self._logger.info('*** Event id: %s, event off time: %s, selection ids: %s'
                          % (self.eventID, self.event_off_time, list(self.selection_ids.values())))

        event_params_lp = self.ob_config.add_racing_specials_event(number_of_runners=2, ew_terms=self.expected_ew_terms,
                                                                   lp_prices={0: '1/4', 1: '7/1'}, time_to_start=10)
        self.__class__.eventID_lp, self.__class__.event_off_time_lp, self.__class__.selection_ids_lp =\
            event_params_lp.event_id, event_params_lp.event_off_time, event_params_lp.selection_ids
        self.__class__.event_name_lp = '%s %s' % (self.event_off_time_lp, self.horseracing_autotest_specials_name_pattern)
        self._logger.info('*** Event id: %s, event off time: %s, selection ids: %s'
                          % (self.eventID_lp, self.event_off_time_lp, self.selection_ids_lp.values()))

    def test_001_tap_horse_racing_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Horse Racing' icon on the Sports Menu Ribbon
        EXPECTED: 'Horse Racing' landing page is opened
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')

    def test_002_click_tap_specials_tab(self):
        """
        DESCRIPTION: Click / tap 'SPECIALS' tab
        EXPECTED: 'SPECIALS' tab is opened
        """
        self.site.horse_racing.tabs_menu.click_button('SPECIALS')

    def test_003_go_to_events_in_the_particular_module(self):
        """
        DESCRIPTION: Go to events in the particular module
        EXPECTED: Events are shown
        """
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found on Specials page')
        section = sections.get(self.racing_specials_name)
        self.assertTrue(section, msg='"%s" was not found in sections "%s"'
                                     % (self.racing_specials_name, ', '.join(sections.keys())))
        events = section.items_as_ordered_dict
        self.assertTrue(events, msg='No events found in "%s"' % self.racing_specials_name)
        self.__class__.specials_event = events.get(self.event_name)
        self.assertTrue(self.specials_event, msg='Event with name "%s" was not found' % self.event_name)
        self.__class__.specials_event_lp = events.get(self.event_name_lp)
        self.assertTrue(self.specials_event_lp, msg='Event with name "%s" was not found' % self.event_name_lp)

    def test_004_verify_event_date(self):
        """
        DESCRIPTION: Verify event date
        EXPECTED: Event date is shown near the event name
        """
        event_date = self.specials_event.event_date
        self.assertTrue(event_date, msg='Event date is empty')
        self._logger.info('*** Event date is "%s"' % event_date)

    def test_005_verify_each_way_terms(self):
        """
        DESCRIPTION: Verify Each-way terms
        EXPECTED: Terms are displayed in the following format:
           "Each Way: x/y odds a places z,j,k" where:
            - x = eachWayFactorNum
            - y = eachWayFactorDen
            - z,j,k = eachWayPlaces
        """
        self.specials_event.expand()
        self.assertTrue(self.specials_event.has_each_way_terms(), msg='Each Way terms is not found')
        self.__class__.ew_terms = self.specials_event.each_way_terms.value
        self._logger.debug('*** Each Way terms: "%s"' % self.ew_terms)
        self.assertTrue(self.ew_terms != '',
                        msg='Each Way terms is not found for event "%s"'
                        % self.event_name)
        self.check_each_way_terms_format(each_way_terms=self.ew_terms)
        self.check_each_way_terms_correctness(each_way_terms=self.ew_terms,
                                              expected_each_way_terms=self.expected_ew_terms)

    def test_006_verify_selection_names(self):
        """
        DESCRIPTION: Verify selection names
        EXPECTED: Selection names correspond to the "name" attribute on selection level event selections
        """
        self.__class__.selections = self.specials_event.items_as_ordered_dict
        self.assertTrue(self.selections, msg='No selections found for "%s" event' % self.event_name)
        selection_names = list(self.selections.keys())
        self.assertListEqual(sorted(selection_names), sorted(list(self.selection_ids.keys())))

    def test_007_verify_SP_prices_of_selections(self):
        """
        DESCRIPTION: Verify price/odds button for SP prices
        EXPECTED: Price is the same as configured in TI
        """
        for selection_name, selection in self.selections.items():
            self.assertEqual(selection.bet_button.outcome_price_text, 'SP',
                             msg='Selection price "%s" is not the same as in TI "%s"'
                             % (selection.bet_button.outcome_price_text, 'SP'))

    def test_008_verify_LP_prices_of_selections(self):
        """
        DESCRIPTION: Verify price/odds button for LP prices
        EXPECTED: Price is the same as configured in TI
        """
        self.specials_event_lp.expand()
        self.__class__.selections_lp = self.specials_event_lp.items_as_ordered_dict
        self.assertTrue(self.selections_lp, msg='No selections found for "%s" event' % self.event_name_lp)
        for (selection_name, selection), (runner_name, runner_price) in zip(self.selections_lp.items(), self.lp_prices.items()):
            self.assertEqual(selection.bet_button.outcome_price_text, runner_price,
                             msg='Selection price "%s" is not the same as in TI "%s"'
                             % (selection.bet_button.outcome_price_text, runner_price))

    def test_009_verify_order_of_selections(self):
        """
        DESCRIPTION: Verify order of selections
        EXPECTED:
            Selection is ordered by rules:
            - by LP price from lowest to highest - when price is available
            - by 'name' alphabetically in case prices are the same
            - by 'name' alphabetically in case SP price
        """
        expected_selections_order = [x for _, x in sorted(zip(self.lp_prices.values(),
                                                              self.selections_lp.keys()))]
        self._logger.debug('*** Expected selections order "%s"' % expected_selections_order)
        self.assertListEqual(list(self.selections_lp.keys()), expected_selections_order,
                             msg='Selections order "%s" is not the same as expected "%s"'
                             % (list(self.selections_lp.keys()), expected_selections_order))

    def test_010_check_betplacement_on_specials_event(self):
        """
        DESCRIPTION: Check adding Bet placement
        EXPECTED: Bet placement is performed as for simple racing events
        """
        self.site.login()
        self.site.close_all_dialogs(async_close=False)
        list(self.selections_lp.values())[0].bet_button.click()
        quick_bet = self.site.quick_bet_panel.selection.content
        quick_bet.amount_form.input.value = self.bet_amount
        self.assertEqual(quick_bet.amount_form.input.value, '{0:.2f}'.format(self.bet_amount),
                         msg='Actual amount "%s" does not match expected "%s"'
                             % (quick_bet.amount_form.input.value, '{0:.2f}'.format(self.bet_amount)))
        self.site.quick_bet_panel.place_bet.click()
        bet_receipt_displayed = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
        self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
