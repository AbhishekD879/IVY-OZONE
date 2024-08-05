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
class Test_C57732089_Verify_the_displaying_of_the_generic_Upsell_when_there_are_no_current_events(Common):
    """
    TR_ID: C57732089
    NAME: Verify the displaying of the generic Upsell when there are no current events
    DESCRIPTION: This test case verifies the displaying of the generic Upsell when there are no current events.
    PRECONDITIONS: 1. The generic Upsell is configured in the CMS -> QUIZ -> Upsell Configuration:
    PRECONDITIONS: * 1.1 -> The fallback image is uploaded.
    PRECONDITIONS: * 1.2 -> Fallback Image URL is set to an event ID within the app (i.e. /event/9875739)
    PRECONDITIONS: 2. No event is set through QUIZ -> 'Event Details' section:
    PRECONDITIONS: 3. Quiz is configured as active in the CMS.
    PRECONDITIONS: 4.'Entry deadline' is set to the past.
    PRECONDITIONS: 5. The User is logged in.
    PRECONDITIONS: 6. The User has not played this Quiz yet.
    """
    keep_browser_open = True

    def test_001_tap_on_the_see_previous_games_button(self):
        """
        DESCRIPTION: Tap on the 'See Previous Games' button.
        EXPECTED: The User is redirected to the 'Previous' tab of the 'End' page.
        """
        pass

    def test_002_select_the_latest_tab(self):
        """
        DESCRIPTION: Select the 'Latest' tab.
        EXPECTED: 1. The User is navigated to the Latest tab of the Results page.
        EXPECTED: 2. The generic Upsell options with a 'Add to betslip' CTA are displayed.
        EXPECTED: To Clarify:
        EXPECTED: Dynamic upsell (based on user answers) is not applicable in this case since the event is finished. Instead, we should use generic upsell as a fallback.
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d4d9629fcbfc79bf47f04d5
        """
        pass

    def test_003_tap_on_the_image(self):
        """
        DESCRIPTION: Tap on the image.
        EXPECTED: The User is redirected to the previously configured page.
        """
        pass
