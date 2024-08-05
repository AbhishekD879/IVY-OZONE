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
class Test_C28995_Verify_Excluding_Non_Runners_selections_from_the_Next_Races_module(Common):
    """
    TR_ID: C28995
    NAME: Verify Excluding Non-Runners selections from the 'Next Races' module
    DESCRIPTION: This test case verifies how 'Non-Runners' will be excluded from the 'Next Races' module
    DESCRIPTION: Jira ticket: BMA-10828 All devices - Next 4 Races
    DESCRIPTION: According to the https://jira.egalacoral.com/browse/BMA-54445 this is accepted behaviour that N/R are shown for Ladbrokes/Greyhounds.
    PRECONDITIONS: To get an info use the following steps:
    PRECONDITIONS: 1) To get class IDs for Greyhound category use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?simpleFilter=class.categoryId:equals:19&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: Greyhound category id = 19
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) To get a list of events "Events" for the classes use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/YYYY?simpleFilter=market.dispSortName:equals:MR&simpleFilter=class.categoryId:equals:19&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: Note :
    PRECONDITIONS: *YYYY is a comma separated list of Class IDs (e.g. 97 or 97,98)*
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 3) To retrieve an information about event outcomes, silks info etc. use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ?racingForm=outcome&translationLang=LL
    PRECONDITIONS: where,
    PRECONDITIONS: *ZZZZ is an **'event id'** which is taken from the link in step 2*
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: **'name'** on outcome level to see horse name
    PRECONDITIONS: **'outcomeStatusCode' **to see outcome status
    PRECONDITIONS: 'Non-Runners' is a selection which contains N/R next to its name; selection should be voided
    PRECONDITIONS: For those selections 'outcomeStatusCode'='S' - those selections are always suspended.
    """
    keep_browser_open = True

    def test_001_on_site_server_find_an_event_which_contains_not_runner_selectionsmake_sure_this_event_will_appear_in_the_next_4_races_module(self):
        """
        DESCRIPTION: On Site Server find an event which contains not runner selections
        DESCRIPTION: Make sure this event will  appear in the 'Next 4 Races' module
        EXPECTED: 
        """
        pass

    def test_002_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_003_tap_greyhounds_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Greyhounds' icon from the sports menu ribbon
        EXPECTED: 1.  'Greyhounds' landing page is opened
        EXPECTED: 2.  'Today' tab is opened
        EXPECTED: 3.  'By Meeting' sorting type is selected
        """
        pass

    def test_004_on_the_next_races_module_find_an_event_which_contains_non_runner_selection(self):
        """
        DESCRIPTION: On the 'Next Races' module find an event which contains 'non-runner' selection
        EXPECTED: Event is displayed in the 'Next Races' module
        """
        pass

    def test_005_verify_selections_in_the_event(self):
        """
        DESCRIPTION: Verify selections in the event
        EXPECTED: 1.  'Non-Runners' won't appear in the 'Next Races' module
        EXPECTED: 2.  'Non-Runners' are excluded by 'outcomeStatusCode' attribute (suspended selections are not shown in the 'Next Races' module)
        """
        pass

    def test_006_find_an_event_which_contains_3_or_less_selection_and_one_of_those_selections_is_non_runners(self):
        """
        DESCRIPTION: Find an event which contains 3 or less selection and one of those selections is 'non-runners'
        EXPECTED: Event is shown
        """
        pass

    def test_007_verify_selections_in_the_next_races_module(self):
        """
        DESCRIPTION: Verify selections in the 'Next Races' module
        EXPECTED: 'Non-Runner' selections still are not displayed
        """
        pass
