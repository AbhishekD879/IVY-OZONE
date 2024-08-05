import pytest
import voltron.environments.constants as vec
import tests
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.bet_placement
@pytest.mark.silks
@pytest.mark.desktop
@pytest.mark.portal_dependant
@pytest.mark.horseracing
@pytest.mark.cash_out
@pytest.mark.medium
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C1358434_Horse_Racing_bets_with_Image_Silks_displaying(BaseRacing, BaseCashOutTest):
    """
    TR_ID: C1358434
    NAME: Horse Racing bets with Image Silks displaying
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find HR event with silks available
        DESCRIPTION: Place bet on selection with image silk available
        """
        cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), \
            simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')

        event_params = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                           additional_filters=cashout_filter,
                                                           number_of_events=1)[0]

        for market in event_params['event']['children']:
            if market['market']['name'] == 'Win or Each Way' and market['market'].get('children'):
                outcomes_resp = market['market']['children']
        all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes_resp if 'Unnamed' not in i['outcome']['name']}
        selection_id = list(all_selection_ids.values())[0]
        self.__class__.event_name = event_params['event']['name']

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
                                                                              bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
                                                                              number_of_bets=1)
        betlegs = bet.items_as_ordered_dict
        self.assertTrue(betlegs, msg=f'No betlegs found for "{bet_name}"')
        betleg_name, betleg = list(betlegs.items())[0]
        self.assertTrue(betleg.has_silk(), msg=f'Silk image for "{betleg_name}" is not shown')
