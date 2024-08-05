from collections import defaultdict
from collections import namedtuple
from datetime import datetime

import pytz
from dateutil.parser import parse
from tzlocal import get_localzone

from tests.Common import Common


class BaseOffersTest(Common):

    def get_available_cms_modules_and_offers(self, device: str = 'desktop') -> namedtuple:
        """
        Method used to get available CMS offers and modules
        :param device: Specifies device type to get offers - tablet/desktop
        :return: namedtuple with CMS module names and offer's parameters that should be available on UI
        """
        all_cms_offer_modules = self.cms_config.get_offer_modules()
        available_offer_module_ids = [offer_module.get('id') for offer_module in all_cms_offer_modules
                                      if not offer_module.get('disabled')]

        all_cms_offers = self.cms_config.get_offers()
        timezone = str(get_localzone())
        self._logger.debug(f'*** Current timezone is: "{timezone}"')
        now = datetime.now(pytz.timezone(timezone))

        available_offers_by_modules = defaultdict(list)
        for offer in all_cms_offers:
            module_id = offer.get('module')
            if module_id in available_offer_module_ids:
                if all((now >= parse(offer.get('displayFrom')),
                        now <= parse(offer.get('displayTo')),
                        offer.get('showOfferOn') in ['both', device],
                        offer.get('showOfferTo') in ['both', 'new'],
                        not offer.get('disabled')
                        )):
                    available_offers_by_modules[module_id].append(offer)
        self._logger.debug(f'*** Found {len(available_offers_by_modules)} available offers')
        available_offers = []
        for offer_id, offers in available_offers_by_modules.items():
            for offer_item in offers:
                if len([offer_ for offer_ in available_offers if offer_id == offer_.get('module')]) < 3:
                    # ˆ Maximum 3 offers images can be presented inside one Offer Module
                    available_offers.append(offer_item)
        available_modules = []
        for offer in available_offers:
            if offer.get('moduleName') not in available_modules:
                available_modules.append(offer.get('moduleName'))

        # For returning correct order of offers, as in CMS
        sorted_modules = {}
        for module in available_modules:
            for _ in all_cms_offer_modules:
                if module == _['name']:
                    sorted_modules[module] = _['sortOrder']
        available_modules = sorted(available_modules, key=lambda item: sorted_modules[item])

        CmsParams = namedtuple('cms_offers_and_modules', ['available_modules', 'available_offers'])
        cms_offers_and_modules = CmsParams(available_modules, available_offers)
        self._logger.debug(f'*** Found {cms_offers_and_modules} available offers')
        return cms_offers_and_modules
