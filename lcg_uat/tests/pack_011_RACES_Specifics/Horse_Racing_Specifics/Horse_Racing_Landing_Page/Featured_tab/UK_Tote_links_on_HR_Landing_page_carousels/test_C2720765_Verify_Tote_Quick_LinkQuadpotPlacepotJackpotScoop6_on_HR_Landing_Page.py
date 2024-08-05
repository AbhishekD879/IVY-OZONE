import pytest

from tests.base_test import vtest
from tests.pack_012_UK_Tote.BaseUKTote import BaseUKTote
import voltron.environments.constants as vec
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.international_tote
@vtest
class Test_C2720765_Verify_Tote_Quick_LinkQuadpotPlacepotJackpotScoop6_on_HR_Landing_Page(BaseUKTote):
    """
    TR_ID: C2720765
    NAME: Verify Tote Quick Link(Quadpot/Placepot/Jackpot/Scoop6) on HR Landing Page
    DESCRIPTION: Verify when clicking on **Quadpot/Placepot/Jackpot/Scoop6** Quick Link(indicator) for HR Landing Page it takes user directly to the **Totepool tab > Quadpot/Placepot/Jackpot/Scoop6>LEG1**
    PRECONDITIONS: **CMS configuration**:
    PRECONDITIONS: - Enable **UK Tote feature** (System configuration > Enable_ UK_ Totepools > True) and save changes
    PRECONDITIONS: **Request on Horse Racing Landing page**: PoolForEvent/ *{events_ids}* ?simpleFilter=pool.type:intersects:UPLP,UQDP,UJKP,USC6&translationLang=en
    PRECONDITIONS: **User is on Horse Racing Page landing page with Tote Pool ***Quadpot/Placepot/Jackpot/Scoop6*** Quick Link for UK & IRE Races**
    """
    enable_bs_performance_log = True
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Navigate to Horse Racing Landing page
        EXPECTED: User should be taken on Horse Racing  Landing page
        """
        if not self.get_initial_data_system_configuration().get('TotePools'):
            raise SiteServeException(f'No UK Tote pools available')

        self.get_uk_tote_event()
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')

    def test_001_tap_on_any_quadpot_placepot_jackpot_scoop6_indicator(self):
        """
        DESCRIPTION: Tap on  any **Quadpot / Placepot / Jackpot / Scoop6** indicator
        EXPECTED: - User should be taken on appropriate Horse Racing Event Detail Page with UK Tote (Quadpot / Placepot / Jackpot / Scoop6) pool type
        EXPECTED: - User should be taken directly to the Totepool tab > Quadpot / Placepot / Jackpot / Scoop6 > LEG1
        EXPECTED: - URL should be changed according to the respective pool (e.g **/totepool/quadpot**)
        EXPECTED: - Event time tab is highlighted
        EXPECTED: - Event details are displayed
        EXPECTED: - Totepool Tab is highlighted
        EXPECTED: - Quadpot subtab is selected
        EXPECTED: - Leg1 is selected by default and content is loaded
        """
        current_tab = self.site.horse_racing.tabs_menu.current
        self.assertEqual(current_tab, vec.racing.RACING_DEFAULT_TAB_NAME,
                         msg='Current tab %s is not the same as expected %s'
                             % (current_tab, vec.racing.RACING_DEFAULT_TAB_NAME))

        accordions = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(accordions, msg='No accordions found on Horse Racing Landing page')
        uk_ire_type_name = self.uk_and_ire_type_name
        self.assertIn(self.uk_and_ire_type_name, accordions,
                      msg=f'Failed to display {uk_ire_type_name} accordion')

        accordion = accordions[uk_ire_type_name]
        accordion.expand()
        meetings = accordion.items_as_ordered_dict
        self.assertTrue(meetings, msg=f'No meetings found in "{uk_ire_type_name}"')

        tote_indicator = None
        for meeting in meetings.values():
            if meeting.has_pool_indicators() and meeting.pool_indicator_container.items_as_ordered_dict:
                tote_indicator = list(meeting.pool_indicator_container.items_as_ordered_dict.keys())[0]
                meeting.pool_indicator_container.items_as_ordered_dict[tote_indicator].click()
                break
        if not tote_indicator:
            raise SiteServeException('There is no tote quick links on Horse Racing Landing page')

        self.site.wait_content_state('RacingEventDetails')
        self.assertTrue(self.site.racing_event_details.tab_content.event_off_times_list.selected_item,
                        msg='There is no highlighted Event time tab')

        tab = self.site.racing_event_details.tab_content.event_markets_list
        self.assertEqual(self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.current,
                         vec.racing.RACING_EDP_MARKET_TABS.totepool,
                         msg=f'"{vec.racing.RACING_EDP_MARKET_TABS.totepool}" tab should be opened')

        tab_content = tab.items_as_ordered_dict[vec.racing.RACING_EDP_MARKET_TABS.totepool]
        tote_indicator = tote_indicator.title() if self.brand == "ladbrokes" else tote_indicator
        self.assertEqual(tab_content.grouping_buttons.current, tote_indicator,
                         msg=f'Current tab is "{tab_content.grouping_buttons.current}", but market tab "{tote_indicator}" should be opened ')
        self.assertIn(f'/{vec.uk_tote.TOTEPOOL.lower()}/{tote_indicator.lower()}', self.device.get_current_url(),
                      msg=f'"/{vec.uk_tote.TOTEPOOL.lower()}/{tote_indicator.lower()}" should be present in url')
        self.assertEqual(tab_content.pool.grouping_buttons.current, vec.uk_tote.LEG_1,
                         msg=f'"{vec.uk_tote.LEG_1}" should be selected by default. Currently it is {tab_content.pool.grouping_buttons.current}')

    def test_002_switch_from_totepool_to_win_or_ew_tab_and_back(self):
        """
        DESCRIPTION: Switch from 'Totepool' to 'Win Or E/W' tab and back
        EXPECTED: User should be taken to the the first available Tote pool type
        """
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.win_or_ew)
        active_tab = self.site.racing_event_details.tab_content.event_markets_list.current_market_tab_name
        self.assertEqual(active_tab, vec.racing.RACING_EDP_MARKET_TABS.win_or_ew,
                         msg=f'Incorrect market tab which is active.'
                         f'\nActual: "{active_tab}"\nExpected: "{vec.racing.RACING_EDP_MARKET_TABS.win_or_ew}"')

        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.totepool)

        tab = self.site.racing_event_details.tab_content.event_markets_list
        self.assertEqual(self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.current,
                         vec.racing.RACING_EDP_MARKET_TABS.totepool,
                         msg=f'"{vec.racing.RACING_EDP_MARKET_TABS.totepool}" tab should be opened')

        tab_content = tab.items_as_ordered_dict[vec.racing.RACING_EDP_MARKET_TABS.totepool]
        first_available_tote_pool = list(tab_content.grouping_buttons.items_as_ordered_dict.keys())[0]
        self.assertEqual(tab_content.grouping_buttons.current, first_available_tote_pool,
                         msg=f'"{first_available_tote_pool}" market tab should be opened')
