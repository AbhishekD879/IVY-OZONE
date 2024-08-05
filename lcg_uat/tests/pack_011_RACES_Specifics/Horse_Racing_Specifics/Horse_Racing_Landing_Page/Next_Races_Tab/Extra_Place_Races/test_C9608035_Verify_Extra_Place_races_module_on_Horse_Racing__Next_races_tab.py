import pytest

from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
import voltron.environments.constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.datafabric.datafabric import Datafabric


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
# @pytest.mark.lad_prod  # Cannot make CMS changes for prod/hl
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.races
@pytest.mark.next_races
@pytest.mark.mobile_only
@vtest
class Test_C9608035_Verify_Extra_Place_races_module_on_Horse_Racing__Next_races_tab(BaseRacing):
    """
    TR_ID: C9608035
    VOL_ID: C17505270
    NAME: Verify 'Extra Place' races module on Horse Racing > 'Next races' tab
    DESCRIPTION: This test case verifies how 'Extra Place' races module look like on Horse Racing > 'Next Races' tab
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: 1. "Next Races" tab for Horse Racing EDP should be enabled in CMS(CMS -> system-configuration -> structure -> NextRacesToggle-> nextRacesTabEnabled=true)
        DESCRIPTION: 2. 'Extra Place' horse racing events should be present
        DESCRIPTION: 3. User is viewing Horse Racing EDP
        DESCRIPTION: **To configure HR Extra Place Race meeting use TI tool** (click [here](https://confluence.egalacoral.com/display/SPI/OpenBet+Systems) for credentials):
        DESCRIPTION: - HR event should be not started ('rawIsOffCode'= 'N' in SS response)
        DESCRIPTION: - HR event should have primary market 'Win or Each Way'
        DESCRIPTION: - HR event should have 'Extra Place Race' flag ticked on market level ('drilldownTagNames'='MKTFLAG_EPR' in SS response)
        DESCRIPTION: **To check info regarding event use the following link:**
        DESCRIPTION: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ
        DESCRIPTION: where,
        DESCRIPTION: X.XX - current supported version of OpenBet release
        DESCRIPTION: ZZZZ - an event id
        DESCRIPTION: **To configure 'Extra Place' signposting icon:**
        DESCRIPTION: 1) Open CMS -> Promotions ->  EXTRA PLACE RACE (if promotion is configured in another case use the instruction: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Promotions+CMS+configuration).
        DESCRIPTION: 2) Required fields for CMS configuration of created EXTRA PLACE RACE promotion:
        DESCRIPTION: * 'Is Signposting Promotion' checkbox (should be checked for activation Promo SIgnposting for different promotions)
        DESCRIPTION: * 'Event-level flag' field
        DESCRIPTION: * 'Market-level flag' field
        DESCRIPTION: * 'Overlay BET NOW button url' field (not required but without current URL 'BET NOW' button will be unclickable)
        DESCRIPTION: * 'Promotion Text' field (for editing promo footer text / not required)
        """
        next_races_toggle = self.get_initial_data_system_configuration().get('NextRacesToggle', {})
        if not next_races_toggle:
            next_races_toggle = self.cms_config.get_system_configuration_item('NextRacesToggle')
        if not next_races_toggle.get('nextRacesTabEnabled'):
            raise CmsClientException('Next Races Tab is not enabled in CMS')

        self.site.open_sport(name=self.get_sport_title(self.ob_config.horseracing_config.category_id))
        self.site.wait_content_state(state_name='HorseRacing')

        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')
        offer_and_featured_races = sections.get(vec.racing.OFFERS_AND_FEATURED_RACES, None)
        if offer_and_featured_races:
            self.__class__.use_present_event = \
                True if len(offer_and_featured_races.extra_place_offer_module.items_as_ordered_dict) > 0 else False
        else:
            self.__class__.use_present_event = False

        if not self.use_present_event:
            event = self.ob_config.add_UK_racing_event(number_of_runners=1, ew_terms=self.ew_terms)
            self.__class__.event_ID = event.event_id
            self.ob_config.change_racing_promotion_state(promotion_name='extra_place_race',
                                                         level='market',
                                                         market_id=self.ob_config.market_ids[self.event_ID],
                                                         event_id=self.event_ID)
        else:
            self._logger.warning('*** Using already present "Extra Place" race event')

    def test_001_tap_on_next_races_tab(self):
        """
        DESCRIPTION: Tap on 'Next Races' tab
        EXPECTED: 'Next Races' tab contains:
        EXPECTED: - 'Extra Place' races module
        EXPECTED: - 'Next Races' module (if configured)
        """
        tab = self.site.horse_racing.tabs_menu.click_button(button_name=vec.racing.RACING_NEXT_RACES_NAME)
        self.assertTrue(tab, msg=f'"{vec.racing.RACING_NEXT_RACES_NAME}" tab is not selected after click')

        if not self.site.horse_racing.next_races.has_extra_place_module(timeout=5):
            self.device.refresh_page()
            self.site.wait_splash_to_hide()

        self.assertTrue(self.site.horse_racing.next_races.has_extra_place_module(timeout=5),
                        msg='Next Races page has no Extra Place Module')
        self.__class__.extra_place_module = self.site.horse_racing.next_races.extra_place_module
        if self.use_present_event:
            self.__class__.event_ID = self.extra_place_module.event_id

    def test_002_verify_extra_place_content_area(self):
        """
        DESCRIPTION: Verify 'Extra Place' content area
        EXPECTED: Contains:
        EXPECTED: - 'Extra place' signposting icon (if configured)
        EXPECTED: - Event time (corresponds to **'startTime'** in SS response)
        EXPECTED: - Event name (taken from event **'name'** from SS response)
        EXPECTED: - Going (corresponds to **'going'** within **'racingFormEvent'** section from SS response)
        EXPECTED: - Distance (corresponds to **'distance'** within 'racingFormEvent' section from SS response)
        EXPECTED: - 'Each Way' terms (correspond to **'eachWayFactorNum'**, **'eachWayFactorDen'** and **'eachWayPlaces'** attributes in SS response)
        EXPECTED: - '>' icon
        """
        self.assertTrue(self.extra_place_module.extra_place_race.is_displayed(),
                        msg='Extra Place SignPosting icon is not displayed')
        event_details_ui = list(self.extra_place_module.value)
        event_name_ui = self.extra_place_module.name

        resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.event_ID)
        event = resp[0]['event']
        self.__class__.market = resp[0]['event']['children'][0]['market']
        event_name_from_ss = event['name']
        # Verification is not needed for "Event time (corresponds to **'startTime'** in SS response)" as UI displays only event name

        self.assertIn(event_name_ui, event_name_from_ss,
                      msg=f'Event name : {event_name_ui} does not match with SS response {event_name_from_ss}')
        self.assertTrue(self.extra_place_module.arrow_icon.is_displayed(), msg='Arrow icon is not displayed')

        resp = Datafabric().get_datafabric_data(event_id=self.event_ID)
        if resp["Error"]:
            self._logger.warning('*** Next Race Event has no distance and going')
        else:
            distance = resp['document'][self.event_ID]['distance']
            going = resp['document'][self.event_ID]['going']
            self.assertTrue(distance, msg=f'Distance "{distance}" is not available in response')
            self.assertTrue(going, msg=f'Going "{going}" is not available in response')

        self.__class__.each_way_present = self.market.get('isEachWayAvailable', None)
        if self.each_way_present:
            each_way_factor_num_from_ss = self.market['eachWayFactorNum']
            each_way_factor_den_from_ss = self.market['eachWayFactorDen']
            each_way_places_from_ss = int(self.market['eachWayPlaces'])
            joiner = '-'
            each_way_places_str = joiner.join(
                [str(each_way_place) for each_way_place in range(1, each_way_places_from_ss + 1)])
            ew_terms_text = vec.sb.NEW_ODDS_A_PLACES.format(num=each_way_factor_num_from_ss,
                                                            den=each_way_factor_den_from_ss,
                                                            arr=each_way_places_str)
            self.assertIn(ew_terms_text, event_details_ui,
                          msg=f'Each Way terms : "{event_details_ui}" does not match with response "{ew_terms_text}"')
        else:
            self._logger.warning(f'*** Each Way terms are not enabled for event {event_name_from_ss} with {self.event_ID} ID')

    def test_003_verify_each_way_terms_displaying(self):
        """
        DESCRIPTION: Verify 'Each Way' terms displaying
        EXPECTED: 'Each Way' terms are displayed if **isEachWayAvailable = true** attribute is present in SS response
        """
        # Done is scope of step #2
