import pytest
import voltron.environments.constants as vec
from voltron.utils.waiters import wait_for_result
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from time import sleep


# @pytest.mark.lad_stg2 # one two free is not available in lower env
# @pytest.mark.lad_tst2 # one two free is not available in lower env
@pytest.mark.lad_hl
@pytest.mark.lad_prod
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.one_two_free
@pytest.mark.other
@vtest
class Test_C57732125_Verify_displaying_Already_entered_message(BaseCashOutTest):
    """
    TR_ID: C57732125
    NAME: Verify displaying 'Already entered' message
    DESCRIPTION: This test case verifies displaying 'Already entered' message
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. User is logged In
    PRECONDITIONS: 2. User made prediction for the current game
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: user logged in
        """
        self.site.login()
        self.navigate_to_page('1-2-free')
        existing_text = None
        try:
            existing_text = self.site.one_two_free.one_two_free_current_screen.already_entered_text.text.split('1-2')[0].strip()
        except Exception:
            if existing_text is None:
                one_two_free = self.site.one_two_free
                wait_for_result(lambda: one_two_free.one_two_free_welcome_screen.play_button.is_displayed(),
                                timeout=15)
                one_two_free.one_two_free_welcome_screen.play_button.click()
                submit_button = wait_for_result(lambda:
                                                one_two_free.one_two_free_current_screen.submit_button.is_enabled(
                                                    expected_result=True),
                                                timeout=15)
                self.assertTrue(submit_button, msg='"Submit Button" is not active')
                match = list(one_two_free.one_two_free_current_screen.items_as_ordered_dict.values())
                for score in match:
                    score_switchers = score.score_selector_container.items
                    for score_switcher in score_switchers:
                        self.assertTrue(score_switcher.increase_score_up_arrow.is_displayed(),
                                        msg=f'Upper arrow not displayed for "{score.name}".')
                        score_switcher.increase_score_up_arrow.click()
                        sleep(1)
                        actual_score = score_switcher.score
                        self.assertEqual(actual_score, '1',
                                         msg=f'Actual Score "{actual_score}" is not the same as expected "1"')
                        break

                self.assertTrue(submit_button, msg='"Submit Button" is not active')
                one_two_free.one_two_free_current_screen.submit_button.click()
                self.__class__.one_two_free_you_are_in = one_two_free.one_two_free_you_are_in
                self.assertTrue(self.one_two_free_you_are_in, msg=f'"1-2 free you are in" is not displayed')
                self.assertTrue(self.one_two_free_you_are_in.items_as_ordered_dict,
                                msg=f'Upsell Market options is not displayed')
                list(self.one_two_free_you_are_in.items_as_ordered_dict.values())[0].add_to_betslip_button.click()
                betslip_sections = wait_for_result(lambda: self.get_betslip_content().betslip_sections_list,
                                                   timeout=1,
                                                   name='Betslip sections to load')
                self.assertTrue(self.site.has_betslip_opened(),
                                msg='"Betslip not opened and One-Two-Free" widget is not closed')
                self.assertTrue(len(betslip_sections) > 0, msg='No bets found')
                result = vec.betslip.MULTIPLES in betslip_sections
                self.assertEqual(result, True,
                                 msg=f'Multiples presence status "{result}" is not the same as expected "{True}"')
                self.place_multiple_bet(number_of_stakes=1)
                self.check_bet_receipt_is_displayed()
                self.site.bet_receipt.footer.click_done()
                self.navigate_to_page('1-2-free')

    def test_001_open_current_tab(self):
        """
        DESCRIPTION: Open 'Current Tab'
        EXPECTED: - 'Already Played' message displayed on 'Current Tab'
        EXPECTED: - Message retrieved from CMS
        EXPECTED: - Designed according to screen:
        EXPECTED: ![](index.php?/attachments/get/27045)
        """
        cms_already_Played_text = list(self.cms_config.get_one_two_free_static_texts())[1]['pageText4'].split('1-2')[0]
        ui_already_Played_text = \
            self.site.one_two_free.one_two_free_current_screen.already_entered_text.text.split('1-2')[0].strip()
        actual_msg = cms_already_Played_text.split('<')[1].split('>')[1]
        self.assertEqual(actual_msg.rstrip().lstrip(), ui_already_Played_text,
                         msg=f'Actual message "{actual_msg.rstrip()}" '
                             f'is not the same as expected "{ui_already_Played_text}"')
