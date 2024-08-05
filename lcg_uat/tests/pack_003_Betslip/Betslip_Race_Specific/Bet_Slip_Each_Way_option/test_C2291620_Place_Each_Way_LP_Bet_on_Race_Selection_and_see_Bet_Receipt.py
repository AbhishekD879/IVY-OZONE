import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter, simple_filter

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.bet_placement
@pytest.mark.betslip
@pytest.mark.each_way
@pytest.mark.critical
@pytest.mark.desktop
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C2291620_Place_Each_Way_LP_Bet_on_Race_Selection_and_see_Bet_Receipt(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C2291620
    NAME: Place Each Way LP Bet on Race Selection and see Bet Receipt
    DESCRIPTION: This test case verifies placing Each Way bet on Race Selection and its Bet Receipt for LP priced selection
    PRECONDITIONS: There is event with 'Win Or Each Way market' with LP prices
    PRECONDITIONS: User is logged in and has positive balance to place a bet
    PRECONDITIONS: User is placed single bet with 'LP' selection and with selected 'Each Way' checkbox
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: TST2/STG2: Create racing test event
        DESCRIPTION: PROD: Find active Horseracing event with Each Way terms
        DESCRIPTION: Login into app
        EXPECTED: Event is created
        EXPECTED: User is logged in
        """
        if tests.settings.backend_env == 'prod':
            additional_filter = exists_filter(LEVELS.EVENT, simple_filter(
                LEVELS.MARKET, ATTRIBUTES.PRICE_TYPE_CODES, OPERATORS.INTERSECTS, 'LP')), \
                exists_filter(LEVELS.EVENT, simple_filter(
                    LEVELS.MARKET, ATTRIBUTES.IS_EACH_WAY_AVAILABLE, OPERATORS.IS_TRUE))
            events = self.get_active_events_for_category(all_available_events=True,
                                                         additional_filters=additional_filter,
                                                         expected_template_market='Win or Each Way',
                                                         category_id=self.ob_config.horseracing_config.category_id)
            for event in events:
                outcomes = next(((market['market'].get('children')) for market in event['event']['children']
                                 if 'LP' in market['market']['priceTypeCodes'] and market['market'].get('children')), None)
                event_ID = event['event']['id']
                market = event['event']['children'][0]['market']
                self.__class__.ew_coef = float(market['eachWayFactorNum']) / float(market['eachWayFactorDen'])
                if not outcomes:
                    raise SiteServeException(f'No outcomes available for "{event["event"]["name"]}" with LP prices')
                selection_id = None
                for outcome in outcomes:
                    if outcome['outcome'].get('children'):
                        for child in outcome['outcome'].get('children'):
                            if child.get('price'):
                                if 'LP' in child.get('price').get('priceType'):
                                    if 'Unnamed' not in outcome['outcome']['name']:
                                        selection_id = outcome['outcome']['id']
                                break
                        break
                break
            if not selection_id:
                raise SiteServeException('No selection available with LP price')
            self.__class__.selection_ids = selection_id
            self._logger.info(f'*** Found Horse Racing event ID "{event_ID}" '
                              f'with selection ID "{self.selection_ids}" '
                              f'and EW coef "{self.ew_coef}"')
        else:
            racing_event = self.ob_config.add_UK_racing_event(number_of_runners=1,
                                                              lp_prices={0: '1/2'},
                                                              ew_terms=self.ew_terms)
            self.__class__.selection_ids = list(racing_event.selection_ids.values())[0]
            self.__class__.ew_coef = float(self.ew_terms['ew_fac_num']) / float(self.ew_terms['ew_fac_den'])

        self.site.login()
        self.__class__.user_balance = self.site.header.user_balance

    def test_001_add_lp_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add 'LP' selection to the Bet Slip
        EXPECTED: 'LP' selection is added to the Bet Slip
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)

    def test_002_click_bet_now_button(self):
        """
        DESCRIPTION: Click 'Bet Now' button
        EXPECTED: Bet is placed
        EXPECTED: Balance is decreased by 'Total Stake' value
        EXPECTED: Bet Slip is replaced with a Bet Receipt view
        """
        self.__class__.betslip_info = self.place_and_validate_single_bet(each_way=True, ew_coef=self.ew_coef)
        self.check_bet_receipt_is_displayed()
        footer = self.site.bet_receipt.footer
        total_stake = footer.total_stake
        total_stake_betreceipt = float(total_stake.replace(',', ''))
        self.verify_user_balance(expected_user_balance=(self.user_balance - float(total_stake_betreceipt)))

    def test_003_verify_bet_receipt(self):
        """
        DESCRIPTION: Verify Bet Receipt
        EXPECTED: Bet Receipt header is present
        EXPECTED: Bet Receipt contains the following information:
        EXPECTED: *   header 'Singles(1)'
        EXPECTED: *   selection name
        EXPECTED: *   the market type user has bet on - i.e. Win or Each Way
        EXPECTED: *   the event name to which the outcome belongs to
        EXPECTED: *   the Bet ID. The Bet ID is start with O and contain numeric values - i.e. O/0123828/0000155
        EXPECTED: *   Odds
        EXPECTED: *   Unit Stake and 'E/W' label
        EXPECTED: *   Total Stake
        EXPECTED: *   Est. Returns
        EXPECTED: **All information corresponds to the information about just placed bet**
        EXPECTED: 'Reuse Selection' and 'Done' buttons
        """
        self.check_bet_receipt(betslip_info=self.betslip_info, each_way=True)
        bet_receipt = self.site.bet_receipt.footer
        self.assertTrue(bet_receipt.has_reuse_selections_button(),
                        msg='Can not find "Reuse selection" button')
        self.assertTrue(bet_receipt.has_done_button(), msg='Can not find "Done" button')
