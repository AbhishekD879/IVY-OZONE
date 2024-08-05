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
class Test_C28999_Verify_Selection_Information_on_the_Event_Details_Page(Common):
    """
    TR_ID: C28999
    NAME: Verify Selection Information on the Event Details Page
    DESCRIPTION: This test case verifies how racing post info will be displayed for each event
    PRECONDITIONS: To retrieve an information from Site Server use steps:
    PRECONDITIONS: 1) To get class IDs for Greyhound sport use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?simpleFilter=class.categoryId:equals:19&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: Greyhound category id = 19
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) To get a list of events for classes use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/YYYY?simpleFilter=market.dispSortName:equals:MR&simpleFilter=class.categoryId:equals:19&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: Notice,
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *YYYY is a comma separated list of Class IDs (e.g. 97 or 97,98)*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 3) To retrieve racing post silks, form and odds information follow the link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ?racingForm=outcome&translationLang=LL
    PRECONDITIONS: Where,
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *ZZZZ - an event id*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Use attributes on outcome level:
    PRECONDITIONS: - **'name'** to see a greyhound name
    PRECONDITIONS: - **'runnerNumber'** to see a greyhound number
    PRECONDITIONS: Silk will be hardcoded based on **'runnerNumber'** attribute (e.g. if 'runnerNumber'=1 -> corresponding silk icon with number '1' will be shown near selection name)
    """
    keep_browser_open = True

    def test_001_load_invictus_appliaction(self):
        """
        DESCRIPTION: Load Invictus appliaction
        EXPECTED: 
        """
        pass

    def test_002_tap_greyhounds_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Greyhounds' icon from the sports menu ribbon
        EXPECTED: 'Greyhounds' landing page is opened
        """
        pass

    def test_003_go_to_event_details_page(self):
        """
        DESCRIPTION: Go to event details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_004_verify_event_which_has_runner_number_foe_all_selections_mapped(self):
        """
        DESCRIPTION: Verify event which has runner number foe all selections mapped
        EXPECTED: NO Generic silks are displayed
        EXPECTED: Correct silks are displayed for mapped selections
        """
        pass

    def test_005_verify_greyhound_name(self):
        """
        DESCRIPTION: Verify greyhound name
        EXPECTED: Greyhound name corresponds to the **'name' **attribute
        """
        pass

    def test_006_verify_greyhound_silk_icon(self):
        """
        DESCRIPTION: Verify greyhound silk icon
        EXPECTED: Based on **'runnerNumber'** attribute corresponding silk with runner number is shown
        """
        pass
