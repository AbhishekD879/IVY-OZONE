import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
@pytest.mark.iphone
@pytest.mark.betslip
@pytest.mark.numeric_keyboard
@pytest.mark.mobile_only
@pytest.mark.high
@vtest
class Test_C710605_Numeric_keyboard_displaying_for_more_than_1_selections(BaseBetSlipTest):
    """
    TR_ID: C710605
    VOL_ID: C9698421
    NAME: Numeric keyboard displaying for >1 selections
    DESCRIPTION: This test case verifies displaying numeric keyboard for >1 selections in Betslip
    PRECONDITIONS: - Oxygen application
    PRECONDITIONS: - Several selections are added to the Betslip
    PRECONDITIONS: - Betslip is opened
    """
    keep_browser_open = True
    device_name = 'iPhone 6 Plus' if not tests.use_browser_stack else tests.mobile_safari_default

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        DESCRIPTION: Open betslip
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            market = next((market for market in event['event']['children']
                           if 'Match Betting' in market['market']['templateMarketName'] and
                           market['market'].get('children')), None)
            outcomes = market['market']['children']
            selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.team1 = next((outcome['outcome']['name'] for outcome in outcomes if
                                         outcome['outcome'].get('outcomeMeaningMinorCode') and
                                         outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            if not self.team1:
                raise SiteServeException('No Home team found')
            selection_ids = selection_ids.values()
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            selection_ids = event.selection_ids.values()
            self.__class__.team1 = event.team1
        self.open_betslip_with_selections(selection_ids=selection_ids)

    def test_001_verify_availability_of_numeric_keyboard(self):
        """
        DESCRIPTION: Verify availability of numeric keyboard
        EXPECTED: Numeric keyboard is NOT available above 'BET NOW'/'LOG IN & BET' button
        EXPECTED: NO 'Stake' boxes are focused
        """
        self.assertFalse(self.get_betslip_content().keyboard.is_displayed(name='Betslip keyboard shown',
                                                                          timeout=3, expected_result=False),
                         msg='Betslip keyboard is not hidden')
        singles_section = self.get_betslip_sections().Singles
        [self.assertFalse(stake.amount_form.is_active(expected_result=False),
                          msg=f'Stake "{stake_name}" input box is focused')
         for stake_name, stake in singles_section.items()]

    def test_002_set_focus_over_any_stake_or_all_single_stakes_box(self):
        """
        DESCRIPTION: Set focus over any 'Stake' or 'All single stakes' box
        EXPECTED: Numeric keyboard is available above 'BET NOW'/'LOG IN & BET' button
        """
        singles_section = self.get_betslip_sections().Singles
        stake = singles_section.get(self.team1)
        self.assertTrue(stake, msg=f'"{self.team1}" stake was not found')
        stake.amount_form.input.click()
        self.assertTrue(stake.amount_form.is_active(), msg=f'Stake for "{self.team1}" input field was not focused')

        self.assertTrue(self.get_betslip_content().keyboard.is_displayed(name='Betslip keyboard shown', timeout=3),
                        msg='Betslip keyboard is not shown')
