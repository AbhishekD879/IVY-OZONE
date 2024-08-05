import { IYourcallSelectedInfo } from '../../models/yourcall-market-player.model';
import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { UserService } from '@core/services/user/user.service';
import { FracToDecService } from '@core/services/fracToDec/frac-to-dec.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { YourcallValidationService } from '@yourcall/services/yourcallValidation/yourcall-validation-service';
import { YourcallProviderService } from '@yourcall/services/yourcallProvider/yourcall-provider.service';
import { LocaleService } from '@core/services/locale/locale.service';
import { GtmService } from '@core/services/gtm/gtm.service';

import { YourCallDashboardItem } from '@yourcall/models/yourcallDashboardItem/yourcall-dashboard-item';

import { IYourcallSelection } from '@yourcall/models/selection.model';
import { IYourcallDashboardOdds } from '@yourcall/models/yourcall-dashboard-odds.model';
import { IYourcallAccumulatorOddsResponse } from '@yourcall/models/yourcall-api-response.model';
import { IOddsParams } from '@yourcall/models/odds-params.model';
import { YourCallEvent } from '@yourcall/models/yourcall-event';
import { Observable, Subject } from 'rxjs';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';
import { BybSelectedSelectionsService } from '@app/lazy-modules/bybHistory/services/bybSelectedSelections/byb-selected-selections';

@Injectable({ providedIn: 'root' })
export class YourcallDashboardService {
  valid: boolean = true;
  error: boolean = false;
  showOdds: boolean = true;
  isBetslipLoading: boolean = false;
  eventObj: { id?: number; name?: string } = {};
  game: YourCallEvent;
  items: YourCallDashboardItem[] = [];
  errorMessage: string;
  loading: boolean;
  removeId$ = new Subject();

  private dashboardItemsUpdate$ = new Subject<void>();
  private _odds: IYourcallDashboardOdds = {};

  constructor(
    private userService: UserService,
    private fracToDecService: FracToDecService,
    private pubsubService: PubSubService,
    private yourcallValidationService: YourcallValidationService,
    private yourcallProviderService: YourcallProviderService,
    private localeService: LocaleService,
    private gtmService: GtmService,
    private awsService: AWSFirehoseService,
    private bybSelectedSelectionsService: BybSelectedSelectionsService
  ) { }

  get dashboardItems$(): Observable<void> {
    return this.dashboardItemsUpdate$.asObservable();
  }
  set dashboardItems(value:Observable<void>){}

  /**
   * Get odds
   * @returns {*}
   */
  get odds(): number | string {
    return this.userService.oddsFormat === 'dec' ? parseFloat(this._odds.dec as string).toFixed(2) : this._odds.frac;
  }

  /**
   * Set odds. If parameter is provided in fractional format,
   * the decimal representation will be calculated for it as well. Same for the decimal format.
   * This avoids loosing original values during conversion, like '6/4' => '2.50' => '3/2'
   * @param odds
   */
  set odds(odds: number | string) {
    if (!odds) {
      return;
    }

    if (typeof odds === 'string' && odds.indexOf('/') >= 0) {
      const parsedOdds = odds.split('/');
      const priceNum = parseInt(parsedOdds[0], 10);
      const priceDen = parseInt(parsedOdds[1], 10);

      this._odds.dec = this.fracToDecService.fracToDec(priceNum, priceDen);
      this._odds.frac = odds;
    } else {
      this._odds.dec = odds;
      this._odds.frac = this.fracToDecService.decToFrac(odds);
    }
  }

  /**
   * Get status for Place Bet button
   * @returns {boolean}
   */
  get isButtonAvailable(): boolean {
    let disable = false;
    _.each(this.items, (item: YourCallDashboardItem) => {
      if (item.selection.disable) {
        disable = disable || item.selection.disable;
      }
    });
    return disable;
  }
  set isButtonAvailable(value:boolean){}

  /**
   * Get status for Edit button
   * @returns {boolean}
   */
  get isEditSection(): boolean {
    return this.items.some((item) => item.selection.edit);
  }
  set isEditSection(value:boolean){}

  /**
   * Add selection to the dashboard
   * @param market
   * @param selection
   * @param {Boolean} isBatchAdd
   */
  add(market: any, selection: IYourcallSelection, isBatchAdd: boolean): void {
    const index = _.findIndex(this.items, (item: YourCallDashboardItem) => {
      return item.market === market;
    });

    if (index === -1 || market.multi) {
      if(!this.bybSelectedSelectionsService.duplicateIdd.has(selection?.idd)){
        this.items.push(new YourCallDashboardItem({ market, selection }));
      }
      if(selection?.idd) {
        this.bybSelectedSelectionsService.duplicateIdd.add(selection.idd);
      }
    } else if (index > -1 && !market.multi) {
      this.removeId$.next(this.items[index].selection.id);
      this.items[index].selection = selection;
    }
    this.validate();

    if (!isBatchAdd) {
      this.calculateOdds();
      this.pubsubService.publish(this.pubsubService.API.YC_DASHBOARD_DISPLAYING_CHANGED, true);

      // if (market.title !== 'Player Bets') {
        // Google analytics
      //   this.trackAddingSelection();
      // }
    }
    this.dashboardItemsUpdate$.next();
    this.callGTM();
  }

  /**
   * to call gtm on adding a selection
   * @returns {void}
   */
     callGTM(): void {
       if(this.items.length > 0) {
         this.bybSelectedSelectionsService.callGTM('add-selection', {selectionName: this.items[this.items.length-1].getTitle()});
       }
    }

  /**
   * Runs calculation and dashboard refresh on demand
   */
  finishBatchAdd(): void {
    this.calculateOdds();
    this.pubsubService.publish(this.pubsubService.API.YC_DASHBOARD_DISPLAYING_CHANGED, [true, true]);
  }

  /**
   * Edit player bets selection
   * @param market
   * @param selection
   * @param newSelection
   */
  edit(market: any, selection: IYourcallSelection, newSelection: IYourcallSelection): void {
    const index = _.findIndex(this.items, (item: YourCallDashboardItem) => {
      return item.market === market && item.selection.id === selection.id;
    });
    this.items[index].selection = newSelection;

    // set odds to recalculate
    this._odds = {};
    this.showOdds = true;
    this.validate();
    this.calculateOdds();
    this.dashboardItemsUpdate$.next();
  }

  /**
   * Remove selection from the dashboard
   * @param market
   * @param selection
   */
  remove(market: any, selection: IYourcallSelection): void {
    let index;
    if(this.bybSelectedSelectionsService.duplicateIdd.has(selection?.idd))
      this.bybSelectedSelectionsService.duplicateIdd.delete(selection.idd);
    if (market.multi) {
      index = _.findIndex(this.items, (item: YourCallDashboardItem) => {
        return item.market === market && item.selection.id === selection.id;
      });
    } else {
      index = _.findIndex(this.items, (item: YourCallDashboardItem) => {
        return item.market === market;
      });
    }
    if (index > -1) {
      this.items.splice(index, 1);
    } else if(index == -1 && market.marketType =='Player Bet'){
      this.items.forEach(player => {
      if(player.selection.idd === undefined){
        player.selection.idd=player.selection.playerId + '-' + player.selection.statisticId + '-' + player.selection.value;
      }
      });
      this.items = this.items.filter(el => el.selection.idd !== selection.idd);
    }
    this.validate();
    this.calculateOdds();
    this.dashboardItemsUpdate$.next();
  }

  /**
   * Return decimal odds
   * @param odds
   * @returns {*}
   */
  convertOdds(odds: string | number): string | number {
    if (typeof odds === 'string' && odds.indexOf('/') >= 0) {
      const parsedOdds = odds.split('/');
      const priceNum = parseInt(parsedOdds[0], 10);
      const priceDen = parseInt(parsedOdds[1], 10);
      return this.fracToDecService.getDecimal(priceNum, priceDen);
    }

    return odds;
  }

  /**
   * Clear the dashboard
   */
  clear(): void {
    this.items = [];
    this.valid = true;
    this.error = false;
    this.dashboardItemsUpdate$.next();
  }

  /**
   * Check if the dashboard has min required selections to place the bet
   * @returns {boolean}
   */
  validSelectionCount(): boolean {
    this.yourcallValidationService.dashboard = this.items;
    return this.yourcallValidationService.isValidSelectionCount();
  }

  canPlaceBet(): boolean {
    return this.validSelectionCount() && this.showOdds;
  }

  /**
   * Calculate odds for whole dashboard
   * @private
   */
  calculateOdds(): void {
    this._odds = {};
    if (!this.items.length || !this.validSelectionCount() || !this.valid) {
      this.error = false;
      delete this.errorMessage;
      return;
    }

    const params: IOddsParams = this.yourcallProviderService.helper
      .buildOddsParams(_.pluck(this.items, 'selection') as IYourcallSelection[], this.game);

    this.loading = true;
    this.error = false;
    this.yourcallProviderService.calculateAccumulatorOdds(params)
      .then((data: IYourcallAccumulatorOddsResponse) => this.yourcallProviderService.helper.parseOddsValue(data))
      .then((odds: string) => this.updateOddsValue(odds), error => this.handleOddsError(error));
  }

  /**
   * Google analytics. Track Editing a Player Bet if player or statistic were changed
   * @params {string} changedField
   * @params {object} newSelection
   */
  trackEditingPlayerBet(changedField: string, newSelection: IYourcallSelection | IYourcallSelectedInfo): void {
    if (changedField === 'statistic') {
      // When user name or statistic were changed
      this.gtmService.push('trackEvent', {
        eventCategory: 'your call',
        eventAction: 'build bet',
        eventLabel: 'select player bet',
        playerName: newSelection.player.name,
        playerStat: newSelection.stat.title,
        playerStatNum: newSelection.statVal
      });
    }
    if (changedField === 'statVal') {
      // When statVal was changed
      this.gtmService.push('trackEvent', {
        eventCategory: 'your call',
        eventAction: 'build bet',
        eventLabel: 'update statistic',
        playerName: newSelection.player.name,
        playerStat: newSelection.stat.title,
        playerStatNum: newSelection.statVal
      });
    }
  }

  /**
   * Google analytics. Track Dash Board Removing Selection
   * @params {string} marketTitle
   */
  trackBoardRemovingSelection(marketTitle: string): void {
    this.gtmService.push('trackEvent', {
      eventCategory: 'your call',
      eventAction: 'dashboard',
      eventLabel: 'remove selection',
      market: marketTitle
    });
  }

  /**
   * Google analytics. Track on the price to add to the YourCall QuickBetSlip
   */
  trackAddToQuickBetSlip(eventAction: string, isLoggedIn: boolean): void {
    this.gtmService.push('trackEvent', {
      eventCategory: 'your call',
      eventAction: eventAction,
      eventLabel: Number(this._odds.dec)
    });

    this.gtmService.push('trackEvent', {
      event: 'trackEvent',
      eventCategory: 'quickbet',
      eventAction: 'add to quickbet',
      eventLabel: 'success',
      ecommerce: {
        add: {
          products: [{
            name: this.eventObj.name,
            category: '16',
            variant: this.game.obTypeId.toString(),
            brand: 'Bet Builder',
            metric1: 0,
            dimension60: this.eventObj.id.toString(),
            dimension62: 0,
            dimension63: 1,
            dimension64: 'EDP',
            dimension65: 'Bet Builder',
            dimension86: 0,
            dimension87: 0,
            dimension89: undefined,
            quantity: 1
          }]
        }
      }
    });

    this.awsService.addAction('yourcallDashboard=>placeBet (add to quickbet)', { isLoggedIn });
  }

  /**
   * Validate dashboard
   * @private
   */
  private validate(): void {
    this.yourcallValidationService.dashboard = this.items;
    this.valid = this.yourcallValidationService.validate();
  }

  /**
   * Google analytics. Track Market Adding Selection
   * @params {Number} position
   * @params {Object} market
   */
  private trackAddingSelection() {
    this.gtmService.push('trackEvent', {
      eventCategory: 'your call',
      eventAction: 'match bet',
      sportName: 'Football',
      eventName: this.eventObj.name,
      eventID: this.eventObj.id
    });
  }

  private updateOddsValue(odds: string): void {
    this.loading = false;
    this.odds = odds;
    // Google analytics
    // this.trackAddToQuickBetSlip('display odds', this.userService.status);
  }

  private handleOddsError(error: any): void {
    if (this.yourcallProviderService.isValidResponse(error, 'calculateAccumulatorOdds')) {
      this.loading = false;
      this.error = true;
      this.errorMessage = this.yourcallProviderService.helper.parseOddsError(error) ||
        this.localeService.getString('yourCall.priceNotAvailable');
    }
  }
}
