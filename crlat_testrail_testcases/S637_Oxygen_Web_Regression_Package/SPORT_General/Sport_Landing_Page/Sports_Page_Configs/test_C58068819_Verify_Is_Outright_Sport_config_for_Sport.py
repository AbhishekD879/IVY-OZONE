import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C58068819_Verify_Is_Outright_Sport_config_for_Sport(Common):
    """
    TR_ID: C58068819
    NAME: Verify  'Is Outright Sport' config for Sport
    DESCRIPTION: This test case verifies 'Is Outright Sport' config for Sport.
    DESCRIPTION: The following Sports should be configured as Outrights:
    DESCRIPTION: **CYCLING, FORMULA 1, GOLF, MOTOR BIKES, MOTOR SPORTS, MOVIES, POLITICS, MOTOR SPEEDWAY, TV SPECIALS**
    DESCRIPTION: **Note: This test case should be run ONLY for the above mentioned list of sports**
    PRECONDITIONS: **OB Configurations:**
    PRECONDITIONS: The following 2 events should be created:
    PRECONDITIONS: 1) event with primary market e.g. for Golf primary market is '3 Ball Betting' and it's 'dispSortName' is "3W"
    PRECONDITIONS: **NOTE!**To configure the Primary market for Sport use the following link: https://confluence.egalacoral.com/display/SPI/Primary+Markets+and+dispSortNames+for+Different+Sports
    PRECONDITIONS: 2) outright event
    PRECONDITIONS: **CMS Configurations:**
    PRECONDITIONS: To configure the 'isOutrightSport' for the particular sport use the following instruction:
    PRECONDITIONS: * Navigate to CMS -> Sports Pages -> Sports Categories -> choose <Sport> -> set 'isOutrightSport': "True"
    PRECONDITIONS: To configure the Primary markets for the particular sport use the following instruction:
    PRECONDITIONS: * Put correct values in 'Disp sort name' field e.g. 3W for Golf
    PRECONDITIONS: * Put correct values in 'Primary markets' field e.g. |3 Ball Betting| for Golf
    PRECONDITIONS: - To verify filtering for markets set via CMS use the following <sport-config> response:
    PRECONDITIONS: https://<particular env e.g. sports-tst2.ladbrokes.com>/cms/api/<Brand>/sport-config/<Category ID> -> config -> tabs -> today/tomorrow/future tab -> verify the presenсe of following parameters:
    PRECONDITIONS: - "marketTemplateMarketNameIntersects"
    PRECONDITIONS: - "dispSortName"
    PRECONDITIONS: ![](index.php?/attachments/get/99322540)
    PRECONDITIONS: **NOTE: In scope of BMA-55206 "marketTemplateMarketNameIntersects" and "dispSortName" will be received in <initial-data>:**
    PRECONDITIONS: ![](index.php?/attachments/get/121567991)
    PRECONDITIONS: - To verify simple filters in <EventToOutcomeForClass> request on 'Matches'/'Competitions' tab please check the Request URL:
    PRECONDITIONS: ![](index.php?/attachments/get/99322539)
    PRECONDITIONS: *The values set for "marketTemplateName" and "dispSortName" via CMS will be add to the filters in <EventToOutcomeForClass> request.*
    PRECONDITIONS: - To verify events filtering on 'Competitions' tab (Tier 2 only e.g. Cricket) see the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Sport+Page+Configs#SportPageConfigs-Competitions
    PRECONDITIONS: - To verify queries from Front-end to SiteServe for data availability checking use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+get+data+from+Openbet+Site+Server
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the Sport Landing page that has 'isOutrightSport': "True" set in CMS
    PRECONDITIONS: 3. Choose the 'Matches' tab
    """
    keep_browser_open = True

    def test_001_verify_events_displaying_on_the_page(self):
        """
        DESCRIPTION: Verify events displaying on the page
        EXPECTED: * Both events from pre-conditions are displayed
        EXPECTED: * Events are displayed with Outrights view
        EXPECTED: * Selections from the Primary Market are NOT displayed on the event card
        """
        pass

    def test_002_verify_the_filters_for_eventtooutcomeforclass_request_to_the_ss(self):
        """
        DESCRIPTION: Verify the filters for <EventToOutcomeForClass> request to the SS
        EXPECTED: The following filter is added to the request:
        EXPECTED: - event.eventSortCode:intersects:TNMT,TR01,TR02,...,TR20,MTCH
        """
        pass

    def test_003_verify_the_received_data_in_eventtooutcomeforclass_response_from_the_ss(self):
        """
        DESCRIPTION: Verify the received data in <EventToOutcomeForClass> response from the SS
        EXPECTED: * Both events are received in <EventToOutcomeForClass> response from the SS
        EXPECTED: * Primary market is received in <EventToOutcomeForClass> response from the SS
        """
        pass

    def test_004__open_the_cms___sports_pages___sports_categories___choose_sport_set_the_isoutrightsport_false_back_to_the_app_refresh_the_page_verify_events_displaying_on_the_page(self):
        """
        DESCRIPTION: * Open the CMS -> Sports Pages -> Sports Categories -> choose <Sport>.
        DESCRIPTION: * Set the 'isOutrightSport': "False".
        DESCRIPTION: * Back to the app.
        DESCRIPTION: * Refresh the page.
        DESCRIPTION: * Verify events displaying on the page.
        EXPECTED: Only event with primary market is displayed on the page
        """
        pass

    def test_005_verify_the_filters_for_eventtooutcomeforclass_request_to_the_ss(self):
        """
        DESCRIPTION: Verify the filters for <EventToOutcomeForClass> request to the SS
        EXPECTED: The following filters are added to the request:
        EXPECTED: - market.templateMarketName:intersects:{value from cms} (|3 Ball Betting in our case)
        EXPECTED: - market.dispSortName:intersects:{value from cms} (3W in our case)
        EXPECTED: - event:simpleFilter:market.dispSortName:intersects: {value from cms}  (3W in our case)
        """
        pass

    def test_006_verify_the_received_data_in_eventtooutcomeforclass_response_from_the_ss(self):
        """
        DESCRIPTION: Verify the received data in <EventToOutcomeForClass> response from the SS
        EXPECTED: * Only event with primary market is received in <EventToOutcomeForClass> response from the SS
        EXPECTED: * Primary market is received in <EventToOutcomeForClass> response from the SS
        """
        pass
