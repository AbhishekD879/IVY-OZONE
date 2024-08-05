import pytest
import voltron.environments.constants as vec
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.base_test import vtest
from json import JSONDecodeError


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.csp
@pytest.mark.other
@pytest.mark.mobile_only
@vtest
class Test_C64881019_Non_segmented_user_should_get_only_one_initial_data_call(BaseUserAccountTest):
    """
    TR_ID: C64881019
    NAME: Non segmented user should get only one initial data call
    DESCRIPTION: This test case verifies initial data call for non segmented user
    PRECONDITIONS: 1) User should mapped to Segment in Optimove Ex SegName = CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL
    PRECONDITIONS: 2)User should not mapped to any of the segment
    """
    enable_bs_performance_log = True
    keep_browser_open = True
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    segment = vec.bma.CSP_CMS_SEGEMENT

    def get_response_url(self, url, segment):
        """
        :param url: Required URl
        :return: Complete url
        """
        initial_data_count = 0
        perflog = self.device.get_performance_log()
        for log in list(reversed(perflog)):
            try:
                data_dict = log[1]['message']['message']['params']['request']
                request_url = data_dict['url']
                if url in request_url:
                    initial_data_count = initial_data_count + 1
            except (KeyError, JSONDecodeError, TypeError, IndexError):
                continue
        if segment:
            self.assertEqual(initial_data_count, 2, msg=" initial data calls count is not correct")
        else:
            self.assertEqual(initial_data_count, 1, msg=" initial data calls count is not correct")

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        username1 = self.gvc_wallet_user_client.register_new_user().username
        self.__class__.username2 = self.gvc_wallet_user_client.register_new_user().username

        self.site.login(username=username1)

    def test_002_login_in_fe_with_user_from_precondition_1(self):
        """
        DESCRIPTION: Login in FE with user from precondition 1
        EXPECTED: User should get 2 initial data calls
        """

        self.site.wait_content_state(state_name='Homepage', timeout=20)
        self.get_response_url('/initial-data/mobile', segment=False)
        self.site.logout()

    def test_003_login_in_fe_with_user_from_precondition_2(self):
        """
        DESCRIPTION: Login in FE with user from precondition 2
        EXPECTED: Non segmented user should get only one initial data call
        """
        self.device.close_current_tab()
        self.create_new_browser_instance()
        self.site.wait_content_state("Homepage")
        self.site.login(username=self.username2)
        self.set_local_storage_cookies_csp(self.cookie_name, self.segment)
        self.device.refresh_page()
        self.get_response_url('/initial-data/mobile', segment=True)
