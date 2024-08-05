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
class Test_C28449_Verify_started_events_removing_from_the_Today_tab_Desktop(Common):
    """
    TR_ID: C28449
    NAME: Verify started events removing from the 'Today' tab: Desktop
    DESCRIPTION: This test case verifies started events removing from the 'Today' tab for Desktop
    DESCRIPTION: **Jira tickets:** BMA-4660
    PRECONDITIONS: 1) There should be events within 'Today' tab's view
    PRECONDITIONS: 2) To retrieve markets and outcomes for event use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_sport_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Sport> icon on the Sports Menu Ribbon
        EXPECTED: *   <Sport> Landing Page is opened
        EXPECTED: *   'Matches'->'Today' tab is opened by default (Desktop/tablet only)
        """
        pass

    def test_003_find_an_event_within_verified_page(self):
        """
        DESCRIPTION: Find an event within verified page
        EXPECTED: Event is displayed correctly with outcomes
        """
        pass

    def test_004_triggerwait_until_for_verified_event_isstartedtrue_attribute_will_be_set_and_refresh_the_page(self):
        """
        DESCRIPTION: Trigger/wait until for verified event '**isStarted="true"**' attribute will be set and refresh the page
        EXPECTED: Started event is removed from 'Today' tab's view
        """
        pass
