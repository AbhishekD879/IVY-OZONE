import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from voltron.utils.helpers import do_request
from json import JSONDecodeError
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #cannot create event hub in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.other
@vtest
class Test_C9726390_Event_hub_Verify_Race_Boosted_Selection_with_LP_price(BaseFeaturedTest, BaseBetSlipTest,
                                                                          BaseRacing):
    """
    TR_ID: C9726390
    NAME: Event hub: Verify <Race> Boosted Selection with 'LP' price
    DESCRIPTION: This test case verifies Modules configured in CMS for <Race> where Module consists of one selection retrieved by 'Selection ID' where priceTypeCodes='LP'.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: 1) CMS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: 2) To retrieve an information about event outcomes use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ?translationLang=LL
    PRECONDITIONS: *   *ZZZZ - an **'event id'***
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 3) User is on Homepage > Event Hub tab
    PRECONDITIONS: 4) Event Hub is created in CMS > Sport Pages > Event Hub
    PRECONDITIONS: 5) Featured events module by Selection ID using ID of Race event is created in this Event Hub.
    PRECONDITIONS: For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True
    watch_live_flags = ['EVFLAG_AVA', 'EVFLAG_IVM', 'EVFLAG_PVM', 'EVFLAG_RVA', 'EVFLAG_RPM', 'EVFLAG_GVM']

    def get_response_url(self, url):
        """
        :param url: Required URl
        :return: Complete url
        """
        perflog = self.device.get_performance_log()
        for log in list(reversed(perflog)):
            try:
                data_dict = log[1]['message']['message']['params']['request']
                request_url = data_dict['url']
                if url in request_url:
                    return request_url
            except (KeyError, JSONDecodeError, TypeError, IndexError):
                continue

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Event Hub is created in CMS > Sport Pages > Event Hub.
        """
        event = self.ob_config.add_UK_racing_event(time_to_start=2,
                                                   number_of_runners=2, lp_prices={0: '1/2', 1: '3/2'})
        self.__class__.eventID = event.event_id
        selection_id = list(event.selection_ids.items())[0][1]
        self.__class__.event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                                              query_builder=self.ss_query_builder)
        markets = self.event_resp[0]['event']['children']
        outcomes = next(((market['market'].get('children')) for market in markets), None)
        if outcomes is None:
            raise SiteServeException('There are no available outcomes')
        self.__class__.is_watch_live = True if event.ss_response["event"]["drilldownTagNames"] in self.watch_live_flags else False
        self.__class__.outcome_name1 = outcomes[0]["outcome"]["name"]

        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]
        index_number = next(index for index in range(1, 20) if index not in existed_index_number)
        self.cms_config.create_event_hub(index_number=index_number)
        self.cms_config.add_sport_module_to_event_hub(page_id=index_number, module_type='FEATURED')
        module_data = self.cms_config.add_featured_tab_module(select_event_by='Selection',
                                                              id=selection_id,
                                                              page_type='eventhub',
                                                              page_id=index_number,
                                                              events_time_from_hours_delta=-10,
                                                              module_time_from_hours_delta=-10)
        self.__class__.module_name = module_data['title'].upper()
        internal_id = f'tab-eventhub-{index_number}'
        event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                           internal_id=internal_id,
                                                                           hub_index=index_number,
                                                                           display_date=True)
        self.__class__.event_hub_tab_name = event_hub_tab_data.get('title').upper()
        self.site.login(tests.settings.betplacement_user)
        self.site.toggle_quick_bet()

    @retry(stop=stop_after_attempt(10), wait=wait_fixed(wait=40),
           retry=retry_if_exception_type((StaleElementReferenceException, VoltronException)), reraise=True)
    def test_001_load_oxygen_application_and_verify_the_selection_within_created_module(self):
        """
        DESCRIPTION: Load Oxygen application and verify the selection within created Module
        EXPECTED: Created module with one selection is displayed only if the selection is from non-started event from any market. The non-started event Open Bet attributes :
        EXPECTED: *   'Status'='A'
        EXPECTED: *   'isOff'='N/A'
        """
        self.device.refresh_page()
        self.__class__.event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        self.assertTrue(self.event_hub_content, msg=f'Event hub module "{self.event_hub_tab_name}" was not found')
        # Status and isOff covered in test 003

    def test_002_verify_selection_name(self):
        """
        DESCRIPTION: Verify 'Selection Name'
        EXPECTED: 'Selection Name' within module corresponds to <name> attribute from SS response OR to <name> set in CMS if name was overridden
        """
        event_hub_modules = self.event_hub_content.accordions_list.items_as_ordered_dict
        self.assertTrue(event_hub_modules, msg=f'No modules found on "{self.event_hub_tab_name}" tab')
        event_hub_module = event_hub_modules.get(self.module_name)
        self.assertTrue(event_hub_module,
                        msg=f'Module "{self.module_name}" is not found on {self.event_hub_tab_name} tab')
        event_time_ui = event_hub_module.event_time
        event_time_resp = self.event_resp[0]['event']['startTime']
        event_time_resp_converted = self.convert_time_to_local(ob_format_pattern=self.ob_format_pattern,
                                                               date_time_str=event_time_resp,
                                                               ui_format_pattern=self.event_card_today_time_format_pattern,
                                                               future_datetime_format=self.event_card_coupon_and_competition_future_time_format_pattern,
                                                               ss_data=True)
        self.assertEqual(event_time_ui, event_time_resp_converted,
                         msg=f'Event time on UI "{event_time_ui}" is not the same as got from '
                             f'response "{event_time_resp_converted}"')
        self.assertTrue("Today" in event_time_ui,
                        msg=f'For events that occur Today date format is not having Today text')
        if self.is_watch_live:
            self.assertTrue(event_hub_module.has_stream(), msg='"Watch Live" icon is not found')
        else:
            self.assertFalse(event_hub_module.has_stream(expected_result=False),
                             msg='"Watch Live" icon should not be present')
        event_hub_module.click()
        self.site.wait_content_state_changed()
        sleep(3)
        response_url = self.get_response_url('EventToOutcomeForEvent')
        self.assertTrue(response_url, msg='EventToOutcomeForEvent data is not received after unblocking request')
        response = do_request(method='GET', url=response_url)
        self.assertTrue(response, msg='No response received for the "EventToOutcomeForEvent" call')
        self.assertEqual("A", response["SSResponse"]["children"][0]["event"]["eventStatusCode"],
                         msg="status code is not equals")
        self.assertEqual("N", response["SSResponse"]["children"][0]["event"]["rawIsOffCode"],
                         msg="rawIsOffCode is not equals")
        self.assertEqual("Y", response["SSResponse"]["children"][0]["event"]["cashoutAvail"],
                         msg="cashoutAvail code is not equals")
        self.site.back_button_click()

        module = self.get_section(self.module_name)
        events = module.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found in "{self.module_name}" module')
        event_outcome = events.get(self.outcome_name1)
        selections = event_outcome.get_available_prices()
        self.assertTrue(selections, msg=f'No selections found in Boosted selections module event')
        self.__class__.selection_name, selection = list(selections.items())[0]
        self.__class__.outcomes_resp = self.event_resp[0]['event']['children'][0]['market']['children']
        name_resp = next(
            (i['outcome']['name'] for i in self.outcomes_resp if i['outcome']['name'] == self.outcome_name1), '')
        self.assertEqual(self.selection_name, name_resp,
                         msg=f'*Selection Name* "{self.selection_name}" within module '
                             f'does not correspond to <name> attribute from SS response "{name_resp}"')

    def test_003_verify_event_start_time_within_created_module(self):
        """
        DESCRIPTION: Verify 'Event Start time' within created Module
        EXPECTED: *   'Event Start time' corresponds to '**startTime**' attribute for Sports and to local time(**'name'** attribute) for Races
        EXPECTED: *   For events that occur Today date format is **"**<Today> 12 hours" for Races and **"**<Today> 12 hours AM/PM" for Sports
        EXPECTED: *   For events that occur Tomorrow date format is **"**<Tomorrow> 12 hours" for Races and  "<Tomorrow> 12 hours AM/PM" for Sports
        EXPECTED: *   For events that occur in the future (beyond tomorrow) date format is **"**DD-MM** **12 hour AM/PM" for Sports and "DD-MM 12 hour" for Races
        """

        # covered in test_003

    def test_004_verify_watch_live_icon_and_label(self):
        """
        DESCRIPTION: Verify 'Watch Live' icon and label
        EXPECTED: 'Watch Live' icon and label are shown if drilldownTagNames attribute is available and contains one or more of following flags:
        EXPECTED: EVFLAG_AVA
        EXPECTED: EVFLAG_IVM
        EXPECTED: EVFLAG_PVM
        EXPECTED: EVFLAG_RVA
        EXPECTED: EVFLAG_RPM
        EXPECTED: EVFLAG_GVM
        """
        # covered in test_003

    def test_005_verifycash_out_and_start_label_on_top_right_corner(self):
        """
        DESCRIPTION: Verify 'CASH OUT' and start label on top right corner
        EXPECTED: 'CASH OUT' label is shown if cashoutAvail="Y" on Market level
        """
        # covered in test_002

    def test_006_verify_priceodds_button_within_created_module(self):
        """
        DESCRIPTION: Verify 'Price/Odds' button within created Module
        EXPECTED: 'Price/Odds' button is shown with correct price which corresponds to **'priceNum/priceDen'** in a fractional format (**'priceDec'** in a decimal format) attributes values in SS response
        """
        module = self.get_section(self.module_name)
        bet_buttons = module.get_available_prices()
        self.assertTrue(bet_buttons, msg=f'No selections found: "{bet_buttons}"')
        self.__class__.bet_button = bet_buttons.get(self.outcome_name1)
        self.assertTrue(self.bet_button,
                        msg=f'"{self.outcome_name1}" selection bet button is not found within module "{self.module_name}"')

        price_resp = next((i["outcome"]["children"][0]["price"] for i in self.outcomes_resp
                           if 'price' in i["outcome"]["children"][0].keys() and i["outcome"][
                               'name'] == self.outcome_name1), '')
        self.assertTrue(price_resp, msg=f'Price is not found in Siteserve response "{self.outcomes_resp}"')
        lp_price_resp = f'{price_resp["priceNum"]}/{price_resp["priceDen"]}'
        self.assertEqual(self.bet_button.outcome_price_text, lp_price_resp,
                         msg=f'Price "{self.bet_button.outcome_price_text}" is not the same as in response "{lp_price_resp}"')

    def test_007_for_the_special_offer_in_featured_section_verify_the_visibility_and_size_of_the_priceodds_button_for_various_screen_resolutions(
            self):
        """
        DESCRIPTION: For the 'Special' offer in 'Featured' section, verify the visibility and size of the 'Price/Odds' button for various screen resolutions
        EXPECTED: * The Price/Odd buttons remain visible throughout the various resolution changes.
        EXPECTED: * The size of the 'Price/Odds' button depends on the screen resolutions
        """
        # NA

    def test_008_for_the_enhanced_offer_in_featured_section_verify_the_visibility_and_size_of_the_priceodds_button_for_various_screen_resolutions(
            self):
        """
        DESCRIPTION: For the 'Enhanced' offer in 'Featured' section, verify the visibility and size of the 'Price/Odds' button for various screen resolutions
        EXPECTED: * The Price/Odd buttons remain visible throughout the various resolution changes.
        EXPECTED: * The size of the 'Price/Odds' button depends on the screen resolutions
        """
        # NA

    def test_009_add_selection_to_the_betslip_from_module_in_featured_section(self):
        """
        DESCRIPTION: Add selection to the Betslip from module in 'Featured' section
        EXPECTED: Betslip counter displays appropriate value
        """
        betslip_counter_value = self.get_betslip_counter_value()
        self.bet_button.click()
        self.verify_betslip_counter_change(expected_value=str(int(betslip_counter_value) + 1))

    def test_010_open_betslip_page(self):
        """
        DESCRIPTION: Open BetSlip page
        EXPECTED: *   Selection is added to the Betslip
        EXPECTED: *   All information is displayed correctly
        """
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        self.assertEqual(stake_name, self.selection_name,
                         msg=f'Selection "{self.selection_name}" should be present in betslip')

    def test_011_place_a_bet_by_tapping_bet_now_button(self):
        """
        DESCRIPTION: Place a bet by tapping 'Bet Now' button
        EXPECTED: *   Bet is placed succesfully
        EXPECTED: *   User's balance is decremented by entered stake
        """
        user_balance = self.site.header.user_balance
        self.place_single_bet()
        self.check_bet_receipt_is_displayed(timeout=20, poll_interval=0.5)
        expected_user_balance = user_balance - self.bet_amount
        self.verify_user_balance(expected_user_balance=float(expected_user_balance), timeout=10)
        self.site.bet_receipt.close_button.click()

    def test_012_clicktap_anywhere_on_event_card_except_for_price_buttons_within_the_verified_module(self):
        """
        DESCRIPTION: Click/Tap anywhere on Event card (except for price buttons) within the verified module
        EXPECTED: Event Details page is opened
        """
        event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        self.assertTrue(event_hub_content, msg=f'Event hub module "{self.event_hub_tab_name}" was not found')
        event_hub_modules = event_hub_content.accordions_list.items_as_ordered_dict
        self.assertTrue(event_hub_modules, msg=f'No modules found on "{self.event_hub_tab_name}" tab')
        event_hub_module = event_hub_modules.get(self.module_name)
        self.assertTrue(event_hub_module,
                        msg=f'Module "{self.module_name}" is not found on {self.event_hub_tab_name} tab')
        event_hub_module.click()
        self.site.wait_content_state('RacingEventDetails')
        self.ob_config.change_event_state(event_id=self.eventID, active=False, displayed=True)
        self.ob_config.change_is_off_flag(event_id=self.eventID, is_off=True)

    @retry(stop=stop_after_attempt(10), wait=wait_fixed(wait=40),
           retry=retry_if_exception_type((StaleElementReferenceException, VoltronException)), reraise=True)
    def test_013_repeat_steps_1_7__set_for_the_event_based_on_which_module_was_created_in_open_bet_the_following_the_event_will_be_startedstatussisoffyes(
            self):
        """
        DESCRIPTION: Repeat steps 1-7 -> Set for the event, based on which module was created, in Open Bet the following (the event will be started):
        DESCRIPTION: 'Status'='S'
        DESCRIPTION: 'isOff'='Yes'
        EXPECTED:
        """
        self.device.refresh_page()
        response_url = self.get_response_url('EventToOutcomeForEvent')
        self.assertTrue(response_url, msg='EventToOutcomeForEvent data is not received after unblocking request')
        response = do_request(method='GET', url=response_url)
        self.assertTrue(response, msg='No response received for the "EventToOutcomeForEvent" call')
        self.assertEqual("S", response["SSResponse"]["children"][0]["event"]["eventStatusCode"],
                         msg="status code is not equals")
        self.assertEqual("Y", response["SSResponse"]["children"][0]["event"]["rawIsOffCode"],
                         msg="rawIsOffCode is not equals")

    def test_014_refresh_page(self):
        """
        DESCRIPTION: Refresh page
        EXPECTED: Verified module is still shown within 'Featured' section
        """
        sleep(2)
        self.site.back_button_click()
        event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        self.assertTrue(event_hub_content, msg=f'Event hub module "{self.event_hub_tab_name}" was not found')
