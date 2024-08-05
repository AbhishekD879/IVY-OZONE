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
class Test_C28461_Verify_Event_Data_on_Coupon_page(Common):
    """
    TR_ID: C28461
    NAME: Verify Event Data on Coupon page
    DESCRIPTION: This test case verifies event data
    PRECONDITIONS: 1. In order to get a list with **Coupon IDs **use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Coupon/
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: 2. For each Coupon retrieve a list of **Events and Outcomes**
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/XX.XX/CouponToOutcomeForCoupon/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - **Coupon **ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **NOTE**: Sport icon is CMS configurable - https://CMS\_ENDPOINT/keystone/sport-categories (check CMS\_ENDPOINT via *devlog *function)
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_for_mobiletabletnavigate_to_sport_landing_page_from_the_sports_menu_ribbonfor_desktopnavigate_to_sport_landing_page_from_the_left_navigation_menu(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Navigate to 'Sport' Landing page from the Sports Menu Ribbon
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to 'Sport' Landing page from the 'Left Navigation' menu
        EXPECTED: **Desktop**:
        EXPECTED: *  <Sport> Landing Page is opened
        EXPECTED: * 'Matches'->'Today' sub tab is opened by default
        EXPECTED: **Mobile**:
        EXPECTED: *  <Sport> Landing Page is opened
        EXPECTED: * 'Matches' tab is opened by default
        """
        pass

    def test_003_clicktap_couponsaccas_tab(self):
        """
        DESCRIPTION: Click/Tap 'Coupons'/ACCAS tab
        EXPECTED: 'Coupons'/ACCAS tab is opened
        """
        pass

    def test_004_go_to_event_section(self):
        """
        DESCRIPTION: Go to Event section
        EXPECTED: 
        """
        pass

    def test_005_verify_event_name(self):
        """
        DESCRIPTION: Verify Event name
        EXPECTED: *   Event name corresponds to '**name**' attribute
        EXPECTED: *   Event name is displayed in format: '<Team1/Player1>** v/vs** <Team2/Player2>'
        """
        pass

    def test_006_verify_event_start_time(self):
        """
        DESCRIPTION: Verify Event Start time
        EXPECTED: *   Event start time corresponds to **startTime** attribute
        EXPECTED: *   Event Start Time is shown below event name ( **CORAL** ) / above event name ( **LADBROKES** )
        EXPECTED: *   For events that occur **Today** date format is 24 hours: for **Coral**: **HH:MM, Today** (e.g. "14:00 or 05:00, Today"), for **Ladbrokes**: **HH:MM Today** (e.g. "14:00 or 05:00 Today")
        EXPECTED: *   For events that occur in the **Future** (including tomorrow) date format is 24 hours: for **Coral**: **HH:MM, DD MMM** (e.g. 14:00 or 05:00, 24 Nov or 02 Nov), for **Ladbrokes**: **HH:MM DD MMM** (e.g. 14:00 or 05:00 24 Nov or 02 Nov)
        """
        pass

    def test_007_clicktapanywhere_on_event_section_except_priceodds_button(self):
        """
        DESCRIPTION: Click/Tap anywhere on Event section (except 'Price/Odds' button)
        EXPECTED: Event Details Page is opened
        """
        pass
