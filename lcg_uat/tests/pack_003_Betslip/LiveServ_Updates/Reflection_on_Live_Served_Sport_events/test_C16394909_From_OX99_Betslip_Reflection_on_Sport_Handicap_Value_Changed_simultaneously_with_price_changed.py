import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from time import sleep
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.betslip
# @pytest.mark.prod #can not create OB event in PROD
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.betslip
@vtest
class Test_C16394909_From_OX99_Betslip_Reflection_on_Sport_Handicap_Value_Changed_simultaneously_with_price_changed(BaseCashOutTest):
    """
    TR_ID: C16394909
    NAME: [From OX99] Betslip Reflection on <Sport> Handicap Value Changed simultaneously with price changed
    DESCRIPTION: his test case verifies Betslip reflection on <Sport> Handicap value Changed simultaneously with price changed
    PRECONDITIONS: To get SiteServer info about event use the following url
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: <Sport> Event should be LiveServed:
    PRECONDITIONS: Event should be LIVE ( isStarted=true )
    PRECONDITIONS: Event should be IN-PLAY:
    PRECONDITIONS: drilldown TagNames=EVFLAG_BL
    PRECONDITIONS: isMarketBetInRun=true
    PRECONDITIONS: rawIsOffCode="Y "or isStarted=true, rawIsOffCode="-"
    PRECONDITIONS: Event, Market, Outcome should be:
    PRECONDITIONS: Active ( eventStatusCode="A", marketStatusCode="A", outcomeStatusCode="A" )
    PRECONDITIONS: Odds format is Fractional
    PRECONDITIONS: NOTE: contact UAT team for all configurations
    PRECONDITIONS: This test case is applied for **Mobile** and **Tablet** application.
    """
    keep_browser_open = True
    new_handicap_value = '+22.0'

    def test_000_pre_conditions(self):
        event = self.ob_config.add_autotest_premier_league_football_event(markets=[('handicap_match_result', {'cashout': True})], is_live=True)
        self.__class__.eventID = event.event_id

    def test_001_login_into_oxygen_applicationadd_selection_that_contains_handicap_value_to_betslipnavigate_to_betslip(self, number_of_selection=1):
        """
        DESCRIPTION: Login into Oxygen application
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
            elif selection == 3:
                self.__class__.old_handicap_value_selection_3 = '%s%s' % (
                    handicap_sigh, '%.1f' % (float(handicap_value)))
                self.__class__.market_id_selection_3 = self.ob_config.market_ids[self.eventID][
                    f'handicap_match_result {self.old_handicap_value_selection_3}']
                self.assertTrue(self.outcomes, msg='No one outcome was found in section: "%s"' % outcome_group_name)

            list(self.outcomes.items)[0].click()
            self.site.wait_content_state_changed(timeout=20)

            if self.device_type == 'mobile' and selection == 1:
                self.site.quick_bet_panel.header.close_button.click()
                self.site.wait_quick_bet_overlay_to_hide()
                self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick bet not closed')
                result = wait_for_result(
                    lambda: self.site.sport_event_details.tab_content.accordions_list.is_displayed(timeout=10) is True,
                    timeout=60)
                self.assertTrue(result, msg='Sport landing page is not loaded completely')
                self.site.wait_content_state(state_name='EventDetails')
                result = wait_for_result(lambda: self.site.header.bet_slip_counter.is_displayed(timeout=10) is True,
                                         timeout=60)
                self.assertTrue(result, msg='Event Details page is not loaded completely')

            if selection == 3:
                break
            selection += 1

            if number_of_selection == 1:
                break

        if self.device_type == 'mobile':
            self.site.header.bet_slip_counter.click()
            self.assertTrue(self.site.has_betslip_opened(expected_result=True), msg='Betslip is not opened')

        if selection == 1:
            self.verify_betslip_counter_change(expected_value=1)

    def test_002_trigger_the_following_situation_for_this_eventchange_on_market_level_handicapvalue_and_price_for_added_selection_and_save_changesand_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self, number_of_selection=1):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: change on market level: HandicapValue and price for added selection and save changes
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: - Notification message is displayed above selection: "Handicap changed from x to x"
        EXPECTED: - info message is displayed at the bottom of the betslip: 'Some of the prices have changed!'
        EXPECTED: - Only Ladbrokes: info message is displayed at the top of the betslip with animations - this is removed after 5 seconds: 'Some of the prices have changed'
        EXPECTED: - Place bet button text is updated to:
        EXPECTED: Ladbrokes: 'ACCEPT AND PLACE BET'
        EXPECTED: Coral: 'ACCEPT & PLACE BET'
        """
        self.__class__.market_template_id = list(self.ob_config.football_config.autotest_class.autotest_premier_league.markets.handicap_match_result.values())[0]
        self.ob_config.change_handicap_market_value(event_id=self.eventID, market_id=self.market_id_selection_1,
                                                    market_template_id=self.market_template_id,
                                                    new_handicap_value=self.new_handicap_value)

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

    def test_003_provide_same_verification_but_add_few_selections_to_betslip(self):
        """
        DESCRIPTION: Provide same verification but add few selections to Betslip
        EXPECTED: Results are the same
        """
        self.place_and_validate_single_bet()
        self.site.is_bet_receipt_displayed(expected_result=True)

        new_handicap_value = '+23.0'
        sleep(10)
        # used sleep due to ob changes is taking to reflect on UI
        # Adding selection
        self.test_001_login_into_oxygen_applicationadd_selection_that_contains_handicap_value_to_betslipnavigate_to_betslip(
            number_of_selection=2)

        self.ob_config.change_handicap_market_value(event_id=self.eventID, market_id=self.market_id_selection_2,
                                                    market_template_id=self.market_template_id,
                                                    new_handicap_value=new_handicap_value)

        self.ob_config.change_handicap_market_value(event_id=self.eventID, market_id=self.market_id_selection_3,
                                                    market_template_id=self.market_template_id,
                                                    new_handicap_value=new_handicap_value)
        sleep(10)
        # verifying button text
        self.test_002_trigger_the_following_situation_for_this_eventchange_on_market_level_handicapvalue_and_price_for_added_selection_and_save_changesand_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(
            number_of_selection=2)

        expected_handicap_message_1 = vec.quickbet.HANDICAP_CHANGED_VALUE.format(old=self.old_handicap_value_selection_2, new=new_handicap_value)
        expected_handicap_message_2 = vec.quickbet.HANDICAP_CHANGED_VALUE.format(old=self.old_handicap_value_selection_3, new=new_handicap_value)

        singles_sections = self.get_betslip_sections().Singles
        actual_handicap_message_first = list(singles_sections.values())[1].error_message
        actual_handicap_message_second = list(singles_sections.values())[2].error_message

        self.assertEqual(actual_handicap_message_first, expected_handicap_message_1,
                         msg=f'Actual handicap value is "{actual_handicap_message_first}" not match with expected handicap value "{expected_handicap_message_1}"')
        self.assertEqual(actual_handicap_message_second, expected_handicap_message_2,
                         msg=f'Actual handicap value is "{actual_handicap_message_second}" not match with expected handicap value "{expected_handicap_message_2}"')
        # Placing bet
        self.place_and_validate_single_bet()
        self.site.is_bet_receipt_displayed(expected_result=True)
