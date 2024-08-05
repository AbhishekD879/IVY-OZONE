import { Injectable } from '@angular/core';
import { VanillaFreebetsBadgeDynamicLoaderService as AppVanillaFreebetsBadgeDynamicLoaderService
} from '@app/vanillaInit/services/vanillaFreeBets/vanilla-fb-badges-loader.service';
import { MenuCountersService, MenuSection } from '@frontend/vanilla/core';
import { FreeBetsBadgeService } from '@app/vanillaInit/services/vanillaFreeBets/vanilla-freebets-badge.service';
import { IFreeBetsBadgeModel } from '@app/vanillaInit/models/free-bets.interface';
import { CmsService } from '@app/core/services/cms/cms.service';

@Injectable({
    providedIn: 'root'
})
export class VanillaFreebetsBadgeDynamicLoaderService extends AppVanillaFreebetsBadgeDynamicLoaderService {
  private headerPromoBadge: IFreeBetsBadgeModel = {
    section: MenuSection.Header,
    item: 'promo',
    count: null
  };
  private readonly badgeCount: string = 'FB';

  constructor(menuCountersService: MenuCountersService,
              freebetsBadgeService: FreeBetsBadgeService,cmsService:CmsService) {
    super(menuCountersService, freebetsBadgeService,cmsService);
  }

  /**
   * Check if fbStatus equal false set null to headerBadge.count and execute addCounter method
   * @param fbStatus
   */
  updateBadge(fbStatus: boolean): void {
    this.headerPromoBadge.count = fbStatus ? this.badgeCount : null;
    this.addCounter(this.headerPromoBadge);
    super.updateBadge(fbStatus);
  }
}
