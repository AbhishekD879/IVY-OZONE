import pytest
from tests.base_test import vtest
from time import sleep
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot configure featured tab events in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.homepage_featured
@vtest
class Test_C11386066_Verify_module_is_removed_from_Featured_when_event_is_finished(BaseFeaturedTest):
    """
    TR_ID: C11386066
    NAME: Verify module is removed from Featured when event is finished
    DESCRIPTION: This test case verifies module is removed from Featured tab when event is finished
    PRECONDITIONS: 1. CMS, TI:
    PRECONDITIONS: Coral: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: Ladbrokes: https://confluence.egalacoral.com/display/SPI/Ladbrokes+Environments
    PRECONDITIONS: 2. Featured module by Market Id is created in CMS > Featured tab module
    PRECONDITIONS: 3. User is on Homepage > Featured tab
    PRECONDITIONS: 4. To complete event:
    PRECONDITIONS: - open the event page in TI;
    PRECONDITIONS: - set results for all markets (Set Results > Confirm Results > Settle).
    PRECONDITIONS: To make event expired:
    PRECONDITIONS: - open the event page in TI;
    PRECONDITIONS: - undisplay it and save changes.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1)Module by <Sport> EventId(not Outright Event with primary market) is created in CMS and is expanded by default.
        """
        params = self.ob_config.add_autotest_premier_league_football_event()
        market_id = params.default_market_id
        self.__class__.eventID = params.event_id
        self.__class__.selection_ids = list(params.selection_ids.values())

        self.__class__.module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Market', id=market_id,
            events_time_from_hours_delta=-10, module_time_from_hours_delta=-10)['title'].upper()

    def test_001_find_module_from_preconditions(self):
        """
        DESCRIPTION: Find module from preconditions
        EXPECTED: Module displayed with correct event/outcomes
        """
        self.site.wait_content_state('Homepage')
        self.wait_for_featured_module(name=self.module_name)
        self.__class__.module = self.get_section(section_name=self.module_name)
        self.assertTrue(self.module.is_expanded(), msg=f'"{self.module_name}" module is not expanded')
        bet_button1 = self.module.get_bet_button_by_selection_id(self.selection_ids[0])
        self.assertTrue(bet_button1.is_enabled(timeout=15, expected_result=True),
                         msg=f'selection is active in "{self.module_name}" module')
        bet_button2 = self.module.get_bet_button_by_selection_id(self.selection_ids[1])
        self.assertTrue(bet_button2.is_enabled(timeout=10, expected_result=True),
                        msg=f'selection is not active in "{self.module_name}" module')
        bet_button3 = self.module.get_bet_button_by_selection_id(self.selection_ids[2])
        self.assertTrue(bet_button3.is_enabled(timeout=10, expected_result=True),
                        msg=f'selection is not active in "{self.module_name}" module')

    def test_002_trigger_completionexpiration_one_of_the_verified_event(self):
        """
        DESCRIPTION: Trigger completion/expiration one of the verified event
        EXPECTED: * Live update with type EVENT is received in WS with attribute 'displayed="N"
        EXPECTED: * Module is removed from Featured tab
        """
        self.ob_config.change_event_state(event_id=self.eventID)
        sleep(3)
        status = self.get_section(section_name=self.module_name)
        self.assertIsNone(status, msg=f'The module "{self.module_name}" is displayed')
