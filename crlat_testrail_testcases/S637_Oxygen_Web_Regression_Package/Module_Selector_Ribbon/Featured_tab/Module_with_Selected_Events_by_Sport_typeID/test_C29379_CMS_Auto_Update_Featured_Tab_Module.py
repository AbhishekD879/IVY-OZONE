import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C29379_CMS_Auto_Update_Featured_Tab_Module(Common):
    """
    TR_ID: C29379
    NAME: CMS: Auto Update Featured Tab Module
    DESCRIPTION: This Test Case verifies Auto Update of Featured Tab's modules.
    DESCRIPTION: Jira ticket: BMA-5234 CMA - Auto Update Featured Tab Module
    DESCRIPTION: Note: Currently, there is no such functionality in cms api according to the comment in BMA-52041.
    PRECONDITIONS: 1) OB URL:
    PRECONDITIONS: TST2: https://backoffice-tst2.coral.co.uk/ti
    PRECONDITIONS: STG2:http://obbackoffice-stg2.gib1.egalacoral.com/ti
    PRECONDITIONS: 2) CMS: https://<CMS_ENDPOINT>/keystone
    PRECONDITIONS: (check <CMS_ENDPOINT> via 'devlog' function)
    PRECONDITIONS: 3) http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: NOTE: For caching needs Akamai service is used, so after saving changes in CMS there could be delay up to 5-10 mins before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_go_to_cms___featured_tab_modules(self):
        """
        DESCRIPTION: Go to CMS -> 'Featured tab Modules'
        EXPECTED: Available modules are displayed
        """
        pass

    def test_002_create_module_by_sport_type_id_where_max_events_to_display_field_is_blank_all_available_events_will_be_shown(self):
        """
        DESCRIPTION: Create module by <Sport> type ID where 'Max Events to Display' field is blank (all available events will be shown)
        EXPECTED: Valid module created by <Sport> type ID is created
        """
        pass

    def test_003_load_application___check_created_module(self):
        """
        DESCRIPTION: Load application -> Check created module
        EXPECTED: All loaded events are shown within module
        """
        pass

    def test_004_go_to_ob_ti_system___create_new_events_within_type_used_in_step_2_that_fits_to_loading_condition_in_cms_eg_start_time_within_events_from_and_events_to_dates(self):
        """
        DESCRIPTION: Go to OB TI system -> Create new event(s) within type used in step #2 that fits to loading condition in CMS (e.g. start time within 'Events from' and 'Events to' dates)
        EXPECTED: Valid event(s) is present within selected type
        """
        pass

    def test_005_wait_till_the_nearest_full_hour_eg_1000_1100_1200_1300_etc_passed___check_created_module_within_the_application(self):
        """
        DESCRIPTION: Wait till the nearest full hour e.g. 10.00, 11.00, 12.00, 13.00 etc. passed -> Check created module within the application
        EXPECTED: - Featured Tab Module content is updated due to changes in SS automaticay every full hour
        EXPECTED: - New event(s) is added within module
        EXPECTED: - All event names are corresponding to 'name' attribute in SS (nameoverrides are replaced)
        EXPECTED: - Number of added/removed events corresponds to set limits (Max Events to Display) and time range for created Featured Tab Module.
        """
        pass
