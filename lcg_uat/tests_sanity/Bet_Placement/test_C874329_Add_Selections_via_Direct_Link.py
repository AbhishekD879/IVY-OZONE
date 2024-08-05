import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter, simple_filter
from crlat_siteserve_client.utils.date_time import get_date_time_as_string
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry, wait_fixed, retry_if_exception_type, stop_after_attempt

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@pytest.mark.bet_placement
@pytest.mark.deeplink
@pytest.mark.desktop
@pytest.mark.login
@pytest.mark.safari
@pytest.mark.sanity
@vtest
class Test_C874329_Add_Selections_via_Direct_Link(BaseBetSlipTest):
    """
    TR_ID: C874329
    NAME: Add Selections via Direct Link
    DESCRIPTION: This test case verifies how one/multiple single selections can be added to the Bet slip via direct link
    PRECONDITIONS: **In order to test adding selections to the Bet Slip via direct link the following remote URL pattern should be used:
    PRECONDITIONS: {invictusAppDomain.com}/betslip/add/{outcomeId},{outcomeId},...,{outcomeId}
    PRECONDITIONS: for example:
    PRECONDITIONS: **https://invictus.coral.co.uk/betslip/add/XXXXXX,XXXXXX,...,XXXXXX - *use this link for testing this functionality on Oxygen application for adding multiple selections***
    PRECONDITIONS: ***OR***
    PRECONDITIONS: **https://invictus.coral.co.uk/betslip/add/XXXXXX - *use this link for testing this functionality on Oxygen application for adding one selection***
    PRECONDITIONS: To find selection Id type 'Buildbet' in Network
    """
    keep_browser_open = True
    end_date = f'{get_date_time_as_string(days=2)}T00:00:00.000Z'

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(wait=30),
           retry=retry_if_exception_type((StaleElementReferenceException, VoltronException)), reraise=True)
    def get_sp_selections(self):
        """
        get sp selections
        """
        additional_filter = exists_filter(LEVELS.EVENT,
                                          simple_filter(LEVELS.MARKET, ATTRIBUTES.PRICE_TYPE_CODES,
                                                        OPERATORS.INTERSECTS, 'SP'))
        sp_events = self.get_active_events_for_category(additional_filters=additional_filter,
                                                        category_id=self.ob_config.horseracing_config.category_id)
        event, self.__class__.selection_id, outcomes_resp = None, None, None
        for event in sp_events:
            market = next((market for market in event['event']['children']
                           if market['market']['templateMarketName'] == 'Win or Each Way' and
                           market['market'].get('children')), None)
            if not market:
                continue
            outcomes_resp = market['market']['children']
            for outcome in outcomes_resp:
                if not outcome['outcome'].get(
                        'children'):  # outcomes that does not have children are usually outcomes with SP prices
                    if 'Unnamed' in outcome.get('outcome', {}).get('name', ''):
                        continue
                    self.selection_id = outcome['outcome']['id']
                    break
            if self.selection_id:
                break

        if not self.selection_id:
            raise SiteServeException(f'There are no outcomes with SP prices')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Creating test event
        """
        if tests.settings.backend_env == 'prod':
            self.__class__.selection_ids = self.get_active_event_selections_for_category(category_id=self.ob_config.football_config.category_id)
            self._logger.info(f'Football outcomes "{self.selection_ids}"')

            additional_filter = exists_filter(LEVELS.EVENT, simple_filter(
                LEVELS.MARKET, ATTRIBUTES.PRICE_TYPE_CODES, OPERATORS.INTERSECTS, 'LP'))

            events = self.get_active_events_for_category(additional_filters=additional_filter,
                                                         category_id=self.ob_config.horseracing_config.category_id,
                                                         all_available_events=True)
            event, outcomes_lp, outcomes_resp = None, None, None
            for event in events:
                market = next((market for market in event['event']['children']
                               if market['market']['templateMarketName'] == 'Win or Each Way' and
                               market['market'].get('children')), None)
                if not market:
                    continue
                outcomes_resp = market['market']['children']
                for outcome in outcomes_resp:
                    for child in outcome.get('outcome', {}).get('children', []):
                        if child.get('price') and 'LP' in child.get('price', {}).get('priceType', ''):
                            outcomes_lp = outcomes_resp
                            break
                    if outcomes_lp:
                        break
                if outcomes_lp:
                    break

            if not outcomes_lp:
                raise SiteServeException(f'There are no outcomes with LP prices')

            all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes_lp
                                 if 'Unnamed' not in i['outcome']['name'] and 'SP' not in i['outcome']['name']}
            if not all_selection_ids:
                raise SiteServeException('There is no available selection id with LP price')
            self.__class__.selection_sp_lp_ids = list(all_selection_ids.values())[0]
            self._logger.info(f'*** Horseracing event with LP outcomes "{self.selection_sp_lp_ids}"')
            self.get_sp_selections()
            self.__class__.selection_sp_ids = self.selection_id
            self._logger.info(f'*** Horseracing event with SP priced outcomes "{self.selection_sp_ids}"')
        else:
            self.__class__.selection_ids = self.ob_config.add_autotest_premier_league_football_event().selection_ids

            racing_event = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices={0: '3/5'}, sp=True)
            self.__class__.selection_sp_lp_ids = list(racing_event.selection_ids.values())[0]

            racing_sp_event = self.ob_config.add_UK_racing_event(number_of_runners=1, sp=True)
            self.__class__.selection_sp_ids = list(racing_sp_event.selection_ids.values())[0]

    def test_001_enter_direct_url_with_active_outcome_ids__outcome_status_code_a_in_address_bar_press_enter_key(self):
        """
        DESCRIPTION: Enter direct URL with active outcome id('s) ( **'outcomeStatusCode'** ='A') in address bar -> press Enter key
        EXPECTED: 1. Oxygen app with Bet Slip page is opened
        EXPECTED: 2.  Added selection(s) are shown in the Bet Slip
        EXPECTED: 3.  Corresponding 'Multiples'/(Before OX98'Forecasts/Tricasts') selections are present and shown correctly (if available)
        EXPECTED: 4.  Numeric keyboard with 'quick stakes' buttons are shown if one selection was added (before OX100)
        """
        self.open_betslip_with_selections(selection_ids=list(self.selection_ids.values())[0])
        #  Numeric keyboard is not shown in versions after OX100

    def test_002_log_in_place_bets_for_added_selections(self):
        """
        DESCRIPTION: Log in -> place bet(s) for added selection(s)
        EXPECTED: Bet(s) are placed successfully
        """
        self.site.close_betslip()
        self.site.login()
        self.site.open_betslip()
        self.place_and_validate_single_bet()
        self.check_bet_receipt_is_displayed()
        self.__class__.expected_betslip_counter_value = 0
        self.site.bet_receipt.footer.click_done()

        self.site.logout()

    def test_003_choose_any_race_event_with_pricetypecodessplp(self):
        """
        DESCRIPTION: Choose any <Race> event with **'priceTypeCodes'**='SP,LP'
        """
        # done in preconditions

    def test_004_enter_direct_url_with_active_outcome_ids_outcome_status_code_a_in_address_bar__press_enter_key(self):
        """
        DESCRIPTION: Enter direct URL with active outcome id('s) ( **'outcomeStatusCode'** ='A') in address bar -> press Enter key
        EXPECTED: 1.  Bet Slip page is opened automatically
        EXPECTED: 2.  Added selection(s) are shown in the Bet Slip
        EXPECTED: 3.  'LP' part of added selection(s) are shown by default
        EXPECTED: 4.  Dropdown control which allows switching between LP and SP parts is shown for each selection
        EXPECTED: 5.  Corresponding 'Multiples'/(Before OX98: 'Forecasts/Tricasts' selections are present and shown correctly within bet slip (if available)
        EXPECTED: 6.  Numeric keyboard with 'quick stakes' buttons are shown if one selection was added
        """
        self.open_betslip_with_selections(selection_ids=self.selection_sp_lp_ids)

        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section, msg='*** No stakes found')
        stake_name, stake = list(singles_section.items())[0]
        selected_option = stake.odds
        self.assertRegexpMatches(selected_option, r'^(\d+)\/(\d+)|\d+.\d{2}',
                                 msg=f'"LP" part is not selected, have "{selected_option}" instead')

        #  Numeric keyboard is not shown in versions after OX100

    def test_005_log_in_place_bets_for_added_selections(self):
        """
        DESCRIPTION: Log in -> place bet(s) for added selection(s)
        EXPECTED: Bet(s) are placed successfully
        """
        self.test_002_log_in_place_bets_for_added_selections()

    def test_006_choose_race_event_with_pricetypecodessp(self):
        """
        DESCRIPTION: Choose <Race> event with **'priceTypeCodes'**='SP'
        """
        #  done in preconditions

    def test_007_enter_direct_url_with_active_outcome_ids_outcome_status_code_a_in_address_bar_press_enter_key(self):
        """
        DESCRIPTION: Enter direct URL with active outcome id('s) ( **'outcomeStatusCode'** ='A') in address bar -> press Enter key
        EXPECTED: 1.  Bet Slip page is opened automatically
        EXPECTED: 2.  Added selection(s) with all detailed information are displayed
        EXPECTED: 3.  'SP' price is shown for such selections
        EXPECTED: 4.  Corresponding 'Multiples'/(Before OX98 'Forecasts/Tricasts' selections are present and shown correctly within bet slip (if available)
        EXPECTED: 5.  Numeric keyboard with quick stakes' buttons are shown if one selection was added (before OX 100)
        """
        self.open_betslip_with_selections(selection_ids=self.selection_sp_ids)
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section, msg='*** No stakes found')
        stake_name, stake = list(singles_section.items())[0]
        selected_option = stake.odds
        self.assertEqual(selected_option, 'SP', msg=f'"SP" is not selected,  have "{selected_option}" instead')

    def test_008_log_in_place_bets_for_added_selections(self):
        """
        DESCRIPTION: Log in -> place bet(s) for added selection(s)
        EXPECTED: Bet(s) are placed successfully
        """
        self.test_002_log_in_place_bets_for_added_selections()
