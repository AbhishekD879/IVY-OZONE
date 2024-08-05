import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C29461_Verify_number_of_DOM_Elements_rendered_on_the_Home_page(Common):
    """
    TR_ID: C29461
    NAME: Verify number of DOM Elements rendered on the Home page
    DESCRIPTION: This test case verifies number of DOM Elements rendered on the Home page
    DESCRIPTION: JIRA TICKETS:
    DESCRIPTION: BMA-9772: As a TA I want to reduce the number of DOM elements rendered on the Home page
    PRECONDITIONS: Type in Firebug's console for checking the number of DOM elements on whole page:
    PRECONDITIONS: document.getElementsByTagName('*').length
    PRECONDITIONS: Use $('.header *').length for elements with class when checking the number of DOM elements for certain part of the page (for example: header).
    PRECONDITIONS: Use $('#header *').length for elements with id when checking number of DOM elements for certain part of the page (for example: header).
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_open_dev_tools_and_enterdocumentgetelementsbytagnamelength_in_console_and_verify_number_of_dom_elements_for_whole_page(self):
        """
        DESCRIPTION: Open Dev Tools and enter **document.getElementsByTagName('*').length **in Console and verify number of DOM elements for whole page
        EXPECTED: Number of DOM elements for whole Homepage is diplayed in Console
        """
        pass

    def test_003_verify_type_class_or_idof_certain_element_for_example_header_in_dev_tools__elements(self):
        """
        DESCRIPTION: Verify type (class or id) of certain element (for example: header) in Dev Tools ->Elements
        EXPECTED: For example: class="header" or id="header"
        """
        pass

    def test_004_enterheader_lengthfor_elements_with_id_type_in_console_and_verify_number_of_dom_elements_for_the_certain_part_of_page_for_example_header(self):
        """
        DESCRIPTION: Enter **$('#header *').length** for elements with **id** type in Console and verify number of DOM elements for the certain part of page (for example header)
        EXPECTED: Number of DOM elements for Header is diplayed in Console
        """
        pass

    def test_005_enterheader_lengthfor_elements_with_class_type_in_consoleand_verify_number_of_dom_elements_for_the_certain_part_of_page_for_example_header(self):
        """
        DESCRIPTION: Enter **$('.header *').length** for elements with **class** type in Console and verify number of DOM elements for the certain part of page (for example header)
        EXPECTED: Number of DOM elements for Header is diplayed in Console
        """
        pass

    def test_006_repeat_step_4_or_5_according_with_type_of_element_and_verify_number_of_dom_elements_on_mobile_portrait_and_landscape_mode(self):
        """
        DESCRIPTION: Repeat step 4 or 5 according with type of element and verify number of DOM elements on Mobile (Portrait and Landscape mode)
        EXPECTED: Number of DOM elements for Header is diplayed in Console
        """
        pass

    def test_007_repeat_step_4_or_5_according_with_type_of_element_and_verify_number_of_dom_elements_on_tablet_portrait_and_landscape_mode(self):
        """
        DESCRIPTION: Repeat step 4 or 5 according with type of element and verify number of DOM elements on Tablet (Portrait and Landscape mode)
        EXPECTED: Number of DOM elements for Header is diplayed in Console
        """
        pass
