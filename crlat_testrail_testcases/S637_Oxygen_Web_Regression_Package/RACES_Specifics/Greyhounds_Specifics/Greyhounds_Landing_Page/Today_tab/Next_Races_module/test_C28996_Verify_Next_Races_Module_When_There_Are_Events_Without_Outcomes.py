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
class Test_C28996_Verify_Next_Races_Module_When_There_Are_Events_Without_Outcomes(Common):
    """
    TR_ID: C28996
    NAME: Verify 'Next Races' Module When There Are Events Without Outcomes
    DESCRIPTION: This test case verifies how events which don't contain outcomes will be shown on the 'Next Races' module
    DESCRIPTION: NOTE, **User Story: **BMA-2878: Events without outcomes should be hidden from 'Next 4 Races' module
    DESCRIPTION: BMA-10828 All devices - Next 4 Races
    PRECONDITIONS: 1.  To find out whether event belongs to 'Next Races' module see link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/YYYY?translationLang=LL
    PRECONDITIONS: See attribute **'typeFlagCodes' = 'NE, '**
    PRECONDITIONS: 2. Make sure there are events for today's day
    PRECONDITIONS: 3. Make sure there are events which don't contain outcomes and those events should appear in the 'Next 4 Races' module (**'typeFlagCodes' = 'NE, ' **is available for such event)
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_greyhounds_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Greyhounds' icon from the Sports Menu Ribbon
        EXPECTED: 'Greyhounds' landing page is opened
        EXPECTED: 'Today' tab is opened
        EXPECTED: 'Next Races' is shown
        """
        pass

    def test_003_on_thesite_server_find_an_event_without_outcomeswhich_should_appear_in_the_next_races_module(self):
        """
        DESCRIPTION: On the Site Server find an event without outcomes which should appear in the 'Next Races' module
        EXPECTED: Event is shown
        """
        pass

    def test_004_on_invictus_application_verify_event_withoutoutcomes_in_the_next_4_races_module(self):
        """
        DESCRIPTION: On Invictus application verify event without outcomes in the 'Next 4 Races' module
        EXPECTED: Event without outcomes is hidded from the 'Next Races' module
        EXPECTED: Only 3 events are shown is the 'Next Races' module
        """
        pass

    def test_005_trigger_the_following_situationselections_become_available_for_the_event_which_didnt_contain_outcomes(self):
        """
        DESCRIPTION: Trigger the following situation:
        DESCRIPTION: Selections become available for the event which didn't contain outcomes
        EXPECTED: Event appears in the 'Next Races' module after page refresh
        EXPECTED: 4 events are shown in the 'Next Races' module
        """
        pass

    def test_006_trigger_the_following_situationall_4_events_from_the_next_races_module_dont_contain_outcomes(self):
        """
        DESCRIPTION: Trigger the following situation:
        DESCRIPTION: All 4 events from the 'Next Races' module don't contain outcomes
        EXPECTED: 'Next Races' module is absent until events will be updated
        """
        pass

    def test_007_repeat_step_4(self):
        """
        DESCRIPTION: Repeat step #4
        EXPECTED: Events appear in the 'Next Races' module after page refresh
        EXPECTED: 4 events are shown in the 'Next Races' module
        """
        pass
