import re
import pytest
from crlat_siteserve_client.constants import LEVELS, OPERATORS, ATTRIBUTES
from crlat_siteserve_client.siteserve_client import exists_filter, simple_filter
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.critical
@pytest.mark.bet_placement
@pytest.mark.open_bets
@pytest.mark.forecast_tricast
@pytest.mark.tricast
@pytest.mark.racing
@pytest.mark.desktop
@pytest.mark.bet_history_open_bets
@pytest.mark.pipelines
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C10375630_Verify_Forecast_Tricast_bet_placing(BaseCashOutTest, BaseRacing):
    """
    TR_ID: C10375630
    NAME: Verify Forecast/Tricast bet placing
    DESCRIPTION: This test case verifies Forecast/Tricast bet placing
    PRECONDITIONS: Login into Application
    PRECONDITIONS: Navigate to 'HR/Greyhounds' page
    PRECONDITIONS: Choose event -> see that Forecast/Tricast Tab is available
    PRECONDITIONS: Navigate to Forecast/Tricast Tab
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: TST2/STG2: Create racing event with Tricast/Forecast, PROD: Find racing event with Tricast/Forecast
        """
        if tests.settings.backend_env == 'prod':
            additional_filter = exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.NCAST_TYPE_CODES,
                                                                          OPERATORS.INTERSECTS, 'CF,TC'))

            event = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                        additional_filters=additional_filter)[0]
            outcomes = event['event']['children'][0]['market']['children']

            self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes[:3] if
                                            'Unnamed' not in i['outcome']['name']}
            start_time_local = self.convert_time_to_local(date_time_str=event['event']['startTime'],
                                                          ob_format_pattern=self.ob_format_pattern)
            search = re.search(r'[aA-zZ\s]+', event['event']['name'])
            type_name = search.group(0).lstrip() if search.group(0) is not None else ''

            self.__class__.created_event_name = f'{type_name} {start_time_local}'
            self.__class__.eventID = event['event']['id']
            self._logger.info(f'*** Found Horse racing event with id "{self.eventID}"')
        else:
            event_params = self.ob_config.add_UK_racing_event(number_of_runners=2,
                                                              forecast_available=True)
            self.__class__.event_start_time = event_params.event_date_time
            self.__class__.selection_ids = event_params.selection_ids
            start_time_local = self.convert_time_to_local(date_time_str=self.event_start_time)
            self.__class__.created_event_name = f'{self.horseracing_autotest_uk_name_pattern} {start_time_local}'
            self.__class__.eventID = event_params.event_id
        self.__class__.selection_names = self.selection_ids.keys()
        self.site.login(username=tests.settings.betplacement_user, async_close_dialogs=False)
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')

    def test_001_add_tote_bets_to_the_betslip_in_forecast_tricast_tab(self):
        """
        DESCRIPTION: Add tote bets to the Betslip in Forecast/Tricast Tab
        EXPECTED: Selections are added to the Betslip
        """
        expected_selection_name = self.place_forecast_tricast_bet_from_event_details_page(sport_name='horse-racing', forecast=True)
        self.site.open_betslip()
        self.__class__.sections = self.get_betslip_sections().Singles
        self.assertTrue(self.sections, msg='No stakes found')
        for actual_selection in self.sections:
            self.assertIn(actual_selection.strip(), expected_selection_name,
                          msg=f'Actual selection name: "{actual_selection}" is not in expected selections: '
                          f'"{expected_selection_name}"')

    def test_002_add_stake_value(self):
        """
        DESCRIPTION: Add Stake value
        EXPECTED: 'Stake value' is added
        """
        stake_name, stake = list(self.sections.items())[0]
        self.enter_stake_amount(stake=(stake_name, stake))
        self.__class__.betnow_btn = self.get_betslip_content().bet_now_button
        self.assertTrue(self.betnow_btn.is_enabled(), msg='Bet Now button is disabled')

    def test_003_tap_place_bet_button_and_verify_that_the_staked_bets_in_the_betslip_are_placed(self):
        """
        DESCRIPTION: Tap 'Place Bet' button and verify that the staked bets in the betslip are placed
        EXPECTED: The staked bets in the betslip are placed
        """
        self.betnow_btn.click()

    def test_004_verify_that_the_bet_receipt_is_displayed_on_successful_bet_placement(self):
        """
        DESCRIPTION: Verify that the bet receipt is displayed on successful bet placement
        EXPECTED: The bet receipt is displayed on successful bet placement
        """
        self.check_bet_receipt_is_displayed()
