import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.streaming
@vtest
class Test_C58836283_Verify_Conviva_metadata_are_sent_correctly_via_tags(Common):
    """
    TR_ID: C58836283
    NAME: Verify Conviva metadata are sent correctly via tags
    DESCRIPTION: 
    PRECONDITIONS: This test case verifies if all needed metadata is successfully passed from app to Conviva
    PRECONDITIONS: URL - https://touchstone.conviva.com/
    PRECONDITIONS: username: andrei.banarescu@ladbrokescoral.com
    PRECONDITIONS: password: LadbrokesCoral19
    PRECONDITIONS: Conviva tags: https://apps.conviva.com/metadata/setup
    PRECONDITIONS: List of CMS endpoints:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=CMS-API+Endpoints
    PRECONDITIONS: To enable/disable Conviva monitoring in CMS: ** CMS > System Configuration > Conviva -> enabled **
    PRECONDITIONS: enable testMode - for testing and debug purpose:
    PRECONDITIONS: CMS > System Configuration > Conviva -> testMode
    PRECONDITIONS: Stream (ATR, IMG or Perform, RUK, RPGTV are supported) is mapped and available for any event in application, IGMedia streams are not supported
    PRECONDITIONS: 1) Set Conviva parameter to enabled in CMS
    PRECONDITIONS: 2) In another tab/browser open Touchstone (https://touchstone.conviva.com/sources ) and login with credentials:
    PRECONDITIONS: username: andrei.banarescu@ladbrokescoral.com
    PRECONDITIONS: password: LadbrokesCoral19
    PRECONDITIONS: 3) Open environment (Coral/Ladbrokes) and login with valid user
    """
    keep_browser_open = True

    def test_001_navigate_to_edp_of_the_event_with_mapped_stream(self):
        """
        DESCRIPTION: Navigate to EDP of the event with mapped stream
        EXPECTED: * EDP is opened
        EXPECTED: * Stream is available for watching
        """
        pass

    def test_002_tapclick_on_watch_live_button_and_make_sure_stream_is_playing(self):
        """
        DESCRIPTION: Tap/click on 'Watch Live' button and make sure stream is playing
        EXPECTED: Stream is successfully started
        """
        pass

    def test_003_open_tabbrowser_with_touchstoneverify_event_appears_in_the_table_on_home_page(self):
        """
        DESCRIPTION: Open tab/browser with Touchstone
        DESCRIPTION: Verify event appears in the table on Home page
        EXPECTED: Event appears in the table with active status, event name and OB id, Browser/OS, Remote address
        EXPECTED: ![](index.php?/attachments/get/109060065)
        """
        pass

    def test_004_tapclick_on_monitor_this_device_button(self):
        """
        DESCRIPTION: Tap/Click on 'Monitor this device' button
        EXPECTED: Page with more information about the stream playing is opened: Content information, Player & SDK Information, Tags and others.
        EXPECTED: ![](index.php?/attachments/get/109060067)
        """
        pass

    def test_005_verify_that_metadata_is_present_in_tags_section(self):
        """
        DESCRIPTION: Verify that metadata is present in 'Tags' section
        EXPECTED: Data is received and is present in 'Tags' section
        """
        pass

    def test_006_verify_the_value_for_brand_platform_for_playername_framework_player_framework_version_is_written_in_a_correct_format(self):
        """
        DESCRIPTION: Verify the value for [Brand] [Platform] for 'PlayerName', 'Framework', 'Player Framework Version' is written in a correct format
        EXPECTED: The value of the parameter is written in the 'Player & SDK Information' sectio in the format:
        EXPECTED: PlayerName: Ladbrokes iOS
        EXPECTED: Framework: Video JS
        EXPECTED: Player Framework Version: 6.10.1
        EXPECTED: ![](index.php?/attachments/get/112060495)
        """
        pass

    def test_007_verify_that_value_for_device_metadata_is_written_in_a_correct_format_device_name_device_hardware_type_device_manufacturer_device_marketing_name_device_operating_system_family_device_operating_system_device_operating_system_version_device_model(self):
        """
        DESCRIPTION: Verify that value for [Device Metadata] is written in a correct format:
        DESCRIPTION: * Device Name
        DESCRIPTION: * Device Hardware Type
        DESCRIPTION: * Device Manufacturer
        DESCRIPTION: * Device Marketing Name
        DESCRIPTION: * Device Operating System Family
        DESCRIPTION: * Device Operating System
        DESCRIPTION: * Device Operating System Version
        DESCRIPTION: * Device Model
        EXPECTED: DeviceMetadata is supposed to be set automatically by Conviva SDK
        EXPECTED: Format of the tag and availability of tags are defined by Conviva SDK
        EXPECTED: ![](index.php?/attachments/get/111269363)
        """
        pass

    def test_008_verify_that_values_for_basic_metadata_is_sent_in_correct_format_for_streaming_information_live_or_vod_asset_name_stream_url_viewer_id(self):
        """
        DESCRIPTION: Verify that values for Basic Metadata is sent in correct format for streaming information:
        DESCRIPTION: * Live OR VOD
        DESCRIPTION: * Asset Name
        DESCRIPTION: * Stream URL
        DESCRIPTION: * viewer ID
        EXPECTED: The value of the parameter is written in the 'Content information' section in  the format:
        EXPECTED: * isLive: true
        EXPECTED: * Asset name:[10262603] 07:55 Doncaster
        EXPECTED: * streamUrl: https://110821-lh.akamaihd.net/i/ruk95hls_0@336128/master.m3u8
        EXPECTED: ![](index.php?/attachments/get/112060496)
        EXPECTED: * viewer ID: username
        """
        pass

    def test_009_verify_that_value_for_device_information_of_experience_insights_custom_metadata_is_written_in_a_correct_format_for_connection_type_channel_type_application_version_build(self):
        """
        DESCRIPTION: Verify that value for Device information of Experience Insights Custom Metadata is written in a correct format for:
        DESCRIPTION: * Connection Type
        DESCRIPTION: * Channel Type
        DESCRIPTION: * Application Version Build
        EXPECTED: The value of the parameter is written in the format:
        EXPECTED: * Channel_Type:	Desktop
        EXPECTED: * Connection_Type: 'slow-2g', '2g', '3g', or '4g' (which represents current connection quality)
        EXPECTED: * App_Type_Version: 103.0.0
        EXPECTED: ![](index.php?/attachments/get/112060501)
        """
        pass

    def test_010_verify_that_value_for_asset_information_of_experience_insights_custom_metadata_is_written_in_a_correct_format_for_sport_type_league_type_event_streamed(self):
        """
        DESCRIPTION: Verify that value for Asset information of Experience Insights Custom Metadata is written in a correct format for:
        DESCRIPTION: * Sport Type
        DESCRIPTION: * League Type
        DESCRIPTION: * Event Streamed
        EXPECTED: The value of the parameter is written in the format:
        EXPECTED: * Sport_Type: Football
        EXPECTED: * League_Type: UEFA Champions League
        EXPECTED: * Event_Streamed: Olympique Lyonnais Srl v Fc Bayern Munich Srl
        EXPECTED: ![](index.php?/attachments/get/112060631)
        """
        pass

    def test_011_verify_that_value_for_business_information_of_experience_insights_custom_metadata_is_written_in_a_correct_format_for_brand_page_url_stream_provider(self):
        """
        DESCRIPTION: Verify that value for Business information of Experience Insights Custom Metadata is written in a correct format for:
        DESCRIPTION: * Brand
        DESCRIPTION: * Page URL
        DESCRIPTION: * Stream Provider
        EXPECTED: The value of the parameter is written in the format:
        EXPECTED: * Brand: Coral
        EXPECTED: * Page_URL: https://environment/event/sport/event
        EXPECTED: * Stream_Provider: Perform
        EXPECTED: ![](index.php?/attachments/get/112060633)
        """
        pass
