import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.waiters import wait_for_result
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # can't set result on prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.bet_placement
@pytest.mark.open_bets
@pytest.mark.bet_history_open_bets
@pytest.mark.desktop
@pytest.mark.slow
@pytest.mark.login
@vtest
class Test_C29212_Verify_Open_Bets_Regular_Filter_Settle_Result(BaseCashOutTest):
    """
    TR_ID: C29212
    NAME: Verify 'Open Bets' tab - 'Regular' filter
    """
    keep_browser_open = True
    num_of_events = 3
    events_info = []

    def set_selections_result(self, result, event_id, selection_id):
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        markets_id = self.ob_config.market_ids[event_id][market_short_name]
        self.ob_config.update_selection_result(event_id=event_id,
                                               market_id=markets_id,
                                               selection_id=selection_id,
                                               result=result)

    def verify_bet_disappear(self, bet_name):
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        if self.device_type == 'desktop':
            self.site.open_my_bets_open_bets()
        result = self.site.open_bets.tab_content.accordions_list.wait_till_bet_disappear(bet_name, timeout=20)
        self.assertTrue(result, msg=f'Bet: "{bet_name}" is still displayed after reloading the page')

    def test_001_login_create_event_and_place_bets(self):
        """
        DESCRIPTION: Login as Oxygen user, create test event, add selections with deep link and place single bets
        """
        self.__class__.events_info = self.create_several_autotest_premier_league_football_events(number_of_events=self.num_of_events)
        self.site.login(username=tests.settings.betplacement_user)
        selection_ids = []
        for event_info in self.events_info:
            selection_ids.append(event_info.selection_ids[event_info.team1])
        self.open_betslip_with_selections(selection_ids=selection_ids)
        self.place_single_bet(number_of_stakes=self.num_of_events)
        self.site.bet_receipt.footer.click_done()

    def test_002_go_to_my_bets(self):
        """
        DESCRIPTION: Tap on 'My Bets' item on Top Menu
        """
        self.site.open_my_bets_open_bets()

    def test_003_tap_open_bets_tab(self):
        """
        DESCRIPTION: Tap 'Open Bets' tab
        EXPECTED: 'Regular' sort filter is selected by default
        """
        result = wait_for_result(
            lambda: self.site.open_bets.tab_content.grouping_buttons.current == vec.bma.SPORTS,
            name=f'"{vec.bma.SPORTS}" to became active',
            timeout=2)
        self.assertTrue(result, msg=f'"{vec.bma.SPORTS}" sorting type is not selected by default')

    def test_004_trigger_situation_of_winning_bet(self):
        """
        DESCRIPTION: Trigger the situation of Winning a bet
        EXPECTED: Bet with status 'Won' is not displayed in 'Open Bets' tab
        """
        event_info = self.events_info[0]
        event_name = f'{event_info.team1} v {event_info.team2} {event_info.local_start_time}'
        bet_name, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            event_names=event_name, bet_type='SINGLE', number_of_bets=3)
        self.assertTrue(bet, msg=f'Bet: "{bet_name}" not displayed in "Open Bets" tab')

        self.set_selections_result(result='W',
                                   event_id=event_info.event_id,
                                   selection_id=event_info.selection_ids[event_info.team1])
        self.verify_bet_disappear(bet_name=bet_name)

    def test_005_trigger_situation_of_losing_bet(self):
        """
        DESCRIPTION: Trigger the situation of Losing a bet
        EXPECTED: Bet with status 'Lost' is not displayed in 'Open Bets' tab
        """
        event_info = self.events_info[1]
        event_name = f'{event_info.team1} v {event_info.team2} {event_info.local_start_time}'
        bet_name, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            event_names=event_name, bet_type='SINGLE', number_of_bets=3)
        self.assertTrue(bet, msg=f'Bet: "{bet_name}" not displayed in "Open Bets" tab')

        self.set_selections_result(result='L',
                                   event_id=event_info.event_id,
                                   selection_id=event_info.selection_ids[event_info.team1])
        self.verify_bet_disappear(bet_name=bet_name)

    def test_006_trigger_situation_of_cancelling_bet(self):
        """
        DESCRIPTION: Trigger the situation of Cancelling a bet
        EXPECTED: Bet with status 'Void' is not displayed in 'Open Bets' tab
        """
        event_info = self.events_info[2]
        event_name = f'{event_info.team1} v {event_info.team2} {event_info.local_start_time}'
        bet_name, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            event_names=event_name, bet_type='SINGLE', number_of_bets=3)
        self.assertTrue(bet, msg=f'Bet: "{bet_name}" not displayed in "Open Bets" tab')

        self.set_selections_result(result='V',
                                   event_id=event_info.event_id,
                                   selection_id=event_info.selection_ids[event_info.team1])
        self.verify_bet_disappear(bet_name=bet_name)
