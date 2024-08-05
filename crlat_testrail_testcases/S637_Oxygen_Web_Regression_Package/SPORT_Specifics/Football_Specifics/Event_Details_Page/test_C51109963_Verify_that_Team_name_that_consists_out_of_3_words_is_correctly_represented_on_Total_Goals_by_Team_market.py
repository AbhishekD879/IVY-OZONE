import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C51109963_Verify_that_Team_name_that_consists_out_of_3_words_is_correctly_represented_on_Total_Goals_by_Team_market(Common):
    """
    TR_ID: C51109963
    NAME: Verify that Team name that consists out of 3 words is correctly represented on  "Total Goals by Team" market
    DESCRIPTION: This case verifies proper representation of complex team names(consisting out 3 or more words) on EDP of the Football event, for "Total Goals by Team" market
    DESCRIPTION: Test case can be run on both Prod and TST endpoints, but the instruction for TI changes is applicable only for TST endpoints.
    PRECONDITIONS: 1) Oxygen App is opened
    PRECONDITIONS: 2) Event with Team names that consist out of 3 words each should be created/present in the app.
    PRECONDITIONS: 3) "Total Goals by Team" market should be present within the event.
    PRECONDITIONS: (!) Usually the "Total Goals by Team" market is present within events that contain 130+ markets.
    PRECONDITIONS: Since events with such long names are truly rare, it is much easier to update any event that contains "Total Goals by Team" market, changing team names in a number of markets, that provide their combined market/selection names for the aforementioned market creation.
    PRECONDITIONS: In order to provide needed changes please change team names within markets/selections of following markets in TI:
    PRECONDITIONS: *. #Team_Name1 within a #Market_Name of |#Team_Name1| |Total Goals| market ![](index.php?/attachments/get/67871786)
    PRECONDITIONS: *. #Team_Name2 within a #Market_Name of |#Team_Name2| |Total Goals| market ![](index.php?/attachments/get/67871785)
    PRECONDITIONS: *. #Team_Name1 within a #Market_Name of |First Half| |#Team_Name1| |Total Goals| market ![](index.php?/attachments/get/67871784)
    PRECONDITIONS: *. #Team_Name2 within a #Market_Name of |First Half| |#Team_Name2| |Total Goals| market ![](index.php?/attachments/get/67871783)
    PRECONDITIONS: *. #Team_Name1 within a #Market_Name of |Second Half| |#Team_Name1| |Total Goals| market ![](index.php?/attachments/get/67871782)
    PRECONDITIONS: *. #Team_Name2 within a #Market_Name of |Second Half| |#Team_Name2| |Total Goals| market ![](index.php?/attachments/get/67871781)
    PRECONDITIONS: *. Selection names that represent #Team_Name1 and #Team_Name2 within |Match Result| market ![](index.php?/attachments/get/67871780)
    PRECONDITIONS: Once the aforementioned changes are provided, you should be able to view the updated team names within the "Total Goals by Team" market.
    PRECONDITIONS: (!) **Just remember** that there should be only 2 unique Team Names and changes provided within markets should match in changed Team Names.
    """
    keep_browser_open = True

    def test_001_navigate_to_edp_of_the_event_that_satisfies_pre_conditions(self):
        """
        DESCRIPTION: Navigate to EDP of the event that satisfies pre-conditions
        EXPECTED: Event Details Page is opened
        EXPECTED: 'All Markets' tab is selected by default
        """
        pass

    def test_002_expand_the_total_goals_by_team_accordion(self):
        """
        DESCRIPTION: Expand the 'Total Goals by Team' accordion
        EXPECTED: Expanded accordion contains 3 tabs
        EXPECTED: 'Total' tab is selected(underlined) by default
        EXPECTED: 2 rows of data are present below the tabs
        EXPECTED: ![](index.php?/attachments/get/67871787)
        """
        pass

    def test_003_verify_that_selected_tab_contains_2_unique_team_names_that_match_those_set_through_the_pre_conditions_phase(self):
        """
        DESCRIPTION: Verify that selected tab contains 2 unique team names that match those set through the pre-conditions phase
        EXPECTED: Each row with selections contains a Unique Team name
        EXPECTED: ![](index.php?/attachments/get/67871788)
        """
        pass

    def test_004_tapclick_on_any_selection_from_second_team_and_verify_that_opened_betslipquickbet_interface_contains_same_team_name_within_market_name_that_is_shown_for_the_selection(self):
        """
        DESCRIPTION: Tap/Click on any selection from second team and verify that opened Betslip/Quickbet interface contains same #Team_Name within #Market_Name, that is shown for the selection.
        EXPECTED: Selection is successfully added into Quickbet/Betslip
        EXPECTED: Market name matches with the market name of the added selection
        EXPECTED: ![](index.php?/attachments/get/67871789) ![](index.php?/attachments/get/67871792)
        EXPECTED: ![](index.php?/attachments/get/67871790) ![](index.php?/attachments/get/67871791)
        """
        pass

    def test_005_switch_to_1st_half_tab(self):
        """
        DESCRIPTION: Switch to '1st Half' tab
        EXPECTED: Clicked/Tapped tab is selected(underlined)
        EXPECTED: 2 rows of **new** data are present below the tabs
        """
        pass

    def test_006_repeat_step_4(self):
        """
        DESCRIPTION: Repeat Step 4
        EXPECTED: Expected results should match those from step 4
        """
        pass

    def test_007_switch_to_1st_half_tab(self):
        """
        DESCRIPTION: Switch to '1st Half' tab
        EXPECTED: Expected results should match those from step 5
        """
        pass

    def test_008_repeat_step_4(self):
        """
        DESCRIPTION: Repeat Step 4
        EXPECTED: Expected results should match those from step 4
        """
        pass
