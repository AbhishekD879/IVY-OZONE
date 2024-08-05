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
class Test_C74997_CMS_Auto_Update_Featured_Tab_Module(Common):
    """
    TR_ID: C74997
    NAME: CMS: Auto Update Featured Tab Module
    DESCRIPTION: This Test Case verifies Auto Update of Featured Tab's modules.
    DESCRIPTION: Jira ticket: BMA-5234 CMA - Auto Update Featured Tab Module
    DESCRIPTION: NOTE: the test case is not up to date and should be rewritten after implementing this story - https://jira.egalacoral.com/browse/BMA-52334
    PRECONDITIONS: - CMS https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=CMS-API+Endpoints
    PRECONDITIONS: - Ladbrokes OpenBet System https://confluence.egalacoral.com/display/SPI/Ladbrokes+OpenBet+System
    PRECONDITIONS: - Coral OpenBet System https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - Kibana logs http://ladbrokescoral-logs.coralsports.dev.cloud.ladbrokescoral.com/_plugin/kibana/app/kibana#/discover?_g=(refreshInterval:(pause:!t,value:0),time:(from:'2020-03-29T21:00:00.000Z',mode:absolute,to:'2020-03-31T14:25:32.531Z'))&_a=(columns:!(log),index:'cms-api-dev2-*',interval:auto,query:(language:lucene,query:'XXXXXXX'),sort:!('@timestamp',desc))
    PRECONDITIONS: XXXXXXX - Module id
    PRECONDITIONS: "Auto-refresh events" checkbox unchecked
    PRECONDITIONS: - http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: NOTE: For caching needs Akamai service is used, so after saving changes in CMS there could be delayed up to 5-10 mins before they will be applied and visible on the front end.
    PRECONDITIONS: NOTE: This test case should check also Virtual Horses/Greyhounds events within Featured Module.
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

    def test_004_go_to_ob_ti_system___create_new_events_within_type_used_in_step_2_that_fits_to_loading_condition_in_cms_eg_with_start_time_within_events_from_and_events_to_dates(self):
        """
        DESCRIPTION: Go to OB TI system -> Create new event(s) within type used in step #2 that fits to loading condition in CMS (e.g. with start time within 'Events from' and 'Events to' dates)
        EXPECTED: Valid event(s) is present within selected type
        """
        pass

    def test_005_wait_till_the_nearest_full_hour_eg_1000_1100_1200_1300_etc_passed___check_created_module(self):
        """
        DESCRIPTION: Wait till the nearest full hour e.g. 10.00, 11.00, 12.00, 13.00 etc. passed -> Check created module
        EXPECTED: - Featured Tab Module content is updated due to changes in SS automaticay every full hour
        EXPECTED: - New event(s) is added within module
        EXPECTED: - All event names are corresponding to 'name' attribute in SS (nameoverrides are replaced)
        EXPECTED: - Number of added/removed events corresponds to set limits (Max Events to Display) and time range for created Featured Tab Module.
        """
        pass

    def test_006_go_to_cms___open_any_of_the_created_featured_tab_module___rename_any_event_within_it_and_click_on_save_button(self):
        """
        DESCRIPTION: Go to CMS -> Open any of the created Featured Tab Module -> Rename any event within it and click on 'Save' button
        EXPECTED: Event is successfully renamed on front end.
        """
        pass

    def test_007_wait_till_the_nearest_full_hour(self):
        """
        DESCRIPTION: Wait till the nearest full hour.
        EXPECTED: Event should not be renamed to default name with auto update.
        """
        pass
