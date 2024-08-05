import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
import voltron.environments.constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.races
@pytest.mark.forecast_tricast
@pytest.mark.event_details
@pytest.mark.desktop
@pytest.mark.safari
@vtest
class Test_C10474864_Verify_Forecast___Tricast_tabs_displaying_on_Horse_Racing_EDP_depending_on_checkboxes_in_Openbet_TI(BaseRacing):
    """
    TR_ID: C10474864
    NAME: Verify Forecast / Tricast tabs displaying on Horse Racing EDP depending on checkboxes in Openbet TI
    DESCRIPTION: This test case verifies  Forecast / Tricast tabs displaying depending on checkboxes in Openbet TI
    PRECONDITIONS: 1. HR event with Win or Each Way market exists.
    PRECONDITIONS: 2. Forecast and Tricast checkboxes are active on market level for Win or Each Way market for event from precondition 1
    PRECONDITIONS: 3. OB TI:
    PRECONDITIONS: - Coral: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - Ladbrokes: https://confluence.egalacoral.com/display/SPI/Ladbrokes+Environments#LadbrokesEnvironments-LadbrokesOB/IMSendpoints
    PRECONDITIONS: 4. User is on Event details page for event from precondition 1
    PRECONDITIONS: 5. To verify SS response check EventToOutcomeForEvent
    PRECONDITIONS: NOTE:
    PRECONDITIONS: 5 flags from SS respone responsible for Forecast/Tricast:
    PRECONDITIONS: ncastTypeCodes="CT,SF,CF,RF,TC,"
    PRECONDITIONS: CT - Combinational Tricast
    PRECONDITIONS: SF - Straight Forecast
    PRECONDITIONS: CF - Combinational Forecast
    PRECONDITIONS: RF - Reverse Forecast
    PRECONDITIONS: TC - Straight Tricast
    """
    keep_browser_open = True

    def get_market_for_event_from_ss(self, event_id: str):
        """
        Gets event for given event_id from SS response
        :param event_id: specifies event id
        :return: event
        """
        resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
        ncastTypeCodes = resp[0]['event']['children'][0]['market']
        return ncastTypeCodes

    def test_000_preconditions(self):
        """
        DESCRIPTION: TST2/STG2: Create racing event with Tricast/Forecast
        """
        event_params = self.ob_config.add_UK_racing_event(number_of_runners=3, forecast_available=True,
                                                          tricast_available=True)
        selection_ids = event_params.selection_ids
        self.__class__.eventID = event_params.event_id
        self.__class__.selection_names = selection_ids.keys()
        self.__class__.marketID = self.ob_config.market_ids[event_params.event_id]
        self.__class__.market_template_id = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.market_template_id
        self.__class__.expected_tab_names = vec.racing.RACING_EDP_MARKET_TABS_NAMES
        self.__class__.forecast_tab_name = vec.racing.RACING_EDP_FORECAST_MARKET_TAB
        self.__class__.tricast_tab_name = vec.racing.RACING_EDP_TRICAST_MARKET_TAB

    def test_001_verify_forecasttricast_tabs_on_edp(self):
        """
        DESCRIPTION: Verify Forecast/Tricast tabs on EDP
        EXPECTED: * Forecast and Tricast tabs are present on
        EXPECTED: * All 5 flags present in  SS response:
        EXPECTED: ncastTypeCodes="CT,SF,CF,RF,TC,"
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        racing_event_tab_content = self.site.racing_event_details.tab_content.event_markets_list
        actual_tabs_names = racing_event_tab_content.market_tabs_list.items_names
        self.assertEqual(actual_tabs_names, self.expected_tab_names,
                         msg=f'Actual tab order "{actual_tabs_names}"" does not match expected "{self.expected_tab_names}"')
        typeCodes = self.get_market_for_event_from_ss(event_id=self.eventID).get('ncastTypeCodes', '')
        self.assertEqual(typeCodes, 'CT,SF,CF,RF,TC,',
                         msg=f'Actual flags present in SS response {typeCodes} are not the same as expected "CT,SF,CF,RF,TC,"')

    def test_002_in_ti_uncheck_forecast_tabrefresh_app(self):
        """
        DESCRIPTION: In TI uncheck Forecast tab.
        DESCRIPTION: Refresh app
        EXPECTED: * Forecast tab in not present on EDP
        EXPECTED: * flags present in  SS response:
        EXPECTED: ncastTypeCodes="CT,TC,"
        """
        self.ob_config.change_racing_market_forecast_tricast_status(event_id=self.eventID,
                                                                    market_id=self.marketID,
                                                                    market_template_id=self.market_template_id,
                                                                    category_id=self.ob_config.backend.ti.horse_racing.category_id,
                                                                    forecast_status=False,
                                                                    tricast_status=True)
        result = wait_for_result(lambda: self.get_market_for_event_from_ss(event_id=self.eventID).get('ncastTypeCodes', '') == 'CT,TC,',
                                 name=f'Button to have name "CT,TC,"',
                                 expected_result=True,
                                 timeout=3)
        self.assertTrue(result, msg=f'Actual flags present in SS response are not the same as expected "CT,TC,"')

        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        racing_event_tab_content = self.site.racing_event_details.tab_content.event_markets_list
        actual_tabs_names = racing_event_tab_content.market_tabs_list.items_names
        self.assertNotIn(self.forecast_tab_name, actual_tabs_names,
                         msg=f'Tab "{self.forecast_tab_name}" is still present on the UI "{actual_tabs_names}"')

    def test_003_in_ti_uncheck_tricast_checkboxrefresh_app(self):
        """
        DESCRIPTION: In TI uncheck Tricast checkbox.
        DESCRIPTION: Refresh app
        EXPECTED: * Tricast tab is not present on EDP
        EXPECTED: *  'ncastTypeCodes' parameter is not present in SS response
        """
        self.ob_config.change_racing_market_forecast_tricast_status(event_id=self.eventID,
                                                                    market_id=self.marketID,
                                                                    market_template_id=self.market_template_id,
                                                                    category_id=self.ob_config.backend.ti.horse_racing.category_id,
                                                                    forecast_status=False,
                                                                    tricast_status=False)

        result = wait_for_result(lambda: 'ncastTypeCodes' not in self.get_market_for_event_from_ss(event_id=self.eventID).keys(),
                                 name=f'ncastTypeCodes should not be in SS response"',
                                 expected_result=True,
                                 timeout=3)
        self.assertTrue(result, msg=f'Actual flags present in SS response are not the same as expected "CT,TC,"')

        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        racing_event_tab_content = self.site.racing_event_details.tab_content.event_markets_list
        actual_tabs_names = racing_event_tab_content.market_tabs_list.items_names
        self.assertNotIn(self.tricast_tab_name, actual_tabs_names,
                         msg=f'Tab "{self.tricast_tab_name}" is still present on the UI "{actual_tabs_names}"')

    def test_004_in_ti_check_only_forecast_checkboxrefresh_app(self):
        """
        DESCRIPTION: In TI check only Forecast checkbox.
        DESCRIPTION: Refresh app
        EXPECTED: *Forecast tab is present on EDP
        EXPECTED: * flags present in  SS response:
        EXPECTED: ncastTypeCodes="SF,CF,RF,"
        """
        self.ob_config.change_racing_market_forecast_tricast_status(event_id=self.eventID,
                                                                    market_id=self.marketID,
                                                                    market_template_id=self.market_template_id,
                                                                    category_id=self.ob_config.backend.ti.horse_racing.category_id,
                                                                    forecast_status=True,
                                                                    tricast_status=False)
        wait_for_result(lambda: 'ncastTypeCodes' in self.get_market_for_event_from_ss(event_id=self.eventID).keys(),
                        name=f'ncastTypeCodes should be in SS response"',
                        expected_result=True,
                        timeout=3)
        result = wait_for_result(lambda: self.get_market_for_event_from_ss(event_id=self.eventID).get('ncastTypeCodes', '') == 'SF,CF,RF,',
                                 name=f'Button to have name "SF,CF,RF,"',
                                 expected_result=True,
                                 timeout=3)
        self.assertTrue(result, msg=f'Actual flags present in SS response are not the same as expected "SF,CF,RF,"')

        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        racing_event_tab_content = self.site.racing_event_details.tab_content.event_markets_list
        actual_tabs_names = racing_event_tab_content.market_tabs_list.items_names
        self.assertIn(self.forecast_tab_name, actual_tabs_names,
                      msg=f'Tab "{self.forecast_tab_name}" is not present on the UI "{actual_tabs_names}"')
        ncastTypeCodes = self.get_market_for_event_from_ss(event_id=self.eventID)['ncastTypeCodes']
        self.assertEqual(ncastTypeCodes, 'SF,CF,RF,',
                         msg=f'Actual flags present in SS response {ncastTypeCodes} are not the same as expected "SF,CF,RF"')
