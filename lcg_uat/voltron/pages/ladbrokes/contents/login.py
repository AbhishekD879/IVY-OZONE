from voltron.pages.shared.contents.base_content import ComponentContent


class Login(ComponentContent):
    """
    Login form on account one portal
    """
    _url_pattern = r'^http[s]?:\/\/.+\/login'
