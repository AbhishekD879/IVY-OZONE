import math
import pytest
from voltron.utils.waiters import wait_for_result
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # need to find selection ids/ ew terms / prices in SS resp
# @pytest.mark.hl
@pytest.mark.betslip
@pytest.mark.each_way
@pytest.mark.racing
@pytest.mark.critical
@pytest.mark.horseracing
@pytest.mark.pipelines
@pytest.mark.desktop
@pytest.mark.pipelines
@vtest
class Test_C28875_Verify_Each_Way_option_for_LP_price_on_the_Betslip(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C28875
    NAME: Verify Each Way option for 'LP' price on the Betslip
    DESCRIPTION: This test case verifies how Each Way option influence 'Total Returns' and 'Total Stakes' values ONLY when 'LP' selection is added to the Bet Slip.
    PRECONDITIONS: **There is a race event with market with Each Way available**
    PRECONDITIONS: To retrieve information from the Site Server (TST-2) use the following links:
    PRECONDITIONS: 1) To get class IDs for <Race> Sport use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?simpleFilter=class.categoryId:equals:21&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: Horse Racing Category ID = 21
    PRECONDITIONS: Greyhounds Category ID = 19
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) To get a list of events for Class use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/YYYY?simpleFilter=market.dispSortName:equals:MR&simpleFilter=class.categoryId:equals:21&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: where,
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *YYYY is a comma separated list of Class IDs (e.g. 97 or 97,98)*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Use attributes :
    PRECONDITIONS: **'priceTypeCodes'**='LP on a market level
    PRECONDITIONS: **'isEachWayAvailable'** on a market level to see whether Each Way checkbox should be displayed on the Bet Slip
    PRECONDITIONS: **'eachWayFactorNum', 'eachWayFactorDen', 'eachWayPlaces'** on a market level to see market terms attributes
    PRECONDITIONS: **'priceNum', 'priceDen'** in the outcome level - to see odds for selection in fraction format
    PRECONDITIONS: **'priceDec'** in the outcome level - to see odds for selection in decimal format
    """
    keep_browser_open = True
    stake_name, stake = None, None
    prices = {0: '1/9'}

    def verify_betslip_stake(self, ew=True):
        self.assertEqual(self.stake.amount_form.input.value, str(self.bet_amount),
                         msg=f'Stake value "{self.stake.amount_form.input.value}" is not the same '
                             f'as entered "{self.bet_amount}"')

        betslip = self.get_betslip_content()
        expected_total_stake = self.bet_amount * 2 if ew else self.bet_amount
        total_stake_result = wait_for_result(lambda: str(float(betslip.total_stake)) == str(float(expected_total_stake)),
                                             timeout=3,
                                             name='Total stake changed')
        self.assertTrue(total_stake_result,
                        msg=f'Total stake value "{betslip.total_stake}" is not the same as '
                            f'expected "{expected_total_stake}"')
        total_est_returns = betslip.total_estimate_returns
        payout_first_stake = self.convert_fraction_price_to_decimal(initial_price=list(self.prices.values())[0],
                                                                    round_to=0) + 1

        expected_total_est_returns_ew = math.floor(((payout_first_stake * self.bet_amount) * 2) * 100) / 100.0
        expected_total_est_returns_no_ew = math.floor((payout_first_stake * self.bet_amount) * 100) / 100.0
        expected_total_est_returns = expected_total_est_returns_ew if ew else expected_total_est_returns_no_ew

        self.assertAlmostEqual(float(total_est_returns), float(expected_total_est_returns), delta=0.01,
                               msg=f'Total estimate returns value "{total_est_returns}" is not the same '
                                   f'as expected "{expected_total_est_returns}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test racing event with each way terms
        """
        event_params = self.ob_config.add_UK_racing_event(number_of_runners=1,
                                                          ew_terms=self.ew_terms,
                                                          lp_prices=self.prices)
        selection_ids = event_params.selection_ids
        selection_name, self.__class__.selection_id = list(selection_ids.items())[0]

    def test_001_add_sp_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add 'LP' selection to the Bet Slip
        DESCRIPTION: Go to the Bet Slip
        EXPECTED: Bet Slip with bet details is opened
        EXPECTED:
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)

    def test_002_verify_each_way_checkbox(self):
        """
        DESCRIPTION: Verify Each Way checkbox
        EXPECTED: 1.  Checkbox is not selected by default
        EXPECTED: 2.  Checkbox label is 'Each Way'
        """
        singles_section = self.get_betslip_sections().Singles
        stake_name, self.__class__.stake = list(singles_section.items())[0]
        self._logger.info(f'*** Verifying stake "{stake_name}"')
        self.assertTrue(self.stake.has_each_way_checkbox,
                        msg=f'Stake {stake_name} does not have Each Way checkbox')

    def test_003_enter_stake_in_a_stake_field(self):
        """
        DESCRIPTION: Enter stake in a stake field
        """
        self.stake.amount_form.input.value = self.bet_amount

    def test_004_verify_total_est_returns_correctness(self):
        """
        DESCRIPTION: Verify 'Total Est. Returns' correctness
        EXPECTED: 'Total Est. Returns' is calculated according to the formula:
        EXPECTED: ***'Total Est. Returns'* = *'stake' *+ *'profit'*, **
        EXPECTED: where
        EXPECTED: ***'stake'* **- is entered value in a stake field
        EXPECTED: ***'profit'*** = (**'priceNum'** / **'priceDen'**) * ***'stake' -*** in case when price/odds are in a fractional format
        """
        self.verify_betslip_stake(ew=False)

    def test_005_on_bet_slip_select_checkbox_each_way(self):
        """
        DESCRIPTION: On Bet Slip select checkbox  'Each Way'
        EXPECTED: Each Way option is enabled
        """
        self.stake.each_way_checkbox.click()

        self.assertTrue(self.stake.each_way_checkbox.is_selected(), msg='Each Way is not selected')

    def test_006_verify_total_est_returns_correctness(self):
        """
        DESCRIPTION: Verify 'Total Est. Returns' correctness
        EXPECTED: 'Total Est. Returns' is calculated according to the formula :
        EXPECTED: ***'Total Est. Returns'* = *'stake' *+ *'profit' + 'extra_profit'*, **
        EXPECTED: where
        EXPECTED: ***'stake'* **- is entered value in a stake field
        EXPECTED: ***'profit'*** = (**'priceNum'** / **'priceDen'**) * ***'stake' -*** in case when price/odds are in a fractional format
        EXPECTED: ***'extra_profit'***= ***'stake'*** + ***[*** (***'eachWayFactorNum'*** / ***'eachWayFactorDen' ) **** (***'priceNum'/'priceDen') **** ***'stake' ]***
        """
        self.verify_betslip_stake()
