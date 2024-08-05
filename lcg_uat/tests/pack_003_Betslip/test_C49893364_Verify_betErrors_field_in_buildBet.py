import pytest
import tests
import json
import voltron.environments.constants as vec
from tests.base_test import vtest
from voltron.utils.helpers import do_request
from voltron.utils.waiters import wait_for_result
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot verify details in OB
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.betslip
@vtest
class Test_C49893364_Verify_betErrors_field_in_buildBet(BaseBetSlipTest, BaseDataLayerTest):
    """
    TR_ID: C49893364
    NAME: Verify <betErrors> field in <buildBet>
    DESCRIPTION: This test case verifies <betErrors> field in <buildBet> request after adding selection to BetSlip
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
        self.__class__.event1 = self.ob_config.add_autotest_premier_league_football_event(markets=[('both_teams_to_score', {'cashout': True})])
        self.__class__.markets = list(self.event1.selection_ids.values())
        self.__class__.selection_ids = list(self.markets[1].values())
        event2 = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.selection_ids_2 = list(event2.selection_ids.values())
        self.__class__.ss_request = self.ss_req.ss_event_to_outcome_for_event(event_id=self.event1.event_id,
                                                                              query_builder=self.ss_query_builder)
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

    def test_004_add_2_selections_from_different_events_to_betslip(self):
        """
        DESCRIPTION: Add 2 selections from different events to Betslip
        EXPECTED: Both selections are added to Betslip
        """
        self.open_betslip_with_selections(selection_ids=(self.selection_ids[0], self.selection_ids_2[0]))

    def test_005_go_to_ti_and_open_one_of_selections_added_to_betslip_previously(self):
        """
        DESCRIPTION: Go to TI, and open one of selections, added to Betslip previously
        EXPECTED: '~ti/hierarchy/selection/selection_id' is opened
        """
        # covered in step 6

    def test_006_change_selections_status_to_suspended_save_changes(self):
        """
        DESCRIPTION: Change selection's Status to 'Suspended', save changes
        """
        self.ob_config.change_selection_state(selection_id=self.selection_ids[0])
        self.device.refresh_page()
        self.site.wait_content_state_changed(timeout=15)

    def test_007_open_oxygen_and_verify_that_one_of_selections_in_betslip_became_suspended(self):
        """
        DESCRIPTION: Open Oxygen and verify that one of selections in Betslip became suspended
        """
        sections = self.get_betslip_sections().Singles
        stake = list(sections.values())[0]
        stake2 = list(sections.values())[1]
        result = wait_for_result(lambda: stake.suspended_stake_label, name='SUSPENDED label to appear',
                                 timeout=20)
        self.assertEqual(result.strip('"'), vec.betslip.SUSPENDED_LABEL,
                         msg=f'"{vec.betslip.SUSPENDED_LABEL}" does not appear Actual content "{result}"')
        stake2.remove_button.click()

    def test_008_remove_active_selection_from_betslip_open_newest_buildbet_request(self):
        """
        DESCRIPTION: Remove ACTIVE selection from Betslip, open newest buildBet request
        EXPECTED: buildBet request is in the requests list with next branches:
        EXPECTED: - legs
        EXPECTED: - bets
        EXPECTED: - outcomeDetails
        EXPECTED: - betErrors
        """
        expected_branches = sorted(['legs', 'bets', 'outcomeDetails', 'betErrors'])

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
        self.__class__.bet_errors = req['betErrors'][0]

    def test_009_expand_outcomedetails_and_beterrors_branches(self):
        """
        DESCRIPTION: Expand outcomeDetails and betErrors branches
        EXPECTED: Next result is displayed (example):
        EXPECTED: outcomeDetails:
        EXPECTED: 0: {id: "112957526", priceNum: "1", priceDen: "56", startPriceNum: "", startPriceDen: "", fbResult: "H"}
        EXPECTED: id: "112957526"
        EXPECTED: priceNum: "1"
        EXPECTED: priceDen: "56"
        EXPECTED: startPriceNum: ""
        EXPECTED: startPriceDen: ""
        EXPECTED: fbResult: "H"
        EXPECTED: eventMarketSort: "MR"
        EXPECTED: handicap: ""
        EXPECTED: eachWayNum: ""
        EXPECTED: eachWayDen: ""
        EXPECTED: eachWayPlaces: ""
        EXPECTED: name: "|Bumble|"
        EXPECTED: marketId: "31500162"
        EXPECTED: marketDesc: "|Match Betting|"
        EXPECTED: eventId: "776548"
        EXPECTED: eventDesc: "|Bumble| |vs| |Bee DNTOUCH|"
        EXPECTED: typeId: "442"
        EXPECTED: typeDesc: "|Premier League|"
        EXPECTED: classId: "97"
        EXPECTED: className: "|Football England|"
        EXPECTED: categoryId: "16"
        EXPECTED: category: "FOOTBALL"
        EXPECTED: status: "S"
        EXPECTED: birIndex: ""
        EXPECTED: accMin: "1"
        EXPECTED: accMax: "25"
        EXPECTED: betErrors: [{errorDesc: "Bet override found", subErrorCode: "OUTCOME_SUSPENDED", code: "EVENT_ERROR"}]
        EXPECTED: 0: {errorDesc: "Bet override found", subErrorCode: "OUTCOME_SUSPENDED", code: "EVENT_ERROR"}
        EXPECTED: errorDesc: "Bet override found"
        EXPECTED: subErrorCode: "OUTCOME_SUSPENDED"
        EXPECTED: code: "EVENT_ERROR"
        EXPECTED: outcomeRef: {id: "112957526"}
        """
        ss_event = self.ss_request[0]['event']
        market = self.get_required_value(ss_event['children'], self.outcome_details['marketId'], 'market')
        out_come = self.get_required_value(market['children'], self.outcome_details['id'], 'outcome')
        prices = out_come['children'][0]['price']
        fb_result = '-' if market['name'] == 'Both Teams To Score' else out_come['outcomeMeaningMinorCode']

        each_way_factor_num = self.get_each_way_value(market=market, factor='eachWayFactorNum')
        each_way_factor_den = self.get_each_way_value(market=market, factor='eachWayFactorDen')
        each_way_places = self.get_each_way_value(market=market, factor='eachWayPlaces')

        type_desc = "|" + ss_event['typeName'] + "|" if '|' in self.outcome_details['typeDesc'] else ss_event[
            'typeName']
        class_name = "|" + ss_event['className'] + "|" if '|' in self.outcome_details['className'] else ss_event[
            'className']

        expected_response = \
            {
                'id': out_come['id'],
                'priceNum': prices['priceNum'],
                'priceDen': prices['priceDen'],
                'startPriceNum': '',
                'startPriceDen': '',
                'fbResult': fb_result,
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
                'status': 'S',
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

        expected_bet_error_response = \
            {
                'errorDesc': 'Bet override found',
                'subErrorCode': 'OUTCOME_SUSPENDED',
                'code': 'EVENT_ERROR',
                'outcomeRef': {'id': out_come['id']}
            }
        self.compare_json_response(self.bet_errors, expected_bet_error_response)
        self.site.betslip.remove_all_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_REMOVE_ALL)
        dialog.continue_button.click()

    def test_010_repeat_steps_8_13_on_market_and_event_levels(self):
        """
        DESCRIPTION: Repeat steps 8-13 on market and event levels
        EXPECTED: Behavior is the same on event and market levels, 'betErrors' branch is added in case of event/market suspension
        """
        # market level
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=(self.selection_ids[1], self.selection_ids_2[1]))
        self.ob_config.change_market_state(event_id=self.event1.event_id, market_id=self.event1.default_market_id)
        self.device.refresh_page()
        self.site.wait_content_state_changed(timeout=15)
        self.test_007_open_oxygen_and_verify_that_one_of_selections_in_betslip_became_suspended()
        self.test_008_remove_active_selection_from_betslip_open_newest_buildbet_request()
        self.test_009_expand_outcomedetails_and_beterrors_branches()

        # event level
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=(list(self.markets[0].values())[0], self.selection_ids_2[1]))
        self.ob_config.change_event_state(event_id=self.event1.event_id)
        self.device.refresh_page()
        self.site.wait_content_state_changed(timeout=15)
        self.test_007_open_oxygen_and_verify_that_one_of_selections_in_betslip_became_suspended()
        self.test_008_remove_active_selection_from_betslip_open_newest_buildbet_request()
        self.test_009_expand_outcomedetails_and_beterrors_branches()
