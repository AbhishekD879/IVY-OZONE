import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import normalize_name
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.quick_bet
@vtest
class Test_C12834350_Tracking_of_adding_selections_to_Quickbet_using_Reuse_Selection_button(BaseSportTest,
                                                                                            BaseBetSlipTest,
                                                                                            BaseDataLayerTest):
    """
    TR_ID: C12834350
    NAME: Tracking of adding selections to Quickbet using 'Reuse Selection' button
    DESCRIPTION: This test case verifies adding of selections to Betslip using 'Reuse Selection' button
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - Quick Bet GA tracking documentation: https://confluence.egalacoral.com/pages/viewpage.action?pageId=91470520
    PRECONDITIONS: - Quick bet should be enabled in CMS > System Configuration > Structure > quickBet
    PRECONDITIONS: - You should be logged in and have a bet placed via Quickbet
    """
    keep_browser_open = True
    expected_response = {'event': "trackEvent",
                         'eventAction': "add to quickbet",
                         'eventCategory': "quickbet",
                         'eventLabel': "success",
                         'ecommerce.add.products': {
                             'brand': "<<EVENT_MARKET>>",
                             'category': "<<OPENBET_SPORT_CATEGORY_ID>>",
                             'dimension60': "<<EVENT_ID>>",
                             'dimension61': "<<SELECTION_ID>>",
                             'dimension62': "0",
                             'dimension63': "0",
                             'dimension64': "MAIN",
                             'dimension65': "edp",
                             'name': "<<EVENT_NAME>>",
                             'variant': "<<OPENBET_TYPE_ID>>"
                         }}

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
            event = self.get_active_events_for_category(category_id=self.category_id)[0]
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
            self.__class__.market_name = event_params.ss_response["event"]["children"][0]["market"][
                "templateMarketName"]

        self.site.login()
        self.navigate_to_edp(event_id=self.eventID, sport_name='football')
        self.__class__.location = self.site.sport_event_details.markets_tabs_list.current
        self.add_selection_from_event_details_to_quick_bet(selection_name=self.selection_name1)

        sleep(2)
        quick_bet = self.site.quick_bet_panel.selection
        quick_bet.content.amount_form.input.value = self.bet_amount
        self.site.quick_bet_panel.place_bet.click()
        bet_receipt = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
        self.assertTrue(bet_receipt, msg='Bet Receipt is not displayed')

    def test_001___tap_reuse_selection_button__type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: - Tap 'Reuse Selection' button
        DESCRIPTION: - Type 'dataLayer' in browser's console and verify GA tracking record
        EXPECTED: dataLayer.push{
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: "add to quickbet"
        EXPECTED: eventCategory: "quickbet"
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
        sleep(5)
        actual_response = self.get_data_layer_specific_object(object_key='eventAction', object_value='add to quickbet')
        self.assertEqual(self.expected_response.get("eventAction"), actual_response.get("eventAction"),
                         msg=f'Expected eventAction value "{self.expected_response.get("eventAction")}" is not '
                             f'same as actual eventAction value "{actual_response.get("eventAction")}"')
        self.assertEqual(self.expected_response.get("event"), actual_response.get("event"),
                         msg=f'Expected event value "{self.expected_response.get("event")}" is not '
                             f'same as actual event value "{actual_response.get("event")}"')
        self.assertEqual(self.expected_response.get("eventCategory"), actual_response.get("eventCategory"),
                         msg=f'Expected eventCategory value "{self.expected_response.get("eventCategory")}" is not '
                             f'same as actual eventCategory value "{actual_response.get("eventCategory")}"')
        self.assertEqual(self.expected_response.get("eventLabel"), actual_response.get("eventLabel"),
                         msg=f'Expected eventLabel value "{self.expected_response.get("eventLabel")}" is not '
                             f'same as actual eventLabel value "{actual_response.get("eventLabel")}"')
        self.assertTrue(actual_response.get("ecommerce")["add"]["products"][0]["brand"],
                        msg=f'"{actual_response.get("ecommerce")["add"]["products"][0]["brand"]}" is not present')
        self.assertEqual(str(self.category_id), actual_response.get("ecommerce")["add"]["products"][0]["category"],
                         msg=f'Expected category_id value "{self.category_id}" is not '
                             f'same as actual category_id value "{actual_response.get("ecommerce")["add"]["products"][0]["category"]}"')
        self.assertEqual(self.eventID, actual_response.get("ecommerce")["add"]["products"][0]["dimension60"],
                         msg=f'Expected eventID value "{self.eventID}" is not '
                             f'same as actual eventID value "{actual_response.get("ecommerce")["add"]["products"][0]["dimension60"]}"')
        self.assertEqual(self.selection_id1, actual_response.get("ecommerce")["add"]["products"][0]["dimension61"],
                         msg=f'Expected selection_id1 value "{self.selection_id1}" is not '
                             f'same as actual selection_id1 value "{actual_response.get("ecommerce")["add"]["products"][0]["dimension61"]}"')
        self.assertEqual(int(self.expected_response["ecommerce.add.products"]["dimension62"]),
                         actual_response.get("ecommerce")["add"]["products"][0]["dimension62"],
                         msg=f'Expected dimension62 value "{self.expected_response["ecommerce.add.products"]["dimension62"]}" is not '
                             f'same as actual dimension62 value "{actual_response.get("ecommerce")["add"]["products"][0]["dimension62"]}"')
        self.assertEqual(int(self.expected_response["ecommerce.add.products"]["dimension63"]),
                         actual_response.get("ecommerce")["add"]["products"][0]["dimension63"],
                         msg=f'Expected dimension63 value "{self.expected_response["ecommerce.add.products"]["dimension63"]}" is not '
                             f'same as actual dimension63 value "{actual_response.get("ecommerce")["add"]["products"][0]["dimension63"]}"')
        self.assertTrue(actual_response.get("ecommerce")["add"]["products"][0]["dimension64"],
                        msg=f'"{actual_response.get("ecommerce")["add"]["products"][0]["dimension64"]}" is not present')
        self.assertEqual(self.expected_response["ecommerce.add.products"]["dimension65"],
                         actual_response.get("ecommerce")["add"]["products"][0]["dimension65"],
                         msg=f'Expected dimension65 value "{self.expected_response["ecommerce.add.products"]["dimension65"]}" is not '
                             f'same as actual dimension65 value "{actual_response.get("ecommerce")["add"]["products"][0]["dimension65"]}"')
        self.assertEqual(self.event_name, actual_response.get("ecommerce")["add"]["products"][0]["name"],
                         msg=f'Expected event_name value "{self.event_name}" is not '
                             f'same as actual event_name value "{actual_response.get("ecommerce")["add"]["products"][0]["name"]}"')
        self.assertEqual(str(self.type_id), actual_response.get("ecommerce")["add"]["products"][0]["variant"],
                         msg=f'Expected type_id value "{self.type_id}" is not '
                             f'same as actual type_id value "{actual_response.get("ecommerce")["add"]["products"][0]["variant"]}"')
