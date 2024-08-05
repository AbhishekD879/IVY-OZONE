import pytest
from random import randint
from time import sleep
from collections import OrderedDict
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C61838_Featured_Module_by_Sport_TypeID__Verify_names_displaying_within_Featured_tab(BaseFeaturedTest):
    """
    TR_ID: C61838
    NAME: Featured: Module by <Sport> TypeID - Verify names displaying within Featured tab
    DESCRIPTION: This test case verifies whether event/selection names are displayed correctly on the frontend for Featured tab module by <Sport> TypeID
    PRECONDITIONS: 1) Featured Module by <Sport> TypeID is created in CMS. Module should contain at least 1 Regular event with long name 1 Outright event with long name. Name can be modified in TI or in CMS Featured Module edit page.
    PRECONDITIONS: 2) CMS, TI: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: (check <CMS_ENDPOINT> via 'devlog' function)
    PRECONDITIONS: 3) http://{domain}/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Where, domain is:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk - for TST2 environment
    PRECONDITIONS: https://ss-aka-ori-stg2.coral.co.uk - for STG2 environment
    PRECONDITIONS: https://ss-aka-ori.coral.co.uk - for HL and PROD environments
    PRECONDITIONS: NOTE: For caching needs Akamai service is used, so after saving changes in CMS there could be delay up to 5-10 mins before they will be applied and visible on the front end.
    """
    keep_browser_open = True
    expected_price = '1/7'
    lp = OrderedDict([('odds_home', expected_price),
                      ('odds_draw', expected_price),
                      ('odds_away', expected_price)])
    featured_tab_name = ''
    long_name = 'Test team %d with a long name, really very long one aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    long_name2 = 'Test team2 %d with a long name, really very long one eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'

    def get_section(self, section_name=None):
        sections = self.site.home.get_module_content(
            module_name=self.featured_tab_name
        ).accordions_list.items_as_ordered_dict
        self.assertIn(section_name, sections, msg=f'"{self.module_name}" module is not in sections')
        return sections[section_name]

    def is_truncated(self, text=None, truncate=None):
        if text:
            if truncate:
                is_ended_with_dots = True if text[-3:] == '...' else False
                self.assertTrue(is_ended_with_dots, msg='event name is not truncated')
            else:
                is_len_100 = True if len(text) <= 104 else False  # for mobile 100 symbols + 3 dots
                self.assertTrue(is_len_100, msg='Event name is truncated')

    def test_000_preconditions(self):
        """
        DESCRIPTION: create event and add to the featured tab
        """
        self.__class__.team1 = self.long_name % randint(1000, 5000)
        self.__class__.team2 = self.long_name % randint(5000, 10000)
        self.__class__.team3 = self.long_name2 % randint(1000, 5000)

        # Regular event( football)
        event_params = self.ob_config.add_football_event_to_featured_autotest_league(lp=self.lp, team1=self.team1,
                                                                                     team2=self.team2)
        fb_type_id = self.ob_config.football_config.autotest_class.featured_autotest_league.type_id

        self.__class__.eventID = event_params.event_id

        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        self.__class__.event_name = normalize_name(event_resp[0]['event']['name'])
        self._logger.info(f'*** Created Football event "{self.event_name}"')
        self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0])

        # adding football event to featured tab
        self.__class__.fb_module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Type', id=fb_type_id, show_expanded=False, show_all_events=True,
            events_time_from_hours_delta=-10, module_time_from_hours_delta=-10)['title'].upper()

        self.__class__.featured_tab_name = self.get_ribbon_tab_name(
            self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)

        # outright event
        self.__class__.outright_event = self.ob_config.add_autotest_premier_league_football_outright_event(lp=self.lp,
                                                                                                           event_name=self.team3)

        outright_type_id = self.outright_event.ss_response['event']['typeId']
        self.__class__.pre_match_event = self.outright_event.ss_response['event']['name']
        self.__class__.pre_match_event_section_name = self.outright_event.ss_response['event']['className'].replace("Football ", "") + " - " + \
            self.outright_event.ss_response['event']['typeName']

        # adding outright  event to featured tab
        self.__class__.module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Type', id=outright_type_id, show_expanded=False, show_all_events=True,
            events_time_from_hours_delta=-10, module_time_from_hours_delta=-10)['title'].upper()

        self.__class__.featured_tab_name = self.get_ribbon_tab_name(
            self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)

    def test_001_navigane_to_homepage__featured_tab(self):
        """
        DESCRIPTION: Navigane to Homepage > Featured tab
        EXPECTED: * Active Featured modules are displayed in Featured tab
        """
        self.site.wait_content_state(state_name='Homepage')
        sleep(3)
        self.wait_for_featured_module(name=self.fb_module_name)
        self.wait_for_featured_module(name=self.module_name)

    def test_002_expand_featured_module_from_preconditions(self):
        """
        DESCRIPTION: Expand Featured Module from Preconditions
        EXPECTED: * Events are displayed within the module as per CMS configuration
        EXPECTED: * Regular <Sport> events' long names are cropped and followed with '...' before the price/odds buttons / scores (if available)
        EXPECTED: * Outright <Sport> events' long names are not cropped and event name is displayed in multiple raws if it doesn't fit the width
        """
        section1 = self.get_section(section_name=self.module_name)
        section1.expand()
        event1 = section1.items_as_ordered_dict
        text_outright = list(event1)[1]
        self.is_truncated(text=text_outright, truncate=False)

        section2 = self.get_section(section_name=self.fb_module_name)
        section2.expand()
        event2 = section2.items_as_ordered_dict
        text_fb = list(event2)[0]
        self.is_truncated(text=text_fb, truncate=True)
