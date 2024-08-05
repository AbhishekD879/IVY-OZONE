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
from voltron.utils.waiters import wait_for_result
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
@pytest.mark.prod
@pytest.mark.betslip
@pytest.mark.each_way
@pytest.mark.racing
@pytest.mark.critical
@pytest.mark.horseracing
@pytest.mark.desktop
@vtest
class Test_C28874_Verify_Each_Way_Option_for_SP_Price_on_the_Betslip(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C28874
    NAME: Verify Each Way Option for 'SP' Price on the Betslip
    DESCRIPTION: This test case verifies how Each Way option influence 'Total Returns' and 'Total Stakes' values ONLY when 'SP' selection is added to the Bet Slip.
    PRECONDITIONS: **There is a race event with market with Each Way available**
    PRECONDITIONS: To retrieve information from the Site Server (TST-2) use the following links:
    PRECONDITIONS: 1) To get class IDs for <Race> Sport use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?simpleFilter=class.categoryId:equals:21&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: Horse Racing Category ID = 21
    PRECONDITIONS: Greyhounds Category ID = 19
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) To get a list of events for Class use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/YYYY?simpleFilter=class.categoryId:equals:21&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: where,
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *YYYY is a comma separated list of Class IDs (e.g. 97 or 97,98)*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Use attributes :
    PRECONDITIONS: **'priceTypeCodes'**='SP' on a market level
    PRECONDITIONS: **'isEachWayAvailable'** on market level to see whether Each Way checkbox should be displayed on the Bet Slip
    """
    keep_browser_open = True
    stake_name = None

    def verify_betslip_stake(self, ew=True):
        amount_value = f'{float(self.stake.amount_form.input.value):.2f}'
        amount = f'{float(self.bet_amount):.2f}'
        self.assertEqual(amount_value, str(amount),
                         msg=f'Stake value "{amount_value}" is not the same as entered "{amount}"')

        betslip = self.get_betslip_content()

        expected_total_stake = self.bet_amount * 2 if ew else self.bet_amount
        expected_amount = f'{float(expected_total_stake):.2f}'
        self.assertTrue(wait_for_result(lambda: betslip.total_stake == expected_amount,
                                        timeout=5,
                                        name='Total stake to update'),
                        msg=f'Total stake value "{betslip.total_stake}" is not the same as expected "{expected_amount}"')
        total_est_returns = betslip.total_estimate_returns
        self.assertEqual(total_est_returns, 'N/A',
                         msg=f'Total estimate returns value "{total_est_returns}" is not the same as expected "N/A"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create/found racing event with each way terms
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
                                    'children') and 'Unnamed' not in outcome['outcome'].get('name'):  # outcomes that does not have children are usually outcomes with SP prices
                                selection_id = outcome['outcome']['id']
                                break
                        break
                if selection_id:
                    break
            if not selection_id:
                raise SiteServeException('There are no selections with SP prices')

            self.__class__.selection_ids = selection_id

            self._logger.info(
                f'*** Found Horse racing event "{event["event"]["id"]}" with selection ids: "{selection_id}"')
        else:
            racing_event = self.ob_config.add_UK_racing_event(number_of_runners=1)
            self.__class__.selection_ids = list(racing_event.selection_ids.values())[0]

    def test_001_add_sp_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add 'SP' selection to the Bet Slip
        DESCRIPTION: Go to the Bet Slip
        EXPECTED: Bet Slip with bet details is opened
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)

    def test_002_verify_each_way_checkbox(self):
        """
        DESCRIPTION: Verify Each Way checkbox
        EXPECTED: 1.  Checkbox is not selected by default
        EXPECTED: 2.  Checkbox label is 'Each Way'
        """
        singles_section = self.get_betslip_sections().Singles
        self.__class__.stake_name, self.__class__.stake = list(singles_section.items())[0]
        self._logger.info(f'*** Verifying stake "{self.stake_name}"')
        self.assertTrue(self.stake.has_each_way_checkbox,
                        msg=f'Stake "{self.stake_name}" does not have Each Way checkbox')

    def test_003_enter_a_stake_in_a_stake_field(self):
        """
        DESCRIPTION: Enter a stake in a Stake field
        EXPECTED: 1.  'Stake' value corresponds to the entered stake
        EXPECTED: 2.  'Total Stake' is equal to entered stake
        EXPECTED: 3.  'Total Est. Returns' is not calculated for 'SP' odds and displays "N/A"
        """
        self.stake.amount_form.input.value = f'{self.bet_amount}:0.2'
        self.verify_betslip_stake(ew=False)

    def test_004_on_a_bet_slip_select_checkbox_each_way(self):
        """
        DESCRIPTION: On a Bet Slip select checkbox 'Each Way'
        EXPECTED: 1. EachWay checkbox is selected
        EXPECTED: 2. 'Stake' value corresponds to the entered stake
        EXPECTED: 3. 'Total Stake' value is doubled
        EXPECTED: 4. 'Total Est. Returns is not calculated for 'SP' odds and displays "N/A"
        """
        self.stake.each_way_checkbox.click()
        self.assertTrue(self.stake.each_way_checkbox.is_selected(), msg='Each Way is not selected')
        self.verify_betslip_stake()
