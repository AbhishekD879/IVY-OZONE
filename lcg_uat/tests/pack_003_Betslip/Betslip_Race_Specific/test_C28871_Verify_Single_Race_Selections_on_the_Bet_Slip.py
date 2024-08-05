import pytest

from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl - Can't be executed now, can't create OB event on prod
# @pytest.mark.prod - Can't be executed now, can't create OB event on prod
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.critical
@pytest.mark.betslip
@pytest.mark.desktop
@vtest
class Test_C28871_Verify_Single_Race_Selections_on_the_Bet_Slip(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C28871
    NAME: Verify Single Race Selections on the Bet Slip
    PRECONDITIONS: The following events are required:
    PRECONDITIONS: - Race with SP prices
    PRECONDITIONS: - Race with LP prices
    PRECONDITIONS: - Race with LP and SP prices
    PRECONDITIONS: To retrieve information from Site Server use the following steps:
    PRECONDITIONS: 1) To get Class IDs for <Race> Sport use the following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/
    PRECONDITIONS: Class?simpleFilter=class.categoryId:equals:21&simpleFilter=
    PRECONDITIONS: class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: Horse Racing Category ID = 21
    PRECONDITIONS: Greyhounds Category ID = 19
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) To get a list of events for Class use the following link :
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/
    PRECONDITIONS: EventToOutcomeForClass/YYYY?simpleFilter=market.dispSortName:equals:MR&simpleFilter=
    PRECONDITIONS: class.categoryId:equals:21&simpleFilter=class.isActive:isTrue&simpleFilter=
    PRECONDITIONS: class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: Note,
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *YYYY is a comma separated list of Class IDs (e.g. 97 or 97,98)*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Use attributes :
    PRECONDITIONS: **'name'** to see the event name and local time
    PRECONDITIONS: **'typeName'** to see the league name
    PRECONDITIONS: **'name'** on the market level - to see the market name
    PRECONDITIONS: **'name' **on the outcome level - to see selection name
    PRECONDITIONS: **'livePriceNum'/'livePriceDen'** in the outcome level -
    PRECONDITIONS: to see odds for a selection in a fractional format
    PRECONDITIONS: **'priceDec'** in the outcome level - to see odds for a selection in a decimal format
    """
    keep_browser_open = True
    prices = {0: '1/5'}
    autotest_uk_name_pattern = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events
        EXPECTED: Events is created
        """
        event_params_SP = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms, number_of_runners=1,
                                                             time_to_start=2, sp=True, lp=False)
        self.__class__.selection_id_SP = list(event_params_SP.selection_ids.values())[0]
        self.__class__.event_off_time_SP = event_params_SP.event_off_time
        event_params_LP = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms, number_of_runners=1,
                                                             time_to_start=20, sp=False, lp=True,
                                                             lp_prices=self.prices)
        self.__class__.selection_id_LP = list(event_params_LP.selection_ids.values())[0]
        self.__class__.event_off_time_LP = event_params_LP.event_off_time
        event_params_LP_SP = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms, number_of_runners=1,
                                                                time_to_start=20, sp=True, lp=True,
                                                                lp_prices=self.prices)
        self.__class__.selection_id_LP_SP = list(event_params_LP_SP.selection_ids.values())[0]
        self.__class__.event_off_time_LP_SP = event_params_LP_SP.event_off_time
        self.__class__.horse_name_SP = list(event_params_SP.selection_ids.keys())[0]
        self.__class__.horse_name_LP = list(event_params_LP.selection_ids.keys())[0]
        self.__class__.horse_name_LP_SP = list(event_params_LP_SP.selection_ids.keys())[0]
        self.__class__.event_name_SP = f"{self.event_off_time_SP} {self.horseracing_autotest_uk_name_pattern}"
        self.__class__.event_name_LP = f"{self.event_off_time_LP} {self.horseracing_autotest_uk_name_pattern}"
        self.__class__.event_name_LP_SP = f"{self.event_off_time_LP_SP} {self.horseracing_autotest_uk_name_pattern}"

    def test_001_add_single_sp_selection_and_go_to_the_bet_slip(self):
        """
        DESCRIPTION: Add single 'SP' selection to the Bet Slip
        EXPECTED: Selection is added to the Bet Slip
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id_SP)

    def test_002_verify_sp_selection(self):
        """
        DESCRIPTION: Verify selection
        EXPECTED: The following info is displayed on the Bet Slip:
        EXPECTED: 1.  Horse name ( **'name'** attribute on the outcome level) and "+" sign on the left
        EXPECTED: 2.  Market name ( **'name'** attribute on the market level)
        EXPECTED: 3.  Event name (**'name'** attributes on event level), Event date and time are shown after clicking "+"
        EXPECTED: 4.  'Odds' is 'SP'
        EXPECTED: 5.  'Each Way' checkbox and label
        EXPECTED: 6.  'Stake' label and edit box
        EXPECTED: 7.  'Est. Returns' is "N/A"
        EXPECTED: 8.  Bin icon
        """
        singles_section = self.get_betslip_sections().Singles
        self.assertIn(self.horse_name_SP, singles_section,
                      msg=f'Horse name "{self.horse_name_LP_SP}" is not present in "{singles_section.keys()}"')
        stake = singles_section[self.horse_name_SP]
        self.assertEqual(stake.outcome_name, self.horse_name_SP,
                         msg=f'Horse name "{stake.outcome_name}" is not the same as expected "{self.horse_name_SP}"')
        market_name = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.market_name.strip('|')
        self.assertEqual(stake.market_name, market_name,
                         msg=f'Market name "{stake.market_name}" is not the same as expected "{market_name}"')
        self.assertEqual(stake.event_name, self.event_name_SP,
                         msg=f'Event name "{stake.event_name}" is not the same as expected "{self.event_name_SP}"')
        self.assertTrue(stake.each_way_checkbox.is_displayed(), msg='Each way check box is not displayed')
        self.assertEqual(stake.each_way_checkbox.each_way_label, 'E/W',
                         msg=f'E/W label is incorrect, actual is : "{stake.each_way_checkbox.each_way_label}"')
        self.assertTrue(stake.amount_form.has_amount_input(), msg='Amount input is not displayed')
        self.assertEqual(stake.amount_form.label, 'Stake', msg='Amount label is not correct')
        self.assertTrue(stake.remove_button.is_displayed())
        self.assertEqual(stake.odds, 'SP', msg=f'Stake Odds "{stake.odds}" is not SP')
        self.assertEqual(stake.est_returns, 'N/A', msg='Stake Est. Returns "%s" is not N/A' % stake.est_returns)

    def test_003_add_single_lp_selection_and_go_to_the_bet_slip(self):
        """
        DESCRIPTION: Add single 'LP' selection to the Bet Slip
        EXPECTED: Bet Slip counter is increased by 1
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id_LP)

    def test_004_verify_lp_selection(self):
        """
        DESCRIPTION: Verify selection
        EXPECTED: The following info is displayed on the Bet Slip:
        EXPECTED: 1.  Horse name ( **'name'** attribute on the outcome level) and "+" sign on the left
        EXPECTED: 2.  Market name ( **'name'** attribute on the market level)
        EXPECTED: 3.  Event name (**'name'** attributes on event level), Event date and time are shown after clicking "+"
        EXPECTED: 4.  Odds ( **'livePriceNum'/'livePriceDen' **attributes in a fractional format or **'price Dec'** in decimal format)
        EXPECTED: 5.  'Each Way' checkbox and label
        EXPECTED: 6.  'Stake' label and edit box
        EXPECTED: 7.  'Est. Returns' is "0.00" and is re-calculated after entering Stake
        EXPECTED: 8.  Bin icon
        """
        singles_section = self.get_betslip_sections().Singles
        self.assertIn(self.horse_name_LP, singles_section,
                      msg=f'Horse name "{self.horse_name_LP_SP}" is not present in "{singles_section.keys()}"')
        stake = singles_section[self.horse_name_LP]
        self.assertEqual(stake.outcome_name, self.horse_name_LP,
                         msg=f'Horse name "{stake.outcome_name}" is not the same as expected "{self.horse_name_LP}"')
        market_name = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.market_name.strip('|')
        self.assertEqual(stake.market_name, market_name,
                         msg=f'Market name "{stake.market_name}" is not the same as expected "{market_name}"')
        self.assertEqual(stake.event_name, self.event_name_LP,
                         msg=f'Event name "{stake.event_name}" is not the same as expected "{self.event_name_LP}"')
        self.assertTrue(stake.each_way_checkbox.is_displayed(), msg='Each way check box is not displayed')
        self.assertEqual(stake.each_way_checkbox.each_way_label, 'E/W',
                         msg=f'E/W label is incorrect, actual is : "{stake.each_way_checkbox.each_way_label}"')
        self.assertTrue(stake.amount_form.has_amount_input(), msg='Amount input is not displayed')
        self.assertEqual(stake.amount_form.label, 'Stake', msg='Amount label is not correct')
        self.assertTrue(stake.remove_button.is_displayed())
        self.assertEqual(stake.odds, self.prices[0])
        self.assertRegex(stake.est_returns, r'\d{1}.\d{2}', msg='Est. Returns is wrong format')
        stake.amount_form.enter_amount('10')
        self.assertEqual(stake.est_returns, '12.00', msg='Stake Est. Returns calculated wrong')

    def test_005_add_single_lp_sp_selection_and_go_to_the_bet_slip(self):
        """
        DESCRIPTION: Add a selection of the event with attribute 'priceTypeCodes' = 'LP, SP'
        EXPECTED: Bet Slip counter is increased by 1
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id_LP_SP)

    def test_006_verify_lp_sp_selection(self):
        """
        DESCRIPTION: Verify selection
        EXPECTED: The following info is displayed on the Bet Slip:
        EXPECTED: 1.  Horse name ( **'name'** attribute on the outcome level)
        EXPECTED: 2.  Market type ( **'name'** attribute on the market level)
        EXPECTED: 3.  Event name ( **'name'** attributes on event level), Event date and time are shown after clicking "+"
        EXPECTED: 4.  'Odds' field is a dropdown which contains LP value and SP. User have a possibility to switch between 'LP' and 'SP' bets
        EXPECTED: 5.  'Each Way' checkbox and label
        EXPECTED: 6.  'Stake' label and edit box
        EXPECTED: 7. 'Est. Returns' are changed according to selected price type
        EXPECTED: 8.  Bin icon
        """
        singles_section = self.get_betslip_sections().Singles
        self.assertIn(self.horse_name_LP_SP, singles_section,
                      msg=f'Horse name "{self.horse_name_LP_SP}" is not present in "{singles_section.keys()}"')
        stake = singles_section[self.horse_name_LP_SP]
        self.assertEqual(stake.outcome_name, self.horse_name_LP_SP,
                         msg=f'Horse name "{stake.outcome_name}" is not the same as expected "{self.horse_name_LP_SP}"')
        market_name = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.market_name.strip('|')
        self.assertEqual(stake.market_name, market_name,
                         msg=f'Market name "{stake.market_name}" is not the same as expected "{market_name}"')
        self.assertEqual(stake.event_name, self.event_name_LP_SP,
                         msg=f'Event name "{stake.event_name}" is not the same as expected "{self.event_name_LP_SP}"')
        self.assertTrue(stake.each_way_checkbox.is_displayed(), msg='Each way check box is not displayed')
        self.assertEqual(stake.each_way_checkbox.each_way_label, 'E/W',
                         msg=f'E/W label is incorrect, actual is : "{stake.each_way_checkbox.each_way_label}"')
        self.assertTrue(stake.amount_form.has_amount_input(), msg='Amount input is not displayed')
        self.assertEqual(stake.amount_form.label, 'Stake', msg='Amount label is not correct')
        self.assertTrue(stake.remove_button.is_displayed())
        self.assertEqual(stake.odds, self.prices[0])
        stake.odds_dropdown.select_value('SP')
        singles_section = self.get_betslip_sections().Singles
        self.assertIn(self.horse_name_LP_SP, singles_section,
                      msg=f'Horse name "{self.horse_name_LP_SP}" is not present in "{singles_section.keys()}"')
        stake = singles_section[self.horse_name_LP_SP]
        odds = stake.odds
        self.assertEqual(odds, 'SP', msg=f'Odds "{odds}" are not the same as expected "SP"')
