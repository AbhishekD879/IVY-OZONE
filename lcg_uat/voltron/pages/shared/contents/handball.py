from voltron.pages.shared.contents.football import SportPage, SportPageDesktop


class Handball(SportPage):
    _url_pattern = r'^https?:\/\/.+\/handball(\/)?(live|matches|coupons|competitions|outrights)?(\/)?(today|tomorrow|future)?'


class HandballDesktop(SportPageDesktop):
    _url_pattern = r'^https?:\/\/.+\/handball(\/)?(live|matches|coupons|competitions|outrights)?(\/)?(today|tomorrow|future)?'
