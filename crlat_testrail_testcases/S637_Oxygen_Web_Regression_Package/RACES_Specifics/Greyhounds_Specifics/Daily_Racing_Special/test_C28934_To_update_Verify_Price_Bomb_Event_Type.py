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
class Test_C28934_To_update_Verify_Price_Bomb_Event_Type(Common):
    """
    TR_ID: C28934
    NAME: (To update) Verify 'Price Bomb' Event Type
    DESCRIPTION: *Note for update*
    DESCRIPTION: TC probably needs updating.
    DESCRIPTION: - No 'Today' tab in Horse Racing
    DESCRIPTION: - No 'Price bombs' section in 'Enhanced multiples'
    DESCRIPTION: - I'm not sure if what I think are enhanced multiples are ACTUALLY the enhanced multiples mentioned in test case (visual aid like screenshot would be EXTREMLY helpful for identifying UI elements)
    DESCRIPTION: - I found some events with 'Price Bomb' markets and other Price Bomb related words in https://ss-aka-ori-dub.coral.co.uk/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/227?translationLang=en *BUT* nothing as described in preconditions, only old event.
    DESCRIPTION: - Continuing on previous point: I don't know how to find/prepare test data needed for test nor how to determine wheter data I have is correct
    DESCRIPTION: This test case verifies how daily racing specials event type 'Price Bomb' will be displayed in the 'Oxygen' application
    PRECONDITIONS: To retrieve an information from the Site Server (tst2) use the following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk//openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/227?translationLang=LL
    PRECONDITIONS: Where *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Class id = 227 for Racing Specials class
    PRECONDITIONS: see attribute** 'typeName'**='Price Bomb'
    PRECONDITIONS: **'classID'** on event level to see class id for selected event type
    PRECONDITIONS: **'className'** on event level to see class name where event belongs to
    PRECONDITIONS: **'name'** on event level to see event name and local time
    PRECONDITIONS: **rawIsOffCode="Y"** , **isStated="true",** **rawIsOffCode="-" - **on event level to see whether event is started
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load 'Oxygen' application
        EXPECTED: 
        """
        pass

    def test_002_tap_horse_racing_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Horse Racing' icon from the sports menu ribbon
        EXPECTED: 1.  Horse Racing landing page is opened
        EXPECTED: 2.  'Today' tab is opened
        EXPECTED: 3.  'By Meeting' sorting type is selected
        """
        pass

    def test_003_verify_price_bomb_section(self):
        """
        DESCRIPTION: Verify 'Price Bomb' section
        EXPECTED: 1.  'Enhanced Multiples' section is displayed under the 'Next 4 Races' module
        EXPECTED: 2.  'Enhanced Multiples' section is expanded by default
        EXPECTED: 3.  It is possible to collapse / expand section by tapping section header
        """
        pass

    def test_004_verify_class_name_and_class_id_from_the_site_server_response_for_price_bomb_event_type(self):
        """
        DESCRIPTION: Verify class Name and Class Id from the Site Server response for 'Price Bomb' event type
        EXPECTED: Displayed event type corresponds to the attributes
        EXPECTED: **'classId'**=227 and **'className'**='|Daily Racing Special|'
        """
        pass

    def test_005_verify_section_header(self):
        """
        DESCRIPTION: Verify section header
        EXPECTED: Section header corresponds to the **'typeName' **attribute
        """
        pass

    def test_006_verify_event_name(self):
        """
        DESCRIPTION: Verify event name
        EXPECTED: Event name corresponds to the **'name'** attribute on event level
        """
        pass

    def test_007_verify_section_content(self):
        """
        DESCRIPTION: Verify section content
        EXPECTED: Only active events are displayed in the section ('eventStatusCode='A')
        """
        pass

    def test_008_verify_events_start_times(self):
        """
        DESCRIPTION: Verify events start times
        EXPECTED: Event start time corresponds to the race local time (see **'name' **attribute)
        EXPECTED: Only events for current day are displayed (see **'startTime'** attribute on event level)
        """
        pass

    def test_009_verify_events_ordering(self):
        """
        DESCRIPTION: Verify events ordering
        EXPECTED: 1.  Events are ordered **by race local time** in the fist instance
        EXPECTED: 2.  Events are sorted alphabetically **by name** in ascending order if race local times are the same
        """
        pass

    def test_010_tap_event_name(self):
        """
        DESCRIPTION: Tap event name
        EXPECTED: Event details page is opened
        """
        pass

    def test_011_verify_event_with_eventstatuscodes(self):
        """
        DESCRIPTION: Verify event with eventStatusCode='S'
        EXPECTED: Suspended events disappear from the 'Price Bomb' section
        """
        pass

    def test_012_verify_event_with_attributesrawisoffcodeyor_isstatedtrueandrawisoffcode_(self):
        """
        DESCRIPTION: Verify event with attributes **rawIsOffCode="Y"** OR (**isStated="true"** AND **rawIsOffCode="-")**
        EXPECTED: Started events disappear from the 'Price Bomb' section
        """
        pass

    def test_013_verify_price_bomb_section_when_all_events_are_started(self):
        """
        DESCRIPTION: Verify 'Price Bomb' section when all events are started
        EXPECTED: Section is no more displayed if there are no events to show
        """
        pass

    def test_014_go_to_the_by_time_sorting_type___verify_price_bomb_section(self):
        """
        DESCRIPTION: Go to the 'By Time' sorting type -> verify 'Price Bomb' section
        EXPECTED: 'Price Bomb' section is absent on 'By Time' sorting type
        """
        pass

    def test_015_go_to_the_tomorrow_tab___verify_price_bomb_section(self):
        """
        DESCRIPTION: Go to the 'Tomorrow' tab -> verify 'Price Bomb' section
        EXPECTED: 'Price Bomb' section is absent on 'Tomorrow' tab
        """
        pass

    def test_016_go_to_the_future_tab___verify_price_bomb_section(self):
        """
        DESCRIPTION: Go to the 'Future' tab -> verify 'Price Bomb' section
        EXPECTED: 'Price Bomb' section is absent on 'Future' tab
        """
        pass