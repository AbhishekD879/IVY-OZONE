import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import get_in_play_module_from_ws
from voltron.utils.helpers import normalize_name
from voltron.utils.helpers import wait_for_category_in_inplay_module_from_ws


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@pytest.mark.football
@pytest.mark.mobile_only
@vtest
class Test_C9229255_In_play_module_layout_on_Featured_tab_at_the_Homepage(BaseSportTest):
    """
    TR_ID: C9229255
    VOL_ID: C10706707
    NAME: 'In-play' module layout on 'Featured' tab at the Homepage
    DESCRIPTION: This test case verifies 'In-play' module layout on 'Featured' tab at the Homepage
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. The homepage is opened and 'Featured' tab is selected
    PRECONDITIONS: 3. 'In-Play' module with live events is displayed in 'Featured' tab
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - 'In-Play' module should be enabled in CMS > Sports Configs > Structure > In-Play module
    PRECONDITIONS: - 'In-Play' module should be 'Active' in CMS > Sports Pages > Homepage > In-Play module
    PRECONDITIONS: - At least 2 Sports with Live event are added in CMS > Sports Pages > Homepage > In-Play module > Add Sport > Set number of events for Sport
    PRECONDITIONS: - To check data received in featured-sports MS open Dev Tools > Network > WS > featured-sports
    """
    keep_browser_open = True
    module_name = vec.sb.IN_PLAY

    def test_000_preconditions(self):
        """
        DESCRIPTION: 1. Load Oxygen app
        DESCRIPTION: 2. The homepage is opened and 'Featured' tab is selected
        DESCRIPTION: 3. 'In-Play' module with live events is displayed in 'Featured' tab
        """
        self.__class__.sport_name = vec.sb.FOOTBALL if not self.brand == 'ladbrokes' else vec.sb.FOOTBALL.upper()
        inplay_module = self.get_initial_data_system_configuration().get('Inplay Module', {})
        if not inplay_module:
            inplay_module = self.cms_config.get_system_configuration_item('Inplay Module')
        if not inplay_module.get('enabled'):
            raise CmsClientException('"Inplay Module" module is disabled in system config')
        self.site.wait_content_state(state_name='HomePage', timeout=5)
        flatten_names = []
        try:
            in_play_module_data = get_in_play_module_from_ws()['data']
            for sport_segment in in_play_module_data:
                if sport_segment['categoryName'] == 'Football':
                    for event in sport_segment.get('eventsByTypeName')[0].get('events'):
                        flatten_names.append(event['name'])
            self._logger.info(f'*** Found events {flatten_names}')
        except KeyError:
            pass
        if flatten_names:
            self.__class__.event_name = normalize_name(flatten_names[-1])
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
            self.__class__.event_name = event_params.team1 + ' v ' + event_params.team2

        inplay_module = self.cms_config.get_sport_module(module_type='INPLAY')
        id_ = inplay_module[0].get('id')
        sport_details = self.cms_config.get_sport_module_details(_id=id_)
        if inplay_module[0]['disabled']:
            raise CmsClientException('"In play module" module is disabled on homepage')
        num_of_sports_to_display = sport_details.get('inplayConfig').get('maxEventCount')
        self.assertTrue(num_of_sports_to_display >= 2,
                        msg=f'Number of events for Sport is not more then 2 current {num_of_sports_to_display}')

        self.site.wait_content_state(state_name='HomePage', timeout=5)
        home_featured_tab_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        current_tab = self.site.home.module_selection_ribbon.tab_menu.current
        self.assertEqual(current_tab, home_featured_tab_name,
                         msg=f'Actual Module Ribbon tab selected by default: "{current_tab}", '
                         f'expected: "{home_featured_tab_name}"')

    def test_001_verify_in_play_module_layout(self):
        """
        DESCRIPTION: Verify 'In-Play' module layout
        EXPECTED: 'In-Play' module consists of:
        EXPECTED: * In-Play header
        EXPECTED: * Sports container
        EXPECTED: * Event cards
        """
        wait_for_category_in_inplay_module_from_ws(category_id=self.ob_config.football_config.category_id)

        self.__class__.in_play_module = self.site.home.tab_content.in_play_module
        self.assertTrue(self.in_play_module.has_in_play_header(), msg='There is no "In Play" header on the page')
        sports = self.in_play_module.items_as_ordered_dict
        self.assertIn(self.sport_name, sports.keys(), msg=f'{self.sport_name} container is not displayed')
        self.__class__.sport = sports.get(self.sport_name)
        self.assertTrue(self.sport, msg='There is no Event cards on the page')

    def test_002_verify_in_play_module_header(self):
        """
        DESCRIPTION: Verify 'In-Play' module header
        EXPECTED: 'In-Play' module header contains:
        EXPECTED: * 'In-Play' text
        EXPECTED: * 'See all (XX)>' link
        """
        self.assertEqual(self.in_play_module.name, self.module_name,
                         msg=f'Actual module name "{self.in_play_module.name}" is not equal to "{self.module_name}"')
        self.assertTrue(self.in_play_module.has_see_all_link(), msg='No "See All" link')

    def test_003_verify_sports_container(self):
        """
        DESCRIPTION: Verify Sports container
        EXPECTED: * Sports are grouped by SportID
        EXPECTED: * SportName is displayed on Odds Card Header and corresponds to 'categoryName' attribute
        EXPECTED: * Home/Draw/Away or 1/2 (depending on 3 or 2 way primary market) displayed on Odds Card Header
        """
        module = get_in_play_module_from_ws()
        inplay_data = module['data']
        inplay_sports = []
        for sport_segment in inplay_data:
            if sport_segment['eventsIds']:
                if not self.brand == 'ladbrokes':
                    inplay_sports.append(sport_segment['categoryName'])
                else:
                    inplay_sports.append(sport_segment['categoryName'].upper())
        inplay_module_items = self.in_play_module.items_as_ordered_dict
        self.assertTrue(inplay_module_items, msg='Can not find any module items')
        self.assertListEqual(list(inplay_module_items.keys()), inplay_sports,
                             msg=f'Actual In Play module list "{list(inplay_module_items.keys())} is not equal '
                             f'to expected "{inplay_sports}"')

        self.assertEqual(self.sport.fixture_header.header1, vec.sb.HOME,
                         msg=f'Actual fixture header "{self.sport.fixture_header.header1}" does not '
                         f'equal to expected "{vec.sb.HOME}"')
        self.assertEqual(self.sport.fixture_header.header2, vec.sb.DRAW,
                         msg=f'Actual fixture header "{self.sport.fixture_header.header2}" does not '
                         f'equal to expected "{vec.sb.DRAW}"')
        self.assertEqual(self.sport.fixture_header.header3, vec.sb.AWAY,
                         msg=f'Actual fixture header "{self.sport.fixture_header.header3}" does not '
                         f'equal to expected "{vec.sb.AWAY}"')

    def test_004_verify_event_card_elements(self):
        """
        DESCRIPTION: Verify event card elements
        EXPECTED: * Team names/players names
        EXPECTED: * Live/Watch live icons (if available)
        EXPECTED: * Scores (if available)
        EXPECTED: * Match time (if available)
        EXPECTED: * Fav icon (Football only)
        EXPECTED: * Price/odds buttons
        """
        events = self.sport.items_as_ordered_dict
        self.assertIn(self.event_name, events.keys(),
                      msg=f'Event "{self.event_name}" is not present in events list "{events.keys()}"')
        event = events[self.event_name]
        if not self.brand == 'ladbrokes':
            self.assertTrue(event.favourite_icon.is_displayed(), msg='No fav icon')
        self.assertIn(event.first_player, self.event_name,
                      msg=f'First player name "{event.first_player}" is not present in "{self.event_name}"')
        self.assertIn(event.second_player, self.event_name,
                      msg=f'Second player name "{event.second_player}" is not present in "{self.event_name}"')
        self.assertTrue(event.has_watch_live_icon, msg='No watch live icon')
        actual_buttons = event.template.items_as_ordered_dict
        self.assertTrue(actual_buttons, msg=f'No Price/Odds buttons found')
        for price_button_name, price_button in actual_buttons.items():
            self.assertTrue(price_button.is_displayed(),
                            msg=f'Primary Market Price/Odds button "{price_button_name}" is not displayed')
