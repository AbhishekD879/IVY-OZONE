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
class Test_C1234460_Verify_Next_Races_Data(Common):
    """
    TR_ID: C1234460
    NAME: Verify 'Next Races' Data
    DESCRIPTION: This test case is for checking the data which is displayed in 'Next Races' module for greyhounds.
    PRECONDITIONS: To get an info use the following steps:
    PRECONDITIONS: 1) To get class IDs for <Race> sport user a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *XX - sport category id*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Greyhound category id =19, Horse Racing category id = 21
    PRECONDITIONS: 2) To get a list of events "Events" for the classes use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/YYYY?simpleFilter=market.dispSortName:equals:MR&simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: Notice,
    PRECONDITIONS: *YYYY is a comma separated list of Class IDs (e.g. 97 or 97,98)*
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *XX - sport category id*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: - **'name'** to check an event time and local time
    PRECONDITIONS: - **'typeFlagCodes' **to check event group
    PRECONDITIONS: - **'eventStatusCode'** to check whether event is active or suspended
    PRECONDITIONS: - **'marketStatusCode' **to see market status
    PRECONDITIONS: - **'outcomeStatusCode'** to see outcome status
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
        EXPECTED: - 'Greyhounds' landing page is opened
        EXPECTED: - 'Today' tab is opened
        """
        pass

    def test_003_verify_next_races_module(self):
        """
        DESCRIPTION: Verify 'Next Races' module
        EXPECTED: 'Next Races' module is shown
        """
        pass

    def test_004_verify_data_in_next_races_module(self):
        """
        DESCRIPTION: Verify data in 'Next Races' module
        EXPECTED: - The next available races in terms of OpenBet event off time are shown.
        EXPECTED: - Data corresponds to the Site Server response. See attribute **'name'**.
        EXPECTED: - Events are sorted in the following order: the first event to start is shown first.
        """
        pass

    def test_005_verify_events_which_are_displayed_in_the_next_races_module(self):
        """
        DESCRIPTION: Verify events which are displayed in the 'Next Races' module
        EXPECTED: *   Only events with attribute **'typeFlagCodes'="NE"**  [Next Events flag] from the Site Server response are shown.
        EXPECTED: *   Only active events are displayed in the 'Next Races' module (for those events attribute **'eventStatusCode'**='A' in the Site Server response)
        EXPECTED: *   Only events with active markets are shown in the 'Next Races' module (**'marketStatusCode'**='A')
        EXPECTED: *   'Next Races' module is not shown if no events with **'typeFlagCodes'="NE"**are available
        """
        pass

    def test_006_verify_event_sectionsqayntity_of_the_events_sets_in_the_cms_cms___systemconfiguration__greyhoundnextraces___numberofselections(self):
        """
        DESCRIPTION: Verify event sections
        DESCRIPTION: Qayntity of the events sets in the CMS (CMS -> systemConfiguration ->GreyhoundNextRaces -> numberOfSelections)
        EXPECTED: 1. Appropriate number of selections (which was set in CMS) is displayed within Next Races module/carousel
        EXPECTED: 2. If number of selections is less than was set in CMS -> display the remaining selections
        EXPECTED: 3. - 'Unnamed Favourite' runner shouldn't be shown on the 'Next Races' module
        EXPECTED: 4. Only active selections are shown (**'outcomeStatusCode'**='A')
        """
        pass

    def test_007_verify_selection_in_the_next_races_module(self):
        """
        DESCRIPTION: Verify selection in the 'Next Races' module
        EXPECTED: Selections ONLY from 'Win or Each Way' market are displayed in the 'Next Races' module
        """
        pass
