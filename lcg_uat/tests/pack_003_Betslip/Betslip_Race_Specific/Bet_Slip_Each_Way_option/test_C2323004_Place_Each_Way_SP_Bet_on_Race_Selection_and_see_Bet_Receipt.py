import pytest
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter
from crlat_siteserve_client.siteserve_client import simple_filter
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
class Test_C2323004_Place_Each_Way_SP_Bet_on_Race_Selection_and_see_Bet_Receipt(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C2323004
    NAME: Place Each Way SP Bet on Race Selection and see Bet Receipt
    DESCRIPTION: This test case verifies placing Each Way bet on Race Selection and its Bet Receipt for SP priced selection
    PRECONDITIONS: There is event with 'Win Or Each Way market' with SP prices
    PRECONDITIONS: User is logged in and has positive balance to place a bet
    PRECONDITIONS: User is placed single bet with 'SP' selection and with selected 'Each Way' checkbox
    PRECONDITIONS: 'Est. Returns' displays "N/A"
    PRECONDITIONS: 'Total Est. Returns' displays "N/A"
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create/find racing event
        DESCRIPTION: Login into app
        EXPECTED: User is logged in
        """
        if tests.settings.backend_env == 'prod':
            additional_filters = exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET,
                                                                           ATTRIBUTES.PRICE_TYPE_CODES,
                                                                           OPERATORS.INTERSECTS,
                                                                           'SP'))
            events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                         additional_filters=additional_filters,
                                                         all_available_events=True)
            event, selection_id = None, None
            for event in events:
                for market in event['event']['children']:
                    if market['market'].get('children') and market.get('market').get(
                            'templateMarketName') == 'Win or Each Way':
                        for outcome in market['market']['children']:
                            if not outcome['outcome'].get(
                                    'children') and 'Unnamed' not in outcome['outcome'].get(
                                    'name'):  # outcomes that does not have children are usually outcomes with SP prices
                                selection_id = outcome['outcome']['id']
                                break
                        break
                if selection_id:
                    break
            if not selection_id:
                raise SiteServeException('There are no selections with SP prices')
            self.__class__.selection_ids = selection_id

            self._logger.info(f'*** Found Horse racing event with selection ids: "{self.selection_ids}"')
        else:
            racing_event = self.ob_config.add_UK_racing_event(number_of_runners=1,
                                                              ew_terms=self.ew_terms)
            self.__class__.selection_ids = list(racing_event.selection_ids.values())[0]

        self.site.login(username=tests.settings.betplacement_user)
        self.__class__.user_balance = self.site.header.user_balance

    def test_001_add_sp_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add 'SP' selection to the Bet Slip
        EXPECTED: 'SP' selection is added to the Bet Slip
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)

    def test_002_click_bet_now_button(self):
        """
        DESCRIPTION: Click 'Bet Now' button
        EXPECTED: Bet is placed
        EXPECTED: Balance is decreased by 'Total Stake' value
        EXPECTED: Bet Slip is replaced with a Bet Receipt view
        """
        self.__class__.betslip_info = self.place_and_validate_single_bet(each_way=True)
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
        EXPECTED: *   Odds displays "SP"
        EXPECTED: *   Unit Stake and 'E/W' label
        EXPECTED: *   Total Stake
        EXPECTED: *   Est. Returns displays "N/A"
        EXPECTED: **All information corresponds to the information about just placed bet**
        EXPECTED: 'Reuse Selection' and 'Done' buttons
        """
        self.check_bet_receipt(betslip_info=self.betslip_info, each_way=True)
        self.assertTrue(self.site.bet_receipt.footer.has_reuse_selections_button(),
                        msg='Can not find "Reuse selection" button')
        self.assertTrue(self.site.bet_receipt.footer.has_done_button(), msg='Can not find "Done" button')
