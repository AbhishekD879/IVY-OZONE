import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C28955_Verify_Unhappy_Pass_of_Next_Races_Type_ID_and_Type_Date_Range_CMS_configuration(Common):
    """
    TR_ID: C28955
    NAME: Verify Unhappy Pass of Next Races Type ID and Type Date Range CMS configuration
    DESCRIPTION: This test case verifies Unhappy Pass of Next Races CMS configuration via Type ID and Type Date Range
    DESCRIPTION: Story Ticket: **BMA-6572** CMS: Next Races Config Group
    DESCRIPTION: BMA-10828 All devices - Next 4 Races
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: CMS_ENDPOINT/keystone/structure
    PRECONDITIONS: where CMS_ENDPOINT can be found using devlog
    PRECONDITIONS: 1. In order to get a list of **Next Races** events and check **typeId**
    PRECONDITIONS: https://{openbet_env_link}/openbet-ssviewer/Drilldown/X.XX/NextNEventToOutcomeForClass/N/YYYY?simpleFilter=event.typeFlagCodes:intersects:UK,IE,INT&simpleFilter=event.isActive:isTrue&simpleFilter=market.templateMarketName:equals:|Win%20or%20Each%20Way|&priceHistory=true&simpleFilter=event.siteChannels:contains:M&existsFilter=event:simpleFilter:market.marketStatusCode:equals:A&simpleFilter=market.marketStatusCode:equals:A&simpleFilter=outcome.outcomeStatusCode:equals:A&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.rawIsOffCode:notEquals:Y&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:1&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:2&limitRecords=outcome:4&translationLang=en&responseFormat=json
    PRECONDITIONS: Where
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY - class ID
    PRECONDITIONS: N - number of events
    PRECONDITIONS: Note: OB supports only values:3, 5, 7 or 12. Example, if CMS value > 12 then 12 events is set on UI, if CMS value <= 5 then 5 events is set on UI and etc.
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_load_cms(self):
        """
        DESCRIPTION: Load CMS
        EXPECTED: CMS is opened
        """
        pass

    def test_002_tap_system_configuration_section(self):
        """
        DESCRIPTION: Tap 'System-configuration' section
        EXPECTED: 'System-configuration' section is opened
        """
        pass

    def test_003_type_in_search_ffiels_nextraces_section(self):
        """
        DESCRIPTION: Type in search ffiels 'NEXTRACES' section
        EXPECTED: NEXTRACES section is shown
        """
        pass

    def test_004_in_type_id_field_enter_valid_horse_racing_id_and_leave_type_date_range_empty___press_submit(self):
        """
        DESCRIPTION: In '**Type ID**' field enter valid <Horse Racing> id and leave '**Type Date Range**' empty -> Press 'Submit'
        EXPECTED: *   Both 'Type ID' and 'Type Date Range' need to have values set in order to display Events within the chosen ‘Type ID’
        EXPECTED: *   Error handling is missing on CMS (data should be valid)
        EXPECTED: *   In case of invalid Type ID and Type Date ranges Next Races are missing on front end
        """
        pass

    def test_005_leave_empty_type_id_and_set_type_date_range___press_submit(self):
        """
        DESCRIPTION: Leave empty '**Type ID**' and set '**Type Date Range**' -> Press 'Submit'
        EXPECTED: Changes are saved in CMS
        """
        pass

    def test_006_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_007_tap_horse_racing_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Horse Racing> icon from the Sports Menu Ribbon
        EXPECTED: *   <Horse Racing> landing page is opened
        EXPECTED: *   'Next Races' module is displayed
        """
        pass

    def test_008_verify_next_races_events(self):
        """
        DESCRIPTION: Verify 'Next Races' events
        EXPECTED: *   Type ID and Type Date Range are not taken into consideration
        EXPECTED: *   Appropriate Events which correspond to inputted configurations in CMS are present (e.g. Is Irish, Number of Events)
        """
        pass

    def test_009_leave_empty_both_type_id_and_type_date_range_fields__press_submit(self):
        """
        DESCRIPTION: Leave empty both 'Type ID' and 'Type Date Range' fields-> Press 'Submit'
        EXPECTED: Changes are saved in CMS
        """
        pass

    def test_010_repeat_6_8(self):
        """
        DESCRIPTION: Repeat #6-8
        EXPECTED: 
        """
        pass
