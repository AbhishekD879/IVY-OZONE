import pytest
from tests.base_test import vtest
from tests.Common import Common


# @pytest.mark.tst2  # Question engine not configured on qa2
# @pytest.mark.stg2
@pytest.mark.qe_crl_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.question_engine
@pytest.mark.desktop
@vtest
class Test_C57732049_Verify_the_dynamic_Question_Engine_route_naming(Common):
    """
    TR_ID: C57732049
    NAME: Verify the dynamic Question Engine route naming
    DESCRIPTION: This test case verifies the dynamic Question Engine route naming.
    """
    keep_browser_open = True

    def test_000_pre_condtions(self):
        """
        PRECONDITIONS: 1. The User is logged in.
        """
        self.create_question_engine_quiz(pop_up=True)
        user_name = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=user_name)
        self.navigate_to_page('footballsuperseries')

    def test_001_click_on_the_play_now_for_free_button(self):
        """
        DESCRIPTION: Click on the 'Play Now For Free' button.
        EXPECTED: A Question page is opened.
        """
        self.assertTrue(self.site.question_engine.has_cta_button(), msg=f'cta button is not displayed')
        self.site.question_engine.cta_button.click()
        self.__class__.questions = list(self.site.quiz_home_page.question_container.items_as_ordered_dict.values())
        self.assertTrue(self.questions, msg=f' questions are not displayed')

    def test_002_check_the_url(self):
        """
        DESCRIPTION: Check the URL.
        EXPECTED: The URL has '/qe/<sample_name>/questions' route.
        """
        curren_url = self.device.get_current_url()
        expected_url = "/questions"
        self.assertIn(expected_url, curren_url, msg="User is not navigated to expected route")
