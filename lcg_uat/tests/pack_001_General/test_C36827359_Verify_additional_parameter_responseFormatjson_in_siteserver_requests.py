import pytest
from json import JSONDecodeError
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.high
@pytest.mark.other
@pytest.mark.desktop
@vtest
class Test_C36827359_Verify_additional_parameter_responseFormatjson_in_siteserver_requests(Common):
    """
    TR_ID: C36827359
    NAME: Verify additional parameter "responseFormat=json" in siteserver requests
    DESCRIPTION: This test case verifies additional parameter "responseFormat=json" in siteserver requests
    DESCRIPTION: NOTE:
    DESCRIPTION: Created after Prod incident https://jira.egalacoral.com/browse/BMA-49510
    PRECONDITIONS: 1. Go to Oxygen application.
    """
    enable_bs_performance_log = True
    keep_browser_open = True
    param = 'responseFormat=json'
    ss_url = 'Event/?simpleFilter'
    Commentary_url = 'openbet-ssviewer/Commentary'

    def get_response_url(self, url):
        """
        :param url: SS or Commentary url
        :return: Complete url
        """
        perflog = self.device.get_performance_log()
        for log in list(reversed(perflog)):
            try:
                data_dict = log[1]['message']['message']['params']['request']
                request_url = data_dict['url']
                if url in request_url:
                    return request_url
            except (KeyError, JSONDecodeError, TypeError, IndexError):
                continue

    def test_001_navigate_through_the_app_pages_where_siteserve_calls_are_madeeg_sports_landing_page_race_landing_page_edp_coupons_etc_and_verify_additional_parameter_responseformatjson_in_siteserver_requests(self):
        """
        DESCRIPTION: Navigate through the app pages where siteserve calls are made(e.g. Sports landing page, Race landing page, EDP, Coupons etc.) and verify additional parameter "responseFormat=json" in siteserver requests.
        EXPECTED: - Siteserve requests contain additional "responseFormat=json" parameter
        EXPECTED: ![](index.php?/attachments/get/18576972)
        """
        self.navigate_to_page("sport/football")
        self.site.wait_content_state("football")
        sp_url = self.get_response_url(url=self.ss_url)
        self.assertIn(self.param, sp_url, msg=f'Required "{self.param}" parameter not found')

        self.navigate_to_page("horse-racing")
        self.site.wait_content_state("HorseRacing")
        racing_url = self.get_response_url(url=self.ss_url)
        self.assertIn(self.param, racing_url, msg=f'Required "{self.param}" parameter not found')

    def test_002_navigate_to_edp_and_verify_the_absence_of_additional_responseformatjson_parameter_in_commentary_request(self):
        """
        DESCRIPTION: Navigate to EDP and verify the additional "responseFormat=json" parameter in Commentary request.
        EXPECTED: - Commentary request has additional "responseFormat=json" parameter
        EXPECTED: ![](index.php?/attachments/get/18576974)
        """
        event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
        self.eventID = event['event']['id']
        self.navigate_to_edp(event_id=self.eventID, sport_name='football')
        edp_url = self.get_response_url(url=self.Commentary_url)
        self.assertIn(self.param, edp_url, msg=f'Required "{self.param}" parameter not found')
