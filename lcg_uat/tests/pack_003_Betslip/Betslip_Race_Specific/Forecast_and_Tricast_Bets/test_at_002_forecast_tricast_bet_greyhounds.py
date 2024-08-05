import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
# @pytest.mark.prod
@pytest.mark.betslip
@pytest.mark.racing
@pytest.mark.greyhounds
@pytest.mark.forecast_tricast
@pytest.mark.event_details
@pytest.mark.medium
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_AT_002_greyhounds_forecast_tricast_bet(BaseBetSlipTest, BaseRacing):
    """
    VOL_ID: C9698438
    NAME: Verify placing forecast/tricast bet on greyhounds events
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event with forecast and tricast enabled
        """
        event_params = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=3,
                                                                    forecast_available=True,
                                                                    tricast_available=True)
        self.__class__.event_off_time = event_params.event_off_time
        self.__class__.created_event_name = f'{self.event_off_time} {self.greyhound_autotest_name_pattern.upper()}'

    def test_001_login(self):
        """
        DESCRIPTION: Login as a user that has sufficient funds to place a bet
        """
        self.site.login(username=tests.settings.betplacement_user, async_close_dialogs=False)
        self.__class__.balance = self.site.header.user_balance

    def test_002_go_to_greyhounds_racing_page(self):
        """
        DESCRIPTION: Tap Greyhounds Racing in menu carousel
        """
        self.site.open_sport(name='Greyhounds', timeout=5)

    def test_003_open_event(self):
        """
        DESCRIPTION: Open event
        """
        click_button = self.site.greyhound.tabs_menu.click_button(button_name=vec.sb.SPORT_DAY_TABS.today.upper())
        self.assertTrue(click_button, msg=f'"{vec.sb.SPORT_DAY_TABS.today}" is not selected after click')

        if self.brand != 'ladbrokes':
            event = self.get_event_from_next_races_module(event_name=self.created_event_name)
        else:
            section_name = vec.racing.UK_AND_IRE_TYPE_NAME
            row_name = self.greyhound_autotest_name_pattern
            sections = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(sections, msg='No event section found on Racing page')
            section = sections.get(section_name)
            self.assertTrue(section, msg=f'Section "{section_name}" was not found in "{sections.keys()}"')
            section.expand()
            rows = section.items_as_ordered_dict
            self.assertTrue(rows, msg=f'No one row was found in section: "{section_name}"')
            row = rows.get(row_name)
            self.assertTrue(row, msg=f'"{row_name}" row was not found in "{rows.keys()}"')
            events = row.items_as_ordered_dict
            self.assertTrue(events, msg=f'No one event was found in row: "{row_name}"')
            event = events.get(self.event_off_time)
            self.assertTrue(event, msg=f'Event with off time "{self.event_off_time}" was not found in "{events.keys()}"')

        event.click()
        self.site.wait_content_state(state_name='GreyHoundEventDetails')

    def test_004_place_forecast_tricast_bet(self):
        """
        DESCRIPTION: Place Forecast Tricast bet
        """
        self.place_forecast_tricast_bet_from_event_details_page(sport_name='greyhound-racing', tricast=True)
        self.site.open_betslip()
        self.place_single_bet()

    def test_005_check_balance(self):
        """
        DESCRIPTION: Check user balance has changed
        """
        self.check_bet_receipt_is_displayed()
        self.verify_user_balance(self.balance - self.bet_amount, timeout=5)
