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
class Test_C44870198_Antepost_Similar_journey_to_land_in_Race_landing_page_user_taps_on_Antepost_and_is_displayed_tabs_as_per_Races_Type_Under_each_subheader_there_are_listed_meetings_expandable_with_all_required_data_complete_and_corect_and_linked_to_EDP_(Common):
    """
    TR_ID: C44870198
    NAME: Antepost : "Similar journey to land in Race landing page, user taps on Antepost and is displayed tabs as per Races Type Under each subheader there are listed meetings, expandable, with all required data complete and corect, and linked to EDP "
    DESCRIPTION: "Similar journey to land in Race landing page, user taps on Antepost and is displayed tabs as per Races Type
    DESCRIPTION: Under each subheader there are listed meetings, expandable, with all required data complete and corect, and linked to EDP "
    DESCRIPTION: Antepost races are seen in Future Tab.
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_hr_antepost___verify_the_contents_of_future_tab(self):
        """
        DESCRIPTION: HR Antepost - Verify the contents of FUTURE TAB
        EXPECTED: User should be able to see Antepost races in following tabs
        EXPECTED: FLAT
        EXPECTED: NATIONAL HUNT
        EXPECTED: INTERNATIONAL
        """
        pass

    def test_002_verify_all_meetings_are_expandablecollapsible_eg_royal_ascot_epsom_etc(self):
        """
        DESCRIPTION: Verify all meetings are expandable/collapsible (e.g. ROYAL ASCOT, EPSOM etc....)
        EXPECTED: User should be able to Expand/Collapse by clicking on Meetings
        """
        pass

    def test_003_verify_the_edps_in_different_meetings(self):
        """
        DESCRIPTION: Verify the EDPs in different meetings
        EXPECTED: User should be able to see details
        EXPECTED: Meeting Filter at the top (User can switch to different Meetings)
        EXPECTED: ANTEPOST
        EXPECTED: E/W terms
        EXPECTED: Selections and odds
        """
        pass

    def test_004_verify_meeting_filter_is_working(self):
        """
        DESCRIPTION: Verify Meeting filter is working
        EXPECTED: User should be able to switch to different meeting by clicking on this filter.
        """
        pass

    def test_005_gh_antepost___verify_the_contents_of_future_tab(self):
        """
        DESCRIPTION: GH Antepost - Verify the contents of FUTURE TAB
        EXPECTED: User should be able to see
        EXPECTED: BY MEETING
        EXPECTED: BY TIME
        EXPECTED: Different Meetings (e.g. Crayford, Hove etc) - Expandable/Collapsible
        """
        pass

    def test_006_verify_the_steps_3__4_for_gh_as_well(self):
        """
        DESCRIPTION: Verify the steps 3 & 4 for GH as well.
        EXPECTED: 
        """
        pass
