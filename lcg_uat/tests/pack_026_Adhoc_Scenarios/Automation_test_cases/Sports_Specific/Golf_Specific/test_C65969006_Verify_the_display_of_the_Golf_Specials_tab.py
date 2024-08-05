import pytest
from crlat_cms_client.utils.exceptions import CMSException
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter, exists_filter
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException


def get_sport_tab_status(tab):
    check_events = tab.get("checkEvents")
    has_events = tab.get("hasEvents")
    enabled = tab.get("enabled")
    if not enabled:
        return False
    if check_events is None or has_events is None:
        raise CMSException(
            f'check_events:{check_events} and has_events:{has_events},The paremeters are not present in response')
    if check_events and not has_events:
        return False
    return True

@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.sports_specific
@pytest.mark.golf_specific
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@vtest
class Test_C65969006_Verify_the_display_of_the_Golf_Specials_tab(BaseBetSlipTest):
    """
    TR_ID: C65969006
    NAME: Verify the display of the Golf Specials tab
    DESCRIPTION: 1. CMS-&gt; Sport pages-&gt; Sport category-&gt; Golf2.
    DESCRIPTION: 2. Click on specials tab-&gt; enable/disable
    DESCRIPTION: Note: If specials events are created in ob, then only specials tab will display in FE
    PRECONDITIONS: CMS-&gt; Sport pages-&gt; Sport category-&gt; Golf
    PRECONDITIONS: CMS-&gt; Sport pages-&gt; Sport category-&gt; Golf-&gt; General Sport Configuration-&gt; Active/Inactive sport
    PRECONDITIONS: Note: If specials events are created in OB, then only specials tab will display in FE
    """
    keep_browser_open = True
    all_sports_page = 'az-sports'

    def get_selection_id_for_specials_market(self):
        ss_req_class = self.ss_req.ss_class(query_builder=self.ss_query_builder.add_filter(
            simple_filter(LEVELS.CLASS, ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS, self.sport_id))
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.IS_ACTIVE))
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, "M"))
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.HAS_OPEN_EVENT)))
        class_id = ss_req_class[0].get("class").get("id")
        queryParams = (self.ss_query_builder. \
            add_filter(simple_filter(LEVELS.EVENT,ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS,"M"))\
            .add_filter(exists_filter(LEVELS.EVENT,simple_filter(LEVELS.MARKET,ATTRIBUTES.DRILLDOWN_TAG_NAMES,OPERATORS.INTERSECTS,"MKTFLAG_SP")))
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN, self.start_date_minus)))
        events = self.ss_req.ss_event_to_outcome_for_class(class_id=class_id, query_builder=queryParams)
        selection_ids = []
        type_names = []
        for event in events:
            selection_id = event['event']['children'][0]['market']['children'][0]['outcome']['id']
            type_name =event['event']['typeName']
            selection_ids.append(selection_id)
            type_names.append(f'golf - {type_name}'.upper())
        unique_type_names =list(set(type_names))
        return selection_ids,unique_type_names

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1.User should have access to oxygen CMS
        PRECONDITIONS: 2.Outrights tab can be configured from CMS->
        PRECONDITIONS: Sports menu-> Sports category-> Table Tennis-> Outright's tab-> Enable/Disable.
        """
        self.__class__.sport_id = self.ob_config.golf_config.category_id
        selections = self.get_selection_id_for_specials_market()[0]
        if len(selections)==0:
            raise SiteServeException('There are not available special events')
        sport_tab_id = self.cms_config.get_sport_tab_id(sport_id=self.sport_id, tab_name="specials")
        sport_tab_data = self.cms_config.get_sports_tab_data(sport_id=self.sport_id, tab_name="specials")
        if not sport_tab_data.get('enabled'):
            self.cms_config.update_sports_tab_status(sport_tab_id=sport_tab_id, enabled=True)
        tab_available = get_sport_tab_status(tab=self.cms_config.get_sports_tab_data(sport_id=self.sport_id, tab_name="specials"))
        if not tab_available:
            raise CmsClientException('data is not available in specials tab')

    def test_001_launch_the_ladbrokes_and_coral_application(self):
        """
        DESCRIPTION: Launch the Ladbrokes and Coral application.
        EXPECTED: The application should be launched successfully.
        """
        self.site.login()
        self.site.wait_content_state(state_name='HomePage')

    def test_002_select_the_golf_sport_either_from_the_sports_ribbon_or_through_the_a_z_menu(self):
        """
        DESCRIPTION: Select the Golf Sport either from the sports ribbon or through the A-Z menu.
        EXPECTED: User should be redirected to the Golf sport landing page.
        """
        self.navigate_to_page(name=self.all_sports_page)
        a_z_menu = self.site.all_sports.a_z_sports_section.items_as_ordered_dict
        self.assertTrue(a_z_menu, msg='A-Z menu is not present')
        golf = a_z_menu.get('Golf')
        self.assertTrue(golf, msg='golf sport is not present in a-z sports')
        golf.click()
        self.site.wait_content_state(state_name='Golf')

    def test_003_select_the_specials_tab(self):
        """
        DESCRIPTION: Select the Specials tab
        EXPECTED: The Specials tab should be loaded with the various Special events.
        """
        current_tab = self.site.golf.tabs_menu.current
        if current_tab.upper() != 'SPECIALS':
            self.site.golf.tabs_menu.click_button("SPECIALS")
        special_events = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.keys()
        self.assertTrue(special_events, msg=f'special events {special_events} are not available')
        special_events_list = list(special_events)
        expected_events_list = self.get_selection_id_for_specials_market()[1]
        special_events_list.sort()
        expected_events_list.sort()
        self.assertListEqual(special_events_list,expected_events_list,msg=f'actual event list {special_events_list}'
                                                           f'is not equal to expected event list {expected_events_list}')

    def test_004_add_various_selections_from_the_special_events_and_place_bet(self):
        """
        DESCRIPTION: Add various selections from the Special events and place bet.
        EXPECTED: The user should be able to add various selections and place bet successfully for the Special event.
        """
        selections_ids = self.get_selection_id_for_specials_market()[0]
        self.open_betslip_with_selections(selection_ids=selections_ids[0])
        self.place_single_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
