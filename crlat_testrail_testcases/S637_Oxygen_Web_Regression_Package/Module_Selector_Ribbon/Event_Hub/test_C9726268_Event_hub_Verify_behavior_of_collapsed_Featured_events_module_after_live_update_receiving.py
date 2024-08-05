import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C9726268_Event_hub_Verify_behavior_of_collapsed_Featured_events_module_after_live_update_receiving(Common):
    """
    TR_ID: C9726268
    NAME: Event hub: Verify behavior of collapsed Featured events module after live update receiving
    DESCRIPTION: This test cases verifies behavior of collapsed Featured events module after live update receiving on Event Hub tab.
    PRECONDITIONS: * Event Hub is created in CMS
    PRECONDITIONS: * Module by <Sport> TypeID is created in Event Hub in CMS and contains events
    PRECONDITIONS: * Module is collapsed
    PRECONDITIONS: * User is on Homepage > Event Hub tab
    PRECONDITIONS: * CMS, TI: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    """
    keep_browser_open = True

    def test_001_trigger_price_change_for_some_outcome(self):
        """
        DESCRIPTION: Trigger price change for some outcome
        EXPECTED: Collapsed Featured events module remains collapsed
        """
        pass

    def test_002_expand_module_from_preconditions(self):
        """
        DESCRIPTION: Expand module from Preconditions
        EXPECTED: Price / Odds button displays new prices without any highlighting
        """
        pass

    def test_003_trigger_suspensionunsuspension_for_some_outcome_marketevent(self):
        """
        DESCRIPTION: Trigger suspension/unsuspension for some outcome (market/event)
        EXPECTED: Collapsed Featured events module remains collapsed
        """
        pass

    def test_004_expand_module(self):
        """
        DESCRIPTION: Expand module
        EXPECTED: Price / Odds button displays suspended
        """
        pass

    def test_005_repeat_steps_1_4_for_module_by_sport_type_id_module_by_race_type_id_module_by_selection_id_module_by_enhanced_multiples(self):
        """
        DESCRIPTION: Repeat steps 1-4 for:
        DESCRIPTION: * Module by Sport Type ID
        DESCRIPTION: * Module by Race Type ID
        DESCRIPTION: * Module by Selection ID
        DESCRIPTION: * Module by Enhanced Multiples
        EXPECTED: 
        """
        pass
