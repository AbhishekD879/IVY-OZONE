import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870268_Verify_user_navigates_to_relevant_event_or_sports_when_clicking_on_the_odd_boost_tokens__Click_on_event_specific_odd_boost_token_and_check_user_navigates_to_particular_event__Click_on_odd_boost_token_which_can_use_for_any_sports_check_user_naviga(Common):
    """
    TR_ID: C44870268
    NAME: "Verify user navigates to relevant event or sports when clicking on the odd boost tokens - Click on event specific odd boost token and check user navigates to particular event. - Click on odd boost token which can use for any sports check user naviga
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_verify_user_navigates_to_relevant_event_or_sports_when_clicking_on_the_odd_boost_tokens(self):
        """
        DESCRIPTION: Verify user navigates to relevant event or sports when clicking on the odd boost tokens
        EXPECTED: when clicking on the odd boost tokens user is navigated to relevant event or sports successfully
        """
        pass

    def test_002_click_on_event_specific_odd_boost_token_and_check_user_navigates_to_particular_event(self):
        """
        DESCRIPTION: Click on event specific odd boost token and check user navigates to particular event.
        EXPECTED: when clicking on the odd boost tokens user is navigated to event specific page (edp)successfully
        """
        pass

    def test_003_click_on_odd_boost_token_which_can_use_for_any_sports_check_user_navigates_to_homepage(self):
        """
        DESCRIPTION: Click on odd boost token which can use for any sports check user navigates to homepage.
        EXPECTED: User is navigated to the homepage
        """
        pass

    def test_004_click_on_sports_specific_token_and_check_user_navigates_to_particular_sports_landing_page(self):
        """
        DESCRIPTION: Click on sports specific token and check user navigates to particular sports landing page"
        EXPECTED: User is navigated to particular sports landing page
        """
        pass
