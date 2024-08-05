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
class Test_C29416_Verify_Racing_Post_Silks_Form_Information_in_Race_events_carousel(Common):
    """
    TR_ID: C29416
    NAME: Verify Racing Post Silks/Form Information in <Race> events carousel
    DESCRIPTION: This test case is for checking of racing post silks & form informaiton which are displayed in the <Race> events carousel
    PRECONDITIONS: update: After BMA-40744 implementation we'll receive needed data from DF api:
    PRECONDITIONS: Racing Data Hub link:
    PRECONDITIONS: Coral DEV : cd-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key={api-key}
    PRECONDITIONS: Ladbrokes DEV : https://ld-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key=LDaa2737afbeb24c3db274d412d00b6d3b
    PRECONDITIONS: URI : /v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key={api-key}
    PRECONDITIONS: {categoryKey} : 21 - Horse racing, 19 - Greyhound
    PRECONDITIONS: {eventKey} : OB Event id
    PRECONDITIONS: - RDH feature toggle:
    PRECONDITIONS: Horse Racing (HR) Racing Data Hub toggle is turned on : System-configuration > RacingDataHub > isEnabledForHorseRacing = true
    PRECONDITIONS: Greyhounds (GH) Racing Data Hub toggle is turned on: System-configuration > RacingDataHub > isEnabledForGreyhound = true
    PRECONDITIONS: -------
    PRECONDITIONS: 1) CMS: https://**CMS_ENDPOINT**/keystone/modular-content/ (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 2) Make sure events are available within module created by <Race> type ID for current day
    PRECONDITIONS: 3) To retrieve an infrormation about event outcomes and silks info etc. use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/YYYY?translationLang=LL?racingForm=outcome
    PRECONDITIONS: where:
    PRECONDITIONS: *YYYY is an **'event id'** which is taken from the link in step 2.*
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: - **'name'** on outcome level to see a horse name
    PRECONDITIONS: - **'jockey'** to see a jockey information
    PRECONDITIONS: **- 'trainer' ** to see trainer name
    PRECONDITIONS: - **'silkName' **to find out a name of file to download needed silk.
    PRECONDITIONS: Silk can be downloaded using Image URL's in the following format:
    PRECONDITIONS: {endpoint}/racingpost/{silkNames} - silk names have to be joined via comma.
    PRECONDITIONS: ENDPOINTS:
    PRECONDITIONS: DEV: https://aggregation-ms-dev.symphony-solutions.eu
    PRECONDITIONS: STG: https://coral-aggregation-ms-stg2.symphony-solutions.eu
    PRECONDITIONS: PROD: https://coral-aggregation-ms.symphony-solutions.eu
    PRECONDITIONS: TST2: https://coral-aggregation-ms-tst2.symphony-solutions.eu
    PRECONDITIONS: **NOTE**: For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    PRECONDITIONS: NOTE: This test case should check also Virtual Horses/Greyhounds events within Featured Module.
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_002_for_mobiletabletgo_to_module_selector_ribbon___module_created_by_race_type_id(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Go to Module Selector Ribbon -> Module created by <Race> type ID
        EXPECTED: *   'Feature' tab is selected by default
        EXPECTED: *   Module created by <Race> type ID is shown
        """
        pass

    def test_003_for_desktopscroll_the_page_down_to_featured_section____module_created_by_race_type_id(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Scroll the page down to 'Featured' section ->-> Module created by <Race> type ID
        EXPECTED: * 'Featured' section is displayed below the following sections: Enhanced/ Sports offer carousel, In-Play & Live Stream, Next Races Carousel (if applicable)
        EXPECTED: * Module created by <Race> type ID is shown
        """
        pass

    def test_004_check_site_server___find_event_which_has_racing_post_rp_silks_mapped_and_is_shown_within_module_created_by_race_type_id(self):
        """
        DESCRIPTION: Check Site Server -> find event which has Racing Post (RP) silks mapped and is shown within module created by <Race> type ID
        EXPECTED: 
        """
        pass

    def test_005_on_race_events_carousel_verify_horse_silk_iconfilter_responses_by_sb_apiladbrokescom_and_seek_for_the_data_in_steps_belowindexphpattachmentsget105776438or_in_featured_msindexphpattachmentsget105776466(self):
        """
        DESCRIPTION: On <Race> events carousel verify Horse Silk icon
        DESCRIPTION: (filter responses by 'sb-api.ladbrokes.com' and seek for the data in steps below)
        DESCRIPTION: ![](index.php?/attachments/get/105776438)
        DESCRIPTION: or in Featured MS
        DESCRIPTION: ![](index.php?/attachments/get/105776466)
        EXPECTED: Horse silk icon corresponds to the image which is downloaded using Image URL's.
        """
        pass

    def test_006_verify_race_selection_name(self):
        """
        DESCRIPTION: Verify <Race Selection> Name
        EXPECTED: <Race Selection> name corresponds to the **'name' **attribute
        """
        pass

    def test_007_verify_jockeytrainer_information(self):
        """
        DESCRIPTION: Verify jockey/trainer information
        EXPECTED: Jockey information corresponds to the **'jockey'** attribute
        EXPECTED: Trainer information corresponds to the **'trainer' **attribute
        EXPECTED: The information is shown in next format: **Jockey/Trainer**
        """
        pass

    def test_008_for_mobiletabletverify_form_informationindexphpattachmentsget105776470(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Verify form information
        DESCRIPTION: ![](index.php?/attachments/get/105776470)
        EXPECTED: Form information corresponds to the **'formGuide' **attribute
        """
        pass

    def test_009_verify_runner_number_information(self):
        """
        DESCRIPTION: Verify runner number information
        EXPECTED: Runner number corresponds to the **'runnerNumber'** attribute
        """
        pass

    def test_010_verify_draw_information(self):
        """
        DESCRIPTION: Verify draw information
        EXPECTED: Draw information corresponds to the '**draw'** attribute
        """
        pass

    def test_011_verify_odds(self):
        """
        DESCRIPTION: Verify odds
        EXPECTED: Price/odds buttons are displayed
        """
        pass

    def test_012_verify_selection_if_some_of_the_racing_post_info_is_absenteg_intercept_response_from_sb_apiladbrokescom_and_remove_some_parameternote_this_will_not_work_for_featured_websocket(self):
        """
        DESCRIPTION: Verify selection if some of the racing post info is absent
        DESCRIPTION: (e.g. intercept response from 'sb-api.ladbrokes.com' and remove some parameter.
        DESCRIPTION: NOTE: this will not work for Featured WebSocket)
        EXPECTED: If some attribute is absent -> it is just not shown in the application
        """
        pass

    def test_013_check_case_when_event_doesnt_have_rp_silks_mappedeg_block_aggregation_service_response_eg_aggregation_hlv0ladbrokescom(self):
        """
        DESCRIPTION: Check case when event doesn't have RP silks mapped
        DESCRIPTION: (e.g. block aggregation service response, e.g. aggregation-hlv0.ladbrokes.com)
        EXPECTED: *   Generic silk icon is displayed
        EXPECTED: *   Horse name corresponds to the **'name'** attribute
        """
        pass
