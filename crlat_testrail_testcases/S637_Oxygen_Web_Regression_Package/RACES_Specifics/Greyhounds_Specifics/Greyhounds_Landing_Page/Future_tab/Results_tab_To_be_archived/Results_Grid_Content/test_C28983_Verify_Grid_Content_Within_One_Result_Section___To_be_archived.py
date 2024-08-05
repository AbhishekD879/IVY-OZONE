import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C28983_Verify_Grid_Content_Within_One_Result_Section___To_be_archived(Common):
    """
    TR_ID: C28983
    NAME: Verify Grid Content Within One Result Section  -  To be archived
    DESCRIPTION: This test case verifies grid content withing one results section
    PRECONDITIONS: 1) To retrieve an information about event outcomes and silks info etc. use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/YYYY?racingForm=outcome&translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: *   *YYYY - is an **'event id'** *
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: *   **'name'** on outcome level to see a horse name
    PRECONDITIONS: *   **'runnerNumber' **to find out whether selection has silk available.
    PRECONDITIONS: *   **eachWayFactorNum, eachWayFactorDen, eachWayPlaces** - to define terms for event
    PRECONDITIONS: 2) In order to receive information about resulted event use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/HistoricDrilldown/X.XX/ResultedEvent/XXXXXX?translationLang=LL
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *   *XXXXXX - an event id (Note, several event ids can also be pasted using comma as a separator. e.g.1574736,1574926**)*
    PRECONDITIONS: *   *LL - language (e.g. en, ukr) *
    PRECONDITIONS: See attributes:
    PRECONDITIONS: **'Position'** to see a place for selection
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_002_from_the_sports_menu_ribbon_tap_greyhounds_icon(self):
        """
        DESCRIPTION: From the sports menu ribbon tap 'Greyhounds' icon
        EXPECTED: 'Greyhounds' landing page is opened
        """
        pass

    def test_003_tap_results_tab(self):
        """
        DESCRIPTION: Tap 'Results' tab
        EXPECTED: **'Results'** tab is selected
        """
        pass

    def test_004_go_to_the_results_section_for_the_particular_event(self):
        """
        DESCRIPTION: Go to the Results section for the particular event
        EXPECTED: 4 columns are shown in the grid:
        EXPECTED: **Place**
        EXPECTED: **Trap**
        EXPECTED: **Greyhounds**
        EXPECTED: **Price (SP)**
        """
        pass

    def test_005_verify_place_column(self):
        """
        DESCRIPTION: Verify **Place **column
        EXPECTED: User place near each selection:
        EXPECTED: 1, 2, 3, 4, etc.
        EXPECTED: Place corresponds to the** 'position'** attribute from the Site Server
        """
        pass

    def test_006_verify_favorite_icon_near_selection_in_the_place_column(self):
        """
        DESCRIPTION: Verify Favorite icon near selection in the **Place** column
        EXPECTED: User can see the following favorite icon (if this is available) near the places:
        EXPECTED: F
        EXPECTED: 2F
        EXPECTED: JF
        EXPECTED: 2JF
        """
        pass

    def test_007_verify_position_ordering(self):
        """
        DESCRIPTION: Verify position ordering
        EXPECTED: The finishing position of the runners is:
        EXPECTED: from lowest to highest (i.e. 1 -> 5)
        """
        pass

    def test_008_verify_trapcolumn_for_event_which_has_silks_avaiable_runnernumber_attribute_is_present(self):
        """
        DESCRIPTION: Verify **Trap **column for event which has silks avaiable (**'runnerNumber' **attribute is present)
        EXPECTED: Silk icon corresponds to the picture which is based on **'runnerNumber'** attribute (the hardcoded picture)
        """
        pass

    def test_009_verify_trap_column_when_event_doesnt_have_silks_mapped_runnernumber_attribute_is_absentat_least_one_runner_number_is_present(self):
        """
        DESCRIPTION: Verify **Trap** column when event doesn't have silks mapped (**'runnerNumber' **attribute is absent)
        DESCRIPTION: (at least one runner number is present)
        EXPECTED: Generic silk icon is displayed for absent runnernumber attributes
        """
        pass

    def test_010_verify_trap_column_when_event_doesnt_have_silks_mapped_runnernumber_attribute_is_absentall_runner_numbers_are_absent(self):
        """
        DESCRIPTION: Verify **Trap** column when event doesn't have silks mapped (**'runnerNumber' **attribute is absent)
        DESCRIPTION: (all runner numbers are absent)
        EXPECTED: NO Generic Silks are displayed
        """
        pass

    def test_011_verify_greyhounds_column(self):
        """
        DESCRIPTION: Verify **Greyhounds** column
        EXPECTED: *   Dog name is shown
        EXPECTED: *   Dog name corresponds to the** 'name'** attribute on outcome level
        """
        pass

    def test_012_verify_price_sp_column(self):
        """
        DESCRIPTION: Verify **Price (SP) **column
        EXPECTED: The actual price/odd is displayed in decimal or fractional format depending on user settings
        """
        pass

    def test_013_verify_each_way_terms_displaying(self):
        """
        DESCRIPTION: Verify **Each Way Terms **displaying
        EXPECTED: Each Way terms are displayed outside the grid
        """
        pass

    def test_014_verify_each_way_terms_correctness(self):
        """
        DESCRIPTION: Verify **Each Way Terms **correctness
        EXPECTED: Terms correspond to the **'eachWayFactorNum'**, **'eachWayFactorDen'** and** 'eachWayPlaces'** attributes from the Site Server and are shown in format:
        EXPECTED: ***" Each Way: x/y odds - places z,j,k"***
        EXPECTED: where:
        EXPECTED: *   x = eachWayFactorNum
        EXPECTED: *   y= eachWayFactorDen
        EXPECTED: *   z,j,k = eachWayPlaces
        """
        pass
