import time
import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import normalize_name
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.football
@pytest.mark.google_analytics
@pytest.mark.event_details
@pytest.mark.other
@pytest.mark.mobile_only
@pytest.mark.safari
@pytest.mark.login
@pytest.mark.quick_bet
@pytest.mark.reg156_fix
@vtest
class Test_C12834347_Tracking_of_adding_selections_to_betslip_using_Reuse_Selection_button(BaseSportTest, BaseBetSlipTest, BaseDataLayerTest):
    """
    TR_ID: C12834347
    VOL_ID: C13815468
    NAME: Tracking of adding selections to betslip using 'Reuse Selection' button
    DESCRIPTION: This test case verifies adding of selections to Betslip using 'Reuse Selection' button
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - Betslip GA tracking documentation: https://confluence.egalacoral.com/pages/viewpage.action?pageId=91091847
    """
    keep_browser_open = True
    bet_amount = 0.1

    def test_000_preconditions(self):
        """
        DESCRIPTION: - Quick bet should be enabled in CMS > System Configuration > Structure > quickBet
        DESCRIPTION: - You should be logged in and have a bet placed via Quickbet
        """
        quick_bet = self.get_initial_data_system_configuration().get('quickBet', {})
        if not quick_bet:
            quick_bet = self.cms_config.get_system_configuration_item('quickBet')
        if not quick_bet.get('EnableQuickBet'):
            raise CmsClientException('Quick Bet is disabled in CMS')

        self.__class__.category_id = self.ob_config.football_config.category_id
        if tests.settings.backend_env == 'prod':
            additional_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_LIVE_NOW_EVENT, OPERATORS.IS_FALSE)
            event = self.get_active_events_for_category(category_id=self.category_id,
                                                        additional_filters=additional_filter)[0]
            self._logger.info(f'Found Football event "{event}"')
            self.__class__.eventID = event['event']['id']
            self.__class__.event_name = normalize_name(event['event']['name'])
            expected_market_name, outcomes = next(((market['market']['name'], market['market']['children'])
                                                  for market in event['event']['children'] if
                                                  market['market'].get('children')), (None, None))
            if not outcomes:
                raise SiteServeException('There are no available outcomes')
            self.__class__.market_name = expected_market_name if self.brand != 'ladbrokes' else expected_market_name.title()
            self.__class__.type_id = event['event']['typeId']

            selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.selection_name1, self.__class__.selection_id1 = list(selection_ids.items())[0]
            self.__class__.team1 = next(i['outcome']['name'] for i in outcomes if
                                        'price' in i['outcome']['children'][0].keys())

            self._logger.info(f'*** Found event "{self.eventID}" - "{self.event_name}" - "{self.market_name}" '
                              f'with selection id {self.selection_id1} selection "{self.selection_name1}"')
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.event_name = f'{event_params.team1} v {event_params.team2}'
            self.__class__.team1 = event_params.team1
            self.__class__.eventID = event_params.event_id
            self.__class__.selection_name1, self.__class__.selection_id1 = list(event_params.selection_ids.items())[0]
            self.__class__.type_id = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id
            self.__class__.market_name = self.expected_market_sections.match_result

        self.site.login()
        self.navigate_to_edp(event_id=self.eventID, sport_name='football')
        self.add_selection_from_event_details_to_quick_bet(selection_name=self.selection_name1,
                                                           market_name=self.market_name)

        quick_bet = self.site.quick_bet_panel.selection
        quick_bet.content.amount_form.input.value = self.bet_amount
        self.site.quick_bet_panel.add_to_betslip_button.click()
        self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False, timeout=15),
                         msg='Quick Bet is still opened')

    def test_001_place_a_bet_via_betslip__tap_reuse_selection__type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: - Place a bet via Betslip
        DESCRIPTION: - Tap 'Reuse Selection'
        DESCRIPTION: - Type 'dataLayer' in browser's console and verify GA tracking record
        EXPECTED: dataLayer.push{
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: "reuse selection"
        EXPECTED: eventCategory: "betslip"
        EXPECTED: eventLabel: "success"
        EXPECTED: ecommerce.add.products{
        EXPECTED: brand: "<<EVENT_MARKET>>"
        EXPECTED: category: "<<OPENBET_SPORT_CATEGORY_ID>>"
        EXPECTED: dimension60: "<<EVENT_ID>>"
        EXPECTED: dimension61: "<<SELECTION_ID>>"
        EXPECTED: dimension62: "<<IN-PLAY_STATUS>>"
        EXPECTED: dimension63: "<<CUSTOMER BUILT>>"
        EXPECTED: dimension64: "<<LOCATION>>"
        EXPECTED: dimension65: "<<MODULE>>"
        EXPECTED: name: "<<EVENT_NAME>>"
        EXPECTED: variant: "<<OPENBET_TYPE_ID>>"
        EXPECTED: }}
        """
        self.site.open_betslip()
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()
        reuse_selection_button = self.site.bet_receipt.footer.reuse_selection_button
        self.assertTrue(reuse_selection_button, msg='There is no "Reuse Selection" button on Bet receipt')

        reuse_selection_button.click()

        self.assertTrue(self.site.has_betslip_opened(), msg='Betslip is not opened, but was expected to be opened')

        time.sleep(2)  # Need to wait for dataLayer update
        self.verify_ga_tracking_record(brand=self.market_name.title(),
                                       category=self.category_id,
                                       event_id=self.eventID,
                                       selection_id=self.selection_id1,
                                       inplay_status=0, customer_built=0,
                                       location='betslip',
                                       module='edp',
                                       name=self.event_name,
                                       variant=self.type_id,
                                       event='trackEvent',
                                       event_action='reuse selection',
                                       event_category='betslip',
                                       event_label='success',
                                       stream_active=False,
                                       stream_ID=None,
                                       normalize_name=True,
                                       dimension166='reuse')
