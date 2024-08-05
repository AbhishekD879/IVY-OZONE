import { Injectable } from '@angular/core';
import { MenuCountersService, MenuSection } from '@frontend/vanilla/core';
import { FreeBetsBadgeService } from './vanilla-freebets-badge.service';

import { IFreeBetsBadgeModel } from '@vanillaInitModule/models/free-bets.interface';
import { IFreebetToken } from '@bpp/services/bppProviders/bpp-providers.model';
import { IFreeBetState } from '@core/services/freeBets/free-bets.model';
import { CmsService } from '@app/core/services/cms/cms.service';
import { ISystemConfig } from '@app/core/services/cms/models';

const badgeCount: string = 'FB';
@Injectable({
    providedIn: 'root'
})
export class VanillaFreebetsBadgeDynamicLoaderService {
    headerBadge: IFreeBetsBadgeModel = {
        section: MenuSection.Header,
        item: 'avatar',
        count: null
    };

    menuOffersBadge: IFreeBetsBadgeModel = {
        section: MenuSection.Menu,
        item: 'offers',
        count: null
    };

    menuSportBadge: IFreeBetsBadgeModel = {
        section: MenuSection.Menu,
        item: 'sportsfreebets',
        count: null
    };
    menuOddsBoostBadge: IFreeBetsBadgeModel = {
        section: MenuSection.Menu,
        item: 'oddsboost',
        count: null
    };
    menuBetBundleBadge: IFreeBetsBadgeModel = {
        section: MenuSection.Menu,
        item: 'betbundles',
        count: null
    };

    headerAvatar:   {[name: string]: any};

    constructor(private menuCountersService: MenuCountersService,
        private freebetsBadgeService: FreeBetsBadgeService,
        private cmsService: CmsService
    ) {
      this.setAvatar();
    }

    setAvatar(): void {
        this.cmsService.getSystemConfig().subscribe((config: ISystemConfig) => {
            if (config && config.isAvatarBalance && config.isAvatarBalance.enabled) {
                this.headerBadge.item = 'avatarbalance';
                this.headerAvatar = config.isAvatarBalance;
            }
        });
    }

    /**
     * add badge and counter to vanilla element
     * @param item
     */
    addCounter(item: IFreeBetsBadgeModel): void {
        this.freebetsBadgeService.freeBetCounters.push(item);
    }

    /**
     * count freebets
     * @param freebetArr
     */

    sportsFreebetsCount(freebetArr: IFreebetToken[]): number | string {
        const count = [];
        freebetArr.forEach((element: IFreebetToken) => {
            if (element.freebetTokenType === 'SPORTS') {
                count.push(element);
            }
        });
        return count.length;
    }
    /**
     * update all counters and badge
     */
    update(): void {
        this.menuCountersService.update();
    }
    /**
     * set value to menuSportBadge.count and menuOddsBoostBadge.count and execute updateBadge, updateCounter, update methods
     * @param freeBetsState
     * @param oddsboostCounter
     */
    addBadgesToVanillaElements(freeBetsState: IFreeBetState): void {
        this.menuSportBadge.count = this.sportsFreebetsCount(freeBetsState.freeBetFanzoneData);
        const bettokens = this.sportsFreebetsCount(freeBetsState.betTokens);
        this.updateBadge(!!bettokens || !!this.menuSportBadge.count);
        this.updateCounter(this.menuSportBadge);
    }
    addBetpackCounter(freeBetsState: IFreeBetState) {
        this.menuBetBundleBadge.count = freeBetsState.betTokens?.length;
        this.updateCounter(this.menuBetBundleBadge);
    }
    addOddsBoostCounter(oddsboostArr: IFreebetToken[]) {
        this.menuOddsBoostBadge.count = oddsboostArr.length;
        this.updateCounter(this.menuOddsBoostBadge);
    }
    /**
     * Check if fbStatus equal false set null to headerBadge.count and menuOffersBadge.count  and execute addCounter method
     * badgeType "icon" + giftCssClass would display Gift box on User Avatar. If we want to display FB icon set badgeType to "counter" and remove giftCssClass from CSS
     * https://vie.git.bwinparty.com/vanilla/vanilla/-/wikis/features/menu-item-badge
     * @param fbStatus
     */
    updateBadge(fbStatus: boolean): void {
        this.headerBadge.count = fbStatus ? this.headerAvatar?.badgeValue : null;
        this.headerBadge.cssClass = fbStatus ? this.headerAvatar?.giftCssClass : null;
        this.headerBadge.type = fbStatus ? this.headerAvatar?.badgeType : null;
        this.menuOffersBadge.count = fbStatus ? badgeCount : null;
        this.addCounter(this.headerBadge);
        this.addCounter(this.menuOffersBadge);
        this.update();
    }

    /**
     * Check if item.count equal zero then set null to item.count and execute addCounter method
     * @param item
     */
    updateCounter(item: IFreeBetsBadgeModel): void {
        item.count = item.count || null;
        this.addCounter(item);
        this.update();
    }
}
