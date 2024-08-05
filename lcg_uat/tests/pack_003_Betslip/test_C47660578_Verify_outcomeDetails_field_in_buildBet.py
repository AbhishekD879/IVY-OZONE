import pytest
import tests
import json
from tests.base_test import vtest
from selenium.common.exceptions import ElementClickInterceptedException
from voltron.utils.helpers import do_request
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot verify details in OB
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.betslip
@vtest
class Test_C47660578_Verify_outcomeDetails_field_in_buildBet(BaseDataLayerTest):
    """
    TR_ID: C47660578
    NAME: Verify <outcomeDetails> field in <buildBet>
    DESCRIPTION: This test case verifies <outcomeDetails> field in <buildBet> request after adding selection to BetSlip
    PRECONDITIONS: - Oxygen app is loaded
    PRECONDITIONS: - TI is loaded
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    headers = {'Content-Type': 'application/json'}

    @staticmethod
    def get_required_value(children, children_id, required_type):
        for value in children:
            if children_id == value[required_type]['id']:
                return value[required_type]

    @staticmethod
    def get_each_way_value(market, factor):
        try:
            return market[factor]
        except KeyError:
            return ""

    def test_001_open_oxygens_home_page(self):
        """
        DESCRIPTION: Open Oxygen's home page
        EXPECTED: Home page is loaded, list of events is displayed
        EXPECTED: (may be tested from sport landing page or from any other place where User can add selection to BetSlip)
        """
        event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.event_id = event.event_id
        self.site.wait_content_state("Homepage")

    def test_002_open_chrome_devtools_and_apply_network___all_filtering(self):
        """
        DESCRIPTION: Open Chrome DevTools and apply Network - All filtering
        EXPECTED: DevTools window is displayed, filter is applied
        """
        performance_log = self.get_web_socket_response_by_url(url='buildBet')
        self.assertFalse(performance_log, msg=' "Buildbet" is found')

    def test_003_filter_requests_by_buildbet(self):
        """
        DESCRIPTION: Filter requests by <buildBet>
        EXPECTED: List of requests is empty
        """
        # Covered in step 2

    def test_004_click_on_any_selection(self):
        """
        DESCRIPTION: Click on any selection
        EXPECTED: Selection is added to BetSlip
        """
        self.navigate_to_edp(event_id=self.event_id)
        self.site.wait_content_state_changed(timeout=15)
        bet_buttons_list = self.site.home.bet_buttons
        self.assertTrue(bet_buttons_list, msg='No bet buttons on UI')

        for selection in range(len(bet_buttons_list)):
            selection_btn = bet_buttons_list[selection]
            self.site.contents.scroll_to_we(selection_btn)
            if selection_btn.is_enabled():
                try:
                    selection_btn.click()
                    break
                except ElementClickInterceptedException:
                    self._logger.info('ElementClickInterceptedException ..')
                    continue
            else:
                continue

    def test_005_verify_buildbet_request(self):
        """
        DESCRIPTION: Verify <buildBet> request
        EXPECTED: buildBet request is in the requests list with next branches:
        EXPECTED: - legs
        EXPECTED: - bets
        EXPECTED: - outcomeDetails
        """
        expected_branches = sorted(['legs', 'bets', 'outcomeDetails'])

        url = f'{tests.settings.BETTINGMS}v1/buildBet'
        placebet_request = self.get_web_socket_response_by_url(url=url)
        post_data = placebet_request.get('postData')
        data = json.dumps(post_data)

        req = do_request(url=url, data=data, headers=self.headers)
        actual_branches = sorted(list(req.keys()))
        self.assertEquals(actual_branches, expected_branches,
                          msg=f'Actual brances :"{actual_branches}" is not same as'
                              f'Expected branches :"{expected_branches}"')
        self.__class__.outcome_details = req['outcomeDetails'][0]

    def test_006_expand_outcomedetails_branch(self):
        """
        DESCRIPTION: Expand outcomeDetails branch
        EXPECTED: Next attributes with values are displayed (for example):
        EXPECTED: id: "565559538"
        EXPECTED: priceNum: "3"
        EXPECTED: priceDen: "1"
        EXPECTED: startPriceNum: ""
        EXPECTED: startPriceDen: ""
        EXPECTED: eachWayNum: ""
        EXPECTED: eachWayDen: ""
        EXPECTED: eachWayPlaces: ""
        EXPECTED: name: "|Away|"
        EXPECTED: marketId: "151673083"
        EXPECTED: marketDesc: "|Match Betting|"
        EXPECTED: eventId: "10120543"
        EXPECTED: eventDesc: "|Ewd| 1 - 2 |Red|"
        EXPECTED: typeId: "442"
        EXPECTED: typeDesc: "|Premier League|"
        EXPECTED: classId: "97"
        EXPECTED: className: "|Football England|"
        EXPECTED: categoryId: "16"
        EXPECTED: category: "FOOTBALL"
        EXPECTED: status: "A"
        EXPECTED: accMin: "1"
        EXPECTED: accMax: "25"
        """
        # Covered in step 7

    def test_007_go_to_ti_and_verify_value_correctness(self):
        """
        DESCRIPTION: Go to TI and verify value correctness
        EXPECTED: Values are identical
        """
        ss_request = self.ss_req.ss_event_to_outcome_for_event(event_id=self.outcome_details['eventId'], query_builder=self.ss_query_builder)

        ss_event = ss_request[0]['event']
        market = self.get_required_value(ss_event['children'], self.outcome_details['marketId'], 'market')
        out_come = self.get_required_value(market['children'], self.outcome_details['id'], 'outcome')
        prices = out_come['children'][0]['price']

        each_way_factor_num = self.get_each_way_value(market=market, factor='eachWayFactorNum')
        each_way_factor_den = self.get_each_way_value(market=market, factor='eachWayFactorDen')
        each_way_places = self.get_each_way_value(market=market, factor='eachWayPlaces')

        type_desc = "|" + ss_event['typeName'] + "|" if '|' in self.outcome_details['typeDesc'] else ss_event['typeName']
        class_name = "|" + ss_event['className'] + "|" if '|' in self.outcome_details['className'] else ss_event['className']

        expected_response = \
            {
                'id': out_come['id'],
                'priceNum': prices['priceNum'],
                'priceDen': prices['priceDen'],
                'startPriceNum': '',
                'startPriceDen': '',
                'fbResult': out_come['outcomeMeaningMinorCode'],
                'eventMarketSort': out_come['outcomeMeaningMajorCode'],
                'handicap': '',
                'eachWayNum': each_way_factor_num,
                'eachWayDen': each_way_factor_den,
                'eachWayPlaces': each_way_places,
                'name': out_come['name'],
                'marketId': market['id'],
                'marketDesc': market['name'],
                'eventId': ss_event['id'],
                'eventDesc': ss_event['name'],
                'typeId': ss_event['typeId'],
                'typeDesc': type_desc,
                'classId': ss_event['classId'],
                'className': class_name,
                'categoryId': ss_event['categoryId'],
                'category': ss_event['categoryCode'],
                'status': out_come['outcomeStatusCode'],
                'birIndex': '',
                'accMin': market['minAccumulators'],
                'accMax': market['maxAccumulators']
            }

        actual_response_keys = sorted(list(self.outcome_details.keys()))
        expected_response_keys = sorted(list(expected_response.keys()))
        self.assertEquals(actual_response_keys, expected_response_keys,
                          msg=f'Actual response keys: "{actual_response_keys}" is not same as'
                              f'Expected response keys: "{expected_response_keys}"')
        self.compare_json_response(self.outcome_details, expected_response)
