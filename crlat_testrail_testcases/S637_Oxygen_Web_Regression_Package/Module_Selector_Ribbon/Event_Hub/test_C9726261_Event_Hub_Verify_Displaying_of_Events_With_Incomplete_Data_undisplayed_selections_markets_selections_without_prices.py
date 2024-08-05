import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C9726261_Event_Hub_Verify_Displaying_of_Events_With_Incomplete_Data_undisplayed_selections_markets_selections_without_prices(Common):
    """
    TR_ID: C9726261
    NAME: Event Hub: Verify Displaying of Events With Incomplete Data (undisplayed selections/markets/selections without prices)
    DESCRIPTION: This test case verifies the displaying events within the module if they have undisplayed primary market, primary market with undisplayed selections or primary market with selections but without prices available
    PRECONDITIONS: 1) There are more than events in the module section in Event Hub
    PRECONDITIONS: 2) CMS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: NOTE: For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_go_to_cms__sport_pages__event_hub__edit_event_hub__add_sport_module__select_featured_events_module_and_create_a_new_module_via_type_id(self):
        """
        DESCRIPTION: Go to CMS > Sport Pages > Event Hub > Edit Event Hub > Add Sport Module > select Featured events module and create a new module via Type Id
        EXPECTED: Module is created
        """
        pass

    def test_002_on_the_ob_side_undisplay_the_primary_market(self):
        """
        DESCRIPTION: On the OB side undisplay the primary market
        EXPECTED: Primary market is undisplayed
        """
        pass

    def test_003_load_the_front_end_and_find_event_in_the_created_module(self):
        """
        DESCRIPTION: Load the front end and find event in the created module
        EXPECTED: Event with undisplayed market is NOT displayed on the Event Hub tab
        """
        pass

    def test_004_repeat_steps_1___4_for_event_which_has_markets_with_undisplayed_selections(self):
        """
        DESCRIPTION: Repeat steps #1 - 4 for event which has markets with undisplayed selections
        EXPECTED: 
        """
        pass

    def test_005_repeat_steps_1_4_for_events_which_contain_selections_without_prices_available(self):
        """
        DESCRIPTION: Repeat steps #1-4 for events which contain selections without prices available
        EXPECTED: 
        """
        pass

    def test_006_repeat_steps_1_6_for_modules_created_via_race_type_id(self):
        """
        DESCRIPTION: Repeat steps #1-6 for modules created via Race Type Id
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_1_6_for_module_created_via_enhanced_multiples_type_id(self):
        """
        DESCRIPTION: Repeat steps #1-6 for module created via Enhanced Multiples Type Id
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_1_6_for_modules_created_via_selection_idmake_sure_that_on_ob_side_all_market_configuration_are_done_for_market_to_which_selections_belongs_to(self):
        """
        DESCRIPTION: Repeat steps #1-6 for modules created via Selection Id
        DESCRIPTION: make sure that on OB side all market configuration are done for market to which selections belongs to
        EXPECTED: 
        """
        pass
