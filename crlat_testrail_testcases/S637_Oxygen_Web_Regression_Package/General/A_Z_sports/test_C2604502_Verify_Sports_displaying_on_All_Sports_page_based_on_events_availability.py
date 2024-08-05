import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C2604502_Verify_Sports_displaying_on_All_Sports_page_based_on_events_availability(Common):
    """
    TR_ID: C2604502
    NAME: Verify Sports displaying on 'All Sports' page based on events availability
    DESCRIPTION: This test case verifies displaying of a Sport based on availability of OB events in 'A-Z Competitions' & 'Top Sports' sections
    DESCRIPTION: - To check whether events are available for a CategoryId:
    DESCRIPTION: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Event/?simpleFilter=event.categoryId:equals:{ID}&simpleFilter=event.siteChannels:contains:M&simpleFilter=event.suspendAtTime:greaterThanOrEqual:YYYY-MM-DDTHH:MM:00.000&includeUndisplayed=false
    DESCRIPTION: - Displaying of a Sport depends on "hasEvents"="true/false" parameter received in "initial-data" response > sportCategories
    PRECONDITIONS: 1. Sport Category is configured in CMS: Sports Pages > Sport Categories with:
    PRECONDITIONS: - Open Bet 'CategoryId' (e.g. 'Football' with 'CategoryId'=16)
    PRECONDITIONS: - Events are available for a Category in Open Bet
    PRECONDITIONS: 2. Sport Category is configured in CMS: Sports Pages > Sport Categories with:
    PRECONDITIONS: - Open Bet 'CategoryId' (e.g. 'Darts' with 'CategoryId'=13)
    PRECONDITIONS: - Events are NOT available for a Category in Open Bet
    PRECONDITIONS: 3. Sport Category is configured in CMS: Sports Pages > Sport Categories with:
    PRECONDITIONS: - Non Open Bet 'CategoryId' e.g. Player Bets
    PRECONDITIONS: 4. 'Top Sports' are configured in CMS for some Sports e.g. Football, Horse Racing, Greyhounds
    PRECONDITIONS: (Sports Pages > Sport Categories > <Sport> 'Is Top Sport' check box is checked)
    PRECONDITIONS: 5. 'A-Z Sports' is configured in CMS for some Sports e.g. Basketball, Football, Greyhounds, Horse Racing etc
    PRECONDITIONS: (Sports Pages > Sport Categories > <Sport> 'Show in AZ' check box is checked)
    PRECONDITIONS: 6. Oxygen application is loaded
    PRECONDITIONS: 7. 'All Sports' page is opened (A-Z Sports)
    """
    keep_browser_open = True

    def test_001_verify_sport_availability_in_a_z_categories_section_that_has_events_from_preconditions_1_eg_football(self):
        """
        DESCRIPTION: Verify Sport availability in 'A-Z Categories' section that has events (from Preconditions 1 e.g. Football)
        EXPECTED: Sport e.g. Football is available in 'A-Z Categories' section
        """
        pass

    def test_002_verify_sport_availability_in_a_z_categories_section_that_has_no_events_from_preconditions_2_eg_darts(self):
        """
        DESCRIPTION: Verify Sport availability in 'A-Z Categories' section that has no events (from Preconditions 2 e.g. Darts)
        EXPECTED: Sport e.g. Darts is NOT available in 'A-Z Categories' section
        """
        pass

    def test_003_verify_sport_availability_in_a_z_categories_section_with_non_ob_categoryid_from_preconditions_3_eg_player_bets(self):
        """
        DESCRIPTION: Verify Sport availability in 'A-Z Categories' section with non OB 'CategoryId' (from Preconditions 3 e.g. Player Bets)
        EXPECTED: Sport e.g. Player Bets is available in 'A-Z Categories' section
        """
        pass

    def test_004___in_ti_add_an_events_to_a_sport_that_has_none_from_preconditions_1_eg_darts__in_app_verify_availability_of_a_sport_from_preconditions_1_eg_darts(self):
        """
        DESCRIPTION: - In TI: Add (an) event(s) to a Sport that has none (from Preconditions 1 e.g. Darts)
        DESCRIPTION: - In app: Verify availability of a Sport (from Preconditions 1 e.g. Darts)
        EXPECTED: Sport (from Preconditions 1  e.g. Darts) is available in 'A-Z Categories' section
        EXPECTED: **NOTE: Sport will appear up to 10 minutes due to backend job
        """
        pass

    def test_005___in_ti_undisplay_all_available_events_of_any_sport_eg_darts__in_app_verify_availability_of_a_sport_eg_darts_in_a_z_categories_section(self):
        """
        DESCRIPTION: - In TI: Undisplay all available events of any Sport e.g. Darts
        DESCRIPTION: - In app: Verify availability of a Sport e.g. Darts in A-Z Categories' section
        EXPECTED: Sport e.g. Darts is NOT available in 'A-Z Categories' section
        EXPECTED: **NOTE: Sport will disappear up to 10 minutes due to backend job
        """
        pass

    def test_006_repeat_steps_1_5_for_sports_in_top_sports_section(self):
        """
        DESCRIPTION: Repeat steps 1-5 for sports in 'Top Sports' section
        EXPECTED: Results are the same
        """
        pass
