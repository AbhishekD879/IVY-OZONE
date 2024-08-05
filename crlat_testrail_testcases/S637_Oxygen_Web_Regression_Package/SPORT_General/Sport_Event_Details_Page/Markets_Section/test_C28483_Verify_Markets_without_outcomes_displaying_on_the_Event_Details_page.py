import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C28483_Verify_Markets_without_outcomes_displaying_on_the_Event_Details_page(Common):
    """
    TR_ID: C28483
    NAME: Verify Markets without outcomes displaying on the Event Details page
    DESCRIPTION: This test case verifies Markets without outcomes displaying on the Event Details page
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tapsporticon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap '<Sport>' icon from the Sports Menu Ribbon
        EXPECTED: <Sport> Landing Page is opened
        """
        pass

    def test_003_open_some_event_details_page(self):
        """
        DESCRIPTION: Open some Event Details page
        EXPECTED: <Sport> Event Details page is opened
        """
        pass

    def test_004_navigate_through_all_tabs_and_verify_if_there_are_marketswithout_outcomes(self):
        """
        DESCRIPTION: Navigate through all tabs and verify if there are Markets without outcomes
        EXPECTED: Markets without outcomes are not  displayed
        """
        pass

    def test_005_go_to_siteserv_and_find_market_without_outcomes_for_chosen_event(self):
        """
        DESCRIPTION: Go to SiteServ and find Market without outcomes for chosen Event
        EXPECTED: 
        """
        pass

    def test_006_navigate_through_all_tabs_and_try_to_find_market_from_step_5(self):
        """
        DESCRIPTION: Navigate through all tabs and try to find Market from step №5
        EXPECTED: Market without outcomes are not displayed
        """
        pass

    def test_007_go_to_sport_landing_page_and_verify_more_link_for_event_which_has_markets_withoutoutcomes(self):
        """
        DESCRIPTION: Go to <Sport> landing page and verify 'More' link for Event which has Markets without outcomes
        EXPECTED: 1. In 'More' link in brackets should be shown amount of available Markets for event
        EXPECTED: 2. If only one Market with outcomes is available for event - 'More' link not shown
        """
        pass

    def test_008_verify_event_details_page_for_event_with_markets_without_outcomes_for_all_available_tabs(self):
        """
        DESCRIPTION: Verify event details page for Event with Markets without outcomes for all available tabs
        EXPECTED: 1. First two Market sections are expanded, other collapsed by default
        EXPECTED: 2. If only one Market section is shown - it should be expanded by default
        """
        pass

    def test_009_go_toevent_details_page_for_event_with_markets_without_outcomes_and_verify_all_available_tabs(self):
        """
        DESCRIPTION: Go to event details page for Event with Markets without outcomes and verify all available tabs
        EXPECTED: No empty tabs are be present
        """
        pass
