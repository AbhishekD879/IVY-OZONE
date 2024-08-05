import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C1234461_Verify_Next_Races_Header_Race_Time_Meeting(Common):
    """
    TR_ID: C1234461
    NAME: Verify 'Next Races' Header, Race Time & Meeting
    DESCRIPTION: This test case if for checking correctness of 'Next Races' module header, race time and meeting for greyhounds.
    PRECONDITIONS: To get an info use the following steps:
    PRECONDITIONS: 1) To get class IDs for <Race> sport use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *XX - sport category id*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Greyhound category id = 19
    PRECONDITIONS: 2) To get a list of events "Events" for the classes use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/YYYY?simpleFilter=market.dispSortName:equals:MR&simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: Note :
    PRECONDITIONS: *YYYY is a comma separated list of Class IDs (e.g. 97 or 97,98)*
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *XX - sport category id*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: - **'name'** to check an event name and local time
    PRECONDITIONS: - **'typeName'** to check a race meeting name
    PRECONDITIONS: - **isEachWayAvailable, eachWayFactorDen,  eachWayPlaces,  eachWayFactorNum **to check if there are each way terms
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: --
        """
        pass

    def test_002_tap_greyhounds_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Greyhounds' icon from the sports menu ribbon
        EXPECTED: 1.  'Greyhounds' landing page is opened
        EXPECTED: 2.  'By Meeting' sorting type is selected
        EXPECTED: 3.  'Next 4 Races' module is displayed
        """
        pass

    def test_003_verify_next_races_accordion_header(self):
        """
        DESCRIPTION: Verify 'Next Races' accordion header
        EXPECTED: 1. Header is 'Next Races' (****|Header is CMS controlled & internationalised***|)*
        EXPECTED: 2. The header is displayed along the left hand side of the accordion
        """
        pass

    def test_004_verify_the_next_races_accordion_collapseexpand_state(self):
        """
        DESCRIPTION: Verify the 'Next Races' accordion collapse/expand state
        EXPECTED: -For **Mobile/Tablet** :
        EXPECTED: * From default state 'expanded', Next 4 Races’ module should collapse when tapping ( - ) or any other area of the accordion header
        EXPECTED: * Next 4 Races’ module should expand back when when tapping ( + ) or any other area of the accordion header
        EXPECTED: -For **Desktop** [screen width > 970 px]:
        EXPECTED: * From default state 'expanded', Next 4 Races’ module collapses when tapping the arrow-down symbol or any other area of the accordion header
        EXPECTED: * Next 4 Races’ module expands back when tapping the arrow-up symbol or any other area of the accordion header
        EXPECTED: Note : The '^' arrow symbol is displayed on the RIGHT hand side of the accordion
        """
        pass

    def test_005_verify_sub_header(self):
        """
        DESCRIPTION: Verify sub-header
        EXPECTED: Race sub-header is shown in next format** 'HH:MM EventName' [Example: "19:27 CRAYFORD"]
        EXPECTED: Cash Out icon is shown on the right if event has cashoutAvail="Y in SS response
        EXPECTED: Text IS NOT clickable
        """
        pass

    def test_006_verify_race_meeting_correctness(self):
        """
        DESCRIPTION: Verify race meeting correctness
        EXPECTED: Race Meeting name corresponds to the SiteServer response.
        EXPECTED: From the list of events look at the attribute **'typeName'** near the selected event.
        """
        pass

    def test_007_verify_event_time_correctness(self):
        """
        DESCRIPTION: Verify event time correctness
        EXPECTED: Event time corresponds to the race local time (see **'name' **attribute from the Site Server)
        """
        pass
