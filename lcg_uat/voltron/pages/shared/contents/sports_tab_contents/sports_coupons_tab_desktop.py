from voltron.pages.shared.contents.sports_tab_contents.sport_coupons_tab \
    import CouponsTabContent, CouponsCategories, SportsCouponsAccordionsList, CouponItem


class CouponItemDesktop(CouponItem):
    _name = 'xpath=.//*[@data-crlat="couponName"]'


class SportsCouponsAccordionsListDesktop(SportsCouponsAccordionsList):
    _item = 'xpath=.//*[@data-crlat="couponItem"]'
    _list_item_type = CouponItemDesktop


class CouponsCategoriesDesktop(CouponsCategories):
    _item = 'xpath=.//*[@data-crlat="couponContainer"]'
    _list_item_type = SportsCouponsAccordionsListDesktop


class CouponsTabContentDesktop(CouponsTabContent):
    _accordions_list_type = CouponsCategoriesDesktop
