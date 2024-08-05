import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C141198_Verify_displaying_of_suspended_selection_on_Sport_Event_Details_page_when_it_is_added_to_the_betslip(Common):
    """
    TR_ID: C141198
    NAME: Verify displaying of suspended selection on <Sport> Event Details page when it is added to the betslip
    DESCRIPTION: This test case verifies displaying of suspended selection on <Sport> Event Details page when it is added to the betslip
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: NOTE: LivePrice updates are NOT applicable for Outrights and Enhanced Multiples events
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: 
        """
        pass

    def test_002_clicktap_on_sport_icon_from_the_sports_ribbon(self):
        """
        DESCRIPTION: Click/Tap on '<Sport>' icon from the sports ribbon
        EXPECTED: <Sport> Landing page is opened
        """
        pass

    def test_003_open_event_details_page_for_particular_event(self):
        """
        DESCRIPTION: Open Event Details page for particular event
        EXPECTED: Event Details page is opened
        """
        pass

    def test_004_verify_the_priceodds_buttons_view_of_the_events_displayed(self):
        """
        DESCRIPTION: Verify the 'Price/Odds' buttons view of the events displayed
        EXPECTED: 'Price/Odds' buttons display price received from backend on light grey background
        """
        pass

    def test_005_clicktap_on_priceodds_button_and_check_its_displaying(self):
        """
        DESCRIPTION: Click/Tap on Price/Odds button and check it's displaying
        EXPECTED: Selected Price/Odds button is marked as added to Betslip (Becomes green)
        """
        pass

    def test_006_verify_that_selection_is_added_to_bet_slip(self):
        """
        DESCRIPTION: Verify that selection is added to Bet Slip
        EXPECTED: Selection is present in Bet Slip and counter is increased on header
        """
        pass

    def test_007_trigger_the_following_situation_for_this_outcomeoutcomestatuscode__sand_at_the_same_time_have_sport_event_details_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Trigger the following situation for this outcome:
        DESCRIPTION: outcomeStatusCode = 'S'
        DESCRIPTION: and at the same time have <Sport> Event Details page opened to watch for updates
        EXPECTED: 
        """
        pass

    def test_008_verify_outcome_for_the_event(self):
        """
        DESCRIPTION: Verify outcome for the event
        EXPECTED: * Price/Odds button for selected outcome is displayed immediately as greyed out and become disabled on <Sport> Event Details page
        EXPECTED: * Price is still displaying on the Price/Odds button
        EXPECTED: * Price/Odds button is not marked as added to Betslip (is not green anymore)
        """
        pass

    def test_009_change_attribute_for_this_outcomeoutcomestatuscode__aand_at_the_same_time_have_sport_event_details_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Change attribute for this outcome:
        DESCRIPTION: outcomeStatusCode = 'A'
        DESCRIPTION: and at the same time have <Sport> Event Details page opened to watch for updates
        EXPECTED: 
        """
        pass

    def test_010_verify_outcome_for_the_event(self):
        """
        DESCRIPTION: Verify outcome for the event
        EXPECTED: * Price/Odds button for selected outcome is no more disabled, it becomes active immediately
        EXPECTED: * Price/Odds button is marked as added to Betslip (Becomes green)
        """
        pass
