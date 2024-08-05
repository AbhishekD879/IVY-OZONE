import pytest
from crlat_siteserve_client.siteserve_client import SiteServeRequests
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.bet_placement
@pytest.mark.silks
@pytest.mark.horseracing
@pytest.mark.desktop
@pytest.mark.cash_out
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C1358434_Horse_Racing_bets_with_Generic_Silks_displaying(BaseCashOutTest):
    """
    TR_ID: C1358434
    NAME: Horse Racing bets with Generic Silks displaying
    """
    keep_browser_open = True
    event_name = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find HR event with silks available
        DESCRIPTION: Place bet on selection with generic silk available
        """
        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=self.ob_config.backend.ti.horse_racing.category_id,
                                   class_id=self.ob_config.backend.ti.horse_racing.class_ids)
        race_event = self.ob_config.add_UK_racing_event(number_of_runners=0, unnamed_favorites=True)
        event_to_outcome_for_event = ss_req.ss_event_to_outcome_for_event(event_id=race_event.event_id)
        type_name = event_to_outcome_for_event[0]['event']['typeName']
        type_name = normalize_name(type_name)
        start_time = race_event.event_date_time
        off_time_local = self.convert_time_to_local(date_time_str=start_time, ob_format_pattern='%Y-%m-%d %H:%M:%S')
        self.__class__.event_name = f'{type_name} {off_time_local}'
        selection_name, selection_id = list(race_event.selection_ids.items())[0]

        username = tests.settings.betplacement_user
        self.site.login(username=username)
        self.open_betslip_with_selections(selection_ids=selection_id)
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()

    def test_001_navigate_to_cashout_tab_on_my_bets_page(self):
        """
        DESCRIPTION: Navigate to 'Cashout' tab on 'My Bets' page
        EXPECTED: 'Cash out' tab has opened
        """
        self.site.open_my_bets_cashout()

    def test_002_verify_single_horse_racing_bet_available(self):
        """
        DESCRIPTION: Verify Single horse racing bet available
        EXPECTED: Correct silk is displayed for placed bet
        """
        bet_name, bet = self.site.cashout.tab_content.accordions_list.get_bet(event_names=self.event_name,
                                                                              bet_type='SINGLE',
                                                                              number_of_bets=1)
        betlegs = bet.items_as_ordered_dict
        self.assertTrue(betlegs, msg=f'No betlegs found for "{bet_name}"')
        betleg_name, betleg = list(betlegs.items())[0]
        self.assertTrue(betleg.silk.is_generic, msg=f'Generic Silk for "{betleg_name}" is not shown')
