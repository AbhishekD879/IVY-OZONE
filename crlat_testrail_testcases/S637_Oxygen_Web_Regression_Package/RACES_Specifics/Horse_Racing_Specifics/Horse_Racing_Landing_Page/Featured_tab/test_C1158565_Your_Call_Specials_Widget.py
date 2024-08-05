import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C1158565_Your_Call_Specials_Widget(Common):
    """
    TR_ID: C1158565
    NAME: Your Call Specials Widget
    DESCRIPTION: This test case verifies the display of the Your Call Specials Widget on Horse Racing Landing Page (Featured tab)
    DESCRIPTION: AUTOTEST: [C1641546]
    PRECONDITIONS: Oxygen application is loaded and Horse Racing Your Call Specials selections available
    PRECONDITIONS: Horse Racing Your Call Specials selections should be configured in TI (https://backoffice-tst2.coral.co.uk/ti/).
    PRECONDITIONS: To retrieve all events with markets and selections for Horse Racing Your Call Specials type:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/TTTT
    PRECONDITIONS: Where:
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: TTTT - Your Call Specials type id (on TST2 = 15031)
    PRECONDITIONS: or
    PRECONDITIONS: Create selections if necessary:
    PRECONDITIONS: on **TST2**: Under the category Horse Racing (category id = 21) select Daily Racing Specials class (id = 227), then select Your Call Specials Type (id = 15031).
    PRECONDITIONS: The widget displays selections of event from the market with name "Featured" without any extra characters
    """
    keep_browser_open = True

    def test_001_navigate_to_horse_racingfeatured_tabscroll_if_necessary_until_yourcall_specials_widget_is_visible(self):
        """
        DESCRIPTION: Navigate to Horse Racing/Featured tab.
        DESCRIPTION: Scroll if necessary until YourCall Specials widget is visible.
        EXPECTED: - When the page is loaded, Your Call Specials Widget is displayed
        EXPECTED: - YourCall Specials widget accordion is expanded by default
        EXPECTED: - On Dektop browsers (starting from 1280px) YourCall Specials widget is displayed in the service column (on the right)
        """
        pass

    def test_002_verifiy_the_widget_accordion_header(self):
        """
        DESCRIPTION: Verifiy the widget accordion header
        EXPECTED: - YourCall Specials accordion contains "2B" yellow icon (on Desktop) and is named "YOURCALL SPECIALS" on Desktop and Mobile
        """
        pass

    def test_003_verifiy_the_widget_accordion_content(self):
        """
        DESCRIPTION: Verifiy the widget accordion content
        EXPECTED: - Up to top 3 selections from Featured market of type Your Call Specials are displayed within the widget;
        EXPECTED: - Selections are ordered by **displayOrder** parameter for outcomes in EventToOutcomeForType response. The lower the value, the higher the position. In case a few outcomes have the same parameter value, the order should be as it is in the response.
        EXPECTED: - The name of each selection begins with "#Yourcall" hashtag
        EXPECTED: - Correct price from EventToOutcomeForType response is displayed for each selection
        """
        pass

    def test_004_collapseexpand_the_widget(self):
        """
        DESCRIPTION: Collapse/expand the widget
        EXPECTED: On mobile and tablet:
        EXPECTED: - Widget is collapsed -  "+" sign is shown
        EXPECTED: - Widget is expanded - "-" sign is shown
        EXPECTED: On Desktop:
        EXPECTED: - Collapsed/ expanded chevron is shown
        """
        pass

    def test_005_verify_view_all_yourcall_specials_link_at_the_bottom(self):
        """
        DESCRIPTION: Verify View all YourCall Specials link at the bottom
        EXPECTED: - "VIEW ALL #YOURCALL SPECIALS" text at the bottom of the widget on Desktop
        EXPECTED: - Underlined "VIEW ALL #YOURCALL SPECIALS" text at the bottom of the widget on Mobile
        """
        pass

    def test_006_click_on_view_all_yourcall_specials_link_at_the_bottom_of_the_widget(self):
        """
        DESCRIPTION: Click on View all YourCall Specials link at the bottom of the widget
        EXPECTED: YOURCALL tab in Horse racing is opened
        """
        pass

    def test_007_verify_yourcall_specials_widget_content_if_there_are_no_yourcall_specials_selections_from_featured_market_available(self):
        """
        DESCRIPTION: Verify YourCall Specials widget content if there are no YourCall Specials selections from Featured market available
        EXPECTED: YourCall Specials widget is NOT displated
        """
        pass
