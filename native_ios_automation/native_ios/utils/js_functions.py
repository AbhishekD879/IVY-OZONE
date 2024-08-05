import os

from native_ios.pages.shared import get_driver
from native_ios.utils.exceptions.general_exception import GeneralException


def get_js_function(function_name):
    try:
        with open(os.path.join(os.path.join(os.path.split(__file__)[0]), 'js_tools', f'{function_name}.js')) as js_file:
            return js_file.read()
    except Exception as e:
        raise GeneralException(f'Error calling "{function_name}" function. {e}')


def set_date_picker(*args, **kwargs):
    driver = get_driver()
    set_date = get_js_function('date_picker_set_date')
    return driver.execute_script(set_date, *args)


def remove_readonly(*args, **kwargs):
    driver = get_driver()
    remove_readonly_attr = get_js_function('remove_readonly_attr')
    return driver.execute_script(remove_readonly_attr, *args)


def set_quick_bet_value(*args, **kwargs):
    driver = get_driver()
    set_value = get_js_function('set_quick_bet_value')
    return driver.execute_script(set_value, *args)


def set_betslip_value(*args, **kwargs):
    driver = get_driver()
    set_value = get_js_function('set_betslip_value')
    return driver.execute_script(set_value, *args)


def set_betslip_complex_stake_value(*args, **kwargs):
    driver = get_driver()
    set_value = get_js_function('set_betslip_complex_stake_value')
    return driver.execute_script(set_value, *args)


def get_value(*args, **kwargs):
    driver = get_driver()
    get_value = get_js_function('get_value')
    return driver.execute_script(get_value, *args)


def set_value(*args, **kwargs):
    driver = get_driver()
    set_value = get_js_function('set_value')
    return driver.execute_script(set_value, *args)


def get_css_property_text(*args):
    driver = get_driver()
    css_prop_text = get_js_function('get_css_property_text')
    return driver.execute_script(css_prop_text, *args)


def click(*args, **kwargs):
    driver = get_driver()
    js_click = get_js_function('click')
    return driver.execute_script(js_click, *args)


def mouse_event_click(*args, **kwargs):
    driver = get_driver()
    mouse_click = get_js_function('mouse_event_click')
    return driver.execute_script(mouse_click, *args)


def get_text_excluding_child_nodes_text(*args, **kwargs):
    driver = get_driver()
    get_text = get_js_function('get_text_excluding_child_nodes_text')
    return driver.execute_script(get_text, *args, **kwargs)


def set_viewport_size(*args, **kwargs):
    driver = get_driver()
    get_text = get_js_function('set_viewport_size')
    return driver.execute_script(get_text, *args, **kwargs)


def get_data_layer(*args, **kwargs):
    driver = get_driver()
    get_text = get_js_function('get_data_layer')
    return driver.execute_script(get_text, *args, **kwargs)


def scroll_into_view_above(*args):
    """ use when scroll_to_we() does not help and element is obstructed by elements like sticky desktop header """
    driver = get_driver()
    scroll_up = get_js_function('scroll_into_view_above')
    return driver.execute_script(scroll_up, *args)


def get_location(*args):
    driver = get_driver()
    get_location_ = get_js_function('get_location')
    return driver.execute_script(get_location_, *args)


def natural_mouse_click(*args, **kwargs):
    """
    Simulating natural mouse click
    source of inspiration: https://stackoverflow.com/q/24025165/3574726
    """
    driver = get_driver()
    natural_mouse_click_ = get_js_function('natural_mouse_click')
    return driver.execute_script(natural_mouse_click_, *args, **kwargs)


def scroll_to_center_of_element(*args, **kwargs):
    """ Scrolls to the center of the element"""
    driver = get_driver()
    scroll_up = get_js_function('scroll_to_center_of_element')
    return driver.execute_script(scroll_up, *args, **kwargs)


def get_document_ready_state(*args, **kwargs):
    """ Return of document.readyState """
    driver = get_driver()
    doc_ready = get_js_function('document_ready_state')
    return driver.execute_script(doc_ready, *args, **kwargs)


def get_shadow_root(*args, **kwargs):
    """ Return of shadowRoot """
    driver = get_driver()
    shadow_root = get_js_function('get_shadow_root')
    return driver.execute_script(shadow_root, *args, **kwargs)
