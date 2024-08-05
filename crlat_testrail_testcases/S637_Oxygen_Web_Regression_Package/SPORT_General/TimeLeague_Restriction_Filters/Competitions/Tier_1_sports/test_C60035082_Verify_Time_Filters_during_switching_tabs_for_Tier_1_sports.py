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
class Test_C60035082_Verify_Time_Filters_during_switching_tabs_for_Tier_1_sports(Common):
    """
    TR_ID: C60035082
    NAME: Verify Time Filters during switching tabs for Tier 1 sports
    DESCRIPTION: This test case verifies Time Filters during switching tabs  for Tier 1 sports
    PRECONDITIONS: To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - SportEventFilters checkbox should be Enabled in CMS -&gt; System Configuration -&gt; Structure -&gt; FeatureToggle -&gt; SportEventFilters
    PRECONDITIONS: - 'Enabled Time Filters' checkbox is ticked in CMS (Sports Pages &gt; Sport Categories &gt; Sport &gt; Competitions)
    PRECONDITIONS: - The following Time Filters are configured in CMS: 1 hour, 3 hours, 6 hours, 12 hours, 24 hours, 48 hours(Sports Pages &gt; Sport Categories &gt; Sport &gt; Competitions)
    PRECONDITIONS: **Designs**
    PRECONDITIONS: Mobile
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f29934dc307873133d8fa8e - Coral
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f2993556a07ac20e13ac09c - Ladbrokes
    PRECONDITIONS: Desktop
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f328dd7a1fe9853c0244e44 - Coral
    PRECONDITIONS: https://app.zeplin.io/project/5ebe56a26aec48472a7a3d3b/screen/5f29934dc307873133d8fa8e - Ladbrokes
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Tier1 Sport Landing page
    PRECONDITIONS: 3. Click/Tap on the 'Competition' tab
    """
    keep_browser_open = True

    def test_001_clicktap_on_some_league(self):
        """
        DESCRIPTION: Click/Tap on some League
        EXPECTED: - Time filters component are displayed according to CMS setting
        EXPECTED: - No filter selected or highlighted
        EXPECTED: - Time Filters is populated with the following time frames: 1 hour,2 hours, 3 hours, 6 hours, 12 hours,21 hours, 24 hours, 48 hours
        """
        pass

    def test_002_select_filter_eg_12_hours(self):
        """
        DESCRIPTION: Select filter, e.g. 12 hours
        EXPECTED: - Page loads only events that are due to start within the next 12 hours for that given league
        EXPECTED: - Events are sorted by time
        EXPECTED: - Time filter is highlighted
        """
        pass

    def test_003_switch_tab_eg_to_sport_landing_page_or_to_in_play_page(self):
        """
        DESCRIPTION: Switch tab, e.g. to Sport Landing page or to In-Play page
        EXPECTED: Filtering would not be applied to newly selected tab
        """
        pass

    def test_004_tapclick_back_into_competitions(self):
        """
        DESCRIPTION: Tap/Click back into Competitions
        EXPECTED: Filtering that previously applied is reset
        """
        pass

    def test_005_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step 2
        EXPECTED: 
        """
        pass

    def test_006_navigate_to_other_sport_gt_competitions_tab(self):
        """
        DESCRIPTION: Navigate to other sport &gt; competitions tab
        EXPECTED: Filtering would not be applied to currently selected tab
        """
        pass

    def test_007_return_to_tab_from_step_1(self):
        """
        DESCRIPTION: Return to tab from step 1
        EXPECTED: Filtering that previously applied is reset
        """
        pass

    def test_008_select_filter_eg_6_hours(self):
        """
        DESCRIPTION: Select filter, e.g. 6 hours
        EXPECTED: - Page loads only events that are due to start within the next 6 hours for that given league
        EXPECTED: - Events are sorted by time
        EXPECTED: - Time filter is highlighted
        """
        pass

    def test_009_tap_change_competition_link_and_select_other_league_from_the_list(self):
        """
        DESCRIPTION: Tap 'Change competition' link and select other league from the list
        EXPECTED: Filtering would not be applied to currently selected league
        """
        pass

    def test_010_tapclick_back_into_previously_league(self):
        """
        DESCRIPTION: Tap/Click back into previously league
        EXPECTED: Filtering that previously applied is reset
        """
        pass
