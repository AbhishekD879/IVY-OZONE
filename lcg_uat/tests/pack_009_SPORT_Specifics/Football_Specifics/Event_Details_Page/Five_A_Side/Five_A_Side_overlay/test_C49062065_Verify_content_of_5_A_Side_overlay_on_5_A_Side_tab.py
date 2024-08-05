import pytest
from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_009_SPORT_Specifics.Football_Specifics.Event_Details_Page.Five_A_Side.five_a_side import BaseFiveASide
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import normalize_name


@pytest.mark.lad_tst2  # Ladbrokes only feature
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.event_details
@pytest.mark.five_a_side
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@pytest.mark.banach
@pytest.mark.desktop
@pytest.mark.football
@pytest.mark.cms
@vtest
class Test_C49062065_Verify_content_of_5_A_Side_overlay_on_5_A_Side_tab(BaseFiveASide):
    """
    TR_ID: C49062065
    NAME: Verify content of '5-A-Side' overlay on 5-A-Side tab
    DESCRIPTION: This test case verifies content displaying on '5-A-Side' overlay for 5 A Side
    PRECONDITIONS: 1. Configure 5-A-Side feature in CMS:
    PRECONDITIONS: * Feature is enabled in CMS > System Configuration -> Structure -> FiveASide
    PRECONDITIONS: * Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: * 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: * Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: * Event is prematch (not live)
    PRECONDITIONS: * Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: 2. Create formations:
    PRECONDITIONS: * Fill all fields in CMS -> BYB -> 5-A-Side -> click 'Add New Formation' button -> 'New 5 A Side Formation' popup
    PRECONDITIONS: * Click 'Save' button
    PRECONDITIONS: 3. Load the app
    PRECONDITIONS: 4. Navigate to Football event details page that has all 5-A-Side configs and created formations
    PRECONDITIONS: 5. Click on '5-A-Side' tab
    PRECONDITIONS: 6. Click 'Build' button
    """
    keep_browser_open = True
    proxy = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Verify 5-A-Side formations list from CMS is not empty
        DESCRIPTION: Find active event with Banach markets
        DESCRIPTION: Navigate to Football event details page that has all 5-A-Side configs
        DESCRIPTION: Choose the '5-A-Side' tab
        DESCRIPTION: Click/Tap on the 'Build Team' button on '5-A-Side' launcher
        EXPECTED: Make sure that '5-A-Side' overlay is opened
        """
        self.__class__.cms_formations = self.cms_config.get_five_a_side_formations()
        if not self.cms_formations:
            raise CmsClientException('5-A-Side formations list from CMS is empty')
        event_id = self.get_ob_event_with_byb_market(five_a_side=True)
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
        self.__class__.event_name = normalize_name(event_resp[0]['event']['name'])
        self._logger.info(f'***Found Football 5-A-Side event {self.event_name} with id "{event_id}"')
        self.navigate_to_edp(event_id=event_id, sport_name='football')
        self.site.wait_content_state(state_name='EventDetails')
        five_a_side_tab = self.site.sport_event_details.markets_tabs_list.open_tab(tab_name=self.expected_market_tabs.five_a_side)
        self.assertTrue(five_a_side_tab, msg=f'{self.expected_market_tabs.five_a_side} tab is not active')
        self.site.sport_event_details.tab_content.team_launcher.build_button.click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_pitch_overlay(),
                        msg='Pitch overlay is not shown')

    def test_001_verify_header_content_of_5_a_side_overlay(self):
        """
        DESCRIPTION: Verify Header content of '5-A-Side' overlay
        EXPECTED: The following UI elements should be displayed:
        EXPECTED: * 'Ladbrokes/Coral 5-A-Side' title (depends on brand)
        EXPECTED: * 'Select a formation and build your team' instruction text
        EXPECTED: * Formation toggles carousel with created formations:
        EXPECTED: * formation icon (corresponding to selected in CMS 'Actual formation' dropdown) ![](index.php?/attachments/get/57668477)
        EXPECTED: * formation name below the icon (corresponding to entered in CMS 'Title' input field)
        EXPECTED: * Close 'x' button
        """
        self.__class__.cms_active_formation = self.cms_formations[0]
        self.__class__.pitch_overlay = self.site.sport_event_details.tab_content.pitch_overlay
        title = self.pitch_overlay.header.title
        self.assertTrue(title, msg=f'Header title "{title}" is not available on UI "{vec.yourcall.FIVE_A_SIDE_DRAWER_TITLE}"')
        instruction = self.pitch_overlay.header.instruction_text
        self.assertEqual(
            instruction, vec.yourcall.SELECT_FORMATION,
            msg=f'Instruction text "{instruction}" is not the same as expected "{vec.yourcall.SELECT_FORMATION}"')
        formation_carousel = self.pitch_overlay.content.formation_carousel.items_as_ordered_dict
        self.assertTrue(formation_carousel, msg='Formation toggles carousel is not displayed')
        formation_name, formation_item = next(iter(formation_carousel.items()))
        cms_formation_name = self.cms_active_formation.get("title").upper()
        self.assertEqual(formation_name, cms_formation_name,
                         msg=f'Formation name "{formation_name}" is not the same as expected '
                             f'from cms "{cms_formation_name}"')
        self.assertTrue(formation_item.has_icon(), msg='Formation icon is not displayed')
        self.assertTrue(self.pitch_overlay.header.has_close_button(), msg='Close "x" button is not displayed')

    def test_002_verify_sub_header_content_of_5_a_side_overlay(self):
        """
        DESCRIPTION: Verify Subheader content of '5-A-Side' overlay
        EXPECTED: The following UI elements should be displayed:
        EXPECTED: * Event name
        EXPECTED: * Formation (corresponding to selected in CMS 'Actual formation' dropdown e.g. 1-1-2-1)
        EXPECTED: * 'Ladbrokes'/'Coral' (depends on brand) two logos:
        EXPECTED: ![](index.php?/attachments/get/111268948)
        """
        event_name = self.pitch_overlay.content.sub_header.event_name
        ss_event_name = self.event_name.upper()
        self.assertEqual(
            event_name, ss_event_name,
            msg=f'Event name "{event_name}" on sub-header is not the same as expected "{ss_event_name}"')
        formation_value = self.pitch_overlay.content.formation_value
        cms_formation_value = self.cms_active_formation.get("actualFormation")
        self.assertEqual(formation_value, cms_formation_value,
                         msg=f'Formation "{formation_value}" on sub-header is not the same as expected '
                             f'from cms "{cms_formation_value}"')

    def test_003_verify_body_content_of_5_a_side_overlay(self):
        """
        DESCRIPTION: Verify Body content of '5-A-Side' overlay
        EXPECTED: The following UI elements should be displayed:
        EXPECTED: * Add buttons
        EXPECTED: * Player Information:
        EXPECTED: * Positions (corresponding to entered in CMS 'Position' input field)
        EXPECTED: * Statistics (corresponding to selected in CMS 'Stat' dropdown)
        EXPECTED: * 'Odds / Place Bet' button
        EXPECTED: * Background Pitch Image
        """
        statistics = []
        for stat in self.stat_keys:
            if stat in self.cms_active_formation.keys():
                statistics.append(self.cms_active_formation.get(stat).get('title'))
        markets = self.pitch_overlay.content.football_field.items_as_ordered_dict
        self.assertTrue(markets, msg='Players are not displayed on the Pitch View')
        for market_name, market in markets.items():
            self.assertTrue(market.icon.is_displayed(), msg='Add button is not shown')
            self.assertIn(market_name, statistics,
                          msg=f'Cannot find statistic/market "{market_name}" in "{statistics}"')
        self.assertTrue(self.pitch_overlay.content.football_field.place_bet_button.is_displayed(),
                        msg='"Odds/Place Bet" button is not displayed')
