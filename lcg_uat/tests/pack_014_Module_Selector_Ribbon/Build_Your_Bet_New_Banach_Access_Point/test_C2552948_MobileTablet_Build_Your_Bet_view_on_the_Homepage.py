import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.mobile_only
@pytest.mark.build_your_bet
@pytest.mark.banach
@pytest.mark.module_ribbon
@pytest.mark.homepage
@pytest.mark.high
@pytest.mark.reg157_fix
@vtest
class Test_C2552948_MobileTablet_Build_Your_Bet_view_on_the_Homepage(BaseBanachTest):
    """
    TR_ID: C2552948
    VOL_ID: C9698322
    NAME: Mobile/Tablet: Build Your Bet view on the Homepage
    DESCRIPTION: This test case verifies displaying of Build Your Bet (BYB) on the homepage within mobile, tablet
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
    tab_index = None
    tab_name = None
    proxy = None
    byb_on_homepage = True
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    segment = vec.bma.CSP_CMS_SEGEMENT
    build_your_bet_internal_id = 'tab-bet-builder' if tests.settings.brand != "bma" else 'tab-build-your-bet'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Check BYB events presence
        DESCRIPTION: Check Build Your Bet module is configured in CMS
        """
        self.get_ob_event_with_byb_market()
        byb_leagues_presence = self.check_byb_leagues_presence()
        self.__class__.today_banach_leagues = byb_leagues_presence.today and bool(self.get_mapped_leagues(date_range='today'))
        self.__class__.upcoming_banach_leagues = byb_leagues_presence.upcoming and bool(self.get_mapped_leagues(date_range='upcoming'))

        if not any([self.today_banach_leagues, self.upcoming_banach_leagues]):
            raise SiteServeException('Neither Today nor Upcoming Banach events found')

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
            if tests.settings.cms_env == 'prd0':
                self.cms_config.module_ribbon_tabs.create_tab(directive_name='BuildYourBet',
                                                              internal_id='tab-bet-builder', title='BUILD YOUR BET',
                                                              inclusionList=[self.segment], universalSegment=False)
            self.cms_config.module_ribbon_tabs.create_tab(directive_name='BuildYourBet')
        self.__class__.tab_index, self.__class__.tab_name = byb_ribbon_tabs[0]

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('HomePage')
        if not self.universal_segment:
            self.site.login()
            self.set_local_storage_cookies_csp(self.cookie_name, self.segment)
            self.device.refresh_page()
            self.site.wait_content_state(state_name='Homepage', timeout=20)

    def test_002_go_to_module_selector_ribbon_and_verify_build_your_bet_tab_presence(self):
        """
        DESCRIPTION: Go to Module Selector Ribbon and verify Build Your Bet tab presence
        EXPECTED: * Build Your Bet tab is displayed in Module Selector Ribbon on the Homepage
        EXPECTED: * Build Your Bet tab position corresponds to the position set in CMS (Module Ribbon Tabs order)
        """
        ui_tabs = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
        self.assertGreater(len(ui_tabs), 0, msg='No Module ribbon tabs found')
        ui_tab_keys = list(ui_tabs.keys())
        self._logger.debug(
            'Tab names on UI: %s' % ui_tab_keys
        )
        cms_byb_name = self.get_ribbon_tab_name(self.build_your_bet_internal_id)
        ui_byb_name = [key.upper() for key in ui_tab_keys]

        self.assertIn(
            cms_byb_name,
            ui_byb_name,
            f'BYB Tab name mismatch CMS ("{cms_byb_name}") not on UI ("{ui_byb_name}")')
        # byb_tab_name = 'BYB V3'  # quick w/a for testing on dev endpoints
        self.site.home.get_module_content(module_name=cms_byb_name)
