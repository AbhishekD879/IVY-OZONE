import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C58668195_Verify_the_GA_tracking_of_the_Submit_pop_up(Common):
    """
    TR_ID: C58668195
    NAME: Verify the GA tracking of the Submit pop-up
    DESCRIPTION: This test case verifies the Google Analytics tracking of the Submit pop-up.
    PRECONDITIONS: For more information please consider https://confluence.egalacoral.com/display/SPI/GA+TRACKING+CORRECT+4
    PRECONDITIONS: 1. The Quiz is configured in the CMS.
    PRECONDITIONS: 2. Open the Correct4 https://phoenix-invictus.coral.co.uk/correct4.
    PRECONDITIONS: 3. The User is logged in.
    PRECONDITIONS: 4. The User has not played a Quiz yet.
    PRECONDITIONS: 5. Open DevTools in browser.
    """
    keep_browser_open = True

    def test_001_click_on_the_play_now_for_free_buttonenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Click on the 'Play now for free' button.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackPageview",
        EXPECTED: virtualUrl: “/correct4/question1”​ }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackPageview",
        EXPECTED: virtualUrl: “/{sourceId}/question1”​ }
        """
        pass

    def test_002_select_any_answerenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Select any answer.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackPageview",
        EXPECTED: virtualUrl: “/correct4/question2”​ }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackPageview",
        EXPECTED: virtualUrl: “/{sourceId}/question2”​ }
        """
        pass

    def test_003_repeat_step_2_to_reach_the_last_questionenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Repeat step 2 to reach the last question.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackPageview",
        EXPECTED: virtualUrl: “/correct4/question{number}”​ }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackPageview",
        EXPECTED: virtualUrl: “/{sourceId}/question{number}”​ }
        """
        pass

    def test_004_select_any_answerenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Select any answer.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The 'Submit' pop-up is opened.
        EXPECTED: No additional code is present in the console.
        """
        pass

    def test_005_click_on_the_go_back__edit_buttonenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Click on the 'Go Back & Edit' button.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventAction: "Confirm Your Selections",
        EXPECTED: eventCategory: "Correct4",
        EXPECTED: eventLabel: "Go Back & Edit" }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventAction: "Confirm Your Selections",
        EXPECTED: eventCategory: "{SourceId}",
        EXPECTED: eventLabel: "Go Back & Edit" }
        """
        pass

    def test_006_repeat_step_3_and_4(self):
        """
        DESCRIPTION: Repeat step 3 and 4.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackPageview",
        EXPECTED: virtualUrl: “/correct4/question{number}”​ }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackPageview",
        EXPECTED: virtualUrl: “/{sourceId}/question{number}”​ }
        EXPECTED: The 'Submit' pop-up is opened.
        """
        pass

    def test_007_click_on_the_submit_buttonenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Click on the 'Submit' button.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventAction: "Confirm Your Selections",
        EXPECTED: eventCategory: "Correct4",
        EXPECTED: eventLabel: "Submit" }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackEvent",
        EXPECTED: eventAction: "Confirm Your Selections",
        EXPECTED: eventCategory: "{SourceId}",
        EXPECTED: eventLabel: "Submit" }
        """
        pass
