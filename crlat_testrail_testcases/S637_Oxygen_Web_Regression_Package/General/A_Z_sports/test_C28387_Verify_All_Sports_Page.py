import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C28387_Verify_All_Sports_Page(Common):
    """
    TR_ID: C28387
    NAME: Verify All Sports Page
    DESCRIPTION: This test case verifies functionality of 'A-Z' page which can be opened via footer menu and via pressing the button 'A - Z' on the Sport menu ribbon
    DESCRIPTION: AUTOTEST: [C2610737]
    PRECONDITIONS: 1. Sports are configured in CMS: Sports Pages > Sport Categories
    PRECONDITIONS: 2. 'Top Sports' are configured in CMS for some Sports
    PRECONDITIONS: (Sports Pages > Sport Categories > <Sport> 'Is Top Sport' check box is checked)
    PRECONDITIONS: 3. 'A-Z Sports' is configured in CMS for some Sports
    PRECONDITIONS: (Sports Pages > Sport Categories > <Sport> 'Show in AZ' check box is checked)
    PRECONDITIONS: 4. Oxygen application is loaded
    """
    keep_browser_open = True

    def test_001_open_all_sports_page(self):
        """
        DESCRIPTION: Open 'All Sports' page
        EXPECTED: *  'All Sports' page is opened
        EXPECTED: *  The following sections are present: Top Sports, A-Z
        """
        pass

    def test_002_verify_page_header_and_back_button(self):
        """
        DESCRIPTION: Verify page header and Back button
        EXPECTED: *   Page header is 'All Sports'
        EXPECTED: *   Tap on Back button gets user back to previous page
        """
        pass

    def test_003_verify_top_sports_section(self):
        """
        DESCRIPTION: Verify 'Top Sports' section
        EXPECTED: *  Section is displayed only if Top Sports are configured in CMS
        EXPECTED: *  Sports are displayed in a list view
        EXPECTED: *  No icon is displayed next to a Sport name
        EXPECTED: *  Only Sports with the CMS setting 'is Top Sport?' are shown in this section
        """
        pass

    def test_004_tap_on_any_sport_from_top_sports_section(self):
        """
        DESCRIPTION: Tap on any sport from 'Top Sports' section
        EXPECTED: Corresponding Sport Landing page is opened
        """
        pass

    def test_005_verify_top_sports_ordering(self):
        """
        DESCRIPTION: Verify 'Top Sports' ordering
        EXPECTED: Top Sports are ordered like configured in CMS (configurations made by dragging)
        """
        pass

    def test_006_verify_a_z_section(self):
        """
        DESCRIPTION: Verify 'A-Z' section
        EXPECTED: *  Title is 'A-Z'
        EXPECTED: *  Sports are displayed in a list view
        EXPECTED: *  There are Sport name and icon
        EXPECTED: *  Only Sports with the CMS setting 'Show in A-Z' are shown in this section
        """
        pass

    def test_007_verify_sports_ordering(self):
        """
        DESCRIPTION: Verify sports ordering
        EXPECTED: All sports are shown in alphabetical A-Z order
        """
        pass

    def test_008_tap_any_sport_item(self):
        """
        DESCRIPTION: Tap any sport item
        EXPECTED: Sport Landing page is opened
        """
        pass
