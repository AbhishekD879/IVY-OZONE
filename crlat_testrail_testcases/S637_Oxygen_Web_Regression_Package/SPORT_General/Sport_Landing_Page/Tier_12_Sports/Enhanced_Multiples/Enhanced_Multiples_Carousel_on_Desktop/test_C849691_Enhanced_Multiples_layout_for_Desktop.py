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
class Test_C849691_Enhanced_Multiples_layout_for_Desktop(Common):
    """
    TR_ID: C849691
    NAME: Enhanced Multiples layout for Desktop
    DESCRIPTION: This test case verifies Enhanced Multiples layout for Desktop.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: 1. Oxygen app is loaded
    PRECONDITIONS: 2. Make sure you have  Enhanced Multiples events on some sports (Sports events with typeName="Enhanced Multiples")
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1. Enhanced Multiples are not available for Lotto and Virtuals.
    PRECONDITIONS: 2. Enhanced Multiples layout remains unchanged for tablet and mobile (EM events are displayed in accordions).
    PRECONDITIONS: 3. For each Class retrieve a list of **Event **IDs
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/XXX?simpleFilter=market.dispSortName:equals:ZZ&simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: XXX - is a comma-separated list of **Class **ID's;
    PRECONDITIONS: XX - sports **Category **ID
    PRECONDITIONS: X.XX - current supported version of the OpenBet release
    PRECONDITIONS: ZZ - dispSortName specific value for each Sport, shows the primary marker (e.g. Football - MR, Tennis - HH).
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_navigate_to_sports_landing_page_where_enhanced_multiples_events_are_present(self):
        """
        DESCRIPTION: Navigate to Sports Landing page where Enhanced Multiples events are present
        EXPECTED: •  &lt;Sports&gt; Landing Page is opened
        EXPECTED: • Event cards are displayed within 'Enhanced Multiples' carousel on the whole width of the section
        """
        pass

    def test_002_verify_enhanced_multiples_events(self):
        """
        DESCRIPTION: Verify 'Enhanced Multiples' events
        EXPECTED: • 'Enhanced Multiples' events are displayed in carousel below banner area
        EXPECTED: • Each event card in carousel contains label 'Enhanced' in the top left corner
        """
        pass

    def test_003_navigate_to_any_ltsportsgt_page_where_only_one_enhanced_multiples_event_is_present(self):
        """
        DESCRIPTION: Navigate to any &lt;Sports&gt; page where only one Enhanced Multiples event is present
        EXPECTED: •  &lt;Sports&gt; Landing Page is opened
        EXPECTED: • Only one card is displayed within 'Enhanced Multiples' carousel on the whole width of the section
        """
        pass

    def test_004_navigate_to_any_ltsportsgt_page_where_enhanced_multiples_events_are_not_present(self):
        """
        DESCRIPTION: Navigate to any &lt;Sports&gt; page where Enhanced Multiples events are NOT present
        EXPECTED: •  &lt;Sports&gt; Landing Page is opened
        EXPECTED: • 'Enhanced Multiples' carousel is NOT displayed
        """
        pass

    def test_005_repeat_steps_2_4_on_ltsportsgt_event_details_page_but_only_for_pre_match_events(self):
        """
        DESCRIPTION: Repeat steps 2-4 on &lt;Sports&gt; Event Details Page but only for Pre-match events
        EXPECTED: •  &lt;Sports&gt; Event Details Page is opened
        EXPECTED: • 'Enhanced Multiples' events are displayed within carousel below Stats (if applicable) or 'Breadcrumbs' trail
        """
        pass

    def test_006_navigate_to_ltsportsgt_event_details_page_but_for_live_events(self):
        """
        DESCRIPTION: Navigate to &lt;Sports&gt; Event Details Page but for LIVE events
        EXPECTED: •  &lt;Sports&gt; Event Details Page is opened
        EXPECTED: • 'Enhanced Multiples' carousel is NOT displayed
        """
        pass

    def test_007_repeat_steps_2_4_on_homepage(self):
        """
        DESCRIPTION: Repeat steps 2-4 on Homepage
        EXPECTED: 
        """
        pass
