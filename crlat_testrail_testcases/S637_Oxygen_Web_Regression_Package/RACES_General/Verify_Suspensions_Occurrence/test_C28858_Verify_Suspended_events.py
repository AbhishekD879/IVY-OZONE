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
class Test_C28858_Verify_Suspended_events(Common):
    """
    TR_ID: C28858
    NAME: Verify Suspended events
    DESCRIPTION: This test case verifies <Race> Suspended event/events.
    PRECONDITIONS: Make sure there is at least on event with attribute **eventStatusCode="S"**
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/YYYYYYY?racingForm=outcome&translationLang=LL
    PRECONDITIONS: Where,
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *   YYYYYY is an event ID
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_taprace_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Race> icon from the sports menu ribbon
        EXPECTED: <Race> landing page is opened
        """
        pass

    def test_003_verify_event_with_attribute_eventstatuscodes(self):
        """
        DESCRIPTION: Verify event with attribute **'eventStatusCode'='S'**
        EXPECTED: 1.  Suspended event off time is shown in the event ribbon
        EXPECTED: 2.  Suspended event is NOT shown on the 'Next 4 Races' module (after refresh)
        """
        pass

    def test_004_go_to_the_race_event_details_page_of_verified_event(self):
        """
        DESCRIPTION: Go to the <Race> event details page of verified event
        EXPECTED: *   All selections of all markets are greyed out
        EXPECTED: *   Selections are greyed and disabled
        """
        pass
