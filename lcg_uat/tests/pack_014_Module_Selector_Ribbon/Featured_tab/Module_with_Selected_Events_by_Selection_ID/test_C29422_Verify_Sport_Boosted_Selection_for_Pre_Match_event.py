import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
@pytest.mark.desktop
# @pytest.mark.prod  # cannot create Featured Modules on prod
@pytest.mark.high
@pytest.mark.featured
@pytest.mark.module_ribbon
@pytest.mark.cms
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-55332')
@vtest
class Test_C29422_Verify_Sport_Boosted_Selection_for_Pre_Match_event(BaseFeaturedTest):
    """
    TR_ID: C29422
    NAME: Verify <Sport> Boosted Selection for Pre-Match event
    DESCRIPTION: This test case verifies Modules configured in CMS for <Sport> where Module consists of one selection retrieved by 'Selection ID'.
    PRECONDITIONS: 1) CMS: https://**CMS_ENDPOINT**/keystone/modular-content/ (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 2) To retrieve an information about event outcomes use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ?translationLang=LL
    PRECONDITIONS: *   *ZZZZ - an **'event id'***
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 3) User is logged in
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
            events = self.get_active_events_for_category(category_id=category_id)
            event = next((event for event in events if event['event'].get('drilldownTagNames')), None)
            if not event:
                raise SiteServeException('No events with drilldownTagNames available')
            self.__class__.eventID = event['event']['id']
            self.__class__.is_watch_live = \
                any(flag in event['event']['drilldownTagNames'] for flag in self.watch_live_flags)
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
            start_time = self.get_date_time_formatted_string(hours=5)
            params = self.ob_config.add_football_event_to_autotest_league2(start_time=start_time, perform_stream=True)
            self.__class__.eventID = params.event_id
            self.__class__.team1, self.__class__.team2, self.__class__.selection_ids = \
                params.team1, params.team2, params.selection_ids
            self.__class__.is_watch_live = True

        self.__class__.module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Selection', id=self.selection_ids[self.team1], show_expanded=True, events_time_from_hours_delta=-10, module_time_from_hours_delta=-10)['title'].upper()

    def test_001_load_oxygen_application_and_verify_selection_within_created_module(self):
        """
        DESCRIPTION: Load Oxygen application and verify selection within created Module
        EXPECTED: Created module with selection is displayed in a separate section
        """
        self.site.wait_content_state('Homepage')
        self.wait_for_featured_module(name=self.module_name)
        if self.device_type == 'mobile':
            self.site.home.get_module_content(module_name=self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))
            self.__class__.module = self.get_section(self.module_name)
        else:
            home_page_modules = self.site.home.desktop_modules.items_as_ordered_dict
            self.assertTrue(home_page_modules, msg='No one module found on Home Page')
            featured_section = home_page_modules.get(vec.sb_desktop.FEATURED_MODULE_NAME)
            featured_modules = featured_section.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(featured_modules, msg='No one FEATURED module found')
            self.__class__.module = featured_modules.get(self.module_name)

        self.assertTrue(self.module, msg=f'"{self.module_name}" module is not found')

        self.assertTrue(self.module.is_expanded(), msg=f'"{self.module}" module is not expanded')

        events = self.module.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found in "{self.module_name}" module')

        self.__class__.event = events.get(self.team1)
        self.assertTrue(self.event, msg=f'Event "{self.team1}" not found among events "{events.keys()}"')

        selections = self.event.get_available_prices()
        self.assertTrue(selections, msg=f'No selections found in Boosted selections module event')
        self.assertIn(self.team1, selections,
                      msg=f'Selection "{self.team1}" not found among selections "{selections.keys()}"')
        self.assertNotIn(self.team2, selections,
                         msg=f'Selection "{self.team2}" found among selections "{selections.keys()}" '
                             f'however it is not expected as it is Boosted selection module')
        self.assertNotIn('Draw', selections,
                         msg=f'Selection Draw found among selections "{selections.keys()}" '
                             f'however it is not expected as it is Boosted selection module')

        self.__class__.selection_name, self.__class__.selection = list(selections.items())[0]

    def test_002_verify_selection_name(self):
        """
        DESCRIPTION: Verify 'Selection Name'
        EXPECTED: * 'Selection Name' within module corresponds to <name> attribute from SS response OR to <name> set in CMS if name was overridden
        EXPECTED: * Name of a long selection is wrapped into a few lines without cutting the text
        """
        self.__class__.event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID, query_builder=self.ss_query_builder)
        self.__class__.outcomes_resp = self.event_resp[0]['event']['children'][0]['market']['children']
        name_resp = next((i['outcome']['name'] for i in self.outcomes_resp if i['outcome']['name'] == self.team1), '')
        self.assertEqual(self.selection_name, name_resp,
                         msg=f'*Selection Name* "{self.selection_name}" within module '
                             f'does not correspond to <name> attribute from SS response "{name_resp}"')

    def test_003_verify_event_start_time_within_created_module(self):
        """
        DESCRIPTION: Verify 'Event Start time' within created Module
        EXPECTED: *   'Event Start time' corresponds to '**startTime**' attribute
        EXPECTED: *   For events that occur Today date format is **HH:MM, Today**
        EXPECTED: *   For events that occur Tomorrow date format is **HH:MM, DD MMM** (e.g. 14:00 or 05:00, 24 Nov or 02 Nov)
        """
        event_time_ui = self.event.event_time
        event_time_resp = self.event_resp[0]['event']['startTime']
        event_time_resp_converted = self.convert_time_to_local(ob_format_pattern=self.ob_format_pattern,
                                                               date_time_str=event_time_resp,
                                                               ui_format_pattern=self.event_card_today_time_format_pattern,
                                                               future_datetime_format=self.event_card_future_time_format_pattern,
                                                               ss_data=True)
        self.assertEqual(event_time_ui, event_time_resp_converted,
                         msg=f'Event time on UI "{event_time_ui}" is not the same '
                             f'as got from response "{event_time_resp_converted}"')

    def test_004_verify_favourites_icon(self):
        """
        DESCRIPTION: Verify 'Favourites' icon
        EXPECTED: 'Favourites' icon is displayed only for Football events within Module section
        """
        favourites_enabled = self.get_favourites_enabled_status()
        self.assertEqual(favourites_enabled, self.event.has_favourite_icon(expected_result=favourites_enabled),
                         msg=f'"Favourites" icon presence status is not "{favourites_enabled}"')

    def test_005_verify_watch_live_icon_and_label(self):
        """
        DESCRIPTION: Verify 'Watch Live' icon and label
        EXPECTED: 'Watch Live' icon and label are shown if **drilldownTagNames** attribute is available and contains one or more of following flags:
        EXPECTED: EVFLAG_AVA / EVFLAG_IVM / EVFLAG_PVM / EVFLAG_RVA / EVFLAG_RPM / EVFLAG_GVM
        """
        if self.is_watch_live:
            self.assertTrue(self.event.has_stream(), msg='"Watch Live" icon is not found')
        else:
            self.assertFalse(self.event.has_stream(expected_result=False),
                             msg='"Watch Live" icon should not be present')

    def test_006_verify_cash_out_label_and_star_icon_on_the_top_right_corner(self):
        """
        DESCRIPTION: Verify 'CASH OUT' label on the top right corner
        EXPECTED: 'CASH OUT' label is not shown on Boosted selection header if  cashoutAvail="Y" on **Market level**
        """
        self.assertFalse(self.module.group_header.has_cash_out_mark(expected_result=False),
                         msg='"Cashout" icon is found')

    def test_007_verify_price_odds_button_within_created_module(self):
        """
        DESCRIPTION: Verify 'Price/Odds' button within created Module
        EXPECTED: 'Price/Odds' button is shown with correct price which corresponds to **'priceNum/priceDen'** in fractional format (**'priceDec'** in decimal format) attributes values in SS response
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

    def test_008_click_tap_anywhere_on_event_card_except_for_price_buttons_within_verified_module(self):
        """
        DESCRIPTION: Click/Tap anywhere on Event card (except for price buttons) within verified module
        EXPECTED: Event Details page is opened
        """
        self.event.click()
        self.site.wait_content_state(state_name='EventDetails')
