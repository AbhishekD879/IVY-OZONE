import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C9346561_Verify_Tennis_Competitions_Landing_Page_Functionality(Common):
    """
    TR_ID: C9346561
    NAME: Verify Tennis Competitions Landing Page Functionality
    DESCRIPTION: This test case verified Tennis Competitions Landing Page Functionality
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to the Tennis Landing page
    PRECONDITIONS: 3. Make sure that the 'Competition' tab is available
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1. The Class accordions on Competitions page are CMS configurable
    PRECONDITIONS: 2. To set classes in CMS navigate to 'System-configuration' -> 'Competitions Tennis' and put class ID's in 'InitialClassIDs' field
    PRECONDITIONS: 3. To verify the availability of events in class please use the following link:
    PRECONDITIONS: https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?translationLang=en&simpleFilter=class.categoryId:equals:6&simpleFilter=class.isActive&simpleFilter=class.siteChannels:contains:M&simpleFilter=class.hasOpenEvent
    PRECONDITIONS: * X.XX - currently supported version of OpenBet release
    PRECONDITIONS: 4. To verify types that are available in the class please use the following link: https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubTypeForClass/XXX?translationLang=en&simpleFilter=type.hasOpenEvent:isTrue
    PRECONDITIONS: * X.XX - currently supported version of OpenBet release
    PRECONDITIONS: * XXX - class id
    PRECONDITIONS: **(!)** 'CompetitionsTennis' request is sent each time Competitions page(tab) is loaded(opened). Values from JSON response on this request are used to get the Class Accordion data from Openbet TI.
    """
    keep_browser_open = True

    def test_001_clicktap_on_competition_tab(self):
        """
        DESCRIPTION: Click/Tap on 'Competition' tab
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: * The leagues (types) are displayed in the list view
        EXPECTED: **For Desktop:**
        EXPECTED: * 'Popular' switcher is selected and highlighted
        EXPECTED: * The leagues (types) are displayed in Horizontal position
        """
        pass

    def test_002_verify_ordering_of_the_leagues_types(self):
        """
        DESCRIPTION: Verify ordering of the leagues (types)
        EXPECTED: Type ID's are ordered by OpenBet display order (starting with lowest one)
        """
        pass

    def test_003_clicktap_on_any_league_type_from_the_list(self):
        """
        DESCRIPTION: Click/Tap on any League (Type) from the list
        EXPECTED: **For mobile/Tablet:**
        EXPECTED: * User navigates to the 'Competition Details' page
        EXPECTED: * Events from the relevant league (type) are displayed
        EXPECTED: * There are 2 tabs (navigation buttons) on the page: 'Matches', 'Outrights' (if Outrights (or Matches) are not available for Type tabs won't be displayed)
        EXPECTED: * 'Matches' tab is selected by default
        EXPECTED: **For Desktop:**
        EXPECTED: * User navigates to the 'Competition Details' page
        EXPECTED: * Events from the relevant league (type) are displayed
        EXPECTED: * There are 'Matches and 'Outrights' switchers
        EXPECTED: * 'Matches' switcher is selected by default
        """
        pass
