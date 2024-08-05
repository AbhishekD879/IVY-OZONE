import pytest
import voltron.environments.constants as vec
from json import JSONDecodeError
from tests.base_test import vtest
from tests.pack_012_UK_Tote.BaseUKTote import BaseUKTote
from voltron.utils.helpers import do_request
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2
# @pytest.mark.stg2 #Can't get feed for test envts
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.races
@vtest
class Test_C15478409_Verify_Silks_are_loaded_from_Aggregation_MS(BaseUKTote):
    """
    TR_ID: C15478409
    NAME: Verify Silks are loaded from Aggregation MS
    DESCRIPTION: This test case verifies that Silks are loaded from Aggregation MS (which uses DF API) and return Silk via ID from silks sprite
    PRECONDITIONS: - Horse Racing Event is mapped with DF API data
    PRECONDITIONS: - List of Aggregation MS {envs.}: https://confluence.egalacoral.com/display/SPI/Aggregation+Java
    PRECONDITIONS: https://{env.}/silks/racingpost/17058,243739,266307,61763,...
    PRECONDITIONS: - Silk ID is received in response from https://ld-{env.}.api.datafabric.{env.}.aws.ladbrokescoral.com/v4/sportsbook-api/categories/21/events/{event id}/content?locale=en-GB&api-key={api key}
    PRECONDITIONS: in horses.silk: "{silk id}.png" attribute
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
                    return request_url
            except (KeyError, JSONDecodeError, TypeError, IndexError):
                continue

    def test_000_navigate_to_hr_edp_from_precondition(self):
        """
        DESCRIPTION: Navigate to HR EDP from precondition
        EXPECTED: - Event details page is opened
        EXPECTED: - 'Win or E/W' tab is opened by default
        """
        event = self.get_uk_tote_event()
        event_id = event.event_id
        self.navigate_to_edp(event_id=event_id, sport_name='horse-racing')
        self.site.wait_content_state_changed()
        tab_names = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_names
        win_ew_tab_name = vec.racing.RACING_EDP_DEFAULT_MARKET_TAB
        self.assertIn(win_ew_tab_name, tab_names,
                      msg=f'Win each way tab "{win_ew_tab_name}" is not in the '
                          f'as tabs "{tab_names}"')
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_DEFAULT_MARKET_TAB)

    def test_001_in_browser_devtools_check_how_silks_are_loadedeg_call_to_aggregation_ms_httpsaggregation_dev0coralsportsdevcloudladbrokescoralcomsilksracingpost123203144359184671b187111218882221353238386249844252924(
            self):
        """
        DESCRIPTION: In browser DevTools check how silks are loaded
        DESCRIPTION: (e.g. call to Aggregation MS: https://aggregation-dev0.coralsports.dev.cloud.ladbrokescoral.com/silks/racingpost/123203,144359,184671b,187111,218882,221353,238386,249844,252924)
        EXPECTED: - Silks should be loaded from Aggregation MS by silksIDs
        EXPECTED: (e.g. silk Id of specific horse received in https://ld-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/21/events/502368/content?locale=en-GB&api-key=LDaa2737afbeb24c3db274d412d00b6d3b corresponds to same silk id from Aggregation MS)
        """
        wait_for_result(lambda: self.get_response_url('aggregation'), timeout=10)
        aggregation_url = self.get_response_url('aggregation')
        aggregation_skins = aggregation_url.rsplit("/", 1)[1].split(",")
        sportsbook_api_url = self.get_response_url('sportsbook-api')
        sportsbook_api_response = do_request(method='GET', url=sportsbook_api_url)
        for skin in aggregation_skins:
            self.assertIn(str(skin), str(sportsbook_api_response),
                          msg=f'aggregation skin "{skin}" is not present in "{sportsbook_api_response}"')
