import pytest
import tests
from voltron.utils.helpers import do_request
from json import JSONDecodeError
from time import sleep
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C59549194_Verify_SS_query_ChildCount_parameter_for_GET_EventToOutcomeForClass_for_Tier_2_Sports(Common):
    """
    TR_ID: C59549194
    NAME: Verify SS query 'ChildCount' parameter for GET/EventToOutcomeForClass for Tier 2 Sports
    DESCRIPTION: This test case verifies 'ChildCount' parameter for GET/EventToOutcomeForClass for Tier 1 and Tier 2 sports on Matches(Mobile) and Today/Tomorrow/Future subtabs(Desktop)
    PRECONDITIONS: 1. https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs - list of Tier 2 sports.
    PRECONDITIONS: 2. Choose one Football event, one more event from  Tier 2 and Tier 2 sport Outright(Golf, Cycling, Hurling, Motorbikes).
    PRECONDITIONS: 3. Go to Dev Tools > Network > enter 'simpleFilter' in search field > EventToOutcomeForClass.
    """
    enable_bs_performance_log = True
    keep_browser_open = True

    def get_response_url(self, url):
        """
        :param url: Required URl
        :return: Complete url
        """
        perflog = self.device.get_performance_log()
        for log in list(reversed(perflog)):
            try:
                data_dict = log[1]['message']['message']['params']['request']
                request_url = data_dict['url']
                if url in request_url:
                    self.count = + 1
                    return request_url

            except (KeyError, JSONDecodeError, TypeError, IndexError):
                continue

    def test_001_go_to_tier_2_sports_landing_page(self):
        """
        DESCRIPTION: Go to Tier 2 Sports landing page
        EXPECTED: The landing page is open
        """
        if tests.settings.backend_env != 'prod':
            self.ob_config.add_autotest_boxing_event()
            self.ob_config.add_volleyball_event_to_austrian_league()
        self.navigate_to_page('sport/volleyball')
        self.site.wait_content_state('volleyball')

    def test_002_open_dev_tools_details_in_preconditions_and_check_eventtomarketforclass_requests(self):
        """
        DESCRIPTION: Open Dev Tools (details in preconditions) and check EventToMarketForClass requests
        EXPECTED: request to SS /EventToOutcomeForClass on sport landing page has query parameter:
        EXPECTED: **ChildCount** under 'children'
        EXPECTED: With such attributes:
        EXPECTED: childRecordType: "market"
        EXPECTED: count: 'amount of markets'
        EXPECTED: id: 'child id'
        EXPECTED: refRecordId: 'event id'
        EXPECTED: refRecordType: "event"
        EXPECTED: request to SS /EventToMarketForClass on sport landing page is **NOT** received
        """
        sleep(3)
        self.__class__.count = 0
        actual_url = self.get_response_url('/EventToOutcomeForClass')
        response = do_request(method='GET', url=actual_url)
        for event in response['SSResponse']['children']:
            if "".join(list(event.keys())) == "childCount":
                self.assertEquals(event['childCount']['childRecordType'], "market",
                                  msg=event['childCount']['childRecordType'] + f'has not same as "market"')
                self.assertEquals(event['childCount']['refRecordType'], "event",
                                  msg=event['childCount']['refRecordType'] + f'has not same as "event"')
                self.assertTrue(event['childCount']['count'],
                                msg=event['childCount']['count'] + f'count attribute is not available')
                self.assertTrue(event['childCount']['id'],
                                msg=event['childCount']['id'] + f'id  attribute is not available')
                self.assertTrue(event['childCount']['refRecordId'],
                                msg=event['childCount']['refRecordId'] + f'refRecordId attribute is not available')
        self.get_response_url('/EventToMarketForClass')
        self.assertEquals(self.count, 1,
                          msg="request to SS /EventToMarketForClass on sport landing page is  received")

    def test_003_repeat_step_2_for_tier_2_sport_outrightgolf_cycling_hurling_motorbikes(self):
        """
        DESCRIPTION: Repeat step 2 for Tier 2 sport Outright(Golf, Cycling, Hurling, Motorbikes)
        EXPECTED: request to SS /EventToOutcomeForClass on sport landing page has query parameter:
        EXPECTED: **ChildCount** under 'children'
        EXPECTED: With such attributes:
        EXPECTED: childRecordType: "market"
        EXPECTED: count: 'amount of markets'
        EXPECTED: id: 'child id'
        EXPECTED: refRecordId: 'event id'
        EXPECTED: refRecordType: "event"
        EXPECTED: request to SS /EventToMarketForClass on sport landing page is **NOT** received
        """
        self.navigate_to_page('sport/boxing')
        self.site.wait_content_state_changed()
        self.test_002_open_dev_tools_details_in_preconditions_and_check_eventtomarketforclass_requests()
