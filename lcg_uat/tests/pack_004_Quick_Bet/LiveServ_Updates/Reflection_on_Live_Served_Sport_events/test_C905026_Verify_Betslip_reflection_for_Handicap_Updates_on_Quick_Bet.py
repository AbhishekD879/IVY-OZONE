import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.helpers import generate_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.quick_bet
@pytest.mark.handicap
@pytest.mark.liveserv_updates
@pytest.mark.ob_smoke
@pytest.mark.mobile_only
@pytest.mark.low
@vtest
class Test_C905026_Verify_Betslip_reflection_for_Handicap_Updates_on_Quick_Bet(BaseSportTest):
    """
    TR_ID: C905026
    VOL_ID: C9697996
    NAME: Verify Betslip reflection for Handicap Updates on Quick Bet
    """
    keep_browser_open = True

    old_handicap_value = None
    new_handicap_value = '+9.0'
    new_price_increased = '97/3'
    team1 = generate_name()
    team2 = generate_name()

    def test_000_create_test_event(self):
        """
        DESCRIPTION: Create test event
        """
        event = self.ob_config.add_autotest_premier_league_football_event(team1=self.team1,
                                                                          team2=self.team2,
                                                                          markets=[('handicap_match_result', {'cashout': True})],
                                                                          is_live=True)
        self.__class__.eventID = event.event_id
        self.__class__.selection_ids = event.selection_ids

    def test_001_open_created_event(self):
        """
        DESCRIPTION: Open created event
        """
        self.navigate_to_edp(event_id=self.eventID)

    def test_002_add_selection_that_contains_handicap_value_to_quick_bet(self):
        """
        DESCRIPTION: Add selection that contains Handicap value to Quick Bet
        EXPECTED: Quick Bet appears at the bottom of the page
        EXPECTED: Betslip counter does NOT increase by one
        """
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        handicap = markets_list.get(self.expected_market_sections.handicap_results)
        self.assertTrue(handicap, msg='*** Can not find Handicap market section')

        outcome_groups = handicap.outcomes.items_as_ordered_dict
        self.assertTrue(outcome_groups, msg='Outcome groups is empty')
        outcome_group_name, outcome_group = list(outcome_groups.items())[0]
        outcomes = outcome_group.items_as_ordered_dict

        handicap_sigh, handicap_value = outcome_group_name[:1], outcome_group_name[1:]
        self.__class__.old_handicap_value = '%s%s' % (handicap_sigh, '%.1f' % (float(handicap_value)))

        self.__class__.marketID = self.ob_config.market_ids[self.eventID]['handicap_match_result %s' % self.old_handicap_value]

        self.assertTrue(outcomes, msg='No one outcome was found in section: "%s"' % outcome_group_name)
        outcome_name, outcome = list(outcomes.items())[0]
        outcome.click()

    def test_003_verify_quick_bet_displaying(self):
        """
        DESCRIPTION: Verify Quick Bet displaying
        """
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')

    def test_004_change_handicap_value_on_market_level(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: change** rawHandicapValue **on market level
        DESCRIPTION: and at the same time have Quick Bet page opened to watch for updates
        EXPECTED: 1. Handicap value is changed
        EXPECTED: 2. Handicap value in selection name is updated
        """
        market_template_id = list(self.ob_config.football_config.autotest_class.autotest_premier_league.markets.handicap_match_result.values())[0]
        self.ob_config.change_handicap_market_value(event_id=self.eventID,
                                                    market_id=self.marketID,
                                                    market_template_id=market_template_id,
                                                    new_handicap_value=self.new_handicap_value)

    def test_005_verify_error_message_handicap_value_and_login__place_betplace_bet_button(self):
        """
        DESCRIPTION: Verify Error message, Handicap value and 'LOGIN & PLACE BET'/'PLACE BET' button
        EXPECTED: 1. Error message: 'Handicap value changed from OLD To NEW' should be displayed on red background below the corresponding selection
        EXPECTED: 2. Handicap value should be updated to reflect the changed value
        """
        expected_message = vec.quickbet.HANDICAP_ERROR.format(old=self.old_handicap_value,
                                                              new=self.new_handicap_value)
        self.site.quick_bet_panel.wait_for_quick_bet_info_panel()
        message = self.site.quick_bet_panel.info_panels_text[0]
        self.assertEqual(message, expected_message,
                         msg=f'Actual message "{message}" does not match expected "{expected_message}"')

        result = wait_for_result(lambda: '+9.0' in self.site.quick_bet_panel.selection.content.outcome_name,
                                 name='Outcome to be changed',
                                 timeout=15)

        self.assertTrue(result, msg='Outcome name was not changed')

        selection_name = self.site.quick_bet_panel.selection.content.outcome_name
        expected_selection_name = self.team1 + ' (%s)' % self.new_handicap_value
        self.assertEqual(selection_name, expected_selection_name, msg='Selection name is not changed from "%s" to "%s"'
                                                                      % (selection_name, expected_selection_name))

    def test_006_change_selection_price_and_make_no_changes_on_market_handicap_value(self):
        """
        DESCRIPTION: Change selection price and make no changes on market handicap value
        EXPECTED: Price value is changed and handicap value remains the same
        """
        selection_id = self.selection_ids['handicap_match_result %s' % self.old_handicap_value][self.team1]
        quick_bet = self.site.quick_bet_panel.selection.content
        odds = quick_bet.odds
        self.ob_config.change_price(selection_id=selection_id, price=self.new_price_increased)

        price_update = self.wait_for_price_update_from_live_serv(selection_id=selection_id, price=self.new_price_increased)
        self.assertTrue(price_update,
                        msg=f'Price update for selection id "{selection_id}" is not received')

        message_change = self.site.quick_bet_panel.wait_for_message_to_change(
            previous_message=vec.quickbet.HANDICAP_ERROR.format(old=self.old_handicap_value,
                                                                new=self.new_handicap_value))
        self.assertTrue(message_change, msg='Old error message is not disappear')
        actual_message = self.site.quick_bet_panel.info_panels_text[0]
        expected_message = vec.quickbet.PRICE_IS_CHANGED.format(old=odds, new=self.new_price_increased)
        self.assertEqual(actual_message, expected_message,
                         msg=f'Actual message "{actual_message}" does not match expected "{expected_message}"')
        self.assertFalse(self.site.quick_bet_panel.place_bet.is_enabled(expected_result=False),
                         msg='LOGIN & PLACE BET button is not disabled')
