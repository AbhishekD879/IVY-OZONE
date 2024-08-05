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
class Test_C58668193_Verify_the_GA_tracking_of_the_Question_pages(Common):
    """
    TR_ID: C58668193
    NAME: Verify the GA tracking of the Question pages
    DESCRIPTION: This test case verifies the Google Analytics tracking of the the Question pages.
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
        EXPECTED: virtualUrl: "/{sourceId}/question2" }
        """
        pass

    def test_003_select_any_answerenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Select any answer.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackPageview",
        EXPECTED: virtualUrl: “/correct4/question3”​ }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackPageview",
        EXPECTED: virtualUrl: "/{sourceId}/question3" }
        """
        pass

    def test_004_click_on_the_previous_arrow_buttonenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Click on the Previous arrow button.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackPageview",
        EXPECTED: virtualUrl: “/correct4/question2”​ }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackPageview",
        EXPECTED: virtualUrl: "/{sourceId}/question2" }
        """
        pass

    def test_005_click_on_the_next_arrow_buttonenter_datalayer_in_the_console(self):
        """
        DESCRIPTION: Click on the Next arrow button.
        DESCRIPTION: Enter 'dataLayer' in the console.
        EXPECTED: The following code is present in the console for Coral:
        EXPECTED: { event: "trackPageview",
        EXPECTED: virtualUrl: “/correct4/question3”​ }
        EXPECTED: The following code is present in the console for Ladbrokes:
        EXPECTED: { event: "trackPageview",
        EXPECTED: virtualUrl: "/{sourceId}/question3" }
        """
        pass
