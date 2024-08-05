import pytest
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.waiters import wait_for_result
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from selenium.common.exceptions import StaleElementReferenceException
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot create events in prod/beta
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.mobile_only
@vtest
class Test_C9726375_Event_Hub_Not_Primary_Market_Becomes_Suspended(BaseFeaturedTest):
    """
    TR_ID: C9726375
    NAME: Event Hub: Not Primary Market Becomes Suspended
    DESCRIPTION: This test case verifies situation when market/markets become suspended on event landing page on the 'Event Huv' tab (mobile/tablet)
    PRECONDITIONS: To get into SiteServer use this link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: *   Z.ZZ  - current supported version of OpenBet SiteServer
    PRECONDITIONS: *   XXXX - event ID
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: ***Boosted selection - this is ******an ******event****** with only one selection which is shown on the 'Featured' tab. ***
    PRECONDITIONS: ***On CMS it  is configured as event shown by selection id.***
    PRECONDITIONS: **NOTE:** **LivePrice updates are NOT applicable for Outrights and Enhanced Multiples events**
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Event Hub is created in CMS > Sport Pages > Event Hub.
        """
        event = self.ob_config.add_UK_racing_event(number_of_runners=1)
        self.__class__.market_id = event.market_id
        self.__class__.eventID = event.event_id
        self.__class__.selection_ids = list(event.selection_ids.values())
        type_id = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.type_id
        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]
        index_number = next(index for index in range(1, 20) if index not in existed_index_number)
        self.cms_config.create_event_hub(index_number=index_number)
        self.cms_config.add_sport_module_to_event_hub(page_id=index_number, module_type='FEATURED')
        module_data = self.cms_config.add_featured_tab_module(select_event_by='RaceTypeId', id=type_id,
                                                              page_type='eventhub',
                                                              page_id=index_number,
                                                              events_time_from_hours_delta=-10,
                                                              module_time_from_hours_delta=-10)
        self.__class__.module_name = module_data['title'].upper()
        internal_id = f'tab-eventhub-{index_number}'
        event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                           internal_id=internal_id,
                                                                           hub_index=index_number,
                                                                           display_date=True)
        self.__class__.event_hub_tab_name = event_hub_tab_data.get('title').upper()
        self.site.wait_content_state(state_name='Homepage')

    @retry(stop=stop_after_attempt(10), wait=wait_fixed(wait=40),
           retry=retry_if_exception_type((StaleElementReferenceException, VoltronException)), reraise=True)
    def test_001_in_the_event_hub_tab_find_boosted_selection(self):
        """
        DESCRIPTION: In the Event hub tab find boosted selection
        EXPECTED: Event with a boosted selection is shown
        """
        self.device.refresh_page()
        event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        self.assertTrue(event_hub_content, msg=f'Event hub module "{self.event_hub_tab_name}" was not found')
        event_hub_modules = event_hub_content.event_hub_items_dict
        self.assertTrue(event_hub_modules, msg=f'No modules found on "{self.event_hub_tab_name}" tab')
        event_hub_module = event_hub_modules.get(self.module_name)
        self.assertTrue(event_hub_module,
                        msg=f'Module "{self.module_name}" was not found on "{self.event_hub_tab_name}" tab')
        self.assertTrue(event_hub_module.is_expanded(timeout=2),
                        msg=f'Module: "{self.module_name}" not expanded')
        self.__class__.module = self.get_section(section_name=self.module_name)

    def test_002_trigger_the_following_situation_for_this_eventmarketstatuscodesfor_market_type_boosted_selection_belongs_to(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: **marketStatusCode="S"**
        DESCRIPTION: for  market type boosted selection belongs to
        """
        self.ob_config.change_market_state(event_id=self.eventID,
                                           market_id=self.market_id,
                                           displayed=True,
                                           active=False)
        event_status = wait_for_result(lambda: self.check_event_is_active(self.eventID), expected_result=False,
                                       name='Event is suspended',
                                       timeout=40)
        self.assertFalse(event_status, msg='Event is not suspended')

    def test_003_verify_outcome_for_the_event(self):
        """
        DESCRIPTION: Verify outcome for the event
        EXPECTED: *   Price/Odds button of this event immediately start displaying "S"
        EXPECTED: *   Price/Odds button is disabled
        """
        bet_button1 = self.module.get_bet_button_by_selection_id(self.selection_ids[0])
        self.assertFalse(bet_button1.is_enabled(timeout=10, expected_result=True),
                         msg=f'selection is active in "{self.module_name}" module')

    def test_004_change_attribute_for_this_eventmarketstatuscodeafor_market_type_boosted_selection_belongs_to(self):
        """
        DESCRIPTION: Change attribute for this event:
        DESCRIPTION: **marketStatusCode="A"**
        DESCRIPTION: for market type boosted selection belongs to
        EXPECTED:
        """
        self.ob_config.change_market_state(event_id=self.eventID,
                                           market_id=self.market_id,
                                           displayed=True,
                                           active=True)
        event_status = wait_for_result(lambda: self.check_event_is_active(self.eventID), expected_result=True,
                                       name='Event is suspended',
                                       timeout=40)
        self.assertTrue(event_status, msg='Event is still suspended')

    def test_005_verify_outcome_for_the_event(self):
        """
        DESCRIPTION: Verify outcome for the event
        EXPECTED: *   Price/Odds button of this event is not disabled anymore
        EXPECTED: *   Price / Odds button displays prices immediately
        """
        module = self.get_section(section_name=self.module_name)
        bet_button1 = module.get_bet_button_by_selection_id(self.selection_ids[0])
        self.assertTrue(bet_button1.is_enabled(timeout=10, expected_result=True),
                        msg=f'selection is not active in "{self.module_name}" module')
