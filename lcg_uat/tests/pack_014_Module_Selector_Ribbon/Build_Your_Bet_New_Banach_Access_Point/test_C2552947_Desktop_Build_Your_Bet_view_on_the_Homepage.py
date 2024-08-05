import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.waiters import wait_for_haul


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.build_your_bet
@pytest.mark.banach
@pytest.mark.reg157_fix
@pytest.mark.module_ribbon
@pytest.mark.homepage
@pytest.mark.high
@vtest
class Test_C2552947_Desktop_Build_Your_Bet_view_on_the_Homepage(BaseBanachTest):
    """
    TR_ID: C2552947
    VOL_ID: C10581854
    NAME: Desktop: 'Build Your Bet' view on the Homepage
    DESCRIPTION: This test case verifies displaying of Build Your Bet (BYB) on the homepage on desktop
    PRECONDITIONS: Request for Banach upcoming leagues: https://buildyourbet-dev1.coralsports.dev.cloud.ladbrokescoral.com/api/v1/leagues-upcoming?days=%&tz=%
    PRECONDITIONS: Request for Banach events of particular league for defined period of time: https://buildyourbet-dev1.coralsports.dev.cloud.ladbrokescoral.com/api/v1/events?dateFrom=2018-06-14T21:00:00.000Z&dateTo=2018-06-15T21:00:00.000Z&leagueIds=xxxx
    PRECONDITIONS: CMS configuration:
    PRECONDITIONS: Build Your Bet tab is available on homepage:
    PRECONDITIONS: 1)BYB is enabled in CMS
    PRECONDITIONS: mobile/tablet/desktop
    PRECONDITIONS: Module Ribbon Tab -> 'Build Your Bet'; 'Visible' = True;
    PRECONDITIONS: Leagues is available when:
    PRECONDITIONS: 1) Banach leagues are mapped in CMS: Your Call > YourCall leagues
    PRECONDITIONS: 2) Banach league is mapped on Banach side
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    byb_module_name = vec.yourcall.DASHBOARD_TITLE
    proxy = None
    byb_on_homepage = True
    device_name = tests.desktop_default

    def check_and_create_byb(self, byb_tab_cms):
        internal_id = 'tab-build-your-bet' if self.brand == 'bma' else 'tab-bet-builder'
        show_tab_on = ['both', 'desktop'] if self.device_type == 'desktop' else ['both', 'mobtablet']
        if byb_tab_cms.get('directiveName') != 'BuildYourBet' or byb_tab_cms.get(
                'internalId') != internal_id or byb_tab_cms.get(
            'showTabOn') not in show_tab_on or not byb_tab_cms.get('universalSegment'):
            self._logger.info(
                f'Configuration of "{self.byb_module_name}" is not created properly. "{self.byb_module_name}" tab is deleting... ')
            self.cms_config.module_ribbon_tabs.delete_tab_by_id(tab_id=byb_tab_cms.get('id'))
            self._logger.info(f'"{self.byb_module_name}" tab is deleted Successfully')
            self._logger.info(f'Creating new tab with the title : "{self.byb_module_name}"  ......')
            self.cms_config.module_ribbon_tabs.create_tab(directive_name='BuildYourBet',
                                                          internal_id=internal_id, title=self.byb_module_name)
            self.cms_config.module_ribbon_tabs._created_tabs.pop()
            self._logger.info(f'"{self.byb_module_name}" tab is created Successfully')
            wait_for_haul(20)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Check BYB events presence
        DESCRIPTION: Check if BYB is enabled in CMS
        """
        self.get_ob_event_with_byb_market()

        byb_leagues_presence = self.check_byb_leagues_presence()
        self.__class__.today_banach_leagues = byb_leagues_presence.today and bool(self.get_mapped_leagues(date_range='today'))
        self.__class__.upcoming_banach_leagues = byb_leagues_presence.upcoming and bool(self.get_mapped_leagues(date_range='upcoming'))

        if not any([self.today_banach_leagues, self.upcoming_banach_leagues]):
            raise SiteServeException('Neither Today nor Upcoming Banach events found')

        if not self.is_bet_builder_tab_created_manually:  # this variable from "BaseBanachTest" class
            byb_tab_cms = next((tab for tab in self.cms_config.module_ribbon_tabs.visible_tabs_data if
                            tab.get('title').upper() == self.byb_module_name), None)
            self.check_and_create_byb(byb_tab_cms=byb_tab_cms)

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('HomePage')

    def test_002_verify_build_your_bet_section_presence(self):
        """
        DESCRIPTION: Verify Build Your Bet section presence
        EXPECTED: Build Your Bet section appears on the Homepage under 'Next Races'
        """
        wait_for_haul(3)
        byb_module = self.site.home.get_module_content(module_name=self.byb_module_name)
        byb_module.scroll_to()

        module_names = list(self.site.home.desktop_modules.items_as_ordered_dict.keys())
        module_above_byb_index = module_names.index(self.byb_module_name) - 1
        module_above_byb_name = module_names[module_above_byb_index]
        home_next_races_tab_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.next_races)
        self.assertEquals(
            module_above_byb_name,
            home_next_races_tab_name,
            f'"{module_above_byb_name}" is above "{self.byb_module_name}" while expected "{home_next_races_tab_name}"'
        )
