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
class Test_C9337874_Verify_Basketball_Competitions_Landing_Page_Functionality(Common):
    """
    TR_ID: C9337874
    NAME: Verify Basketball Competitions Landing Page Functionality
    DESCRIPTION: This test case verified Basketball Competitions Landing Page Functionality
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to the Basketball Landing page
    PRECONDITIONS: 3. Make sure that the 'Competition' tab is available
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1. The Class accordions on Competitions page are CMS configurable
    PRECONDITIONS: 2. To set classes in CMS navigate to 'System-configuration' -> 'Competitions Basketball' and put class ID's in 'InitialClassIDs' and/or 'A-ZClassIDs' field
    PRECONDITIONS: 3. To verify the availability of events in class please use the following link:
    PRECONDITIONS: https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?translationLang=en&simpleFilter=class.categoryId:equals:6&simpleFilter=class.isActive&simpleFilter=class.siteChannels:contains:M&simpleFilter=class.hasOpenEvent
    PRECONDITIONS: * X.XX - currently supported version of OpenBet release
    PRECONDITIONS: 4. To verify types that are available in the class please use the following link: https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubTypeForClass/XXX?translationLang=en&simpleFilter=type.hasOpenEvent:isTrue
    PRECONDITIONS: * X.XX - currently supported version of OpenBet release
    PRECONDITIONS: * XXX - class id
    PRECONDITIONS: **(!)** 'CompetitionsBasketball' request is sent each time Competitions page(tab) is loaded(opened). Values from JSON response on this request are used to get the Class Accordion data from Openbet TI.
    """
    keep_browser_open = True

    def test_001_clicktap_on_competition_tab(self):
        """
        DESCRIPTION: Click/Tap on 'Competition' tab
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: * 'Popular' label is NOT displayed above the 'Popular' class accordions
        EXPECTED: * The 'Popular' class accordions are loaded based on settings in 'InitialClassIDs' field at CMS
        EXPECTED: * 'A-Z COMPETITIONS' label is displayed above the 'A-Z' class accordions
        EXPECTED: * The A-Z' class accordions are loaded based on settings in 'A-ZClassIDs' field at CMS
        EXPECTED: **For Desktop:**
        EXPECTED: * 'Popular' and 'A-Z' switchers are displayed below Sports Sub Tabs
        EXPECTED: * 'Popular' switcher is selected by default and highlighted
        EXPECTED: * The 'Popular' class accordions are loaded based on settings in 'InitialClassIDs' field at CMS
        """
        pass

    def test_002_for_mobiletabletcheck_popular_class_accordionsfor_desktopcheck_popular_class_accordions_when_popular_switcher_is_selected(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Check 'Popular' class accordions
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Check 'Popular' class accordions when 'Popular' switcher is selected
        EXPECTED: * 'Popular' accordions for classes that are set in 'InitialClassIDs' at CMS are displayed
        EXPECTED: * The First accordion is expanded by default
        EXPECTED: * 'Popular' class accordions  are ordered according to settings is CMS
        """
        pass

    def test_003_for_mobiletabletcheck_a_z_class_accordionsfor_desktopcheck_a_z_class_accordions_when_a_z_switcher_is_selected(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Check 'A-Z' class accordions
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Check 'A-Z' class accordions when 'A-Z' switcher is selected
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: * 'A-Z' accordions are loaded based on settings in 'A-ZClassIDs' at CMS
        EXPECTED: * All accordions are collapsed by default
        EXPECTED: * 'A-Z' class accordions are ordered alphabetically
        EXPECTED: **For Desktop:**
        EXPECTED: * 'A-Z' switcher is selected and highlighted
        EXPECTED: * 'A-Z' accordions are loaded based on settings in 'A-ZClassIDs' at CMS
        EXPECTED: * The First accordion is expanded by default
        EXPECTED: * 'A-Z' class accordions are ordered alphabetically
        """
        pass

    def test_004_expand_any_class_accordion_with_available_competitions(self):
        """
        DESCRIPTION: Expand any Class accordion with available competitions
        EXPECTED: **For mobile/Tablet:**
        EXPECTED: * The leagues (types) are displayed in the list view
        EXPECTED: * Type ID's are ordered by OpenBet display order (lowest display order at the top)
        EXPECTED: **For Desktop:**
        EXPECTED: * The leagues (types) are displayed in Horizontal position
        EXPECTED: * Type ID's are ordered by OpenBet display order (starting with lowest one)
        """
        pass

    def test_005_clicktap_on_any_league_type_from_the_list(self):
        """
        DESCRIPTION: Click/Tap on any League (Type) from the list
        EXPECTED: **For mobile/Tablet:**
        EXPECTED: * User navigates to the 'Competition Details' page
        EXPECTED: * Events from the relevant league (type) are displayed
        EXPECTED: * There are 3 tabs (navigation buttons) on the page: 'Matches', 'Outrights'
        EXPECTED: * 'Matches' tab is selected by default
        EXPECTED: **For Desktop:**
        EXPECTED: * User navigates to the 'Competition Details' page
        EXPECTED: * Events from the relevant league (type) are displayed
        EXPECTED: * There are 'Matches and 'Outrights' switchers
        EXPECTED: * 'Matches' switcher is selected by default
        """
        pass
