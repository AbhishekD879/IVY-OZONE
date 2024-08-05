import pytest
from time import sleep
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # cannot configure featured tab events in prod
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C10877976_Featured_module_by_Sport_Event_ID_Expiration_of_Sport_Event(BaseFeaturedTest):
    """
    TR_ID: C10877976
    NAME: Featured module by <Sport> Event ID: Expiration of <Sport> Event
    DESCRIPTION: This test case verifies that Featured module by <Sport> Event ID is removed when event is expired
    PRECONDITIONS: 1)Module by <Sport> EventId(not Outright Event with primary market) is created in CMS and is expanded by default.
    PRECONDITIONS: 2) User is on Homepage > Featured tab
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: - To retrieve all events for verified Type: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: - To retrieve markets and outcomes for event use: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: To complete event:
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
        self.__class__.market_id = params.default_market_id
        self.__class__.eventID = params.event_id
        self.__class__.selection_ids = list(params.selection_ids.values())

        self.__class__.module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Event', id=self.eventID,
            events_time_from_hours_delta=-10, module_time_from_hours_delta=-10)['title'].upper()

    def test_001_navigate_to_module_with_sport_event_from_preconditions(self):
        """
        DESCRIPTION: Navigate to module with <Sport> event from preconditions
        EXPECTED: Event is displayed with correct outcomes
        """
        self.site.wait_content_state('Homepage')
        self.wait_for_featured_module(name=self.module_name)
        self.__class__.module = self.get_section(section_name=self.module_name)
        self.assertTrue(self.module.is_expanded(), msg=f'"{self.module_name}" module is not expanded')

    def test_002_trigger_completionexpiration_one_of_the_verified_event(self):
        """
        DESCRIPTION: Trigger completion/expiration one of the verified event
        EXPECTED: Module from Step 1 is undisplayed
        """
        self.ob_config.change_event_state(event_id=self.eventID)
        sleep(3)
        status = self.get_section(section_name=self.module_name)
        self.assertIsNone(status, msg=f'The module "{self.module_name}" is displayed')
