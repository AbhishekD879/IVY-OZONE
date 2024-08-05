import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C59551309_Verify_betradar_scoreboard__iFrame_sizes(Common):
    """
    TR_ID: C59551309
    NAME: Verify betradar scoreboard - iFrame sizes
    DESCRIPTION: Test case verifies betradar scoreboard iframe sizes for iphone 5 and iphone 8
    PRECONDITIONS: 1. TFutsal event(s) should subscribe to Betradar Scoreboards
    PRECONDITIONS: 2. Event should be in InPlay state
    PRECONDITIONS: How to check event is mapped to betradar or not?
    PRECONDITIONS: inspect elements click on inplay event and while loading EDP check for api-key network call. if we get 200 response then event has betradar and if we get 404 this event should show fallback
    PRECONDITIONS: Confluence link:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=139380661
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_url_and_navigate_to_table_tennis_event_landing_page_from_a_z_menu___table_tennis___inplay(self):
        """
        DESCRIPTION: Launch ladbrokes URL and Navigate to Table tennis event landing page from A-Z menu - table tennis - inplay
        EXPECTED: 
        """
        pass

    def test_002_click_on_inplay_event_which_is_subscribed_to_betradar_scoreboard(self):
        """
        DESCRIPTION: click on inplay event which is subscribed to betradar scoreboard
        EXPECTED: Table tennis event detail page should display
        """
        pass

    def test_003_verify_iframe_size_for_iphone_5(self):
        """
        DESCRIPTION: Verify iframe size for Iphone 5
        EXPECTED: EDP visible are should be -77 PX and scoreboard visible are should be - 327 Px
        """
        pass

    def test_004_repeat_above_steps_for_iphone_8(self):
        """
        DESCRIPTION: Repeat above steps for Iphone 8
        EXPECTED: EDP visible are should be -138 PX and scoreboard visible are should be - 364 Px
        EXPECTED: ![](index.php?/attachments/get/106671132)
        """
        pass

    def test_005_launch_coral_application_and_repeat_above_steps(self):
        """
        DESCRIPTION: Launch coral application and repeat above steps
        EXPECTED: should work as expected iframes sizes should match as above steps
        EXPECTED: ![](index.php?/attachments/get/106671133)
        """
        pass
