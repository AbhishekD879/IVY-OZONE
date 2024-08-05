import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.timeline
@vtest
class Test_C59927329_Verify_Post_with_invalid_event_selection_ID(Common):
    """
    TR_ID: C59927329
    NAME: Verify Post with invalid event/selection ID
    DESCRIPTION: This test case verifies how post should be displayed if it contains invalid event/selection ID
    PRECONDITIONS: 1.Posts Count should be set in CMS(CMS>System Configuration - Structure- Timeline)- Enter the total number of posts count and save it- The same count should be reflected in the FE after page refresh in the FE.
    PRECONDITIONS: Confluence instruction - How to create Timeline Template, Campaign, Posts - -
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Creating+Timeline+Template%2C+Campaign+and+Posts
    PRECONDITIONS: 1.Live Campaign is created
    PRECONDITIONS: 2.Post with corrupted selection is available/configured
    PRECONDITIONS: 3.Post with corrupted event is available/configured
    PRECONDITIONS: 4.Post with corrupted event and selection is available/configured
    PRECONDITIONS: 5. Load the app
    PRECONDITIONS: 6. User is logged in
    PRECONDITIONS: Navigate to the page with configured 'Timeline' (e.g./home/featured)
    PRECONDITIONS: Note:
    PRECONDITIONS: Desktop means Mobile Emulator
    PRECONDITIONS: Timeline feature is for both Brands:
    PRECONDITIONS: Ladbrokes - Ladbrokes L
    """
    keep_browser_open = True

    def test_001_tap_on_the_timeline_header(self):
        """
        DESCRIPTION: Tap on the Timeline header
        EXPECTED: - Timeline is opened and displayed in the expanded state
        EXPECTED: - 'POST' response is present with all fields form CMS in WS
        """
        pass

    def test_002_publish_post_with_invalid_selection_on_cms_and_look_on_ui_app_eg_1298140379_12981f37_1298140_frfrefrev(self):
        """
        DESCRIPTION: Publish post with **invalid selection** on CMS and look on UI app, e.g. 1298140379, 12981f37, 1298140, frfrefrev
        EXPECTED: Post is displayed but without price button
        """
        pass

    def test_003_publish_post_with_invalid_event_on_cms_and_look_on_ui_app_eg_10937881_10937h8_fhury784hf(self):
        """
        DESCRIPTION: Publish post with **invalid event** on CMS and look on UI app, e.g. 10937881, 10937h8, fhury784hf
        EXPECTED: Post is displayed but without price button
        """
        pass

    def test_004_publish_post_with_invalid_selection_and_event_on_cms_and_look_on_ui_eg_selection_id_1298140379_12981f37_1298140_frfrefrev_event_id_10937881_10937h8_fhury784hf(self):
        """
        DESCRIPTION: Publish post with **invalid selection and event** on CMS and look on UI, e.g. selection ID: 1298140379, 12981f37, 1298140, frfrefrev; event ID: 10937881, 10937h8, fhury784hf
        EXPECTED: Post is displayed but without price button
        """
        pass
