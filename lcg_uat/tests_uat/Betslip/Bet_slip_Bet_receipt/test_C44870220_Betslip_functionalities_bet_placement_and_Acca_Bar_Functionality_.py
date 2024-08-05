import random
import pytest
import tests
from time import sleep
import voltron.environments.constants as vec
from selenium.common.exceptions import ElementClickInterceptedException
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.p1
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C44870220_Betslip_functionalities_bet_placement_and_Acca_Bar_Functionality_(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C44870220
    NAME: "Betslip functionalities bet placement and Acca Bar Functionality "
    DESCRIPTION: "Betslip functionalities bet placement and Acca Bar Functionality "
    PRECONDITIONS: Customer can view the Bet slip logged in or logged out
    """
    keep_browser_open = True
    selection_list = []
    count = 0

    def selections(self, selection):
        bet_buttons_list = self.site.home.acca_bet_buttons
        self.assertTrue(bet_buttons_list, msg='No bet buttons on UI')
        length = len(bet_buttons_list)
        sel = 0
        for i in range(0, 10):
            index = random.randint(0, length - 1)
            selection_btn = bet_buttons_list[index]
            self.site.contents.scroll_to_we(selection_btn)
            if selection_btn.get_attribute('disabled') == "true":
                continue
            elif selection_btn.is_enabled() and not selection_btn.is_selected() and selection_btn.text != 'SP':
                try:
                    selection_btn.click()
                    sleep(2)
                    self.__class__.selection_list.append(selection_btn)
                    self.__class__.count += 1
                    sel = sel + 1
                except ElementClickInterceptedException:
                    continue
            if self.device_type == 'mobile':
                if self.__class__.count == 1:
                    self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet was not shown')
                    self.assertTrue(self.site.quick_bet_panel.add_to_betslip_button.is_displayed(),
                                    msg='"ADD TO BETSLIP" button is not displayed')
                    self.assertTrue(self.site.quick_bet_panel.place_bet.is_displayed(),
                                    msg=f'"{vec.betslip.LOGIN_AND_PLACE_BET_QUICK_BET}" button is not displayed')
                    self.site.add_first_selection_from_quick_bet_to_betslip()
            elif self.device_type == 'desktop':
                betslip_counter = self.site.header.bet_slip_counter.counter_value
                self.assertEqual(betslip_counter, str(len(self.__class__.selection_list)),
                                 msg="The selection is not added to the betslip")
            if sel == selection:
                return

    def remove_all_buttons(self):
        remove_all_button = self.get_betslip_content().remove_all_button
        self.assertTrue(remove_all_button.is_displayed(), msg='"REMOVE ALL" button is not displayed')
        self.assertEqual(remove_all_button.name, vec.betslip.REMOVE_ALL_SELECTIONS,
                         msg=f'Button name "{remove_all_button.name}" is not as expected "{vec.betslip.REMOVE_ALL_SELECTIONS}"')
        return remove_all_button

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create/select different selections from different sports
        """
        if tests.settings.backend_env == 'prod':
            # Selection from football event
            self.__class__.selection_ids_1 = self.get_active_event_selections_for_category(
                category_id=self.ob_config.football_config.category_id)
            self._logger.info(f'*** Found Football event with selections  "{self.selection_ids_1}"')
            self.__class__.sel1_1 = list(self.selection_ids_1.keys())[0]

            # Selection from tennis event
            self.__class__.selection_ids_2 = self.get_active_event_selections_for_category(
                category_id=self.ob_config.tennis_config.category_id)
            self.__class__.sel2_1 = list(self.selection_ids_2.keys())[0]
            self._logger.info(f'*** Found Tennis event with selections "{self.selection_ids_2}"')

            # Selection from races event
            events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                         number_of_events=3, expected_template_market='Win or Each Way')
            outcomes = None
            for market in events[0]['event']['children']:
                if market['market']['templateMarketName'] == 'Win or Each Way':
                    outcomes = market['market']['children']
            self.__class__.selection_name, self.__class__.race_selection_id = \
                list({i['outcome']['name']: i['outcome']['id'] for i in outcomes}.items())[0]
            self.__class__.eventID = events[0]['event']['id']
        else:
            # Selection from football event
            event_params1 = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.team1_1, self.__class__.selection_ids_1 = event_params1.team1, event_params1.selection_ids

            # Selection from tennis event
            event_params_2 = self.ob_config.add_volleyball_event_to_austrian_league()
            self.__class__.team2_1, self.__class__.selection_ids_2 = event_params_2.team1, event_params_2.selection_ids

            # Selection from races event
            event = self.ob_config.add_UK_racing_event()
            self.__class__.selection_name, self.__class__.race_selection_id = list(event.selection_ids.items())[0]
            self.__class__.eventID = event.event_id

    def test_001_launch_the_app(self):
        """
        DESCRIPTION: Launch the app
        EXPECTED: User can able to launch the app
        """
        self.__class__.is_mobile = True if self.device_type == 'mobile' else False
        self.site.wait_content_state("Homepage")

    def test_002_tap_on_any_selection(self):
        """
        DESCRIPTION: Tap on any selection
        EXPECTED: User must be displayed Quick bet Pop up
        EXPECTED: -User sees Add to bet slip and Login and place a bet buttons
        EXPECTED: For desktop: the selection is added to the betslip.
        """
        self.selections(1)

    def test_003_verify_bet_slip_icon(self):
        """
        DESCRIPTION: Verify Bet slip icon
        EXPECTED: -'Bet Slip' icon consists Bet Slip counter bubble
        EXPECTED: -If no selections added to Bet Slip, Bet slip bubble is not shown at all
        """
        self.is_betslip_icon_shown()

    def test_004_tap_the_bet_slip_icon_add_a_few_selections_to_bet_slip(self):
        """
        DESCRIPTION: Tap the 'Bet Slip' icon ,Add a few selections to Bet slip
        EXPECTED: Bet Slip is opened,
        EXPECTED: -Selections are added
        EXPECTED: -Bet slip icon is present
        """
        self.site.login()
        self.selections(1)
        betslip_counter = self.site.header.bet_slip_counter.counter_value
        self.assertEqual(betslip_counter, str(self.__class__.count),
                         msg=f'Betslip counter "{betslip_counter}" is not same as selections added "{self.__class__.count}"')
        self.is_betslip_icon_shown()

    def test_005_remove_all_selection_from_bet_slip_and_log_outverify_bet_slip_icon(self):
        """
        DESCRIPTION: Remove all selection from Bet slip and log out,Verify Bet slip icon
        EXPECTED: User is logged out ,Verify Bet slip icon and Bet slip icon is not displayed
        """
        if self.is_mobile:
            self.site.open_betslip()
        remove_all_buttons = self.remove_all_buttons()
        remove_all_buttons.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_REMOVE_ALL)
        dialog.continue_button.click()
        self.site.logout()
        self.site.wait_content_state("HomePage")
        self.assertFalse(self.is_betslip_icon_shown(), "Betslip icon is displayed")
        self.__class__.expected_betslip_counter_value = 0
        self.__class__.selection_list = []
        self.__class__.count = 0

    def test_006_add_any_selection_from_a_sport_to_the_bet_slip(self):
        """
        DESCRIPTION: Add any selection from a sport to the Bet Slip
        EXPECTED: Bet Slip counter is 1
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids_1[self.sel1_1])
        betslip_counter = self.site.header.bet_slip_counter.counter_value
        self.assertEqual(betslip_counter, '1',
                         msg="The selection is not added to the betslip")

    def test_007_go_to_the_bet_slip(self):
        """
        DESCRIPTION: Go to the Bet Slip
        EXPECTED: The 'Your Selections (1)' section is shown with "REMOVE ALL" next to it
        EXPECTED: Added selection is displayed
        """
        singles_section = self.get_betslip_sections().Singles
        self.assertEqual(singles_section.name, vec.betslip.BETSLIP_SINGLES_NAME,
                         msg=f'Section title "{singles_section.name}" '
                             f'is not the same as expected "{vec.betslip.BETSLIP_SINGLES_NAME}"')
        self.assertEqual(self.get_betslip_content().selections_count, '1',
                         msg=f'Singles selection count "{self.get_betslip_content().selections_count}" '
                             f'is not the same as expected "1"')
        self.assertEqual(self.get_betslip_content().your_selections_label, vec.betslip.YOUR_SELECTIONS,
                         msg=f'Selection message "{self.get_betslip_content().your_selections_label}" '
                             f'is not the same as expected "{vec.betslip.YOUR_SELECTIONS}"')
        if self.device_type in ['desktop', 'tablet']:
            self._logger.warning(f'*** Skipping clicking on close button '
                                 f'as this element is not present on "{self.device_name}"')
        else:
            self.get_betslip_content().close_button.click()
        betslip_counter = self.site.header.bet_slip_counter.counter_value
        self.assertEqual(betslip_counter, '1', msg=f'BetSlip counter value "{betslip_counter}" '
                                                   f'is not the same as expected "1"')

    def test_008_add_one_more_selection_from_another_sport_races_event(self):
        """
        DESCRIPTION: Add one more selection from another Sport ,Races event
        EXPECTED: Bet Slip counter is 2
        """
        selection_ids = self.selection_ids_2[self.sel2_1]
        self.open_betslip_with_selections(selection_ids=selection_ids, timeout=15)

    def test_009_go_to_bet_slip(self):
        """
        DESCRIPTION: Go to Bet Slip
        EXPECTED: 'Your Selections (2)' section is shown with  "REMOVE ALL" next to it
        EXPECTED: 'All single stakes' label and edit box appears in Singles section
        EXPECTED: The 'Multiples' section is shown under the selections. available multiples bets is shown
        """
        sections = self.get_betslip_sections(multiples=True)
        singles_section, multiples_section = sections.Singles, sections.Multiples
        self.assertEqual(singles_section.name, vec.betslip.BETSLIP_SINGLES_NAME,
                         msg=f'Section title "{singles_section.name}" is not '
                             f'the same as expected "{vec.betslip.BETSLIP_SINGLES_NAME}"')
        betslip = self.get_betslip_content()
        self.assertEqual(betslip.selections_count, '2', msg=f'Singles selections count '
                                                            f'"{betslip.selections_count}" is not the same as expected "2"')
        self.assertEqual(betslip.your_selections_label, vec.betslip.YOUR_SELECTIONS,
                         msg=f'Selection message "{betslip.your_selections_label}" '
                             f'is not the same as expected "{vec.betslip.YOUR_SELECTIONS}"')
        if self.brand == 'bma':
            self.assertTrue(singles_section.has_all_stakes(), msg='"All single stakes" section is not shown')
            self.assertEqual(singles_section.all_stakes_label, vec.betslip.ALL_SINGLE_STAKES,
                             msg=f'Label "{singles_section.all_stakes_label}" '
                                 f'is not the same as expected "{vec.betslip.ALL_SINGLE_STAKES}"')
        self.assertTrue(multiples_section.get('Double'), msg='"Multiples" section is not shown')

        stake_title, stake = list(multiples_section.items())[0]
        self.assertEqual(stake_title, vec.betslip.DBL, msg=f'Stake title "{stake_title}" '
                                                           f'is not the same as expected "{vec.betslip.DBL}"')
        if self.device_type in ['desktop', 'tablet']:
            self._logger.info(f'*** Skipping clicking on close button '
                              f'as this element is not present on "{self.device_name}"')
        else:
            self.get_betslip_content().close_button.click()
        betslip_counter = self.site.header.bet_slip_counter.counter_value
        self.assertEqual(betslip_counter, '2', msg=f'BetSlip counter value "{betslip_counter}" '
                                                   f'is not the same as expected "2"')

    def test_010_add_one_more_selections_from_another_sports_races_event(self):
        """
        DESCRIPTION: Add one more selections from another Sports, Races event
        EXPECTED: Bet Slip counter is 3
        """
        selection_ids = self.race_selection_id
        self.open_betslip_with_selections(selection_ids=selection_ids, timeout=15)

    def test_011_go_to_bet_slip(self):
        """
        DESCRIPTION: Go to Bet Slip
        EXPECTED: 'All single stakes' label and edit box appears in Singles section
        EXPECTED: The Multiples section is displayed and contains (e.g. Treble 1, Double 3, Trixie 4 & Patent 7)
        """
        section = self.get_betslip_sections(multiples=True).Multiples
        self.assertEquals(self.get_betslip_content().selections_count, '3',
                          msg=f'Selections count "{self.get_betslip_content().selections_count}" '
                              f'is not the same as expected "3"')
        self.assertEqual(self.get_betslip_content().your_selections_label, vec.betslip.YOUR_SELECTIONS,
                         msg=f'Selection message "{self.get_betslip_content().your_selections_label}" '
                             f'is not the same as expected "{vec.betslip.YOUR_SELECTIONS}"')

        stake_title, stake = list(section.items())[0]
        self.assertEqual(stake_title, vec.betslip.TBL, msg=f'Stake title "{stake_title}" '
                                                           f'is not the same as expected "{vec.betslip.TBL}"')
        stake_title, stake = list(section.items())[1]
        self.assertEqual(stake_title, vec.betslip.DBL, msg=f'Stake title "{stake_title}" '
                                                           f'is not the same as expected "{vec.betslip.DBL}"')
        stake_title, stake = list(section.items())[2]
        self.assertEqual(stake_title, vec.betslip.TRX, msg=f'Stake title "{stake_title}" '
                                                           f'is not the same as expected "{vec.betslip.TRX}"')
        stake_title, stake = list(section.items())[3]
        self.assertEqual(stake_title, vec.betslip.PAT, msg=f'Stake title "{stake_title}" '
                                                           f'is not the same as expected "{vec.betslip.PAT}"')
        if self.device_type in ['desktop', 'tablet']:
            self._logger.warning(f'*** Skipping clicking on close button '
                                 f'as this element is not present on "{self.device_name}"')
        else:
            self.get_betslip_content().close_button.click()
        betslip_counter = self.site.header.bet_slip_counter.counter_value
        self.assertEqual(betslip_counter, '3', msg=f'BetSlip counter value "{betslip_counter}" '
                                                   f'is not the same as expected "3"')

        self.site.open_betslip()
        self.clear_betslip()

    def test_012_user_is_able_to_place_a_bet_for_single_multiples_from_pre_playin_play_tricast_hrgh_and_forecasthrgh(self):
        """
        DESCRIPTION: User is able to place a bet for single, multiples (from pre play,In play), Tricast (HR/GH) and forecast(HR/GH)
        EXPECTED: User Successfully placed bets
        """
        # single bet
        self.site.login(username=tests.settings.betplacement_user)
        self.open_betslip_with_selections(selection_ids=self.selection_ids_2[self.sel2_1])
        self.place_and_validate_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()
        self.__class__.expected_betslip_counter_value = 0

        # TODO: Add inplay events when actual match start
        select_ids = [self.selection_ids_1[self.sel1_1], self.selection_ids_2[self.sel2_1]]
        self.open_betslip_with_selections(selection_ids=select_ids)
        self.place_and_validate_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()
        self.site.wait_content_state('Homepage')
        self.expected_betslip_counter_value = 0

        # Forecast_Tricast_bet_placing
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        expected_selection_name = self.place_forecast_tricast_bet_from_event_details_page(sport_name='horse-racing',
                                                                                          forecast=True)
        self.site.open_betslip()
        self.__class__.sections = self.get_betslip_sections().Singles
        self.assertTrue(self.sections, msg='No stakes found')
        for actual_selection in self.sections:
            self.assertIn(actual_selection.strip(), expected_selection_name,
                          msg=f'Actual selection name: "{actual_selection}" is not in expected selections: '
                              f'"{expected_selection_name}"')
        stake_name, stake = list(self.sections.items())[0]
        self.enter_stake_amount(stake=(stake_name, stake))
        self.__class__.betnow_btn = self.get_betslip_content().bet_now_button
        self.assertTrue(self.betnow_btn.is_enabled(), msg='Bet Now button is disabled')
        self.betnow_btn.click()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()
        self.expected_betslip_counter_value = 0
        self.site.logout()

    def test_013_acca_bar_functionality__applicable_for_mobile_onlyload_coral_siteapp_and_add_one_selection_to_bet_slip_and_check_that_acca_price_price_bar_is_not_displayedx(self):
        """
        DESCRIPTION: Acca Bar Functionality : Applicable for mobile only.
        DESCRIPTION: Load Coral site/app and Add one selection to bet slip and check that Acca Price price bar is not displayedx
        EXPECTED: User is displayed Coral site/app then Selection is added to bet slip, no special feature observed
        """
        if self.device_type == 'mobile':
            self.site.wait_content_state('Homepage')
            self.site.wait_splash_to_hide(1)
            self.selections(1)
            self.assertFalse(self.site.home.acca_price_bar, "Acca Price Bar is displayed")

    def test_014_add_more_selections_to_bet_slip_and_observe_each_time_if_acca_price_price_bar_is_displayed(self):
        """
        DESCRIPTION: Add more selections to bet slip and observe each time if Acca Price price bar is displayed
        EXPECTED: Acca Price price bar is displayed as soon as the second selection is added, and is updated each time a new selection is added
        """
        # Part of this test is covered in step 16
        if self.device_type == 'mobile':
            self.selections(1)
            self.assertTrue(self.site.home.acca_price_bar, "Acca Price Bar not shown")
            # Acca bar should display on pages that have odds
            tabs = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
            if self.brand == 'bma':
                self.assertTrue(tabs.get('FEATURED').is_selected(),
                                msg='FEATURED tab from "{tabs}" is not selected after clicking on it')
            else:
                self.assertTrue(tabs.get('HIGHLIGHTS').is_selected(),
                                msg='HIGHLIGHTS tab from "{tabs}" is not selected after clicking on it')
            for i in range(len(tabs.items())):
                tabs = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
                page, item = list(tabs.items())[i]
                item.click()
                self.assertTrue(self.site.home.acca_price_bar, "Acca Price Bar not shown")
                break
            self.site.wait_splash_to_hide(1)
            self.site.open_betslip()
            self.clear_betslip()
            self.expected_betslip_counter_value = 0
            self.__class__.selection_list = []
            self.__class__.count = 0

    def test_015_navigate_in_site_to_observe_acca_price_bar_displayed(self):
        """
        DESCRIPTION: Navigate in site to observe Acca Price Bar displayed
        EXPECTED: Acca price bar will show during navigation to pages that have odds on them
        """
        # this test is covered in step 14

    def test_016_verify_the_acca_price_price_bar_shows_correct_data_and_updates_accordingly_when_adding_selection(self):
        """
        DESCRIPTION: Verify the Acca Price price bar shows correct data and updates accordingly when adding selection
        EXPECTED: User must see:
        EXPECTED: - bet type: Double, Treble..
        EXPECTED: - number of selections for Acca
        EXPECTED: - updated odds, in fractions by default
        EXPECTED: - potential returns for a £1 stake
        EXPECTED: - for SP - N/A
        """
        if self.device_type == 'mobile':
            self.site.go_to_home_page()
            self.site.wait_splash_to_hide(1)
            self.selections(1)
            self.assertFalse(self.site.home.acca_price_bar, "Acca Price Bar is displayed")

            self.selections(1)
            self.assertTrue(self.site.home.acca_price_bar, "Acca Price Bar not shown")
            bet_type = self.site.home.acca_price_bar_bettype.text
            self.assertEqual(bet_type, vec.betslip.DBL, msg=f'Acca bar bet type "{bet_type}" '
                                                            f'is not the same as expected "{vec.betslip.DBL}"')
            betslip_counter = self.site.header.bet_slip_counter.counter_value
            self.assertEqual(betslip_counter, '2',
                             msg="The 2nd selection is not added to the betslip")
            bet_odds = self.site.home.acca_price_bar_price.text
            self.assertIn('/', bet_odds, msg=f'"{bet_odds}" is not in fraction by default')
            returns_for_stake = str.split(bet_odds, '/')[1]
            self.assertEqual(returns_for_stake, '1', msg=f'Potential return for £1 stake is not "{returns_for_stake}"')

            self.selections(1)
            self.assertTrue(self.site.home.acca_price_bar, "Acca Price Bar not shown")
            self.site.wait_splash_to_hide(1)
            bet_type = self.site.home.acca_price_bar_bettype.text
            self.assertEqual(bet_type, vec.betslip.TBL, msg=f'Acca bar bet type "{bet_type}" '
                                                            f'is not the same as expected "{vec.betslip.TBL}"')
            betslip_counter = self.site.header.bet_slip_counter.counter_value
            self.assertEqual(betslip_counter, '3',
                             msg="The 3rd selection is not added to the betslip")
            bet_odds = self.site.home.acca_price_bar_price.text
            self.assertIn('/', bet_odds, msg=f'"{bet_odds}" is not in fraction by default')
            returns_for_stake = str.split(bet_odds, '/')[1]
            self.assertEqual(returns_for_stake, '1', msg=f'Potential return for £1 stake is not "{returns_for_stake}"')

            self.selections(1)
            self.assertTrue(self.site.home.acca_price_bar, "Acca Price Bar not shown")
            self.site.wait_splash_to_hide(1)
            bet_type = self.site.home.acca_price_bar_bettype.text
            if self.brand == 'bma':
                self.assertEqual(bet_type, vec.betslip.ACC4, msg=f'Acca bar bet type "{bet_type}" '
                                                                 f'is not the same as expected "{vec.betslip.ACC4}"')
            else:
                self.assertEqual(bet_type, vec.bet_history._bet_types_ACC4, msg=f'Acca bar bet type "{bet_type}" '
                                                                                f'is not the same as expected "{vec.bet_history._bet_types_ACC4}"')
            betslip_counter = self.site.header.bet_slip_counter.counter_value
            self.assertEqual(betslip_counter, '4',
                             msg="The 4th selection is not added to the betslip")
            bet_odds = self.site.home.acca_price_bar_price.text
            self.assertIn('/', bet_odds, msg=f'"{bet_odds}" is not in fraction by default')
            returns_for_stake = str.split(bet_odds, '/')[1]
            self.assertEqual(returns_for_stake, '1', msg=f'Potential return for £1 stake is not "{returns_for_stake}"')

    def test_017_verify_the_acca_price_price_bar_shows_correct_data_and_updates_accordingly_when_deleting_selection(self):
        """
        DESCRIPTION: Verify the Acca Price price bar shows correct data and updates accordingly when deleting selection
        EXPECTED: User must see:
        EXPECTED: - bet type: Double, Treble..
        EXPECTED: - number of selections in brackets for Acca
        EXPECTED: - updated odds, in fractions by default
        EXPECTED: - potential returns for a £1 stake
        EXPECTED: - for SP - N/A
        """
        if self.device_type == 'mobile':
            self.site.contents.scroll_to_we(self.__class__.selection_list[3])
            self.site.wait_splash_to_hide(1)
            self.__class__.selection_list[3].click()
            sleep(2)
            self.assertTrue(self.site.home.acca_price_bar, "Acca Price Bar not shown")
            bet_type = self.site.home.acca_price_bar_bettype.text
            self.assertEqual(bet_type, vec.betslip.TBL, msg=f'Acca bar bet type "{bet_type}" '
                                                            f'is not the same as expected "{vec.betslip.TBL}"')
            betslip_counter = self.site.header.bet_slip_counter.counter_value
            self.assertEqual(betslip_counter, '3',
                             msg="The 3rd selection is not added to the betslip")
            bet_odds = self.site.home.acca_price_bar_price.text
            self.assertIn('/', bet_odds, msg=f'"{bet_odds}" is not in fraction by default')
            returns_for_stake = str.split(bet_odds, '/')[1]
            self.assertEqual(returns_for_stake, '1', msg=f'Potential return for £1 stake is not "{returns_for_stake}"')

            self.site.contents.scroll_to_we(self.__class__.selection_list[2])
            self.__class__.selection_list[2].click()
            sleep(2)
            self.assertTrue(self.site.home.acca_price_bar, "Acca Price Bar not shown")
            bet_type = self.site.home.acca_price_bar_bettype.text
            self.assertEqual(bet_type, vec.betslip.DBL, msg=f'Acca bar bet type "{bet_type}" '
                                                            f'is not the same as expected "{vec.betslip.DBL}"')
            betslip_counter = self.site.header.bet_slip_counter.counter_value
            self.assertEqual(betslip_counter, '2',
                             msg="The 2nd selection is not added to the betslip")
            bet_odds = self.site.home.acca_price_bar_price.text
            self.assertIn('/', bet_odds, msg=f'"{bet_odds}" is not in fraction by default')
            returns_for_stake = str.split(bet_odds, '/')[1]
            self.assertEqual(returns_for_stake, '1', msg=f'Potential return for £1 stake is not "{returns_for_stake}"')

            self.site.contents.scroll_to_we(self.__class__.selection_list[1])
            self.__class__.selection_list[1].click()
            sleep(2)
            self.assertFalse(self.site.home.acca_price_bar, "Acca Price Bar is displayed")
