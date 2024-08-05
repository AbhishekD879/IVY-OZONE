import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import { StorageService } from '../storage/storage.service';
import { IItemDateModel } from './item-date.model';
import { IVipItemModel } from './vip-item.model';
import { IOffer } from '../cms/models/offer/offer.model';

// ===== New User/Existing & VIP User Rules ====//
// New User & VIP Level blank = Show ONLY to new customer (no cookie set)
// Existing User & VIP Level blank = Show to all existing customers only
// Existing User & VIP Level populated = show to existing users with specified VIP Level only
// Both & VIP Level blank = Show to all users
// Both & VIP Level populated = Show to new customers & existing users with specified VIP Level ONLY

@Injectable()
export class ExistNewUserService {

  constructor(
    private storage: StorageService
  ) {}

  /**
   * Get filtered item for exist/new/vip User
   * @param {array} items
   * @param {boolean} isDateChecking - tells if to check date fit
   * @returns {*}
   */
  filterExistNewUserItems<T>(items: T[] | IOffer[], isDateChecking: boolean = true): T[] {
    return _.filter((items as any[]), (item: IVipItemModel) => {
      const fitTimePeriod = isDateChecking ? this.checkDate(item) : true, // =============> Fit in Time Period
        vipLevel = Number(this.storage.get('vipLevel')), // ==================> User Vip Level
        existingUser = this.storage.get('existingUser'), // ==================> Existing User
        hasVipLevel = (item.vipLevels && item.vipLevels.length > 0) && _.contains(item.vipLevels, vipLevel), // => User has Vip Level
        noVipLevel = item.vipLevels && !item.vipLevels.length, // ============================================> User has no Vip Level
        showToNewUser = !existingUser && _.contains(item.showToCustomer, 'new'), // ========> Show for New User
        showToExistingUser = existingUser && _.contains(item.showToCustomer, 'existing'), // => Show for Existing User
        showToAllUser = item.showToCustomer && item.showToCustomer.length === 2, // ===============================> Show for All Users
        showToNewVipUser = !existingUser && showToAllUser && item.vipLevels.length > 0; // => Show for New Vip User
      return (fitTimePeriod && (showToNewVipUser || hasVipLevel || noVipLevel) &&
        (showToNewUser || showToExistingUser || showToAllUser));
    });
  }

  /**
   * Check if date fits
   * @param {Object} item
   * @returns {boolean}
   */
  private checkDate(item: IItemDateModel): boolean {
    const currentTime = Date.now();
    const startTime = item.displayFrom ? Date.parse(item.displayFrom) : Date.parse(item.validityPeriodStart);
    const endTime = item.displayFrom ? Date.parse(item.displayTo) : Date.parse(item.validityPeriodEnd);
    return startTime <= currentTime && endTime >= currentTime;
  }

}
