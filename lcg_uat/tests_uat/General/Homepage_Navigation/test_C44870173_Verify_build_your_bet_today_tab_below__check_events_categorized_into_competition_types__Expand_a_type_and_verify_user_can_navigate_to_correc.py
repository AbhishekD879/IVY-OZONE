import pytest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from voltron.environments import constants as vec
from tests.base_test import vtest
from time import sleep
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import normalize_name


@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870173_Verify_build_your_bet_today_tab_below__check_events_categorized_into_competition_types__Expand_a_type_and_verify_user_can_navigate_to_correct_EDP__Not_Applicable_for_Roxanne(BaseBetSlipTest, BaseBanachTest):
    """
    TR_ID: C44870173
    NAME: "Verify  'build your bet' today tab below, - check events categorized into competition types. - Expand a type and verify user can navigate to correct EDP " .. Not Applicable for Roxanne
    DESCRIPTION: "Verify  'build your bet' today tab below,
    DESCRIPTION: - check events categorized into competition types.
    DESCRIPTION: - Expand a type and verify user can navigate to correct EDP
    """
    keep_browser_open = True
    market = {0: 'MATCH BETTING', 1: 'BOTH TEAMS TO SCORE'}
    proxy = None
    bet_amount = 0.1

    def clicking_an_event_and_placing_bet_under_byb(self, eventID):

        if self.device_type == 'mobile':
            self.site.home.module_selection_ribbon.tab_menu.click_button(vec.siteserve.EXPECTED_MARKET_TABS.build_your_bet)
            self.assertEqual(self.site.home.module_selection_ribbon.tab_menu.current, vec.siteserve.EXPECTED_MARKET_TABS.build_your_bet,
                             msg='"Build Your Bet/Bet Builder" tab is not selected')
            byb_events = list(self.site.home.tab_content.accordions_list.items_as_ordered_dict.values())[0]
            event = list(byb_events.items_as_ordered_dict.values())[0]
            event.go_to_event_link.click()
            sleep(5)
        event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=eventID, query_builder=self.ss_query_builder)
        event_start_time = event_details[0]['event']['startTime']
        self.__class__.event_start_time_local = self.convert_time_to_local(
            date_time_str=event_start_time,
            ob_format_pattern=self.ob_format_pattern,
            future_datetime_format=self.event_card_future_time_format_pattern,
            ss_data=True)

        self.__class__.event_name = normalize_name(event_details[0]['event']['name'])

        self.navigate_to_edp(event_id=eventID)
        self.assertTrue(
            self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet),
            msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')

    def test_001_httpsbeta_sportscoralcouk(self):
        """
        DESCRIPTION: https://beta-sports.coral.co.uk/
        EXPECTED: User is logged in and on the Homepage
        """
        self.site.login()
        self.__class__.eventID_1 = self.get_ob_event_with_byb_market()
        self.__class__.eventID_2 = self.get_ob_event_with_byb_market()

    def test_002_select_build_your_bet_from_module_ribbon_tab(self):
        """
        DESCRIPTION: Select 'Build your bet' from Module Ribbon Tab
        EXPECTED: User is on the Build Your Bet tab within a football event detail page
        """
        # covered in test_003

    def test_003_add_any_selections_from_the_events(self):
        """
        DESCRIPTION: Add any selections from the events
        EXPECTED: Selections (Game Market or Player Bet) are added to the Build Your Bet dashboard
        """
        self.clicking_an_event_and_placing_bet_under_byb(eventID=self.eventID_1)

    def test_004_verify_if_the_user_is_able_to_add_and_delete_selections(self):
        """
        DESCRIPTION: Verify if the user is able to add and delete selections.
        EXPECTED: User can add and delete selections.
        """
        # covered in test_003

    def test_005_verify_if_the_user_is_able_to_place_bet_with_appropriate_selections(self):
        """
        DESCRIPTION: Verify if the user is able to place bet with appropriate selections
        EXPECTED: Bet placement successful.
        """
        # Match betting selection
        match_betting = self.get_market(market_name=self.expected_market_sections.match_betting)
        self.assertTrue(match_betting, msg=f'"{self.expected_market_sections.match_betting}" market does not exist')
        match_betting_selection_name = match_betting.set_market_selection(selection_index=1)
        match_betting.set_market_selection(selection_index=1, time=True)
        self.assertTrue(match_betting_selection_name, msg='Match betting selection is not added to Dashboard')
        match_betting.add_to_betslip_button.click()
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            self.initial_counter)
        self.__class__.initial_counter += 1

        # Both Teams To Score selection
        both_teams_to_score_market = self.get_market(market_name=self.expected_market_sections.both_teams_to_score)
        self.assertTrue(both_teams_to_score_market,
                        msg=f'"{self.expected_market_sections.both_teams_to_score}" market does not exist')
        both_teams_to_score_names = both_teams_to_score_market.set_market_selection(selection_index=1, time=True)
        self.assertTrue(both_teams_to_score_names, msg='No one selection added to Dashboard')
        both_teams_to_score_market.add_to_betslip_button.click()

        self.__class__.initial_counter += 1
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            self.initial_counter)

        if self.site.sport_event_details.tab_content.dashboard_panel.has_price_not_available_message():
            self.assertFalse(
                self.site.sport_event_details.tab_content.dashboard_panel.price_not_available_message.is_displayed(
                    expected_result=False),
                msg=f'Message: "{vec.yourcall.PRICE_NOT_AVAILABLE}" displayed')

        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.place_bet.click()

        self.assertTrue(self.site.wait_for_byb_betslip_panel(), msg='BYB Betslip has not appeared')
        byb_betslip_panel = self.site.byb_betslip_panel
        self.assertTrue(byb_betslip_panel, msg='BYB BetSlip is not shown')
        byb_betslip_panel.selection.content.amount_form.enter_amount(value=self.bet_amount)
        try:
            byb_betslip_panel.place_bet.click()
            self.assertTrue(self.site.wait_for_byb_bet_receipt_panel(timeout=25),
                            msg='Build Your Bet Receipt is not displayed')
        except VoltronException:
            byb_betslip_panel.place_bet.click()
            self.assertTrue(self.site.wait_for_byb_bet_receipt_panel(timeout=25),
                            msg='Build Your Bet Receipt is not displayed')

        self.assertTrue(self.site.wait_for_byb_bet_receipt_panel(timeout=15),
                        msg='Build Your Bet Bet Receipt NOT displayed')

        self.site.byb_bet_receipt_panel.header.close_button.click()
        self.assertFalse(self.site.wait_for_byb_bet_receipt_panel(expected_result=False),
                         msg='Build Your Bet Bet Receipt still displayed')

    def test_006_repeat_steps_by_selecting_several_byb_football_events(self):
        """
        DESCRIPTION: Repeat steps by selecting several BYB football events.
        """
        self.navigate_to_page('homapage')
        self.site.wait_content_state('homepage')
        self.clicking_an_event_and_placing_bet_under_byb(eventID=self.eventID_2)
        self.test_005_verify_if_the_user_is_able_to_place_bet_with_appropriate_selections()