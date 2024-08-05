import pytest
from time import sleep
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.Common import Common


# @pytest.mark.tst2  # QE not configured on qa2
# @pytest.mark.stg2
@pytest.mark.qe_crl_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.question_engine
@pytest.mark.desktop
@pytest.mark.other
@vtest
class Test_C57732082_Verify_the_view_and_data_of_End_page_for_Cash_for_Questions(Common):
    """
    TR_ID: C57732082
    NAME: Verify the view and data of End page for Cash for Questions
    DESCRIPTION: This test case verifies the view and data of End page for Cash for Questions.
    PRECONDITIONS: 1. CMS User is logged in.
    PRECONDITIONS: 2. An active Quiz is configured.
    PRECONDITIONS: 3. Navigate to the 'Quiz Configuration tab.
    PRECONDITIONS: 4. Set all toggles off, except the 'Show Progress bar' and 'Use back button to exit and hide X button'.
    PRECONDITIONS: 5. Save the changes.
    PRECONDITIONS: 6. The User is logged in.
    """
    keep_browser_open = True

    @classmethod
    def custom_tearDown(cls):
        cms_config = cls.get_cms_config()
        cls.question['exitPopup']['description'] = "Leaving the quiz now will mean your answers will not be submitted"
        cms_config.update_question_engine_quiz(quiz_id=cls.quiz_id, title=cls.title, payload=cls.question)

    def test_000_preconditions(self):
        """
        Create a Quiz and login with created User
        """
        self.__class__.question = self.create_question_engine_quiz()
        self.__class__.quiz_id = self.question['id']
        self.__class__.title = self.question['title']
        self.__class__.exitpopup_desc = self.question['exitPopup']['description']
        username = self.gvc_wallet_user_client.register_new_user().username
        self.__class__.user2 = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)

    def test_001_navigate_to_the_page_which_is_configured_in_the_cms_to_trigger_the_quiz_pop_up_eg_football_page(self):
        """
        DESCRIPTION: Navigate to the page, which is configured in the CMS to trigger the Quiz pop-up (e.g. Football page).
        EXPECTED: The Quiz pop-up is opened.
        """
        self.__class__.quiz_popup_url = self.cms_config.get_qe_pop_up_page()['pageUrls']
        self.navigate_to_page(name=self.quiz_popup_url[0:self.quiz_popup_url.rindex('/') + 1], qe=True)
        popup = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_QUIZ, verify_name=False)
        self.assertTrue(popup, msg='Quiz popup is not displayed')
        self.__class__.dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_QUIZ,
                                                          verify_name=False)
        self.dialog.yes_button.click()

    def test_002_tap_the_take_a_quiz_cta_button(self):
        """
        DESCRIPTION: Tap the 'Take a Quiz' CTA button.
        EXPECTED: The User is redirected to the Question page of Cash For Questions.
        """
        self.assertTrue(self.site.question_engine.has_cta_button(), msg=f'cta button is not displayed')
        self.site.question_engine.cta_button.click()

    def test_003_select_the_1st_option_to_trigger_the_end_page_1(self):
        """
        DESCRIPTION: Select the 1st Option to trigger the End page #1.
        EXPECTED: The End page page is displayed and designed accordingly:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d7271e2ccb615186fb53d47.
        """
        self.__class__.questions = list(self.site.quiz_home_page.question_container.items_as_ordered_dict.values())
        for question in self.questions:
            options = list(question.answer_options.items_as_ordered_dict.values())
            options[0].click()
            sleep(4)  # time required to swipe to next question
            self.site.wait_splash_to_hide(timeout=10)
        self.site.quiz_page_popup.submit_button.click()
        sleep(4)
        self.site.wait_splash_to_hide(timeout=10)
        self.assertTrue(self.site.quiz_results_page.latest_tab, msg=f'Quiz not submitted successfully')

    def test_004_makes_changes_in_each_field_in_the_cms_and_save_themreload_the_fe(self):
        """
        DESCRIPTION: Makes changes in each field in the CMS and save them.
        DESCRIPTION: Reload the FE.
        EXPECTED: The changes are reflected on the FE.
        """
        self.question['exitPopup']['description'] = 'updated ' + self.exitpopup_desc
        self.cms_config.update_question_engine_quiz(quiz_id=self.quiz_id, title=self.title, payload=self.question)
        self.device.refresh_page()
        self.site.wait_content_state_changed()

    def test_005_logout_and_login_with_the_credentials_of_the_user_2(self):
        """
        DESCRIPTION: Logout and login with the credentials of the User #2.
        EXPECTED: The User is successfully logged in.
        """
        self.site.logout()
        self.site.login(username=self.user2)

    def test_006_navigate_to_the_page_which_is_configured_in_the_cms_to_trigger_the_quiz_pop_up_eg_football_page(self):
        """
        DESCRIPTION: Navigate to the page, which is configured in the CMS to trigger the Quiz pop-up (e.g. Football page).
        EXPECTED: The Quiz pop-up is opened.
        """
        self.navigate_to_page(name=self.quiz_popup_url[0:self.quiz_popup_url.rindex('/') + 1], qe=True)
        popup = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_QUIZ, verify_name=False)
        self.assertTrue(popup, msg='Quiz popup is not displayed')
        self.__class__.dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_QUIZ,
                                                          verify_name=False)
        self.dialog.yes_button.click()

    def test_007_tap_the_take_a_quiz_cta_button(self):
        """
        DESCRIPTION: Tap the 'Take a Quiz' CTA button.
        EXPECTED: The User is redirected to the Question page of Cash For Questions.
        """
        self.test_002_tap_the_take_a_quiz_cta_button()

    def test_008_select_the_1st_option_to_trigger_the_end_page_2(self):
        """
        DESCRIPTION: Select the 1st Option to trigger the End page #2.
        EXPECTED: The End page page is displayed and designed accordingly:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d7271e2039b774ecd527748.
        """
        self.test_003_select_the_1st_option_to_trigger_the_end_page_1()

    def test_009_makes_changes_in_each_field_in_the_cms_and_save_themreload_the_fe(self):
        """
        DESCRIPTION: Makes changes in each field in the CMS and save them.
        DESCRIPTION: Reload the FE.
        EXPECTED: The changes are reflected on the FE.
        """
        self.question['exitPopup']['description'] = 'updated ' + self.exitpopup_desc
        self.cms_config.update_question_engine_quiz(quiz_id=self.quiz_id, title=self.title, payload=self.question)
        self.device.refresh_page()
        self.site.wait_content_state_changed()
