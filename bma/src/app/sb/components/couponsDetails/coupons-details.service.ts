import { Injectable } from '@angular/core';
import { map, switchMap } from 'rxjs/operators';
import { Observable, of, from } from 'rxjs';
import * as _ from 'underscore';

import { BetFilterParamsService } from '@app/retail/services/betFilterParams/bet-filter-params.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { SiteServerService } from '@core/services/siteServer/site-server.service';
import { TimeService } from '@core/services/time/time.service';
import { CacheEventsService } from '@core/services/cacheEvents/cache-events.service';

import { FOOTBALL_COUPONS } from '@platform/sb/components/couponsDetails/coupons-details.constant';

import { ISystemConfig } from '@core/services/cms/models';
import { ITypeSegment } from '@app/inPlay/models/type-segment.model';
import { IMarket } from '@core/models/market.model';
import { ICouponMarketSelector, IMarketSelectorConfig } from '@shared/components/marketSelector/market-selector.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { ICoupon } from '@core/models/coupon.model';
import { IBetFilterParams } from '@app/retail/services/betFilterParams/bet-filter-params.model';
import { GamingService } from '@app/core/services/sport/gaming.service';
import environment from '@environment/oxygenEnvConfig';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';

@Injectable({
  providedIn: 'root'
})
export class CouponsDetailsService {
  footballCoupons: IMarketSelectorConfig;
  isGoalscorerCoupon: boolean = false;
  isCorrectScoreCoupon: boolean = false;
  sportId: string = environment.CATEGORIES_DATA.footballId;

  private readonly defaultFootballCouponsMarkets: ICouponMarketSelector[];
  private readonly FOOTBALL_COUPONS = FOOTBALL_COUPONS;

  constructor(
    private gtmService: GtmService,
    private siteServerService: SiteServerService,
    private timeService: TimeService,
    private betFilterParamsService: BetFilterParamsService,
    private cmsService: CmsService,
    private cacheEventsService: CacheEventsService,
    private windowRef: WindowRefService,
  ) {
    this.footballCoupons = this.FOOTBALL_COUPONS;
    this.defaultFootballCouponsMarkets = this.FOOTBALL_COUPONS.DEFAULT_MARKETS;
  }

  get isCustomCoupon(): boolean {
    return this.isCorrectScoreCoupon || this.isGoalscorerCoupon;
  }
  set isCustomCoupon(value:boolean){}

  getCouponEvents(couponId: string, couponName: string, footballService: GamingService):
    Observable<{ coupons: ISportEvent[], options: ICouponMarketSelector[]}> {
    const requestParams = footballService.couponEventsRequestParams(couponId);
    const options = [];
    const cmsOptions = [];
    this.sportId = requestParams.categoryId;
    this.pushToGTM(couponName);
    return from(footballService.couponEventsByCouponId(_.extend({}, requestParams, { couponId })))
      .pipe(switchMap((coupons: ISportEvent[]) => {
        this.isCorrectScoreCoupon = this.isCorrectScoreMarkets(coupons);
        return this.isCustomCoupon ? of({ coupons, options: [] }) : this.getCMSCouponMarketSelector(couponId, coupons);
      }));
  }

  isBetFilterEnable(coupon: ICoupon): Observable<boolean> {
    const params: IBetFilterParams = {};
    if (coupon.couponSortCode === 'MR') {
      params.couponName = coupon.name;
      params.mode = 'online';
      params.pathname = this.windowRef.nativeWindow.location.pathname;
      this.betFilterParamsService.betFilterParams = params;
      return this.cmsService.getSystemConfig().pipe(map((config: ISystemConfig) => {
        return config.Connect && config.Connect.footballFilter;
      }));
    }
    return of(false);
  }

  /**
   * pushToGTM()
   */
  pushToGTM(couponName: string): void {
    const eventLabel = couponName.replace(/\w\S*/g, txt => txt.charAt(0).toUpperCase() + txt.substr(1));

    this.gtmService.push('trackEvent', {
      eventCategory: 'Coupon Selector',
      eventAction: 'Select Coupon',
      eventLabel
    });
  }

  setOddsHeader(selectOptions: ICouponMarketSelector[], marketFilter: string): string[] {
    if (selectOptions && selectOptions.length) {
      const headerObj = selectOptions.find(
        (option: ICouponMarketSelector) => option.templateMarketName.toLowerCase() === marketFilter.toLowerCase()
      );
      return headerObj ? headerObj.header : [];
    }
    return [];
  }

  /**
   * Group Coupon Events
   * @param {ISportEvent[]} data
   * @returns {boolean[]}
   */
  groupCouponEvents(data: ISportEvent[], footballService: GamingService): ITypeSegment[] {
    return _.uniq(_.chain(_.map(_.groupBy(data, 'typeName'), (events: ISportEvent[]) => {
      return footballService.arrangeEventsBySection(events, !this.isCustomCoupon)[0];
    })).sortBy('classDisplayOrder').sortBy('typeDisplayOrder').value());
  }

  /**
   * Check if quick bet is blocked on coupons details page
   * @returns {Observable<boolean>}
   */
  isQuickBetBlocked(): Observable<boolean> {
    return this.cmsService.getSystemConfig().pipe(
      map((config: ISystemConfig) => config.quickBet && config.quickBet.blockOnCouponDetailsPage));
  }

  /**
   * Filter event with same property
   * @param array
   * @param property
   * @param childKey
   */
  filteredArr(array: any[] = [], property: string, childKey: string = ''): any[] {
    return array.reduce((acc, current) => {
      const sameProperty = acc.find(item => item[property] === current[property]);
      if (sameProperty && sameProperty[childKey]) {
        sameProperty[childKey] = this.filteredArr(current[childKey].concat(sameProperty[childKey]), property);
      }
      return !sameProperty ? acc.concat([current]) : acc;
    }, []);
  }

  private getCMSCouponMarketSelector(couponId: string, coupons: ISportEvent[]): Observable<any> {
    let cmsOptions: ICouponMarketSelector[] = [];
    let options: ICouponMarketSelector[] = [];
    return this.cmsService.getCouponMarketSelector().pipe(
      switchMap((marketOptions: ICouponMarketSelector[]) => {
        cmsOptions = marketOptions;
        options = this.getMarketOptions(options, cmsOptions, coupons);
        return this.cmsService.getToggleStatus('FootballCoupons');
      }),
      switchMap((toggleStatus: boolean) => {
        if (toggleStatus) {
          const ids = coupons.map(match => match.id);
          const params = {
            eventsIds: ids,
            isStarted: false,
            marketsCount: false,
            childCount: true,
            suspendAtTime: this.timeService.getSuspendAtTime(),
            templateMarketNameOnlyIntersects: true
          };
          return from(this.siteServerService.getEventsByEventsIds(params)).pipe(
            map((events: ISportEvent[]) => {
              coupons = events && events.length ? this.filteredArr(events.concat(coupons), 'id', 'markets') : coupons;
              this.cacheEventsService.store('coupons', couponId, coupons);
              options = this.getMarketOptions(options, cmsOptions, coupons);
              return { coupons, options };
            })
          );
        }
        return of({ coupons, options });
      }));
  }

  /**
   * Check if events have Correct Score Markets
   * @param {ISportEvent[]} events
   * @returns {boolean}
   */
  private isCorrectScoreMarkets(events: ISportEvent[]): boolean {
    const markets = events && _.flatten(_.pluck(events, 'markets'));
    const csMarkets = _.where(markets, { dispSortName: 'CS' });
    return csMarkets && markets.length === csMarkets.length;
  }

  private getMarketOptions(options: ICouponMarketSelector[] = [], cmsOptions: ICouponMarketSelector[] = [], coupons: ISportEvent[])
    : ICouponMarketSelector[] {
    this.modifyTemplateName(coupons);
    const marketOptions = this.filteredArr(options.concat(cmsOptions), 'templateMarketName');
    const couponsMarketsNames = this.getOpenBetMarketNames(coupons);
    const availableMarkets = this.filterMarketOptions(marketOptions, couponsMarketsNames);
    const availableMarketsNames = availableMarkets.map((market) => market.templateMarketName);
    const defaultMarketsOptions = this.filterDefaultOptions(couponsMarketsNames, availableMarketsNames);

    return availableMarkets.concat(defaultMarketsOptions);
  }

  /**
   * Modify Template Name for markets witch has rawHandicapValue attr
   * @param {ITypeSegment[]} events
   */
  private modifyTemplateName(events: ISportEvent[]): void {
    events.forEach((event: ISportEvent) => {
      event.markets.forEach((market: IMarket) => {
        if (market.rawHandicapValue && !/[0-9]/g.test(market.templateMarketName)) {
          market.templateMarketName = `${market.templateMarketName} ${market.rawHandicapValue}`;
        }
      });
    });
  }

  private getOpenBetMarketNames(events: ISportEvent[]): string[] {
    const markets = _.flatten(_.pluck(events, 'markets'));
    const names = _.uniq(_.flatten(_.pluck(markets, 'templateMarketName')));
    return names.map( name => name && name.toLowerCase());
  }

  private filterMarketOptions(cmsCouponMarkets: ICouponMarketSelector[], couponsMarketsNames: string[]): ICouponMarketSelector[] {
    const defaultMarketsNames = _.map(_.pluck(_.filter(this.defaultFootballCouponsMarkets, (market: ICouponMarketSelector) =>
        this.matchName(couponsMarketsNames, market.templateMarketName)), 'templateMarketName'),
      market => market.toLowerCase());
    return cmsCouponMarkets.filter((option: ICouponMarketSelector) => {
      return this.matchName(couponsMarketsNames, option.templateMarketName) ||
        this.matchName(defaultMarketsNames, option.templateMarketName);
    });
  }

  private filterDefaultOptions(allMarketsNames: string[], cmsMarketsNames: string[]): ICouponMarketSelector[] {
    const cmsMarkets = cmsMarketsNames.map(market => market.toLowerCase());
    return this.defaultFootballCouponsMarkets.filter((market: ICouponMarketSelector) => {
      return this.matchName(allMarketsNames, market.templateMarketName) &&
        !this.matchName(cmsMarkets, market.templateMarketName) ||
        (market.templateMarketName === 'Match Betting' && this.matchName(allMarketsNames, 'match result'));
    });
  }

  private matchName(names: string[], name: string): boolean {
    const marketName = name.toLowerCase();
    return names && names.indexOf(marketName) >= 0;
  }
}
