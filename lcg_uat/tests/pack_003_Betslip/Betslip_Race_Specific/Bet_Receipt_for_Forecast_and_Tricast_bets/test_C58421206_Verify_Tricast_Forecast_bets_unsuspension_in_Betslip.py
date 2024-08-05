import pytest
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - event suspension can't be done in prod/beta
@pytest.mark.desktop
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C58421206_Verify_Tricast_Forecast_bets_unsuspension_in_Betslip(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C58421206
    NAME: Verify Tricast/Forecast bets unsuspension in Betslip
    DESCRIPTION: This test case verifies unsuspension notifications for Tricast/Forecast bets in Betslip.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: The related OCC ticket: https://jira.egalacoral.com/browse/BMA-51664
        PRECONDITIONS: Defect video from the OCC ticket available here: https://jira.egalacoral.com/secure/attachment/1380838/RPReplay-Final1583227399.MP4
        PRECONDITIONS: - Tricast/Forecast ckeck boxes are selected on Market level for the event in OB TI.
        PRECONDITIONS: - User is on HR EDP with Tricast/Forecast markets available.
        PRECONDITIONS: For manipulations with bet statuses use OB TI system according to brand needed:
        PRECONDITIONS: Coral: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=OpenBet+Systems
        PRECONDITIONS: Ladbrokes: https://confluence.egalacoral.com/display/SPI/Ladbrokes+OpenBet+System
        """
        event = self.ob_config.add_UK_racing_event(number_of_runners=5, forecast_available=True, tricast_available=True)
        self.__class__.eventID = event.event_id
        self.__class__.marketID = event.market_id

        self.site.login()
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertTrue(market_tabs, msg='No market tabs found on EDP')
        self.assertIn(vec.racing.RACING_EDP_FORECAST_MARKET_TAB, market_tabs,
                      msg=f'"{vec.racing.RACING_EDP_FORECAST_MARKET_TAB}" not found in the list of tabs {list(market_tabs.keys())}')
        self.assertIn(vec.racing.RACING_EDP_TRICAST_MARKET_TAB, market_tabs,
                      msg=f'"{vec.racing.RACING_EDP_TRICAST_MARKET_TAB}" not found in the list of tabs {list(market_tabs.keys())}')

    def test_001_add_2_different_forecast_bets_to_betslip_eg_1st2nd_runner_anyany_runners_bets(self, forecast=True):
        """
        DESCRIPTION: Add 2 different Forecast bets to betslip (eg. 1st/2nd runner, Any/Any runners bets)
        EXPECTED: Bets are added to Betslip
        """
        if forecast:
            self.place_forecast_tricast_bet_from_event_details_page(forecast=True, any_button=False, any_iteration_range=2)
            self.place_forecast_tricast_bet_from_event_details_page(forecast=True, any_button=True, any_iteration_range=2)
        else:
            self.place_forecast_tricast_bet_from_event_details_page(tricast=True, any_button=False, any_iteration_range=2)
            self.place_forecast_tricast_bet_from_event_details_page(tricast=True, any_button=True, any_iteration_range=3)

    def test_002_open_betslip_and_meanwhile_suspend_the_entire_event_in_ti_backoffice_event_level(self, event_level=True):
        """
        DESCRIPTION: Open Betslip and meanwhile suspend the entire event in TI backoffice (event level)
        EXPECTED: - Bets become suspended immediately (greyed out with 'suspended' labels across the bets)
        EXPECTED: - Notification on blue background about suspension appears at the top of Betslip
        EXPECTED: ![](index.php?/attachments/get/101694100)
        """
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section, msg='No stakes found')
        if event_level:
            self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=False)
        else:
            self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, active=False,
                                               displayed=True)
        for i in range(2):
            sleep(3)
            stake = list(singles_section.values())[i]
            result = wait_for_result(lambda: stake.suspended_stake_label.strip('"') == vec.betslip.SUSPENDED_LABEL, name='SUSPENDED label to appear', timeout=15)
            self.assertTrue(result, msg=f'{vec.betslip.SUSPENDED_LABEL} does not appear Actual content "{stake.suspended_stake_label}"')
        result = self.get_betslip_content().wait_for_specified_error(
            expected_message=vec.betslip.BELOW_MULTIPLE_DISABLED,
            timeout=10)
        self.assertTrue(result,
                        msg=f'Actual Error message "{self.get_betslip_content().error}" != expected Error message"{vec.betslip.BELOW_MULTIPLE_DISABLED}"')

    def test_003_refresh_the_pagekill_the_app_and_load_again(self):
        """
        DESCRIPTION: Refresh the page/kill the app and load again
        EXPECTED: Page is refreshed/App is up
        """
        self.device.refresh_page()
        self.site.wait_content_state(state_name='RacingEventDetails')

    def test_004_open_betslip_and_meanwhile_unsuspend_the_event_in_ti(self, event_level=True):
        """
        DESCRIPTION: Open Betslip and meanwhile unsuspend the event in TI
        EXPECTED: - Bets become active
        EXPECTED: - None of notifications about suspension are displayed to the user
        EXPECTED: ![](index.php?/attachments/get/101694099)
        """
        if event_level:
            self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)
        else:
            self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, active=True,
                                               displayed=True)
        self.site.open_betslip()
        self.assertTrue(self.site.has_betslip_opened(), msg='Failed to open Betslip')
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section, msg='No stakes found')
        for i in range(2):
            stake = list(singles_section.values())[i]
            result = wait_for_result(lambda: stake.suspended_stake_label, name='SUSPENDED label to appear', timeout=3)
            self.assertEqual(result, 'none', msg=f'Bet{i+1} is still suspended')
        result = self.get_betslip_content().wait_for_specified_error(
            expected_message=vec.betslip.BELOW_MULTIPLE_DISABLED,
            timeout=3)
        self.assertFalse(result, msg=f'Suspension message: "{vec.betslip.BELOW_MULTIPLE_DISABLED}" is still displaying')
        self.site.close_betslip()

    def test_005_repeat_steps_above_for_the_forecast_bets_and_suspension_on_market_level(self):
        """
        DESCRIPTION: Repeat steps above for the Forecast bets and suspension on Market level
        EXPECTED: Results are the same
        """
        self.test_002_open_betslip_and_meanwhile_suspend_the_entire_event_in_ti_backoffice_event_level(event_level=False)
        self.test_003_refresh_the_pagekill_the_app_and_load_again()
        self.test_004_open_betslip_and_meanwhile_unsuspend_the_event_in_ti(event_level=False)

    def test_006_repeat_steps_above_for_the_tricast_bet(self):
        """
        DESCRIPTION: Repeat steps above for the Tricast bet.
        EXPECTED: Results are the same
        """
        self.site.open_betslip()
        self.clear_betslip()
        self.test_001_add_2_different_forecast_bets_to_betslip_eg_1st2nd_runner_anyany_runners_bets(forecast=False)
        self.test_002_open_betslip_and_meanwhile_suspend_the_entire_event_in_ti_backoffice_event_level()
        self.test_003_refresh_the_pagekill_the_app_and_load_again()
        self.test_004_open_betslip_and_meanwhile_unsuspend_the_event_in_ti()
        self.test_005_repeat_steps_above_for_the_forecast_bets_and_suspension_on_market_level()
