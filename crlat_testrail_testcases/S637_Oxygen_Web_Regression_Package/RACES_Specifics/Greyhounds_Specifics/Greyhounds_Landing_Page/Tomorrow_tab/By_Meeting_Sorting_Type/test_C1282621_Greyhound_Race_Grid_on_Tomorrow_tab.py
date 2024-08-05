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
class Test_C1282621_Greyhound_Race_Grid_on_Tomorrow_tab(Common):
    """
    TR_ID: C1282621
    NAME: Greyhound Race Grid on Tomorrow tab
    DESCRIPTION: This test case verifies the Race Grid on Tomorrow tab of Greyhounds
    DESCRIPTION: New Design (LADBROKES Desktop) - https://app.zeplin.io/project/5c6d3e910cb0f599dfd2145b/screen/5d01033ae1287915e4816435
    PRECONDITIONS: Greyhound landing page is opened
    PRECONDITIONS: To retrieve data from the Site Server use the following:
    PRECONDITIONS: 1) To get Classe IDs use a link
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: Where:
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: XX - category id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Greyhound category id = 19
    PRECONDITIONS: 2) To get all 'Events' for the class ID's use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/YYYY?translationLang=LL
    PRECONDITIONS: Where:
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY is a comma separated list of class ID's (e.g. 97 or 97, 98).
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Parameter **startTime** defines event start time (note, this is not a race local time)
    PRECONDITIONS: Load the app
    PRECONDITIONS: Navigate to Greyhounds landing page -> 'TODAY'tab is selected by default
    """
    keep_browser_open = True

    def test_001_navigate_to_tomorrow_tab(self):
        """
        DESCRIPTION: Navigate to Tomorrow tab
        EXPECTED: **FOR CORAL:**
        EXPECTED: - 'TOMORROW' tab is opened and race grid is shown with 'BY MEETING' sorting switched on by default
        EXPECTED: - 'TOMORROW' tab contains 2 sub-tabs - 'BY MEETING' and 'BY TIME'
        EXPECTED: **FOR LADBROKES:**
        EXPECTED: - 'TOMORROW' tab is opened and race grid is shown with 'BY MEETING' sorting switched on by default
        EXPECTED: - NO sub-tabs available
        """
        pass

    def test_002_verify_race_grid_sections(self):
        """
        DESCRIPTION: Verify race grid sections
        EXPECTED: The following sections are displayed and expanded by default:
        EXPECTED: **FOR CORAL (Mobile/Desktop):**
        EXPECTED: - UK&IRE
        EXPECTED: - VIRTUAL
        EXPECTED: **FOR LADBROKES (Mobile/Desktop):**
        EXPECTED: - UK/IRELAND RACES
        EXPECTED: - VIRTUAL RACES
        """
        pass

    def test_003_collapse_and_expand_the_grid_by_tapping_on_the_headers(self):
        """
        DESCRIPTION: Collapse and expand the grid by tapping on the headers
        EXPECTED: It is possible to collapse/expand accordions by tapping on the headers
        EXPECTED: **FOR MOBILE (Coral/Ladbrokes) and DESKTOP (Ladbrokes):**
        EXPECTED: - After collapsing: the downward arrow is displayed on the right side
        EXPECTED: - After expanding: No arrows displayed
        EXPECTED: **FOR DESKTOP (Coral):**
        EXPECTED: - After collapsing: the downward arrow is displayed on the right side
        EXPECTED: - After expanding: the upward arrow is displayed on the right side
        """
        pass

    def test_004_veriy_race_grid_content(self):
        """
        DESCRIPTION: Veriy Race Grid content
        EXPECTED: All events from SS response with start time ( **startTime** attribute) corresponding to the day tomorrow are displayed within corresponding type (race meeting) section
        """
        pass

    def test_005_verify_filtered_out_events(self):
        """
        DESCRIPTION: Verify filtered out events
        EXPECTED: - Antepost events are not received and are not shown (drilldownTagNames:"EVFLAG_AP)
        EXPECTED: - Events that passed "Suspension Time" are not received and shown (**suspendAtTime** attribute)
        """
        pass
