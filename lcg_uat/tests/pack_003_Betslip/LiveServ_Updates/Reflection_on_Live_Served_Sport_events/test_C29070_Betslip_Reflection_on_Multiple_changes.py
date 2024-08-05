import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # can't change event state for prod/hl env
# @pytest.mark.hl
@pytest.mark.prod_incident
@pytest.mark.betslip
@pytest.mark.liveserv_updates
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.slow
@pytest.mark.login
@vtest
class Test_C29070_Betslip_Reflection_on_Multiple_changes(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C29070
    NAME: Betslip Reflection on Multiple changes
    """
    keep_browser_open = True
    new_price_home_1 = '7/1'
    new_price_home_2 = '15/1'
    default_price_home = None
    outcome_id1 = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.team1, self.__class__.outcome_id1 = event_params.team1, event_params.selection_ids[
            event_params.team1]
        self.__class__.eventID_1 = event_params.event_id

        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.team2, self.__class__.outcome_id2 = event_params.team1, event_params.selection_ids[
            event_params.team1]
        self.__class__.eventID_2 = event_params.event_id

        self.__class__.event_ids = [self.eventID_1]
        self.__class__.event_teams = [self.team1]
        self.__class__.outcome_ids = [self.outcome_id1]

        self.__class__.stakes = []

        self.__class__.default_price_home = self.ob_config.event.prices['odds_home']

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        self.site.wait_content_state('HomePage')

    def test_002_add_to_the_betslip_one_sport_selection(self):
        """
        DESCRIPTION: Add to the betslip one <Sport> selection
        EXPECTED: Betslip counter is increased
        """
        self.open_betslip_with_selections(selection_ids=self.outcome_ids)

        singles_section = self.get_betslip_sections().Singles

        self.__class__.stakes.clear()

        for team in self.event_teams:
            stake = singles_section.get(team)
            self.assertTrue(stake, msg=f'"{team}" stake is not displayed')
            self.__class__.stakes.append(stake)

    def test_003_change_price_for_event(self):
        """
        DESCRIPTION: Change output price of Home selection (increase price)
        """
        for outcome_id in self.outcome_ids:
            self.ob_config.change_price(selection_id=outcome_id, price=self.new_price_home_1)

    def test_004_verify_error_message_odds_indicator_and_bet_now_button(self,
                                                                        old_price=default_price_home,
                                                                        new_price=new_price_home_1):
        """
        DESCRIPTION: Verify Error message, Odds indicator and 'Bet now' button
        EXPECTED: The selection price change is displayed via push
        EXPECTED: (Price change from x to y - need to ensure we do not show x to x where price changes quickly away and then back to original price)
        EXPECTED: Info message is displayed at the bottom of the betslip: 'Some of the prices have changed!'
        EXPECTED: 'Log In & Bet' button is disabled
        EXPECTED: **Ladbrokes**:
        EXPECTED: Info message is displayed at the top of the betslip with animations - this is removed after 5 seconds: 'Some of the prices have changed'
        """
        if not old_price:
            old_price = self.default_price_home

        for outcome_id in self.outcome_ids:
            price_update = self.wait_for_price_update_from_live_serv(selection_id=outcome_id)
            self.assertTrue(price_update,
                            msg=f'Price update for selection with id "{outcome_id}" is not received')

        expected_message = vec.betslip.STAKE_PRICE_CHANGE_MSG.format(old=old_price, new=new_price)
        for stake in self.stakes:
            result = stake.wait_for_message_to_change(expected_message=expected_message, timeout=10)
            self.assertTrue(result, msg=f'Expected error message "{expected_message}" did not arrive')
            current_price = stake.odds
            self.assertEqual(current_price, new_price,
                             msg=f'Current stake price "{current_price}" != expected "{new_price}"')

        betnow_section_error = self.get_betslip_content().wait_for_warning_message()
        self.assertEqual(betnow_section_error, vec.betslip.PRICE_CHANGE_BANNER_MSG,
                         msg=f'Error message "{betnow_section_error}" != expected "{vec.betslip.PRICE_CHANGE_BANNER_MSG}"')

        self.assertFalse(self.get_betslip_content().bet_now_button.is_enabled(expected_result=False),
                         msg=f'"{vec.betslip.LOGIN_AND_BET_BUTTON_CAPTION}" button is not disabled')

    def test_005_change_price_for_event(self):
        """
        DESCRIPTION: Change output price of Home selection (increase price)
        """
        for outcome_id in self.outcome_ids:
            self.ob_config.change_price(selection_id=outcome_id, price=self.new_price_home_2)

    def test_006_verify_error_message_odds_indicator_and_bet_now_button(self):
        """
        DESCRIPTION: Verify Error message, Odds indicator and 'Bet now' button
        EXPECTED: The selection price change is displayed via push
        EXPECTED: (Price change from x to y - need to ensure we do not show x to x where price changes quickly away and then back to original price)
        EXPECTED: Info message is displayed at the bottom of the betslip: 'Some of the prices have changed!'
        EXPECTED: 'Log In & Bet' button is disabled
        EXPECTED: **Ladbrokes**:
        EXPECTED: Info message is displayed at the top of the betslip with animations - this is removed after 5 seconds: 'Some of the prices have changed'
        """
        self.test_004_verify_error_message_odds_indicator_and_bet_now_button(old_price=self.new_price_home_1,
                                                                             new_price=self.new_price_home_2)

    def test_007_suspend_event(self):
        """
        DESCRIPTION: Trigger the following situation for same event:
        DESCRIPTION: **eventStatusCode="S"**
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: Event becomes suspended
        """
        for event_id in self.event_ids:
            self.ob_config.change_event_state(event_id=event_id, displayed=True, active=False)

    def test_008_verify_error_message_and_odds_indicator_for_bet(self):
        """
        DESCRIPTION: Verify Error message and Odds indicator for Bet
        EXPECTED: **Coral:**
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection'
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: **Ladbrokes:**
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection'
        EXPECTED: * 'Place Bet' ( 'Login and Place Bet') button is disabled and greyed out
        EXPECTED: *  Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'One of your selections have been suspended' with duration: 5s
        """
        self.verify_betslip_is_suspended(stakes=self.stakes, verify_overlay_message=False)

    def test_009_change_price_for_event(self):
        """
        DESCRIPTION: Change output price of Home selection (increase price)
        """
        for outcome_id in self.outcome_ids:
            self.ob_config.change_price(selection_id=outcome_id, price=self.new_price_home_2)

    def test_010_verify_error_message_odds_indicator_and_bet_now_button(self):
        """
        DESCRIPTION: Verify Error message, Odds indicator and 'Bet now' button
        EXPECTED: 1. *NO* Message: 'Price changed from FROM to NEW'
        EXPECTED: 2. Coral: Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: Ladbrokes: Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: 3. 'SUSPENDED' label is sown at the center of selection'
        EXPECTED: 4. 'Login & Place Bet' (Coral) 'Login and Place Bet' (Ladbrokes) button is disabled
        """
        for outcome_id in self.outcome_ids:
            price_update = self.wait_for_price_update_from_live_serv(selection_id=outcome_id)
            self.assertTrue(price_update,
                            msg=f'Price update for selection with id "{outcome_id}" is not received')

        self.verify_betslip_is_suspended(stakes=self.stakes, verify_overlay_message=False)

    def test_011_change_price_for_event_and_make_event_active_again(self):
        """
        DESCRIPTION: Trigger the following situation for this suspended event:
        DESCRIPTION: **eventStatusCode="A"**
        DESCRIPTION: **change priceNum and priceDen**
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: * Selection becomes enable
        EXPECTED: * Price Odds is changed
        EXPECTED: * Animation is visible (color changes) (**N/A for OX 99)
        """
        for event_id in self.event_ids:
            self.ob_config.change_event_state(event_id=event_id, displayed=True, active=True)
        for outcome_id in self.outcome_ids:
            self.ob_config.change_price(selection_id=outcome_id, price=self.new_price_home_1)

        for stake in self.stakes:
            self.assertFalse(stake.is_suspended(expected_result=False, timeout=30), msg=f'Stake is suspended')

    def test_012_verify_error_message_odds_indicator_and_bet_now_button(self):
        """
        DESCRIPTION: Verify Error message, Odds indicator and 'Bet now' button
        EXPECTED: The selection price change is displayed via push
        EXPECTED: (Price change from x to y - need to ensure we do not show x to x where price changes quickly away and then back to original price)
        EXPECTED: Info message is displayed at the bottom of the betslip: 'Some of the prices have changed!'
        EXPECTED: 'Log In & Bet' button is disabled
        EXPECTED: **Ladbrokes**:
        EXPECTED: Info message is displayed at the top of the betslip with animations - this is removed after 5 seconds: 'Some of the prices have changed'
        """
        self.test_004_verify_error_message_odds_indicator_and_bet_now_button(old_price=self.new_price_home_2,
                                                                             new_price=self.new_price_home_1)

    def test_013_repeat_steps_2_12_but_add_few_sport_selections_to_the_betslip(self):
        """
        DESCRIPTION: Repeat steps 2-12 but add few <Sport> selections to the betslip
        EXPECTED: *   'Multiples' section is shown in the bet slip
        EXPECTED: *   Price change affects 'Multiples' (Double with 1 bet or a Multiple in 'Place your ACCA' section): Odds from each Single selections are multiplied and new Odds value is displayed. Old Odds are crossed out in black color and New Odds are displayed to the right of Old Odds :
        EXPECTED: - in Red color  with Red colored Down direct arrows if Odds decreased
        EXPECTED: - in Green color with Green colored Up direct arrows if Odds increased
        EXPECTED: should be displayed correct values to reflect the changes
        EXPECTED: * If Stake value is entered for a Multiple with available Odds, new 'Estimated Returns' value is shown for a Multiple
        """
        # make multiple events
        self.__class__.event_ids = [self.eventID_1, self.eventID_2]
        self.__class__.event_teams = [self.team1, self.team2]
        self.__class__.outcome_ids = [self.outcome_id1, self.outcome_id2]

        self.clear_betslip()

        # cleaning before multiple
        for outcome_id in self.outcome_ids:
            self.ob_config.change_price(selection_id=outcome_id, price=self.default_price_home)

        self.test_002_add_to_the_betslip_one_sport_selection()
        self.test_003_change_price_for_event()
        self.test_004_verify_error_message_odds_indicator_and_bet_now_button()
        self.test_005_change_price_for_event()
        self.test_006_verify_error_message_odds_indicator_and_bet_now_button()
        self.test_007_suspend_event()
        self.test_008_verify_error_message_and_odds_indicator_for_bet()
        self.test_009_change_price_for_event()
        self.test_010_verify_error_message_odds_indicator_and_bet_now_button()
        self.test_011_change_price_for_event_and_make_event_active_again()
        self.test_012_verify_error_message_odds_indicator_and_bet_now_button()

    def test_014_login_with_user_account_with_positive_balance(self):
        """
        DESCRIPTION: Login with user account with positive balance
        EXPECTED: User is logged in
        """
        self.clear_betslip()

        # cleaning before logged in user
        for outcome_id in self.outcome_ids:
            self.ob_config.change_price(selection_id=outcome_id, price=self.default_price_home)

        # make single event
        self.__class__.event_ids = [self.eventID_1]
        self.__class__.event_teams = [self.team1]
        self.__class__.outcome_ids = [self.outcome_id1]

        self.site.login(async_close_dialogs=False)

    def test_015_repeat_steps_2_13_for_logged_in_user(self):
        """
        DESCRIPTION: Repeat steps 2-13 for Logged In User
        """
        self.test_002_add_to_the_betslip_one_sport_selection()
        self.test_003_change_price_for_event()
        self.test_004_verify_error_message_odds_indicator_and_bet_now_button()
        self.test_005_change_price_for_event()
        self.test_006_verify_error_message_odds_indicator_and_bet_now_button()
        self.test_007_suspend_event()
        self.test_008_verify_error_message_and_odds_indicator_for_bet()
        self.test_009_change_price_for_event()
        self.test_010_verify_error_message_odds_indicator_and_bet_now_button()
        self.test_011_change_price_for_event_and_make_event_active_again()
        self.test_012_verify_error_message_odds_indicator_and_bet_now_button()
        self.test_013_repeat_steps_2_12_but_add_few_sport_selections_to_the_betslip()
