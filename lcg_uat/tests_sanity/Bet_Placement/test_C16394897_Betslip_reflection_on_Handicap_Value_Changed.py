import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.waiters import wait_for_result
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Events cannot be created on prod & beta
# @pytest.mark.hl
@pytest.mark.betslip
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.sanity
@vtest
class Test_C16394897_Betslip_reflection_on_Handicap_Value_Changed(BaseCashOutTest):
    """
    TR_ID: C16394897
    NAME: Betslip reflection on Handicap Value Changed
    DESCRIPTION: This test case verifies Betslip reflection on <Sport> Handicap value Changed
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: <Sport> Event should be LiveServed:
    PRECONDITIONS: Event should be **Live (isStarted=true)**
    PRECONDITIONS: Event should be **in-Pla**y:
    PRECONDITIONS: drilldown****TagNames=EVFLAG_BL
    PRECONDITIONS: isMarketBetInRun=true
    PRECONDITIONS: rawIsOffCode="Y "or isStarted=true, rawIsOffCode="-"
    PRECONDITIONS: Event, Market, Outcome should be **Active** (**eventStatusCode="A", ****marketStatusCode="A", ****outcomeStatusCode="A"****)**
    """
    keep_browser_open = True
    new_handicap_value = '+22.0'

    def test_000_pre_conditions(self):
        event = self.ob_config.add_autotest_premier_league_football_event(markets=[('handicap_match_result', {'cashout': True})], is_live=True)
        self.__class__.eventID = event.event_id

    def test_001_login_into_the_applicationadd_selection_that_contains_handicap_value_to_betslipnavigate_to_betslip(
            self, number_of_selection=1):
        """
        DESCRIPTION: Login into the application
        DESCRIPTION: Add selection that contains Handicap value to Betslip
        DESCRIPTION: Navigate to Betslip
        EXPECTED: Betslip counter is increased
        EXPECTED: Selection is added
        """
        if number_of_selection == 1:
            self.navigate_to_page('Homepage')
            self.site.wait_splash_to_hide(timeout=60)
            self.site.login(username=tests.settings.betplacement_user)

        self.navigate_to_edp(event_id=self.eventID, sport_name='football')
        self.site.wait_content_state(state_name='EventDetails', timeout=60)

        if number_of_selection == 2:
            self.device.refresh_page()
            result = wait_for_result(lambda: self.site.sport_event_details.tab_content.accordions_list.is_displayed(timeout=10) is True,
                                     timeout=60)
            self.assertTrue(result, msg='Sport landing page is not loaded completely')

        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        handicap = markets_list.get(self.expected_market_sections.handicap_results)
        self.assertTrue(handicap, msg='*** Can not find Handicap market section')

        outcome_groups = handicap.outcomes.items_as_ordered_dict
        self.assertTrue(outcome_groups, msg='Outcome groups is empty')

        selection = 1
        for outcome_group_name, outcome_group in list(outcome_groups.items()):
            self.outcomes = outcome_group
            handicap_sigh, handicap_value = outcome_group_name[:1], outcome_group_name[1:]
            if selection == 1:
                self.__class__.old_handicap_value_selection_1 = '%s%s' % (
                    handicap_sigh, '%.1f' % (float(handicap_value)))
                if number_of_selection == 1:
                    self.__class__.market_id_selection_1 = self.ob_config.market_ids[self.eventID][
                        f'handicap_match_result {self.old_handicap_value_selection_1}']
            elif selection == 2:
                self.__class__.old_handicap_value_selection_2 = '%s%s' % (
                    handicap_sigh, '%.1f' % (float(handicap_value)))
                self.__class__.market_id_selection_2 = self.ob_config.market_ids[self.eventID][
                    f'handicap_match_result {self.old_handicap_value_selection_2}']
                self.assertTrue(self.outcomes, msg='No one outcome was found in section: "%s"' % outcome_group_name)
            list(self.outcomes.items)[0].click()
            sleep(20)

            if self.device_type == 'mobile' and selection == 1:
                self.site.quick_bet_panel.header.close_button.click()
                self.site.wait_quick_bet_overlay_to_hide()
                self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick bet not closed')
                result = wait_for_result(
                    lambda: self.site.sport_event_details.tab_content.accordions_list.is_displayed(timeout=10) is True,
                    timeout=60)
                self.site.wait_content_state(state_name='EventDetails')
                result = wait_for_result(lambda: self.site.header.bet_slip_counter.is_displayed(timeout=10) is True,
                                         timeout=60)
                self.assertTrue(result, msg='Event Details page is not loaded completely')

            if selection == 2:
                break
            selection += 1

            if number_of_selection == 1:
                break

        if self.device_type == 'mobile':
            self.site.header.bet_slip_counter.click()
            self.assertTrue(self.site.has_betslip_opened(expected_result=True), msg='Betslip is not opened')

        if selection == 1:
            self.verify_betslip_counter_change(expected_value=1)

    def test_002_trigger_the_following_situation_for_this_eventchange_rawhandicapvalue_on_market_leveland_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(
            self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: change** rawHandicapValue **on market level
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: Handicap value is changed
        """
        self.__class__.market_template_id = list(self.ob_config.football_config.autotest_class.autotest_premier_league.markets.handicap_match_result.values())[0]
        self.ob_config.change_handicap_market_value(event_id=self.eventID, market_id=self.market_id_selection_1,
                                                    market_template_id=self.market_template_id,
                                                    new_handicap_value=self.new_handicap_value)

    def test_003_verify_changes_in_betslip(self, number_of_selection=1):
        """
        DESCRIPTION: Verify changes in Betslip
        EXPECTED: **Before OX 99**
        EXPECTED: 1. Error message: 'Handicap value changed from FROM to NEW' should be displayed on red background below the corresponding selection
        EXPECTED: 2. Handicap value should be updated to reflect the changed value
        EXPECTED: **After OX 99**
        EXPECTED: - Notification message is displayed above selection: "Handicap changed from x to x"
        EXPECTED: - The Place bet button text is updated to:
        EXPECTED: Ladbrokes: 'ACCEPT AND PLACE BET'
        EXPECTED: Coral: 'ACCEPT & PLACE BET'
        """
        result = wait_for_result(lambda: self.site.betslip.bet_now_button.name.__contains__(vec.betslip.ACCEPT_BET) is True, timeout=30)
        self.assertTrue(result, msg='Bet Button name is not changed to Accept and Place Bet')

        bet_button_now = self.site.betslip.bet_now_button.name

        if self.brand == 'bma':
            self.assertEquals(vec.betslip.ACCEPT_BET, bet_button_now,
                              msg=f'Button text is "{bet_button_now}" not match with text "{vec.betslip.ACCEPT_BET}"')
        else:
            self.assertEquals(vec.betslip.ACCEPT_BET, bet_button_now,
                              msg=f'Button text is "{bet_button_now}" not match with text "{vec.betslip.ACCEPT_BET}"')

        if number_of_selection == 1:
            expected_handicap_message = vec.quickbet.HANDICAP_CHANGED_VALUE.format(
                old=self.old_handicap_value_selection_1, new=self.new_handicap_value)

            singles_sections = self.get_betslip_sections().Singles
            actual_handicap_message = list(singles_sections.values())[0].error_message
            self.assertEqual(expected_handicap_message, actual_handicap_message,
                             msg=f'Actual handicap value is "{actual_handicap_message}" not match with expected handicap value "{expected_handicap_message}"')

    def test_004_enter_value_in_stake_field_for_bet_and_tap_place_bet_button(self):
        """
        DESCRIPTION: Enter value in 'Stake' field for bet and tap 'Place Bet' button
        EXPECTED: *   Bet is placed successfully
        EXPECTED: *   Bet Receipt is present
        """
        self.place_and_validate_single_bet()
        self.site.is_bet_receipt_displayed(expected_result=True)

    def test_005_repeat_steps_2_4_but_make_few_selections(self):
        """
        DESCRIPTION: Repeat steps #2-4 but make few selections
        EXPECTED: **Before OX 99**
        EXPECTED: 1. Error message: 'Handicap value changed from FROM to NEW' should be displayed on red background for all bets
        EXPECTED: 2. Handicap value should be updated to reflect the changed value
        EXPECTED: 3. 'Bet Now' button should remain active
        EXPECTED: **After OX 99**
        EXPECTED: - Notification message is displayed above the selection: "Handicap changed from x to x"
        EXPECTED: - The Place bet button text is updated to:
        EXPECTED: Ladbrokes: 'ACCEPT AND PLACE BET'
        EXPECTED: Coral: 'ACCEPT & PLACE BET'
        """
        new_handicap_value = '+23.0'
        sleep(30)
        # Adding selection
        self.test_001_login_into_the_applicationadd_selection_that_contains_handicap_value_to_betslipnavigate_to_betslip(
            number_of_selection=2)

        self.ob_config.change_handicap_market_value(event_id=self.eventID, market_id=self.market_id_selection_1,
                                                    market_template_id=self.market_template_id,
                                                    new_handicap_value=new_handicap_value)

        self.ob_config.change_handicap_market_value(event_id=self.eventID, market_id=self.market_id_selection_2,
                                                    market_template_id=self.market_template_id,
                                                    new_handicap_value=new_handicap_value)
        sleep(30)
        # verifying button text
        self.test_003_verify_changes_in_betslip(number_of_selection=2)

        expected_handicap_message_1 = vec.quickbet.HANDICAP_CHANGED_VALUE.format(old=self.old_handicap_value_selection_1, new=new_handicap_value)
        expected_handicap_message_2 = vec.quickbet.HANDICAP_CHANGED_VALUE.format(old=self.old_handicap_value_selection_2, new=new_handicap_value)

        singles_sections = self.get_betslip_sections().Singles
        actual_handicap_message_first = list(singles_sections.values())[0].error_message
        actual_handicap_message_second = list(singles_sections.values())[1].error_message

        self.assertEqual(expected_handicap_message_1, actual_handicap_message_first,
                         msg=f'Actual handicap value is "{actual_handicap_message_first}" not match with expected handicap value "{expected_handicap_message_1}"')
        self.assertEqual(expected_handicap_message_2, actual_handicap_message_second,
                         msg=f'Actual handicap value is "{actual_handicap_message_second}" not match with expected handicap value "{expected_handicap_message_2}"')
        # Placing bet
        self.test_004_enter_value_in_stake_field_for_bet_and_tap_place_bet_button()
