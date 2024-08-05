from random import choice

import pytest
from crlat_ob_client.utils.date_time import validate_time

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.bet_placement
@pytest.mark.cash_out
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C146508_C141206_event_start_time_start_date_on_Cash_Out_bet_lines(BaseCashOutTest):
    """
    TR_ID: C146508
    TR_ID: C141206
    NAME: Event Start Time/Start Date on Cash Out bet lines
    """
    keep_browser_open = True
    event_name_today, event_name_live, event_name_future = None, None, None
    event_time_today, event_time_live, event_time_future = None, None, None
    today_date_format_pattern = '%H:%M, Today'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        DESCRIPTION: Login
        DESCRIPTION: Place bets
        """
        event_today = self.ob_config.add_autotest_premier_league_football_event(cashout=True)
        self.__class__.event_name_today = f'{event_today.team1} v {event_today.team2} ' \
                                          f'{self.convert_time_to_local(date_time_str=event_today.event_date_time)}'

        self.__class__.event_time_today = event_today.event_date_time

        event_future = self.ob_config.add_autotest_premier_league_football_event(
            cashout=True, start_time=self.get_date_time_formatted_string(days=14))
        start_time_local = self.convert_time_to_local(date_time_str=event_future.event_date_time,
                                                      future_datetime_format=self.event_card_future_time_format_pattern)
        self.__class__.event_name_future = f'{event_future.team1} v {event_future.team2} {start_time_local}'
        self.__class__.event_time_future = event_future.event_date_time

        event_live = self.ob_config.add_autotest_premier_league_football_event(
            cashout=True, is_live=True, img_stream=True)
        self.__class__.event_name_live = event_live.team1 + ' v ' + event_live.team2
        self.__class__.event_time_live = event_live.event_date_time

        username = tests.settings.betplacement_user
        self.site.login(username=username)

        self.open_betslip_with_selections(selection_ids=(choice(list(event_today.selection_ids.values())),
                                                         choice(list(event_future.selection_ids.values())),
                                                         choice(list(event_live.selection_ids.values()))))

        self.place_bet_on_all_available_stakes()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()

    def test_001_navigate_to_cash_out_tab_on_my_bets_page_bet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/ 'Bet Slip' widget
        EXPECTED: 'Cash out' tab has opened
        """
        self.site.open_my_bets_cashout()

    def test_002_verify_single_live_event(self):
        """
        DESCRIPTION: Verify single Live event
        EXPECTED: 'LIVE' badge is displayed next to Event Name
        """
        bet_name, bet = self.site.cashout.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event_name_live,
            number_of_bets=9)
        betlegs = bet.items_as_ordered_dict
        self.assertTrue(betlegs, msg=f'No one bet leg was found for bet: {bet_name}')
        betleg_name, betleg = list(betlegs.items())[0]

        self.assertTrue(betleg.has_live_label, msg=f'"LIVE" badge is not shown for "{betleg_name}"')

    def test_003_verify_match_start_time_for_today_match(self):
        """
        DESCRIPTION: Verify Match Start Time for today match
        EXPECTED: The time is displayed in format: **HH:MM AM/PM** (example: 7:00 PM)
        """
        bet_name, bet = self.site.cashout.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event_name_today,
            number_of_bets=9)
        betlegs = bet.items_as_ordered_dict
        self.assertTrue(betlegs, msg=f'No betlegs found for {bet_name}')
        betleg_name, betleg = list(betlegs.items())[0]
        validate_time(actual_time=betleg.event_time, format_pattern=self.today_date_format_pattern)
        self.compare_date_time(
            item_time_ui=betleg.event_time,
            event_date_time_ob=self.event_time_today,
            format_pattern=self.today_date_format_pattern)

    def test_004_verify_match_start_time_for_future_match(self):
        """
        DESCRIPTION: Verify Match Start Time for future match
        EXPECTED: The time is displayed in format: **DD MM, HH:MM AM/PM** (example: 23 Feb, 8:00 PM)
        """
        bet_name, bet = self.site.cashout.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event_name_future,
            number_of_bets=9)
        betlegs = bet.items_as_ordered_dict
        self.assertTrue(betlegs, msg=f'No betlegs found for {bet_name}')
        betleg_name, betleg = list(betlegs.items())[0]
        validate_time(actual_time=betleg.event_time, format_pattern=self.event_card_future_time_format_pattern)
        self.compare_date_time(item_time_ui=betleg.event_time, event_date_time_ob=self.event_time_future,
                               format_pattern=self.event_card_future_time_format_pattern, dayfirst=False)

    def test_005_verify_match_start_time_for_multiple_bet(self):
        """
        DESCRIPTION: Verify Match Start Time for betlegs in Multiple bet
        EXPECTED: For Today event: The time is displayed in format: **HH:MM AM/PM** (example: 7:00 PM)
        EXPECTED: For Live event: 'LIVE' badge is displayed next to Event Name
        EXPECTED: For Future event: The date is displayed in format: **DD MM, HH:MM AM/PM** (example: 23 Feb, 8:00 PM)
        """
        bet_name, bet = self.site.cashout.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE,
            event_names=[self.event_name_today, self.event_name_future, self.event_name_live],
            number_of_bets=9)
        betlegs = bet.items_as_ordered_dict
        self.assertTrue(betlegs, msg=f'No betlegs found for "{bet_name}"')

        today_betleg_name, today_betleg = next(((leg_name, leg) for (leg_name, leg) in betlegs.items()
                                                if self.event_name_today in leg_name), (None, None))
        self.assertTrue(today_betleg, msg=f'Cannot find betleg for event "{self.event_name_today}"')
        validate_time(actual_time=today_betleg.event_time, format_pattern=self.today_date_format_pattern)
        self.compare_date_time(item_time_ui=today_betleg.event_time, event_date_time_ob=self.event_time_today,
                               format_pattern=self.today_date_format_pattern, dayfirst=False)

        future_betleg_name, future_betleg = next(((leg_name, leg) for (leg_name, leg) in betlegs.items()
                                                  if self.event_name_future in leg_name), (None, None))
        self.assertTrue(future_betleg, msg=f'Cannot find betleg for event "{self.event_name_future}"')
        validate_time(actual_time=future_betleg.event_time, format_pattern=self.event_card_future_time_format_pattern)
        self.compare_date_time(item_time_ui=future_betleg.event_time, event_date_time_ob=self.event_time_future,
                               format_pattern=self.event_card_future_time_format_pattern, dayfirst=False)

        live_betleg_name, live_betleg = next(((leg_name, leg) for (leg_name, leg) in betlegs.items()
                                              if self.event_name_live in leg_name), (None, None))
        self.assertTrue(live_betleg, msg=f'Cannot find betleg for event "{self.event_name_live}"')
        self.assertTrue(live_betleg.has_live_label, msg=f'"LIVE" badge is not shown for "{live_betleg_name}"')
