import pytest
import tests
from tests.base_test import vtest
from json import JSONDecodeError
from voltron.environments import constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
# @pytest.mark.hl
# @pytest.mark.lad_prod # we can not disable the Mybets Counter in prod/beta cms
@pytest.mark.negative_p1  # Marker for testcases having negativing scenario like disabling a functionality
@pytest.mark.mobile_only
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C16408287_Verify_my_Bets_counter_is_not_displayed_when_Bets_counter_is_turned_off_in_CMS(BaseUserAccountTest,
                                                                                                    BaseBetSlipTest):
    """
    TR_ID: C16408287
    NAME: Verify my Bets counter is not displayed when Bets counter is turned off in CMS
    DESCRIPTION: This test case verifies disabling Bet counter toggle in CMS
    PRECONDITIONS: 1. CMS-API Endpoints:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: 2. Make sure that development tool is opened once loading Oxygen/Ladbrokes app
    PRECONDITIONS: 3. Make sure to have a user with placed bets (open bets)
    PRECONDITIONS: 4. open Development tool> Network> 'XHR' filter
    """
    keep_browser_open = True
    status = None

    @classmethod
    def custom_tearDown(cls, **kwargs):
        cms_config = cls.get_cms_config()
        bets_counter = cls.get_initial_data_system_configuration().get('BetsCounter')
        if bets_counter:
            bets_counter = cms_config.get_system_configuration_item('BetsCounter')
            if not bets_counter.get('enabled'):
                cms_config.update_system_configuration_structure(config_item='BetsCounter',
                                                                 field_name='enabled',
                                                                 field_value=True)

    def test_001__go_to_cms_and_navigate_to_system_configuration__structure__bet_counter_and_disable_toggle_save_changes(
            self):
        """
        DESCRIPTION: * Go to CMS and navigate to System configuration > Structure > Bet counter and disable toggle
        DESCRIPTION: * Save changes
        EXPECTED: * Changes are submitted successfully
        EXPECTED: * 'Bets counter' is disabled in CMS
        """
        bets_counter = self.get_initial_data_system_configuration().get('BetsCounter')
        if bets_counter:
            bets_counter = self.cms_config.get_system_configuration_item('BetsCounter')
            if not bets_counter.get('disabled'):
                self.cms_config.update_system_configuration_structure(config_item='BetsCounter',
                                                                      field_name='disabled',
                                                                      field_value=False)
        event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.selection_ids = event.selection_ids[event.team1]

    def test_002__load_coralladbrokes_app_and_login_with_user_from_preconditions_verify_that_my_bets_counter_is_not_displayed_on_footer(
            self):
        """
        DESCRIPTION: * Load Coral/Ladbrokes app and login with user from preconditions
        DESCRIPTION: * Verify that 'My Bets' counter is NOT displayed on Footer
        EXPECTED: 'Bet counter' is NOT displayed on the right top corner of 'My Bets' Footer Menu
        """
        self.site.login()
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_single_bet(number_of_stakes=1)
        self.site.bet_receipt.footer.click_done()
        self.site.wait_content_state_changed(timeout=10)
        bets = self.site.navigation_menu.items_as_ordered_dict.get(vec.bet_history.TAB_TITLE)
        self.device.refresh_page()
        self.assertFalse(bets.has_indicator(expected_result=False),
                         msg=' "Bet Counter" is displayed')

    def test_003_check_request_to_get_my_bets_counter_is_not_senteghttpsbpp_dev0ladbrokesoxygendevcloudladbrokescoralcomproxyaccounthistorycountfromdate2018_09_2520153a283a08todate2019_09_2620003a003a00groupbetpagingblocksize20settledn(
            self):
        """
        DESCRIPTION: Check request to get my bets counter is not sent
        DESCRIPTION: (e.g.https://bpp-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/Proxy/accountHistory/count?fromDate=2018-09-25%2015%3A28%3A08&toDate=2019-09-26%2000%3A00%3A00&group=BET&pagingBlockSize=20&settled=N)
        EXPECTED: Request to BBP for betCount is missing
        """
        url = f'{tests.settings.bpp}accountHistory/'
        logs = self.device.get_performance_log()
        for log in list(reversed(logs)):
            try:
                data_dict = log[1]['message']['message']['params']['request']
                request_url = data_dict['url']
                if url in request_url:
                    self.__class__.status = True
                    break
                else:
                    self.__class__.status = False
            except (KeyError, JSONDecodeError, TypeError, IndexError):
                continue
        self.assertFalse(self.status, msg='request to get my bets counter is sent')
