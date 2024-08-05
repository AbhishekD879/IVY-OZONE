import pytest
import tests
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #cannot create event hub in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.module_ribbon
@pytest.mark.mobile_only
@vtest
class Test_C9726391_Event_Hub_Verify_Race_Boosted_Selection_with_SP_price(BaseBetSlipTest):
    """
    TR_ID: C9726391
    NAME: Event Hub: Verify <Race> Boosted Selection with 'SP' price
    DESCRIPTION: This test case verifies Modules configured in CMS for <Races> where Module consists of one selection retrieved by 'Selection ID' where priceTypeCodes='SP'.
    DESCRIPTION: Need to run the test case on Mobile/Tablet
    PRECONDITIONS: 1) CMS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: 2) To retrieve an information about event outcomes use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ?translationLang=LL
    PRECONDITIONS: *   *ZZZZ - an **'event id'***
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 3) User is on Homepage > Event Hub tab
    PRECONDITIONS: 4) Event Hub is created in CMS > Sport Pages > Event Hub.
    PRECONDITIONS: 5) Featured Events module by Selection ID is created in this Event Hub using ID of Race event.
    PRECONDITIONS: **NOTE: **Sport icon is CMS configurable - https://CMS\_ENDPOINT/keystone/sport-categories (check CMS\_ENDPOINT via *devlog *function)
    PRECONDITIONS: For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True
    watch_live_flags = ['EVFLAG_AVA', 'EVFLAG_IVM', 'EVFLAG_PVM', 'EVFLAG_RVA', 'EVFLAG_RPM', 'EVFLAG_GVM']

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Event Hub is created in CMS > Sport Pages > Event Hub.
        """
        event = self.ob_config.add_UK_racing_event(hours=22, number_of_runners=1, lp=False, sp=True)
        self.__class__.selection_name, self.__class__.selection_id = list(event.selection_ids.items())[0]
        self.__class__.eventID = event.event_id
        self.__class__.is_watch_live = True if event.ss_response["event"]["drilldownTagNames"] in self.watch_live_flags else False
        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]
        index_number = next(index for index in range(1, 20) if index not in existed_index_number)
        self.cms_config.create_event_hub(index_number=index_number)
        self.cms_config.add_sport_module_to_event_hub(page_id=index_number, module_type='FEATURED')
        self.__class__.module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Selection',
            id=self.selection_id,
            page_type='eventhub',
            page_id=index_number,
            events_time_from_hours_delta=-10,
            module_time_from_hours_delta=-10)['title'].upper()
        internal_id = f'tab-eventhub-{index_number}'
        event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                           internal_id=internal_id,
                                                                           hub_index=index_number,
                                                                           display_date=True)
        self.__class__.event_hub_tab_name = event_hub_tab_data.get('title').upper()
        self.site.login(username=tests.settings.betplacement_user)

    @retry(stop=stop_after_attempt(10), wait=wait_fixed(wait=40),
           retry=retry_if_exception_type((StaleElementReferenceException, VoltronException)), reraise=True)
    def test_001_load_the_oxygen_application_and_verify_selection_within_created_module(self):
        """
        DESCRIPTION: Load the Oxygen application and verify selection within created Module
        EXPECTED: Created module with one selection is displayed only if:
        EXPECTED: Selection is from non-started event from any market (with NO attribute '**isStarted="true"**' )
        """
        self.navigate_to_page("homepage")
        self.device.refresh_page()
        event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        self.assertTrue(event_hub_content, msg=f'Event hub module "{self.event_hub_tab_name}" was not found')

        event_hub_modules = event_hub_content.accordions_list.items_as_ordered_dict
        self.assertTrue(event_hub_modules, msg=f'No modules found on "{self.event_hub_tab_name}" tab')
        self.__class__.event_hub_module = event_hub_modules.get(self.module_name)
        self.assertTrue(self.event_hub_module,
                        msg=f'Module "{self.module_name}" is not found on {self.event_hub_tab_name} tab')
        self.assertTrue(self.event_hub_module.is_expanded(timeout=2),
                        msg=f'Module: "{self.module_name}" not expanded')

        self.__class__.module = self.get_section(self.module_name)

    def test_002_verify_selection_name(self):
        """
        DESCRIPTION: Verify 'Selection Name'
        EXPECTED: 'Selection Name' within module corresponds to <name> attribute from SS response OR to <name> set in CMS if name was overridden
        """
        self.__class__.event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                                              query_builder=self.ss_query_builder)

        selection = self.event_resp[0]['event']['children'][0]['market']['children'][0]['outcome']
        self.assertTrue(selection, msg='selections is not displayed in module')
        self.assertTrue('isStarted' not in [self.event_resp[0]['event'].keys()],
                        msg='with attribute **isStarted="true"**')
        outcomes_resp = self.event_resp[0]['event']['children'][0]['market']['children']
        self.assertEqual(self.selection_name, outcomes_resp[0]['outcome']['name'],
                         msg=f'*Selection Name* "{self.selection_name}" within module '
                             f'does not correspond to <name> attribute from SS response')

    def test_003_verify_event_start_time_within_created_module(self):
        """
        DESCRIPTION: Verify 'Event Start Time' within created Module
        EXPECTED: *   'Event Start time' corresponds to '**startTime**' attribute for Sports and to local time(**'name'** attribute) for Races
        EXPECTED: *   For events that occur Today date format is **"**<Today> 12 hours" for Races and **"**<Today> 12 hours AM/PM" for Sports
        EXPECTED: *   For events that occur Tomorrow date format is **"**<Tomorrow> 12 hours" for Races and  "<Tomorrow> 12 hours AM/PM" for Sports
        EXPECTED: *   For events that occur in the future (beyond tomorrow) date format is **"**DD-MM** **12 hour AM/PM" for Sports and "DD-MM 12 hour" for Races
        """
        event_time_ui = self.event_hub_module.event_time
        event_time_resp = self.event_resp[0]['event']['startTime']
        event_time_resp_converted = self.convert_time_to_local(ob_format_pattern=self.ob_format_pattern,
                                                               date_time_str=event_time_resp,
                                                               ui_format_pattern=self.event_card_today_time_format_pattern,
                                                               future_datetime_format=self.event_card_coupon_and_competition_future_time_format_pattern,
                                                               ss_data=True)

        self.assertEqual(event_time_ui, event_time_resp_converted,
                         msg=f'Event time on UI "{event_time_ui}" is not the same as got from '
                             f'response "{event_time_resp_converted}"')

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
        if self.is_watch_live:
            self.assertTrue(self.event_hub_module.has_stream(), msg='"Watch Live" icon is not found')
        else:
            self.assertFalse(self.event_hub_module.has_stream(expected_result=False),
                             msg='"Watch Live" icon should not be present')

    def test_005_verifycash_out_and_start_icon_label_on_right_top_corner(self):
        """
        DESCRIPTION: Verify 'CASH OUT' and start icon  label on right top corner
        EXPECTED: *   'CASH OUT' label is shown if cashoutAvail="Y" on Market level
        EXPECTED: *   White start icon on red background is present on top right corner
        """
        # NA

    def test_006_verify_priceodds_button_within_created_module(self):
        """
        DESCRIPTION: Verify 'Price/Odds' button within created Module
        EXPECTED: 'Price/Odds' button with 'SP' label is shown
        """
        self.__class__.bet_button = self.module.get_bet_button_by_selection_id(self.selection_id)
        self.assertEquals(self.bet_button.outcome_price_text, 'SP',
                          msg=f'Outcome "{self.bet_button.outcome_price_text}" does not have "SP" price')

    def test_007_add_selection_to_the_betslip_from_module_in_featured_section(self):
        """
        DESCRIPTION: Add selection to the Betslip from module in 'Featured' section
        EXPECTED: Betslip counter displays appropriate value
        """
        self.bet_button.click()
        self.site.add_first_selection_from_quick_bet_to_betslip()
        self.verify_betslip_counter_change(expected_value=1)

    def test_008_open_betslip_page(self):
        """
        DESCRIPTION: Open Betslip page
        EXPECTED: *   Selection is added to the Betslip
        EXPECTED: *   All information is displayed correctly
        """
        self.site.open_betslip()
        section = self.get_betslip_sections().Singles
        stake_name, self.__class__.stake = list(section.items())[0]
        self.assertTrue(section.items(), msg='*** No stakes found')
        self.assertTrue(self.stake, msg=f'"{self.selection_name}" stake was not found on the Betslip')

    def test_009_place_a_bet_by_clicking_bet_now_button(self):
        """
        DESCRIPTION: Place a bet by clicking 'Bet Now' button
        EXPECTED: *   Bet is placed succesfully
        EXPECTED: *   User's balance is decremented by entered stake
        """
        self.place_single_bet()
        self.check_bet_receipt_is_displayed(timeout=20, poll_interval=0.5)
        self.site.bet_receipt.close_button.click()

    def test_010_click_anywhere_on_event_card_except_for_price_buttons_within_verified_module(self):
        """
        DESCRIPTION: Click anywhere on Event card (except for price buttons) within verified module
        EXPECTED: Event Details page is opened
        """
        event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        event_hub_modules = event_hub_content.accordions_list.items_as_ordered_dict
        self.assertTrue(event_hub_modules, msg=f'No modules found on "{self.event_hub_tab_name}" tab')
        event_hub_module = event_hub_modules.get(self.module_name)
        event_hub_module.click()
        self.site.wait_content_state(state_name='RacingEventDetails')
