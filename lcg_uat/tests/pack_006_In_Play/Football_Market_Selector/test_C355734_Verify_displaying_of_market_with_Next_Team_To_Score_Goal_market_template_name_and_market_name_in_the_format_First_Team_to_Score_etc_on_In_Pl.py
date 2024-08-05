import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from selenium.webdriver.support.ui import Select
from voltron.utils.waiters import wait_for_result
from voltron.utils.exceptions.voltron_exception import VoltronException
from time import sleep
from crlat_ob_client.create_event import CreateSportEvent


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot modify existing market name in OB for prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C355734_Verify_displaying_of_market_with_Next_Team_To_Score_Goal_market_template_name_and_market_name_in_the_format_First_Team_to_Score_etc_on_In_Play_page(Common):
    """
    TR_ID: C355734
    NAME: Verify displaying of market with 'Next Team To Score Goal' market template name and market name in the format  "First Team to Score" etc. on In-Play page
    DESCRIPTION: This test case verifies displaying of market with 'Next Team To Score Goal' market template name and market name in the format  "First Team to Score" etc. on In-Play page
    PRECONDITIONS: **Note:**
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: Add market for any Football event using 'Next Team To Score' market template and 'First Team to Score' market name in TI
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the application
    PRECONDITIONS: 2. Navigate to 'In-Play' page
    PRECONDITIONS: 3. Tap on 'Football' icon on Ribbon
    """
    keep_browser_open = True
    new_market_name1 = '|First Team to Score|'
    new_market_name2 = '|Second Team to Score|'
    new_market_name3 = '|Secondeer Team to Score|'

    def verfying_event_from_ui(self):
        sleep(6)
        if self.device_type not in ['mobile', 'tablet']:
            grouping_buttons = self.site.inplay.tab_content
            self.assertTrue(grouping_buttons,
                            msg=f'"Live" events are not available in inplay tab for sport ""')
            self.__class__.actual_sport_type = grouping_buttons.accordions_list.items_as_ordered_dict[
                'AUTO TEST - AUTOTEST PREMIER LEAGUE']
        else:
            grouping_buttons = self.site.inplay.tab_content.live_now
            self.assertTrue(grouping_buttons, msg=f'"Live" events are not available in inplay tab for sport "')
            self.__class__.actual_sport_type = grouping_buttons.items_as_ordered_dict['AUTOTEST PREMIER LEAGUE']
        self.__class__.events = self.actual_sport_type.items_as_ordered_dict
        self.assertTrue(self.events, msg=f'No events found in league "AUTOTEST PREMIER LEAGUE"')
        section_header = self.actual_sport_type.fixture_header
        self.assertEqual(section_header.header1, vec.sb.HOME,
                         msg=f'Actual fixture header "{section_header.header1}" does not equal to'
                             f'Expected "{vec.sb.HOME}"')
        self.assertEqual(section_header.header2, vec.sb.AWAY,
                         msg=f'Actual fixture header "{section_header.header2}" does not equal to'
                             f'Expected "{vec.sb.AWAY}"')
        self.assertEqual(section_header.header3, vec.sb.NO_GOAL,
                         msg=f'Actual fixture header "{section_header.header2}" does not equal to'
                             f'Expected "{vec.sb.NO_GOAL}"')

    def test_000_preconditions(self):
        """
         PRECONDITIONS: Create Football Event using 'Next Team To Score' market template and 'Next Team To Score' market name in TI
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(markets=[('next_team_to_score',)], is_live=True)
        self.__class__.event_id = event_params.event_id
        market = event_params.ss_response['event']['children'][1]['market']
        self.__class__.market_id = market['id']
        self.__class__.old_market_name = market['templateMarketName']
        self.__class__.market_template_id = market['templateMarketId']
        self.__class__.eventName = event_params.ss_response['event']['name']
        self.__class__.category_id = self.ob_config.football_config.category_id
        self.__class__.class_id = self.ob_config.football_config.autotest_class.class_id
        self.__class__.type_id = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id
        event = CreateSportEvent(env=tests.settings.backend_env, brand=self.brand, category_id=self.category_id,
                                 class_id=self.class_id, type_id=self.type_id)
        event.update_market_settings(market_id=self.market_id, event_id=self.event_id,
                                     market_template_id=self.market_template_id, market_display_sort_code='--',
                                     new_market_name=self.new_market_name1)

    def test_001_clicktap_on_market_selector(self, inplaytab=True):
        """
        DESCRIPTION: Click/Tap on 'Market selector'
        EXPECTED: 'Next Team To Score' item is present in the Market selector drop down
        """
        sleep(4)
        if inplaytab:
            self.navigate_to_page('in-play/football')
            self.device.refresh_page()
        else:
            self.navigate_to_page('sport/football/live')
            self.site.football.tabs_menu.click_button(vec.siteserve.IN_PLAY_TAB)
            self.device.refresh_page()
            self.site.football.tabs_menu.click_button(vec.siteserve.IN_PLAY_TAB)
        self.site.wait_content_state_changed(timeout=6)
        sleep(6)
        try:
            if self.device_type == 'desktop' and self.brand == 'bma':
                market_selector_list = []
                market_selector = self.site.football.tab_content.market_selector_element.text.split('\n')
                for item in market_selector:
                    market_selector_list.append(item.strip())
            else:
                market_selector_list = self.site.football.tab_content.dropdown_market_selector.items_names
            self.assertIn(self.old_market_name, market_selector_list,
                          msg=f'actual market list "{market_selector_list}" '
                              f'does not contain expected market "{self.old_market_name}"')
        except Exception:
            if self.device_type == 'desktop' and self.brand == 'bma':
                market_selector_list = []
                market_selector = self.site.football.tab_content.market_selector_element.text.split('\n')
                for item in market_selector:
                    market_selector_list.append(item.strip())
            else:
                market_selector_list = self.site.football.tab_content.dropdown_market_selector.items_names
            self.assertIn(self.old_market_name, market_selector_list,
                          msg=f'actual market list "{market_selector_list}" '
                              f'does not contain expected market "{self.old_market_name}"')
        self.site.wait_content_state_changed(timeout=6)
        try:
            if self.device_type == 'desktop' and self.brand == 'bma':
                select = Select(self.site.football.tab_content.market_selector_element)
                select.select_by_visible_text(self.market_name_higest_order)
            else:
                self.site.football.tab_content.dropdown_market_selector.select_value(self.old_market_name)
        except Exception:
            if self.device_type == 'desktop' and self.brand == 'bma':
                select = Select(self.site.football.tab_content.market_selector_element)
                select.select_by_visible_text(self.old_market_name)
            else:
                self.site.football.tab_content.dropdown_market_selector.select_value(self.old_market_name)

    def test_002_choose_next_team_to_score_item_in_the_market_selector_drop_down(self):
        """
        DESCRIPTION: Choose 'Next Team To Score' item in the Market selector drop down
        EXPECTED: * Only event that contains 'Next Team To Score' market is displayed
        EXPECTED: * The fixture header for this market contains following titles:
        EXPECTED: * Home
        EXPECTED: * Away
        EXPECTED: * No Goal
        """
        self.verfying_event_from_ui()
        event = self.events.get(self.eventName)
        self.assertTrue(event, msg=f'Event "{self.eventName}" is not found among events "{self.events.keys()}"')
        goals = wait_for_result(lambda: event.template.goal_number,
                                bypass_exceptions=(VoltronException, AttributeError),
                                timeout=5)
        self.assertTrue(goals, msg=f'Goals are not present for "{self.eventName}"')

    def test_003_verify_if_goals_number_is_displayed_on_sports_card_under_priceodds_button_before_plus__markets_link(self):
        """
        DESCRIPTION: Verify if goals number is displayed on Sports card under Price/Odds button before "+ # Markets" link
        EXPECTED: Goals number is displayed on Sports card
        """
        # Covered in above step

    def test_004_repeat_steps_1_3_for_different_number_of_goals_for_example_second_third_etc(self, inplaytab=True):
        """
        DESCRIPTION: Repeat steps 1-3 for different number of goals, for example, Second, Third, etc.
        EXPECTED: Goals number is displayed on Sports card
        """
        event = CreateSportEvent(env=tests.settings.backend_env, brand=self.brand, category_id=self.category_id,
                                 class_id=self.class_id, type_id=self.type_id)
        event.update_market_settings(market_id=self.market_id, event_id=self.event_id,
                                     market_template_id=self.market_template_id, market_display_sort_code='--',
                                     new_market_name=self.new_market_name2)
        self.device.refresh_page()
        self.test_001_clicktap_on_market_selector(inplaytab=inplaytab)
        self.test_002_choose_next_team_to_score_item_in_the_market_selector_drop_down()

    def test_005_repeat_steps_1_3_for_an_incorect_number_of_goals_for_example_make_grammar_mistake_seconde_etc(self, inplaytab=True):
        """
        DESCRIPTION: Repeat steps 1-3 for an incorect number of goals, for example, make grammar mistake 'Seconde', etc.
        EXPECTED: Goals number is NOT displayed on Sports card
        """
        event = CreateSportEvent(env=tests.settings.backend_env, brand=self.brand, category_id=self.category_id,
                                 class_id=self.class_id, type_id=self.type_id)
        event.update_market_settings(market_id=self.market_id, event_id=self.event_id,
                                     market_template_id=self.market_template_id, market_display_sort_code='--',
                                     new_market_name=self.new_market_name3)
        self.device.refresh_page()
        self.test_001_clicktap_on_market_selector(inplaytab=inplaytab)
        self.verfying_event_from_ui()
        event = self.events.get(self.eventName)
        self.assertTrue(event, msg=f'Event "{self.eventName}" is not found among events "{self.events.keys()}"')
        goals = wait_for_result(lambda: event.template.goal_number,
                                bypass_exceptions=(VoltronException, AttributeError),
                                timeout=5)
        self.assertFalse(goals, msg=f'Goals are present for "{self.eventName}"')

    def test_006_repeat_steps_1_5_for_in_play_tab_on_football_landing_page(self):
        """
        DESCRIPTION: Repeat steps 1-5 for In-Play tab on Football Landing page
        """
        self.test_000_preconditions()
        self.test_001_clicktap_on_market_selector(inplaytab=False)
        self.test_002_choose_next_team_to_score_item_in_the_market_selector_drop_down()
        self.test_004_repeat_steps_1_3_for_different_number_of_goals_for_example_second_third_etc(inplaytab=False)
        self.test_005_repeat_steps_1_3_for_an_incorect_number_of_goals_for_example_make_grammar_mistake_seconde_etc(inplaytab=False)
