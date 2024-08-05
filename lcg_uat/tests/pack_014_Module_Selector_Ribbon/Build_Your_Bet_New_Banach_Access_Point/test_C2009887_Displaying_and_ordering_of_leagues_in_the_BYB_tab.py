from collections import OrderedDict

import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import normalize_name


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.build_your_bet
@pytest.mark.banach
@pytest.mark.module_ribbon
@pytest.mark.homepage
@pytest.mark.medium
@pytest.mark.adhoc_suite
@pytest.mark.slow
@pytest.mark.timeout(800)
@vtest
class Test_C2009887_Displaying_and_ordering_of_leagues_in_the_BYB_tab(BaseBanachTest):
    """
    TR_ID: C2009887
    NAME: Displaying and ordering of leagues in the BYB tab
    DESCRIPTION: This test case verifies displaying and ordering of leagues in the BYB tab
    PRECONDITIONS: Request for Banach upcoming leagues: https://buildyourbet-dev1.coralsports.dev.cloud.ladbrokescoral.com/api/v1/leagues-upcoming?days=%&tz=%
    PRECONDITIONS: Request for Banach events of particular league for defined period of time: https://buildyourbet-dev1.coralsports.dev.cloud.ladbrokescoral.com/api/v1/events?dateFrom=2018-06-14T21:00:00.000Z&dateTo=2018-06-15T21:00:00.000Z&leagueIds=xxxx
    PRECONDITIONS: CMS configuration:
    PRECONDITIONS: Build Your Bet tab is available on homepage:
    PRECONDITIONS: 1)BYB is enabled in CMS
    PRECONDITIONS: mobile/tablet/desktop
    PRECONDITIONS: Module Ribbon Tab -> 'Build Your Bet'; 'Visible' = True;
    PRECONDITIONS: Leagues is available on Build Your Bet tab when:
    PRECONDITIONS: 1) Banach leagues are mapped in CMS: Your Call > YourCall leagues
    PRECONDITIONS: 2) Banach league is mapped on Banach side
    """
    keep_browser_open = True
    proxy = None
    byb_name = None
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    segment = vec.bma.CSP_CMS_SEGEMENT
    byb_on_homepage = True

    @staticmethod
    def get_event_names_for_league(response: list) -> list:
        """
        Gets event names list from response of <byb_endpoint>/events?leagueIds=xxx&dateFrom=yyy&dateTo=zzz and normalize white spaces
        :param response: list of event objects (dict)
        :return: event names
        """
        return [normalize_name(event['title']) for event in response]

    def verify_events_in_accordion(self, accordions: OrderedDict, mapped_leagues: dict, day_from: int, day_to: int) -> None:
        """
        Compares if list of events in accordions on UI are the same as from response
        :param accordions: Ordered dictionary with BYB accordions
        :param mapped_leagues: dictionary with OB type id and league name
        :param day_from: day number starting from 0 (today)
        :param day_to: day number 1 (tomorrow)
        """
        league_type_id, league_name = list(mapped_leagues.items())[0]

        accordion_name, accordion = next(
            ((accordion_name, accordion) for accordion_name, accordion in accordions.items()
             if league_name.upper() in accordion_name), (None, None))
        self.assertTrue(accordion_name,
                        msg=f'League "{league_name.upper()}" is not found among BYB accordions "{accordions.keys()}"')
        accordion.expand()
        self.assertTrue(accordion.is_expanded(), msg=f'Accordion "{accordion_name}" is not expanded')
        expected_events_response = self.get_events_for_league(league_id=league_type_id, day_from=day_from,
                                                              day_to=day_to)
        self.assertTrue(expected_events_response,
                        msg=f'No events found for league "{league_name}" with type id "{league_type_id}"')
        expected_events = self.get_event_names_for_league(response=expected_events_response)

        events = accordion.items  # not using items_as_ordered_dict to handle cases when mapped several BYB events with the same name
        self.assertTrue(events, msg=f'No events found in "{accordion_name}"')
        events_ui = [normalize_name(event.event_name) for event in events]
        self.assertLessEqual(events_ui, expected_events, msg=f'Events on UI: \n"{events_ui}" \nare not the same as got '
                                                             f'from BYB response: \n{expected_events}')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Check BYB events presence
        DESCRIPTION: Find BYB tab on Homepage and click on it
        EXPECTED: BYB tab is active
        """
        byb_tab_cms = next((tab.get('title').upper() for i, tab in enumerate(self.cms_config.module_ribbon_tabs.visible_tabs_data)
                            if tab.get('directiveName') == 'BuildYourBet'), None)
        if not byb_tab_cms:
            self.cms_config.module_ribbon_tabs.create_tab(directive_name='BuildYourBet',
                                                          internal_id='tab-build-your-bet', title='BUILD YOUR BET')

        if byb_tab_cms:
            data = next((tab for tab in self.cms_config.module_ribbon_tabs.visible_tabs_data
                         if tab.get('directiveName') == 'BuildYourBet'), None)
            self.__class__.universal_segment = data['universalSegment']
            if not self.universal_segment:
                self.cms_config.module_ribbon_tabs.create_tab(directive_name='BuildYourBet',
                                                              internal_id='tab-build-your-bet', title='BUILD YOUR BET', sort_order=-5)

        self.get_ob_event_with_byb_market()
        self.__class__.byb_name = byb_tab_cms if self.device_type != 'desktop' else vec.yourcall.DASHBOARD_TITLE

        byb_leagues_presence = self.check_byb_leagues_presence()
        self.__class__.today_banach_leagues = byb_leagues_presence.today and bool(self.get_mapped_leagues(date_range='today'))
        self.__class__.upcoming_banach_leagues = byb_leagues_presence.upcoming and bool(self.get_mapped_leagues(date_range='upcoming'))

        if not any([self.today_banach_leagues, self.upcoming_banach_leagues]):
            raise SiteServeException('Neither Today nor Upcoming Banach events found')

        # byb_tab_name = 'BYB V3'  # quick w/a for testing on dev endpoints
        self.__class__.byb_tab_content = self.site.home.get_module_content(module_name=self.byb_name)

    def test_001_verify_ordering_of_leagues_in_today__upcoming_tab(self):
        """
        DESCRIPTION: Verify ordering of leagues in 'Today' / 'Upcoming' tab
        EXPECTED: The order of leagues which appear in BYB is defined by the order defined in CMS>YourCall>YourCall Leagues
        """
        if self.today_banach_leagues:
            byb_accordions = self.get_byb_module_accordions(module_name=self.byb_name)
            self.__class__.today_mapped_leagues = self.get_mapped_leagues(date_range='today')
            self._logger.debug(f'*** Mapped today leagues: {self.today_mapped_leagues}')
            ui_leagues = list([x.split('- ')[2] for x in byb_accordions.keys()])
            cms_leagues_today = list([x for x in self.today_mapped_leagues.values() if x.upper() in ui_leagues])
            for ui_league, mapped_league in zip(ui_leagues, cms_leagues_today):
                self.assertIn(mapped_league.upper(), ui_league,
                              msg=f'Found league "{ui_league}" but expected "{mapped_league.upper()}"')

        if self.upcoming_banach_leagues:
            byb_accordions = self.get_byb_module_accordions(module_name=self.byb_name,
                                                            switcher_name=vec.yourcall.UPCOMING)
            self.__class__.upcoming_mapped_leagues = self.get_mapped_leagues(date_range='upcoming')
            self._logger.debug(f'*** Mapped upcoming leagues {self.upcoming_mapped_leagues}')
            total_leagues = list(
                list(self.upcoming_mapped_leagues.values()) + (list(self.today_mapped_leagues.values())))
            self._logger.debug(f'*** Mapped upcoming leagues {self.upcoming_mapped_leagues}')
            ui_upcoming_leagues = list([' - '.join(x.split(' - ')[2:]) for x in byb_accordions.keys() if 'test' not in x.lower()])
            cms_leagues = list([x.upper() for x in total_leagues])
            for ui_league in ui_upcoming_leagues:
                self.assertIn(ui_league, cms_leagues,
                              msg=f'UI league "{ui_league}" not found in "{cms_leagues}"')

    def test_002_verify_correctness_of_leagues_and_their_events_displaying_in_today_section(self):
        """
        DESCRIPTION: Verify correctness of leagues and their events displaying in 'Today' section
        EXPECTED: Events happening 'Today' appear within their League in the 'Today' section of BYB
        EXPECTED:  corresponding to Request for Banach upcoming leagues/Banach events of particular league
        EXPECTED:  for defined period of time from precondition
        """
        if self.today_banach_leagues:
            byb_tab_accordions = self.get_byb_module_accordions(module_name=self.byb_name)
            self.verify_events_in_accordion(accordions=byb_tab_accordions, mapped_leagues=self.today_mapped_leagues,
                                            day_from=-1, day_to=0)

    def test_003_verify_correctness_of_leagues_and_their_events_displaying_in_upcoming_section(self):
        """
        DESCRIPTION: Verify correctness of leagues and their events displaying in "Upcoming" section
        EXPECTED: Events happening in the future appear within their League in the 'Upcoming' section of
        EXPECTED:  BYB corresponding Request for Banach upcoming leagues/Banach events of particular league
        EXPECTED:  for defined period of time from precondition
        """
        if self.upcoming_banach_leagues:
            byb_tab_accordions = self.get_byb_module_accordions(module_name=self.byb_name,
                                                                switcher_name=vec.yourcall.UPCOMING)
            self.verify_events_in_accordion(accordions=byb_tab_accordions, mapped_leagues=self.upcoming_mapped_leagues,
                                            day_from=0, day_to=5)
