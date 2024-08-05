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
class Test_C60037206_Verify_interaction_between_Time_Filters_and_Today_Tomorrow_Future_filter(Common):
    """
    TR_ID: C60037206
    NAME: Verify interaction between Time Filters and Today/Tomorrow/Future filter
    DESCRIPTION: This Test Case verifies interaction between Time Filters and Today/Tomorrow/Future filter
    PRECONDITIONS: * 'Enabled Time Filters' checkbox is ticked in CMS (Sports Pages > Sport Categories > Sport > Matches)
    PRECONDITIONS: * The following Time Filters are configured in CMS: 1 hour, 3 hours, 6 hours, 12 hours, 24 hours, 48 hours (Sports Pages > Sport Categories > Sport > Matches)
    PRECONDITIONS: * Master Toggle should be Enabled in CMS -> System Configuration -> Structure -> Time restriction filters
    PRECONDITIONS: Notes:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints - CMS endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed - CMS creds
    PRECONDITIONS: Designs for filters:
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f4e718f6c5d6903075e47d8 - Coral
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f4e71ac900a50b2123a003b - Ladbrokes
    PRECONDITIONS: **Time Filters are available for Desktop only up to 12 hours and only on Today Tab**
    PRECONDITIONS: 1. Load the app
    """
    keep_browser_open = True

    def test_001_navigate_to_sports_landing_page_today_tab(self):
        """
        DESCRIPTION: Navigate to Sports Landing page (Today Tab)
        EXPECTED: * Time Filters Component is displayed with the following time frames (only for 'Today' tab and only filters up to 12 hours): 1 hour, 3 hours, 6 hours, 12 hours
        EXPECTED: * Filters are not selected or highlighted by default
        """
        pass

    def test_002_switch_to_tomorrow_tab(self):
        """
        DESCRIPTION: Switch to Tomorrow Tab
        EXPECTED: * Time Filters Component is not displayed
        """
        pass

    def test_003_switch_back_to_today_tab_and_select_some_time_filter_eg_3h(self):
        """
        DESCRIPTION: Switch back to Today Tab and Select some Time filter (e.g. 3h)
        EXPECTED: * Selected Time Filter is highlighted
        EXPECTED: * Page loads only Today events (Upcoming Matches List only) that are due to start within the next 3 hours for that given Sport
        EXPECTED: * Events are sorted by Start Time
        """
        pass

    def test_004_switch_to_tomorrow_tab(self):
        """
        DESCRIPTION: Switch to Tomorrow Tab
        EXPECTED: * Time Filters Component is not displayed
        EXPECTED: * Page loads all Tomorrow Events
        """
        pass

    def test_005_switch_back_to_today_tab(self):
        """
        DESCRIPTION: Switch back to Today Tab
        EXPECTED: * Filters are not selected or highlighted
        EXPECTED: * Time Filters Component is displayed with the following time frames (only for 'Today' tab and only filters up to 12 hours): 1 hour, 3 hours, 6 hours, 12 hours
        """
        pass

    def test_006_verify_the_above_steps_for_both_the_tier_1_and_tier_2_sports(self):
        """
        DESCRIPTION: Verify the above steps for both the Tier 1 and Tier 2 sports.
        EXPECTED: The behavior for both the Tier 1 and Tier 2 sports should be as expected.
        """
        pass
