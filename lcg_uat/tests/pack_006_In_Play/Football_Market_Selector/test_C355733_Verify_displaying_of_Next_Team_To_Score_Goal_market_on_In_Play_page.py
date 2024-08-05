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
# @pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C355733_Verify_displaying_of_Next_Team_To_Score_Goal_market_on_In_Play_page(Common):
    """
    TR_ID: C355733
    NAME: Verify displaying of 'Next Team To Score Goal' market on In-Play page
    DESCRIPTION: This test case verifies displaying of 'Next Team To Score Goal' market on In-Play page
    PRECONDITIONS: **Note:**
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: Create Football Event using 'Next Team To Score' market template and 'Next Team To Score' market name in TI
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the application
    PRECONDITIONS: 2. Navigate to 'In-Play' page
    PRECONDITIONS: 3. Tap on 'Football' icon on Ribbon
    """
    keep_browser_open = True
    new_market_name = '|Next Team to Score Goal 1|'

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

    def test_001_go_to_network___all___preview_and_find_templatemarketname_attribute_for_next_team_to_score_market_in_ss_response(self, inplaytab=True):
        """
        DESCRIPTION: Go to Network -> All -> Preview and find 'templateMarketName attribute' for "Next Team To Score" market in SS response
        EXPECTED: The following value is displayed in the SS response for the event:
        EXPECTED: * templateMarketName="Next Team To Score"
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
        event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=self.event_id)[0]
        self.assertTrue(event_details, msg=f'Event "{self.event_id}" does not exists')
        market = event_details['event']['children'][1]
        template_name = market['market']['templateMarketName'].replace('|', "")
        self.assertEqual(template_name, str(self.old_market_name), msg=f'Actual template name "{template_name}" is not equal to '
                                                                       f'Expected template name "{self.old_market_name}"')
        sleep(6)
        try:
            if self.device_type == 'desktop' and self.brand == 'bma':
                market_selector_list = self.site.football.tab_content.market_selector_element.text.split('\n')
            else:
                market_selector_list = self.site.football.tab_content.dropdown_market_selector.items_names
            self.assertIn(self.old_market_name, market_selector_list,
                          msg=f'actual market list "{market_selector_list}" '
                          f'does not contain expected market "{self.old_market_name}"')
        except Exception:
            if self.device_type == 'desktop' and self.brand == 'bma':
                market_selector_list = self.site.football.tab_content.market_selector_element.text.split('\n')
            else:
                market_selector_list = self.site.football.tab_content.dropdown_market_selector.items_names
            self.assertIn(self.old_market_name, market_selector_list,
                          msg=f'actual market list "{market_selector_list}" '
                          f'does not contain expected market "{self.old_market_name}"')

    def test_002_verify_if_value_is_available_for_football_in_the_market_selector_drop_down(self):
        """
        DESCRIPTION: Verify if value is available for Football in the Market selector drop down
        EXPECTED: 'Next Team To Score' item is present in the Market selector drop down
        """
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

    def test_003_choose_next_team_to_score_item_in_the_market_selector_drop_down(self):
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
        goals = wait_for_result(lambda: event.template.goal_number, bypass_exceptions=(VoltronException, AttributeError),
                                timeout=5)
        self.assertFalse(goals, msg=f'Goals are present for "{self.eventName}"')

    def test_004_verify_if_goals_number_is_displayed_on_sports_card_under_priceodds_button_before_plus__markets_link(self):
        """
        DESCRIPTION: Verify if goals number is displayed on Sports card under Price/Odds button before "+ # Markets" link
        EXPECTED: Goals number is NOT displayed on Sports card
        """
        # covered in step 3

    def test_005_open_tiedit_market_for_the_event_and_add_goals_number_to_market_name_something_like_next_team_to_score_goal_1(self):
        """
        DESCRIPTION: Open TI
        DESCRIPTION: Edit market for the event and add goals number to market name, something like "Next Team To Score Goal 1"
        EXPECTED: Changes are added successfully
        """
        category_id = self.ob_config.football_config.category_id
        class_id = self.ob_config.football_config.autotest_class.class_id
        type_id = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id
        event = CreateSportEvent(env=tests.settings.backend_env, brand=self.brand, category_id=category_id, class_id=class_id,
                                 type_id=type_id)
        event.update_market_settings(market_id=self.market_id, event_id=self.event_id,
                                     market_template_id=self.market_template_id, market_display_sort_code='--',
                                     new_market_name=self.new_market_name)
        self.device.refresh_page()
        sleep(6)

    def test_006_back_to_the_app_and_refresh_the_pagerepeat_steps_1_4_for_the_same_event(self, inplaytab=True):
        """
        DESCRIPTION: Back to the app and refresh the page
        DESCRIPTION: Repeat steps 1-4 for the same event
        """
        self.test_001_go_to_network___all___preview_and_find_templatemarketname_attribute_for_next_team_to_score_market_in_ss_response(inplaytab=inplaytab)
        self.test_002_verify_if_value_is_available_for_football_in_the_market_selector_drop_down()
        self.verfying_event_from_ui()
        event = self.events.get(self.eventName)
        self.assertTrue(event, msg=f'Event "{self.eventName}" is not found among events "{self.events.keys()}"')
        goals = wait_for_result(lambda: event.template.goal_number, bypass_exceptions=(VoltronException, AttributeError), timeout=5)
        if not goals:
            self.test_001_go_to_network___all___preview_and_find_templatemarketname_attribute_for_next_team_to_score_market_in_ss_response(
                inplaytab=inplaytab)
            self.test_002_verify_if_value_is_available_for_football_in_the_market_selector_drop_down()
            self.verfying_event_from_ui()
            event = self.events.get(self.eventName)
            self.assertTrue(event, msg=f'Event "{self.eventName}" is not found among events "{self.events.keys()}"')
            goals = wait_for_result(lambda: event.template.goal_number,
                                    bypass_exceptions=(VoltronException, AttributeError), timeout=3)
        self.assertTrue(goals, msg=f'Goals are not present for "{self.eventName}"')

    def test_007_verify_if_goals_number_is_displayed_on_sports_card_under_priceodds_button_before_plus__markets_link(self):
        """
        DESCRIPTION: Verify if goals number is displayed on Sports card under Price/Odds button before "+ # Markets" link
        EXPECTED: Goals number is displayed on Sports card under Price/Odds button before "+ # Markets" link
        """
        # covered in above step

    def test_008_repeat_steps_1_7_for_in_play_tab_on_football_landing_page(self):
        """
        DESCRIPTION: Repeat steps 1-7 for In-Play tab on Football Landing page
        EXPECTED:
        """
        self.test_000_preconditions()
        self.test_001_go_to_network___all___preview_and_find_templatemarketname_attribute_for_next_team_to_score_market_in_ss_response(inplaytab=False)
        self.test_002_verify_if_value_is_available_for_football_in_the_market_selector_drop_down()
        self.test_003_choose_next_team_to_score_item_in_the_market_selector_drop_down()
        self.test_005_open_tiedit_market_for_the_event_and_add_goals_number_to_market_name_something_like_next_team_to_score_goal_1()
        self.test_006_back_to_the_app_and_refresh_the_pagerepeat_steps_1_4_for_the_same_event(inplaytab=False)
