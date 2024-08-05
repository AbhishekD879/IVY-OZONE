import pytest

import tests
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # cannot create Featured Modules on prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.featured
@pytest.mark.module_ribbon
@pytest.mark.homepage_featured
@pytest.mark.desktop
@pytest.mark.cms
@pytest.mark.safari
@vtest
class Test_C878819_Verify_Featured_Module_adding_by_Selection_ID_Boosted_Selections(BaseFeaturedTest):
    """
    TR_ID: C878819
    NAME: Verify Featured Module adding by Selection ID (Boosted Selections) [HL/TEST2]
    DESCRIPTION: This test case verifies Modules configured in CMS where Module consists of one selection retrieved by 'Selection ID'
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to 'Featured' tab/section
    PRECONDITIONS: **Configurations**
    PRECONDITIONS: 1) For creating the module in the 'Featured' tab/section by 'Selection ID' via CMS use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=126685715
    PRECONDITIONS: 2) For reaching the appropriate CMS per env use the following link:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) To verify data for created 'Featured' module use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket (featured-sports...) -> response with type: "FEATURED_STRUCTURE_CHANGED" -> modules -> @type: "EventsModule" an choose the appropriate module.
    PRECONDITIONS: 2) Be aware that Live events are not displayed in the 'Featured' modules for Desktop
    """
    keep_browser_open = True
    selection_name, selection, event = None, None, None
    event_resp, outcomes_resp = None, None
    watch_live_flags = ['EVFLAG_AVA', 'EVFLAG_IVM', 'EVFLAG_PVM', 'EVFLAG_RVA', 'EVFLAG_RPM', 'EVFLAG_GVM']

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test prematch event
        DESCRIPTION: Create Featured module in CMS by selection id
        """
        if tests.settings.backend_env == 'prod':
            category_id = self.ob_config.football_config.category_id
            event = self.get_active_events_for_category(category_id=category_id)[0]
            self.__class__.eventID = event['event']['id']
            if event['event'].get('drilldownTagNames'):
                self.__class__.is_watch_live = any(flag in event['event']['drilldownTagNames'] for flag in self.watch_live_flags)
            else:
                self.__class__.is_watch_live = False
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            # outcomeMeaningMinorCode: A - away, H - home, D - draw
            self.__class__.team1 = next((outcome['outcome']['name'] for outcome in outcomes if
                                         outcome['outcome'].get('outcomeMeaningMinorCode') and
                                         outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            self.__class__.team2 = next((outcome['outcome']['name'] for outcome in outcomes if
                                         outcome['outcome'].get('outcomeMeaningMinorCode') and
                                         outcome['outcome']['outcomeMeaningMinorCode'] == 'A'), None)
            if not self.team1:
                raise SiteServeException('No Home team found')

            if not self.team2:
                raise SiteServeException('No Away team found')
        else:
            params = self.ob_config.add_football_event_to_autotest_league2(perform_stream=True)
            self.__class__.eventID = params.event_id
            self.__class__.team1, self.__class__.team2, self.__class__.selection_ids = \
                params.team1, params.team2, params.selection_ids
            self.__class__.is_watch_live = True

        self.__class__.module_data = self.cms_config.add_featured_tab_module(
            select_event_by='Selection', id=self.selection_ids[self.team1], show_expanded=True)

        self.__class__.module_name = self.module_data['title'].upper()

    def test_001_verify_created_module_on_featured_tab_section(self):
        """
        DESCRIPTION: Verify created module on 'Featured' tab/section
        EXPECTED: The created module is displayed and contains the following elements:
        EXPECTED: * 'Featured' module header with module name set in CMS
        EXPECTED: * 'Specials' or 'Enhanced' label in the header if it set in CMS
        EXPECTED: * Card with 'Selection' name and 'Price/Odds' button
        EXPECTED: * Event Start time
        EXPECTED: * 'Watch Stream' icon if available
        EXPECTED: * 'Favourite' icon **Football Coral only**
        EXPECTED: * 'Footer' link set in CMS
        """
        self.site.wait_content_state(state_name='Homepage')
        module_name = self.get_ribbon_tab_name(internal_id=self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)

        if not self.is_safari:
            self.wait_for_featured_module(name=self.module_name)
        self.__class__.module = self.get_module(module_content_name=module_name, module_name=self.module_name)
        self.assertTrue(self.module, msg=f'Featured module "{self.module_name}" not found')
        self.assertTrue(self.module.is_expanded(), msg=f'Featured module "{self.module_name}" is not expanded')
        self.assertEqual(self.module.name, self.module_name,
                         msg=f'Featured module name "{self.module.name}" is not as set in CMS "{self.module_name}"')

        events = self.module.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found in "{self.module_name}" module')

        self.__class__.event = events.get(self.team1)
        self.assertTrue(self.event, msg=f'Event "{self.team1}" not found among events "{events.keys()}"')

        selections = self.event.get_available_prices()
        self.assertTrue(selections, msg=f'No selections found in Boosted selections module event')
        self.assertIn(self.team1, selections,
                      msg=f'Selection "{self.team1}" not found among selections "{selections.keys()}"')
        footer_link_text = self.module_data['footerLink']['text']
        if self.device_type == 'desktop':
            footer_link_text = footer_link_text.upper()
        self.assertEqual(self.module.footer.text, footer_link_text,
                         msg=f'Footer link text "{self.module.footer.text}" '
                             f'is not as expected "{footer_link_text}"')

        self.__class__.selection_name, self.__class__.selection = list(selections.items())[0]

    def test_002_verify_selection_name(self):
        """
        DESCRIPTION: Verify 'Selection' name
        EXPECTED: * 'Selection' name within module corresponds to <name> attribute the response OR to <name> set in CMS if name was overridden
        EXPECTED: * 'Selection' long name is wrapped into a few lines without cutting the text
        """
        self.__class__.event_resp = self.ss_req.ss_event_to_outcome_for_event(
            event_id=self.eventID, query_builder=self.ss_query_builder)
        self.__class__.outcomes_resp = self.event_resp[0]['event']['children'][0]['market']['children']

        name_resp = next((i['outcome']['name'] for i in self.outcomes_resp if i['outcome']['name'] == self.team1), '')
        self.assertEqual(self.selection_name, name_resp,
                         msg=f'Selection: "{self.selection_name}" within module '
                             f'does not correspond to <name> attribute from SS response "{name_resp}"')

    def test_003_verify_event_start_time_within_created_module(self):
        """
        DESCRIPTION: Verify 'Event Start Time' within created Module
        EXPECTED: * 'Event Start Time' corresponds to 'startTime' attribute
        EXPECTED: *  For events that occur Today format is 24 hours:
        EXPECTED: HH:MM, Today (e.g. "14:00 or 05:00 Today").
        EXPECTED: *  For events that occur in the future (including tomorrow) date format is 24 hours:
        EXPECTED: HH:MM DD MMM (e.g. "14:00 or 05:00 24 Nov or 02 Nov")
        EXPECTED: * Start time is not displayed for started events
        """
        event_time_ui = self.event.event_time
        event_time_resp = self.event_resp[0]['event']['startTime']
        event_time_resp_converted = self.convert_time_to_local(
            ob_format_pattern=self.ob_format_pattern,
            date_time_str=event_time_resp,
            ui_format_pattern=self.event_card_today_time_format_pattern,
            future_datetime_format=self.event_card_coupon_and_competition_future_time_format_pattern,
            ss_data=True)
        self.assertEqual(event_time_ui, event_time_resp_converted,
                         msg=f'Event time on UI "{event_time_ui}" is not the same '
                             f'as got from response "{event_time_resp_converted}"')

    def test_004_verify_live_label_for_mobile_tablet_only(self):
        """
        DESCRIPTION: Verify 'Live' label **For Mobile/Tablet only**
        EXPECTED: 'LIVE' label is shown if event is started
        """
        if self.is_watch_live:
            self.assertTrue(self.event.has_stream(), msg='"Watch Live" icon is not found')
        else:
            self.assertFalse(self.event.has_stream(expected_result=False),
                             msg='"Watch Live" icon should not be present')

    def test_005_verify_price_odds_button_within_the_created_module(self):
        """
        DESCRIPTION: Verify 'Price/Odds' button within the created Module
        EXPECTED: 'Price/Odds' button is shown with the correct price of the selection
        """
        bet_buttons = self.module.get_available_prices()
        self.assertTrue(bet_buttons, msg=f'No selections found: "{bet_buttons}"')

        bet_button = bet_buttons.get(self.team1)
        self.assertTrue(bet_button,
                        msg=f'"{self.team1}" selection bet button is not found within module "{self.module_name}"')

        price_resp = next((i["outcome"]["children"][0]["price"] for i in self.outcomes_resp
                           if 'price' in i["outcome"]["children"][0].keys() and i["outcome"]['name'] == self.team1), '')
        self.assertTrue(price_resp, msg=f'Price is not found in Siteserve response "{self.outcomes_resp}"')

        lp_price_resp = f'{price_resp["priceNum"]}/{price_resp["priceDen"]}'
        self.assertEqual(bet_button.outcome_price_text, lp_price_resp,
                         msg=f'Price "{bet_button.outcome_price_text}" is not the same as in response "{lp_price_resp}"')
