import pytest
from json import JSONDecodeError
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.helpers import do_request
from tests.base_test import vtest
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  #  Event creation/market value changing is invovled
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C145826_Verify_displaying_of_Total_Goals_Over_Under_in_the_Market_Selector_dropdown_list(BaseSportTest):
    """
    TR_ID: C145826
    NAME: Verify displaying of 'Total Goals Over/Under' in the 'Market Selector' dropdown list
    DESCRIPTION: This test case verifies displaying of 'Total Goals Over/Under' in the 'Market Selector' dropdown list with different "rawHandicapValue" values
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Football Landing page -> 'Matches' tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The market with the following parameters should be created in OB system for a particular event:
    PRECONDITIONS: **'templateMarketName' = Over/Under Total Goals** and **'rawHandicapValue' = 2.5**
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def template_market_name_SS_response(self):

        url = 'market.templateMarketName'
        perflog = self.device.get_performance_log()
        final_request_url = ''

        for log in list(perflog[::-1]):
            try:
                data_dict = log[1]['message']['message']['params']['request']
                request_url = data_dict['url']
                if url in request_url:
                    final_request_url = request_url
                    break
            except (KeyError, JSONDecodeError, TypeError, IndexError):
                continue

        response = do_request(url=final_request_url, method='GET')

        return response

    def template_market_name_raw_handicap_validation(self, raw_handicap_value):

        response = self.template_market_name_SS_response()
        result = False
        for event in response['SSResponse']['children']:
            if "".join(list(event.keys())) == "event":
                for market in event['event']['children']:
                    if market['market']['templateMarketName'] == 'Over/Under Total Goals' or market['market']['templateMarketName'] == 'Total Goals Over/Under':
                        if market['market']['rawHandicapValue'] == raw_handicap_value:
                            result = True
                            return result

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add football event and navigate to football/matches
        EXPECTED: Navigate to Football Matches tab
        """
        markets_params = [('over_under_total_goals', {'cashout': True, 'over_under': 2.5})]
        event = self.ob_config.add_autotest_premier_league_football_event(markets=markets_params)
        self.__class__.eventID = event.event_id
        self.__class__.marketID = self.ob_config.market_ids[event.event_id]['over_under_total_goals']
        self.__class__.market_template_id = \
            self.ob_config.football_config.autotest_class.autotest_premier_league.markets.over_under_total_goals[
                '|Over/Under Total Goals|']

        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('FOOTBALL', timeout=60)

    def test_001_go_to_network___all___preview_and_find_templatemarketname_attribute_for_total_goals_overunder_market_in_ss_response(
            self):
        """
        DESCRIPTION: Go to Network -> All -> **Preview** and find 'templateMarketName' attribute for 'Total Goals Over/Under' market in SS response
        EXPECTED: The following values are displayed in the SS response:
        EXPECTED: * templateMarketName='Over/Under Total Goals'
        EXPECTED: * rawHandicapValue='2.5'
        """
        raw_handicap_value = "2.5"
        result = self.template_market_name_raw_handicap_validation(raw_handicap_value=raw_handicap_value)
        self.assertTrue(result,
                        msg=f'templateMarketName="Over/Under Total Goals" and rawHandicapValue = "{raw_handicap_value}" is not present in SS reponse')

    def test_002_verify_if_the_option_is_present_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify if the option is present in the 'Market Selector' dropdown list
        EXPECTED: 'Total Goals Over/Under 2.5' option is present in the 'Market Selector' dropdown list
        """
        markets_list = list(
            self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        self.assertIn(vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_over_under_2_5,
                      markets_list,
                      msg='Market "Total Goals Over/Under 2.5" is not present in market selector dropdown list')

    def test_003_in_ob_system_edit_the_rawhandicapvalue_value_to_25_for_example_35_and_save_the_changes(self):
        """
        DESCRIPTION: In OB system edit the 'rawHandicapValue' value to **=!2.5** (for example 3.5) and save the changes
        """
        new_handicap_value = "+3.5"
        self.ob_config.change_handicap_market_value(event_id=self.eventID, market_id=self.marketID,
                                                    market_template_id=self.market_template_id,
                                                    new_handicap_value=new_handicap_value)

    def test_004_back_to_the_app_and_refresh_the_page(self):
        """
        DESCRIPTION: Back to the app and refresh the page
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide(10)
        self.site.wait_content_state('FOOTBALL', timeout=30)

    def test_005_go_to_network___all___preview_and_find_templatemarketname_attribute_for_total_goals_overunder_market_in_ss_response(
            self):
        """
        DESCRIPTION: Go to Network -> All -> **Preview** and find 'templateMarketName' attribute for 'Total Goals Over/Under' market in SS response
        EXPECTED: The following values are displayed in the SS response for the edited event:
        EXPECTED: * templateMarketName='Over/Under Total Goals'
        EXPECTED: * rawHandicapValue='3.5' (edited value in the step 3)
        """
        raw_handicap_value = "3.5"
        result = self.template_market_name_raw_handicap_validation(raw_handicap_value=raw_handicap_value)
        self.assertTrue(result,
                        msg=f'templateMarketName="Over/Under Total Goals" and rawHandicapValue = "{raw_handicap_value}" is not present in SS reponse')

    def test_006_verify_if_the_option_is_present_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify if the option is present in the 'Market Selector' dropdown list
        EXPECTED: 'Total Goals Over/Under 3.5' option is NOT present in the 'Market Selector' dropdown list
        """
        markets_list = list(
            self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        self.assertNotIn(vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_over_under_2_5, markets_list,
                         msg='Market "Total Goals Over/Under 2.5" is present in market selector dropdown list')
