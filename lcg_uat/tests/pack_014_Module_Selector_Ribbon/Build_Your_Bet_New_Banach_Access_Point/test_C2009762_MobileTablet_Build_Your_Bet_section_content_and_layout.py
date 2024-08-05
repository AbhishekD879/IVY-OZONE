from collections import OrderedDict

import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.homepage
@pytest.mark.build_your_bet
@pytest.mark.banach
@pytest.mark.module_ribbon
@pytest.mark.mobile_only
@pytest.mark.high
@vtest
class Test_C2009762_MobileTablet_Build_Your_Bet_section_content_and_layout(BaseBanachTest):
    """
    TR_ID: C2009762
    VOL_ID: C9697680
    NAME: Mobile/Tablet: Build Your Bet section content and layout
    DESCRIPTION: This test case verifies displaying of Build Your Bet (BYB) tab content and layout of event cards on mobile and tablet
    PRECONDITIONS: Check the following requests in Dev tools > Network > XHR:
    PRECONDITIONS: Request for Banach upcoming leagues: https://buildyourbet-dev1.coralsports.dev.cloud.ladbrokescoral.com/api/v1/leagues-upcoming?days=%&tz=%
    PRECONDITIONS: Request for Banach events of particular league for defined period of time: https://buildyourbet-dev1.coralsports.dev.cloud.ladbrokescoral.com/api/v1/events?dateFrom=2018-06-14T21:00:00.000Z&dateTo=2018-06-15T21:00:00.000Z&leagueIds=xxxx
    PRECONDITIONS: CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: Build Your Bet tab is available on homepage:
    PRECONDITIONS: 1)BYB is enabled in CMS
    PRECONDITIONS: mobile/tablet/desktop:
    PRECONDITIONS: Module Ribbon Tab -> 'Build Your Bet'; 'Visible' = True;
    PRECONDITIONS: Leagues is available when:
    PRECONDITIONS: 1) Banach leagues are mapped in CMS: Your Call > YourCall leagues
    PRECONDITIONS: 2) Banach league is mapped on Banach side
    PRECONDITIONS: **Build Your Bet module ribbon tab is opened**
    """
    keep_browser_open = True
    proxy = None
    byb_tab_accordions = None
    today_banach_leagues, upcoming_banach_leagues = None, None
    today_mapped_leagues, upcoming_mapped_leagues = None, None
    byb_name = None
    byb_on_homepage = True
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    segment = vec.bma.CSP_CMS_SEGEMENT

    def verify_byb_accordions(self, byb_tab_accordions: OrderedDict) -> None:
        """
        :param byb_tab_accordions: dictionary with accordions names and web elements
        Verifies Build Your Bet accordions does not display
        """
        self.assertTrue(byb_tab_accordions, msg='No accordions found on BYB tab on Home page')
        self._logger.debug(f'*** BYB accordions "{list(byb_tab_accordions.keys())}"')
        for i, (league_name, league) in enumerate(byb_tab_accordions.items(), 1):
            if i <= 2:
                self.assertTrue(league.is_expanded(),
                                msg=f'League accordion "{league_name}" is not expanded by default')
            else:
                self.assertFalse(league.is_expanded(expected_result=False),
                                 msg=f'League accordion "{league_name}" is not collapsed by default')
            self.assertFalse(league.has_byb_icon(expected_result=False),
                             msg=f'League accordion "{league_name}" has Build Your Bet sign')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Check BYB events presence
        DESCRIPTION: Find BYB tab on Homepage and click on it
        EXPECTED: BYB tab is active
        """
        self.get_ob_event_with_byb_market()
        self.__class__.today_banach_leagues, self.__class__.upcoming_banach_leagues = self.check_byb_leagues_presence()
        if not any([self.today_banach_leagues, self.upcoming_banach_leagues]):
            raise SiteServeException('Neither Today nor Upcoming Banach events found')

        byb_leagues_presence = self.check_byb_leagues_presence()
        self.__class__.today_banach_leagues = byb_leagues_presence.today and bool(self.get_mapped_leagues(date_range='today'))
        self.__class__.upcoming_banach_leagues = byb_leagues_presence.upcoming and bool(self.get_mapped_leagues(date_range='upcoming'))

        byb_ribbon_tabs = [
            (i, tab.get('title')) for i, tab in enumerate(self.cms_config.module_ribbon_tabs.visible_tabs_data)
            if tab.get('directiveName') == 'BuildYourBet'
        ]

        if byb_ribbon_tabs:
            data = next((tab for tab in self.cms_config.module_ribbon_tabs.visible_tabs_data
                         if tab.get('directiveName') == 'BuildYourBet'), None)
            self.__class__.universal_segment = data['universalSegment']
            if not self.universal_segment:
                self.cms_config.module_ribbon_tabs.create_tab(directive_name='BuildYourBet',
                                                              internal_id='tab-bet-builder', title='BUILD YOUR BET',
                                                              inclusionList=[self.segment], universalSegment=False)
        if len(byb_ribbon_tabs) < 1:
            self.cms_config.module_ribbon_tabs.create_tab(directive_name='BuildYourBet',
                                                          internal_id='tab-bet-builder', title='BUILD YOUR BET',
                                                          inclusionList=[self.segment], universalSegment=False)
        self.__class__.tab_index, self.__class__.byb_name = byb_ribbon_tabs[0]
        self.site.wait_content_state('HomePage')
        if not self.universal_segment:
            self.site.login()
            self.set_local_storage_cookies_csp(self.cookie_name, self.segment)
            self.device.refresh_page()
            self.site.wait_content_state(state_name='Homepage', timeout=20)

        # byb_tab_name = 'BYB V3'  # quick w/a for testing on dev endpoints
        self.site.home.get_module_content(module_name=self.byb_name.upper())

    def test_001_verify_accordions_and_events_within_today_upcoming_sections(self):
        """
        DESCRIPTION: Verify accordions and events within Today/Upcoming sections
        EXPECTED: - 2 league accordions are expanded by default
        EXPECTED: - Each accordion does not contain "Build Your Bet" sign
        EXPECTED: - "Today" section with events received from "Banach" starting today
        EXPECTED: - "Upcoming" section with events received from "Banach" within the next 5 days
        """
        byb_tab_content = self.site.home.tab_content
        self.assertTrue(byb_tab_content.has_grouping_buttons,
                        msg='Build Your Bet tab does not have Today/Upcoming switchers')
        if self.today_banach_leagues:
            byb_accordions = self.get_byb_module_accordions(module_name=self.byb_name.upper())
            self.__class__.today_mapped_leagues = self.get_mapped_leagues(date_range='today')
            self._logger.debug(f'*** Mapped today leagues: {self.today_mapped_leagues}')
            ui_leagues = list([x.split('- ')[2] for x in byb_accordions.keys()])
            cms_leagues_today = list([x for x in self.today_mapped_leagues.values() if x.upper() in ui_leagues])
            for ui_league, mapped_league in zip(ui_leagues, cms_leagues_today):
                self.assertIn(mapped_league.upper(), ui_league,
                              msg=f'Found league "{ui_league}" but expected "{mapped_league.upper()}"')

        if self.upcoming_banach_leagues:
            self.__class__.upcoming_mapped_leagues = self.get_mapped_leagues(date_range='upcoming')
            self._logger.debug(f'*** Mapped upcoming leagues {self.upcoming_mapped_leagues}')
            byb_tab_accordions = self.get_byb_module_accordions(module_name=self.byb_name.upper(),
                                                                switcher_name=vec.yourcall.UPCOMING)
            for mapped_league in self.upcoming_mapped_leagues.values():
                self.assertTrue(any(mapped_league.upper() in s for s in byb_tab_accordions.keys()),
                                msg=f'Upcoming sorting: League "{mapped_league.upper()}" is not present in list'
                                    f' of BYB accordions "{", ".join(byb_tab_accordions.keys())}""')

            self.verify_byb_accordions(byb_tab_accordions=byb_tab_accordions)
            self.__class__.byb_tab_accordions = byb_tab_accordions

    def test_002_verify_collapsing_a_league_accordion(self):
        """
        DESCRIPTION: Verify collapsing a league accordion
        EXPECTED: - Accordion is collapsed
        EXPECTED: - Accordion header collapsed state sign "+" # cannot automate this check: there's no specific html attribute or style to verify this
        """
        for accordion_name, accordion in list(self.byb_tab_accordions.items())[:3]:
            accordion.collapse()
            self.assertFalse(accordion.is_expanded(expected_result=False),
                             msg=f'Accordion "{accordion_name}" is not collapsed')

    def test_003_verify_expanding_a_league_accordion(self):
        """
        DESCRIPTION: Verify expanding a league accordion
        EXPECTED: - League accordion is expanded
        EXPECTED: - Accordion header expanded state sign "-" # cannot automate this check: there's no specific html attribute or style to verify this
        EXPECTED: - Request for Banach events of particular league for defined period of time from preconditions is sent after expanding a league accordion
        """
        for accordion_name, accordion in list(self.byb_tab_accordions.items())[:3]:
            accordion.expand()
            self.assertTrue(accordion.is_expanded(), msg=f'Accordion "{accordion_name}" is not expanded')

    def test_004_verify_events_cards_layout_within_accordions(self):
        """
        DESCRIPTION: Verify events cards layout within accordions
        EXPECTED: - Event cards are displayed in 2 columns if there are 2 and more events in the accordion
        EXPECTED: - The last (the only) event card is stretched to the width of the accordion if there is an odd number of events
        """
        # cannot verify if events are stretched or displayed in 2 columns, can only verify if they CAN be displayed
        # in 2 columns/stretched (by checking if css style is applied)
        pass

    def test_005_verify_event_card_information(self):
        """
        DESCRIPTION: Verify event card information
        EXPECTED: Event card contains:
        EXPECTED: - Match name
        EXPECTED: - Match date and time
        EXPECTED: - "Add to favorite" button
        EXPECTED: - "Go to event" link
        """
        favourites_enabled = self.get_favourites_enabled_status()

        for accordion_name, accordion in list(self.byb_tab_accordions.items())[:1]:
            accordion.expand()
            self.assertTrue(accordion.is_expanded(), msg=f'Accordion "{accordion_name}" is not expanded')
            events = accordion.items_as_ordered_dict
            self.assertTrue(events, msg=f'No events found in "{accordion_name}"')
            for event_name, event in events.items():
                self.assertTrue(event.event_name, msg=f'Event name not found for "{event_name}"')
                self.assertTrue(event.event_date, msg=f'Event date not found for "{event_name}"')
                self.assertTrue(event.has_go_to_event_link(), msg=f'Go to event link not found for "{event_name}"')
                self.assertEqual(favourites_enabled, event.has_favourite_icon(expected_result=favourites_enabled),
                                 msg=f'"Favourites" icon presence status is not "{favourites_enabled}" for event "{event_name}"')
