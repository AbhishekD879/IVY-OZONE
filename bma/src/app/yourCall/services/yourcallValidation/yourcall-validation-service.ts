import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { YourCallDashboardItem } from '@yourcall/models/yourcallDashboardItem/yourcall-dashboard-item';
import { IYourcallSelection } from '@yourcall/models/selection.model';
import { IYourCallMarket } from '@core/services/cms/models';

@Injectable({ providedIn: 'root' })
export class YourcallValidationService {
  ERRORS: { [key: string]: string } = {
    samePlayerSameStatistic: 'samePlayerSameStatistic',
    sameGameStatistic: 'sameGameStatistic'
  };

  dashboard: YourCallDashboardItem[];

  /**
   * Validate minimum selection amount and combination:
   * - if single selection is selected - valid would be only from "Player Bets" market,
   * - if more than 2 selections are selected - all possible combinations are valid.
   * @returns {boolean}
   */
  isValidSelectionCount(): boolean {
    if (!this.dashboard.length) {
      return false;
    }

    const isPlayerBetsMarket = _.filter(this.dashboard, (item: YourCallDashboardItem) => {
      return !!item && (item.market as IYourCallMarket).grouping === 'Player Bets';
    });

    if (isPlayerBetsMarket.length === 1 || this.dashboard.length >= 2) {
      return true;
    }

    return false;
  }

  /**
   * Validate single selection
   * @param selection
   * @returns {boolean}
   */
  validateSelection(selection: IYourcallSelection): boolean {
    let isValid = true;
    _.each(this.dashboard, (item: YourCallDashboardItem) => {
      if (item.selection !== selection) {
        isValid = this.validatePlayerStatistic(item.selection, selection) && isValid;
        isValid = this.validateGameStatistic(item.selection, selection) && isValid;
      }
    });
    return isValid;
  }

  /**
   * Validate whole dashboard
   * @returns {boolean}
   */
  validate(): boolean {
    let valid = true;
    _.each(this.dashboard, (item: YourCallDashboardItem) => {
      delete item.selection.error;
      delete item.selection.errorMessage;
    });
    _.each(this.dashboard, (item: YourCallDashboardItem) => {
      valid = this.validateSelection(item.selection) && valid;
    });
    return valid;
  }

  /**
   * Check if dashboard already has selection with same player and statistic
   * @param compared
   * @param selection
   * @returns {boolean}
   * @private
   */
  private validatePlayerStatistic(compared: IYourcallSelection, selection: IYourcallSelection): boolean {
    if (selection.playerId) {
      if (selection.playerId === compared.playerId && selection.statisticId === compared.statisticId) {
        compared.error = selection.error = true;
        selection.errorMessage = selection.errorMessage || [];
        selection.errorMessage.push(this.ERRORS.samePlayerSameStatistic);
        return false;
      }
    }
    return true;
  }

  /**
   * Check if dashboard already has selection with same game statistic
   * @param compared
   * @param selection
   * @returns {boolean}
   * @private
   */
  private validateGameStatistic(compared: IYourcallSelection, selection: IYourcallSelection): boolean {
    if (selection.type === 20) {
      if (selection.statisticId === compared.statisticId) {
        compared.error = selection.error = true;
        selection.errorMessage = selection.errorMessage || [];
        selection.errorMessage.push(this.ERRORS.sameGameStatistic);
        return false;
      }
    }
    return true;
  }
}
