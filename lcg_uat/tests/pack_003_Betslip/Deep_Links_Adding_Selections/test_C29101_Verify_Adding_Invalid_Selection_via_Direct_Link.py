import voltron.environments.constants as vec
import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # can't change selection state on prod/hl
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.deeplink
@pytest.mark.desktop
@vtest
class Test_C29101_Verify_Adding_Invalid_Selection_via_Direct_Link(BaseBetSlipTest):
    """
    TR_ID: C29101
    TR_ID: C18636113
    NAME: Verify Adding Invalid Selection via Direct Link
    """
    keep_browser_open = True
    expected_selections_on_betslip = 1

    def open_betslip_with_selections(self, selection_ids):
        """
        Using custom method instead of present in BaseBetSlipTest in order to not change logic of common method too much for need of this case.
        :param selection_ids: either a string (single value) or tuple
        """
        selections = ''
        if isinstance(selection_ids, (str, int)):
            selections = selection_ids
        else:
            selections += ''.join(['%s,' % selection for selection in selection_ids])
        url = '%s/betslip/add/%s' % (tests.HOSTNAME, selections.rstrip(','))
        self._logger.info('*** Opening betslip by deeplink via URL: %s' % url)
        self.device.navigate_to(url=url)
        self.site.wait_splash_to_hide()
        self.site.close_all_dialogs(async_close=False, timeout=0.5)
        if self.valid_selection in selections:
            self.assertTrue(self.site.has_betslip_opened(timeout=5), msg='BetSlip not opened')

            self.verify_betslip_counter_change(expected_value=self.expected_selections_on_betslip)
        else:
            self._logger.warning('*** One or more selections are unavailable')
            expected_error_url = f'https://{tests.HOSTNAME}/betslip/unavailable'
            result = wait_for_result(lambda: self.device.get_current_url() == expected_error_url,
                                     name='Page URL to change',
                                     timeout=0.5)
            actual_error_url = self.device.get_current_url()
            self.assertTrue(result,
                            msg=f'Expected "{expected_error_url}" error url, but opened: "{actual_error_url}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event with different selections (valid and invalid)
        """
        selection_ids = self.ob_config.add_autotest_premier_league_football_event().selection_ids
        self.__class__.selection_ids_list = list(selection_ids.values())

        self.ob_config.change_selection_state(selection_id=self.selection_ids_list[0], displayed=False)
        self.ob_config.change_selection_state(selection_id=self.selection_ids_list[1], displayed=False)
        self.__class__.valid_selection = self.selection_ids_list[2]

    def test_001_enter_direct_url_for_adding_selections_to_the_bet_slip_but_instead_of_outcome_id_enter_one_invalid_id(self):
        """
        DESCRIPTION: Enter direct URL for adding selections to the Bet Slip, but instead of outcome id enter one invalid id
        EXPECTED: User sees an error message:
        EXPECTED: *'One or more of your selections are currently unavailable'*
        """

        self.open_betslip_with_selections(selection_ids=self.selection_ids_list[0])

        self.__class__.expected_error_message = vec.betslip.REMOTE_PATTERN_ERROR_MSG
        self.__class__.actual_error_message = self.site.betslip_unavailable.selections_unavailable_message

        self.assertEquals(self.expected_error_message, self.actual_error_message,
                          msg=f'Actual error message, "{self.actual_error_message}",'
                              f' is not as expected: "{self.expected_error_message}"')

        self.__class__.actual_header_text = self.site.betslip_unavailable.header_line.page_title.title
        self.assertEquals(self.actual_header_text, vec.betslip.ERROR,
                          msg=f'Header line, "{self.actual_header_text}", is not "{vec.betslip.ERROR}"')

    def test_002_enter_direct_url_for_adding_selections_to_the_bet_slip_but_enter_several_invalid_ids(self):
        """
        DESCRIPTION: Enter direct URL for adding selections to the Bet Slip, but enter several invalid id's in address bar -> press Enter key
        EXPECTED: User sees an error message displayed on the Betslip:
        EXPECTED: *'One or more of your selections are currently unavailable'*
        """
        self.open_betslip_with_selections(selection_ids=(self.selection_ids_list[0], self.selection_ids_list[1]))

        self.assertEquals(self.expected_error_message, self.actual_error_message,
                          msg=f'Actual error message, "{self.actual_error_message}",'
                              f' is not as expected: "{self.expected_error_message}"')

        self.assertEquals(self.actual_header_text, vec.betslip.ERROR,
                          msg=f'Header line, "{self.actual_header_text}", is not "{vec.betslip.ERROR}"')

    def test_003_enter_direct_url_for_adding_selections_to_the_bet_slip_but_enter_invalid_ids_and_valid_ids(self):
        """
        DESCRIPTION: Enter direct URL for adding selections to the Bet Slip, but enter invalid id's and valid id('s) in address bar -> press Enter key
        EXPECTED: 1.  Bet Slip is opened automatically
        EXPECTED: 2.  **Only valid added selection(s)** with all detailed info are shown
        EXPECTED: 3.  Invalid id's are ignored
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids_list)
