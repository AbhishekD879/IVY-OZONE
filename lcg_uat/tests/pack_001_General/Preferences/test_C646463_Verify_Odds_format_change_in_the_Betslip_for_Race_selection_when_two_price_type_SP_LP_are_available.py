import pytest
import voltron.environments.constants as vec
import tests
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.portal_dependant
@pytest.mark.user_account
@pytest.mark.preferences
@pytest.mark.betslip
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.navigation
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C646463_Verify_Odds_format_change_in_the_Betslip_for_Race_selection_when_two_price_type_SP_LP_are_available(BaseBetSlipTest):
    """
    TR_ID: C646463
    NAME: Verify Odds format change in the Betslip for <Race> selection when two price type SP, LP are available
    """
    enable_bs_performance_log = True
    keep_browser_open = True
    selection = None
    prices = {0: '1/4'}

    def get_number_of_build_bet_requests(self) -> int:
        """
        Method is used only to get number of buildBet requests
        :return: Number of buildBet requests in performance log
        """
        from time import sleep
        sleep(1.5)
        log = self.device.get_performance_log()
        expected_url = f'{tests.settings.BETTINGMS}v1/buildBet'
        number_of_build_bet_requests = 0
        for entry in log:
            for entry_field in entry:
                for entry_type, entry_value in entry_field.items():
                    if entry_type == 'message':
                        url = entry_value.\
                            get('message', {}).\
                            get('params', {}).\
                            get('request', {}).\
                            get('url', '')
                        number_of_build_bet_requests += 1 if url == expected_url else 0

        self._logger.info(f'*** Found "{number_of_build_bet_requests}" buildBet requests')
        return number_of_build_bet_requests

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event and Login
        EXPECTED: Event is created
        EXPECTED: User is logged in
        """
        if tests.settings.backend_env == 'prod':
            additional_filter = exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.PRICE_TYPE_CODES, OPERATORS.INTERSECTS, 'LP'))
            events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                         additional_filters=additional_filter,
                                                         all_available_events=True)
            selection_id = None
            for event in events:
                market = next((market for market in event['event']['children']
                               if market['market']['templateMarketName'] == 'Win or Each Way' and
                               market['market'].get('children')), None)
                if not market:
                    continue
                outcomes_resp = market['market']['children']
                selection_id = None
                for outcome in outcomes_resp:
                    for child in outcome.get('outcome', {}).get('children', []):
                        if child.get('price') and 'LP' in child.get('price', {}).get('priceType', ''):
                            selection_id = outcome['outcome']['id']
                            break
                    if selection_id:
                        break
                if selection_id:
                    break
            if not selection_id:
                raise SiteServeException('There are no selections with LP prices')
            self.__class__.selection = selection_id
        else:
            self.__class__.selection = list(self.ob_config.add_UK_racing_event(number_of_runners=1,
                                                                               lp_prices=self.prices).selection_ids.values())[0]
        self._logger.info(f'*** Using selection id: "{self.selection}"')
        self.site.login(async_close_dialogs=False, timeout_close_dialogs=5)
        format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_FRAC)
        self.assertTrue(format_changed, msg='Odds format is not changed to fractional')

    def test_001_add_race_selection_that_contains_sp_and_lp_price_type_to_the_betslip_and_open_it(self):
        """
        DESCRIPTION: Add <Race> selection that contains SP and LP price type to the Betslip and open it
        EXPECTED: Selection is added
        EXPECTED: Dropdown with price types is displayed for the selection
        EXPECTED: LP is selected by default
        """
        self.open_betslip_with_selections(selection_ids=self.selection)

        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        odds = stake.odds
        self.assertRegexpMatches(odds, self.fractional_pattern,
                                 msg=f'Stake odds value "{odds}" not match fractional pattern: "{self.fractional_pattern}"')

    def test_002_tap_on_right_menu_icon_and_select_setting_item(self):
        """
        DESCRIPTION: **Coral:**
        DESCRIPTION: Tap on Right menu icon and select 'Setting' item
        DESCRIPTION: **Ladbrokes:**
        DESCRIPTION: Tap an avatar or balance button
        EXPECTED: **Coral:**
        EXPECTED: * 'Preferences' page is opened
        EXPECTED: * 'Select Odds Format' option is present with buttons 'Fractional' and 'Decimal'
        EXPECTED: * By default 'Fractional' button is selected, all 'Price/Odds' buttons display prices in fractional format
        EXPECTED: **Ladbrokes:**
        EXPECTED: * Settings page is opened
        EXPECTED: * 'Select Odds Format' option is present with buttons 'Fractional' and 'Decimal'
        EXPECTED: * By default 'Fractional' button is selected, all 'Price/Odds' buttons display prices in fractional format
        """
        self.site.close_betslip()
        self.navigate_to_page(name='settings')
        self.site.wait_content_state('Settings')
        self.assertTrue(self.site.settings.fractional_btn.is_selected(),
                        msg='Fractional option is not active by default')

    def test_003_switch_to_decimal_format_and_verify_changes_in_the_betslip(self):
        """
        DESCRIPTION: Switch to Decimal format and verify changes in the Betslip
        EXPECTED: 'Decimal' switcher is selected
        EXPECTED: New 'buildBet' request is sent
        EXPECTED: Price format is changed from Fractional to Decimal within dropdown in the Betslip
        """
        initial_build_bet_request_number = self.get_number_of_build_bet_requests()

        self.site.settings.decimal_btn.click()
        self.assertTrue(self.site.settings.decimal_btn.is_selected(),
                        msg='Decimal option is not active after selection')

        new_build_bet_request_number = self.get_number_of_build_bet_requests()
        self.assertTrue(new_build_bet_request_number > initial_build_bet_request_number,
                        msg=f'New "buildBet" request was not sent')

        self.site.header.bet_slip_counter.click()

        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        odds = stake.odds
        self.assertRegexpMatches(odds, self.decimal_pattern,
                                 msg=f'Stake odds number "{odds}" not match decimal pattern "{self.decimal_pattern}"')

    def test_004_switch_to_fractional_format_and_verify_changes_in_the_betslip(self):
        """
        DESCRIPTION: Switch to Fractional format and verify changes in the Betslip
        EXPECTED: 'Fractional' switcher is selected
        EXPECTED: New 'buildBet' request is sent
        EXPECTED: Price format is changed from Decimal to Fractional within dropdown in the Betslip
        """
        self.site.close_betslip()
        self.navigate_to_page(name='settings')
        self.site.wait_content_state('Settings')
        initial_build_bet_request_number = self.get_number_of_build_bet_requests()

        self.site.settings.fractional_btn.click()
        self.assertTrue(self.site.settings.fractional_btn.is_selected(),
                        msg='Fractional option is not active after selection')

        new_build_bet_request_number = self.get_number_of_build_bet_requests()
        self.assertTrue(new_build_bet_request_number > initial_build_bet_request_number,
                        msg=f'New "buildBet" request was not sent')

        self.site.header.bet_slip_counter.click()

        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        odds = stake.odds
        self.assertRegexpMatches(odds, self.fractional_pattern,
                                 msg=f'Stake odds number "{odds}" not match fractional pattern "{self.fractional_pattern}"')
