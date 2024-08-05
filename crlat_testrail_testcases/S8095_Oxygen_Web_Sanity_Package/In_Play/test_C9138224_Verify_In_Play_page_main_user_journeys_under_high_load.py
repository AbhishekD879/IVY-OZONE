import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C9138224_Verify_In_Play_page_main_user_journeys_under_high_load(Common):
    """
    TR_ID: C9138224
    NAME: Verify In-Play page main user journeys under high load
    DESCRIPTION: This test case verifies  In-Play page main user journeys under high load.
    DESCRIPTION: Load test running time or prod load peak period should be used during the testing
    PRECONDITIONS: 1. Load test for In-play page is running OR load peak period in prod is used during the testing.
    PRECONDITIONS: 2. In-Play page is opened in application
    """
    keep_browser_open = True

    def test_001_verify_in_play_page_scrolling_in_following_areas__in_play_tab_on_the_homepage_homein_play__in_play_in_sport_landing_page__in_play_section_with_all_sports_available_in_play(self):
        """
        DESCRIPTION: Verify In-Play page scrolling in following areas:
        DESCRIPTION: - In-Play tab on the Homepage (/home/in-play)
        DESCRIPTION: - In-Play in sport landing page
        DESCRIPTION: - In-Play section with all sports available (in-play)
        EXPECTED: - All page content is scrollable and can be viewed
        EXPECTED: - Loading spinners are not displayed during the scrolling
        """
        pass

    def test_002_verify_switching_between_live_now_and_upcoming_events_in_following_areas__in_play_tab_on_the_homepage_homein_play__in_play_in_sport_landing_page__in_play_section_with_all_sports_available_in_play(self):
        """
        DESCRIPTION: Verify switching between Live Now and Upcoming events in following areas:
        DESCRIPTION: - In-Play tab on the Homepage (/home/in-play)
        DESCRIPTION: - In-Play in sport landing page
        DESCRIPTION: - In-Play section with all sports available (in-play)
        EXPECTED: - User can switch between tabs
        EXPECTED: - All content is updated according to selected tab with any delays
        """
        pass

    def test_003_verify_possibility_to_expand_all_available_modules_in_following_areas__in_play_tab_on_the_homepage_homein_play__in_play_in_sport_landing_page__in_play_section_with_all_sports_available_in_play(self):
        """
        DESCRIPTION: Verify possibility to expand all available modules in following areas:
        DESCRIPTION: - In-Play tab on the Homepage (/home/in-play)
        DESCRIPTION: - In-Play in sport landing page
        DESCRIPTION: - In-Play section with all sports available (in-play)
        EXPECTED: All modules are successfully expanded and module content is loaded without any delays
        """
        pass

    def test_004_verify_live_updates_in_following_areas__in_play_tab_on_the_homepage_homein_play__in_play_in_sport_landing_page__in_play_section_with_all_sports_available_in_play(self):
        """
        DESCRIPTION: Verify live updates in following areas:
        DESCRIPTION: - In-Play tab on the Homepage (/home/in-play)
        DESCRIPTION: - In-Play in sport landing page
        DESCRIPTION: - In-Play section with all sports available (in-play)
        EXPECTED: Live updates are displayed on In-Play page
        EXPECTED: No issues with delays of showing content or rendering of the page
        """
        pass

    def test_005_verify_in_play_data_retrieving_after_connection_is_lost_app_was_inactive_during_the_high_load_for_following_areas__in_play_tab_on_the_homepage_homein_play__in_play_in_sport_landing_page__in_play_section_with_all_sports_available_in_play(self):
        """
        DESCRIPTION: Verify In-Play data retrieving after connection is lost/ app was inactive during the high load for following areas:
        DESCRIPTION: - In-Play tab on the Homepage (/home/in-play)
        DESCRIPTION: - In-Play in sport landing page
        DESCRIPTION: - In-Play section with all sports available (in-play)
        EXPECTED: All data is successfully retrieved for in-play page
        """
        pass
