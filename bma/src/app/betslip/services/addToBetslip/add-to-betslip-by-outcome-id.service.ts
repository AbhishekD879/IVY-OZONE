import {
  forkJoin as observableForkJoin,
  from as observableFrom,
  EMPTY,
  of as observableOf,
  throwError,
  Observable
} from 'rxjs';

import { catchError, map, switchMap, mergeMap, finalize, concatMap } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { BetslipApiModule } from '@betslipModule/betslip-api.module';
import { Router } from '@angular/router';
import { Location } from '@angular/common';
import * as _ from 'underscore';
import environment from '@environment/oxygenEnvConfig';

import { IMarketEntity } from '@core/models/market-entity.model';
import { IOutcomeEntity } from '@core/models/outcome-entity.model';
import { ISportEventEntity } from '@core/models/sport-event-entity.model';
import { IMarket } from '@core/models/market.model';
import { IOutcomePrice } from '@core/models/outcome-price.model';
import { IOutcome, IOutcomeDetails } from '@core/models/outcome.model';
import { ISystemConfig } from '@core/services/cms/models';
import { ISSResponse } from '@core/models/ss-response.model';
import { IBetSelection } from '@betslip/services/betSelection/bet-selection.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { BetslipBetDataUtils } from '@betslip/models/betslip-bet-data.utils';
import { IOutputPrice } from '@app/inPlay/models/output-price.model';
import { IHandicapOutcome } from '@betslip/models/betslip-bet-data.model';
import { IGtmOrigin } from '@core/services/gtmTracking/models/gtm-origin.model';
import { IBetDetail, IBetDetailLeg, IBetDetailLegPart, IBetOdds } from '@app/bpp/services/bppProviders/bpp-providers.model';

import { DialogService } from '@core/services/dialogService/dialog.service';
import { SiteServerRequestHelperService } from '@core/services/siteServerRequestHelper/site-server-request-helper.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { OverAskService } from '@betslip/services/overAsk/over-ask.service';
import { BetslipService } from '@betslip/services/betslip/betslip.service';
import { ToteBetslipService } from '@betslip/services/toteBetslip/tote-betslip.service';
import { StorageService } from '@core/services/storage/storage.service';
import { DynamicLoaderService } from '@app/dynamicLoader/dynamic-loader.service';
import { DeviceService } from '@core/services/device/device.service';
import { GtmTrackingService } from '@core/services/gtmTracking/gtm-tracking.service';
import { UserService } from '@core/services/user/user.service';
import { BetslipStorageService } from '@betslip/services/betslip/betslip-storage.service';
import { SiteServerService } from '@core/services/siteServer/site-server.service';
import { MaxStakeDialogComponent } from '@betslipModule/components/maxStakeDialog/max-stake-dialog.component';
import { FanzoneStorageService } from '@app/core/services/fanzone/fanzone-storage.service';

@Injectable({ providedIn: BetslipApiModule })
export class AddToBetslipByOutcomeIdService {

  syncProcess: { inProgress: boolean } = { inProgress: false };
  isValidSelection: boolean = false; 
  filteredOutcomeIds: any[] = []; 
  private maxBets: number;
  private showMaxBetsErr: boolean;
  private racingPostGTM: IGtmOrigin;
  // TODO: @Oleh Vykhopen
  private modulePath: string = '@betslipModule/betslip.module#BetslipModule';
  private env = environment;


  constructor(
    private siteServerRequestHelperService: SiteServerRequestHelperService,
    private cmsService: CmsService,
    private dialogService: DialogService,
    private overaskService: OverAskService,
    private gtmService: GtmService,
    private pubsub: PubSubService,
    private windowRef: WindowRefService,
    private betslipService: BetslipService,
    private storageService: StorageService,
    private toteBetslipService: ToteBetslipService,
    private router: Router,
    private dynamicComponentLoader: DynamicLoaderService,
    private deviceService: DeviceService,
    private location: Location,
    private gtmTrackingService: GtmTrackingService,
    private userService: UserService,
    private betslipStorageService: BetslipStorageService,
    private siteServerService: SiteServerService,
    private fanzoneStorageService: FanzoneStorageService
  ) {
    this.getEvents = this.getEvents.bind(this);
    this.buildSelections = this.buildSelections.bind(this);
  }

  /**
   * Get outcomes by outcome ids
   * @param {array} ids -  outcome ids
   * @return {array} outcomes
   */
  getEventsByOutcomeIds(ids: string[]): Observable<({ SSResponse }) => Partial<IBetSelection>[]> {
    return this.getEvents(ids).pipe(
      concatMap(this.buildSelections.bind(this)));
  }

  /**
   * Get outcomes from events received from SS
   * @param {array} event
   * @return {array} outcomes
   */
  getOutcomesFromQuickBetEvent(event: ISportEvent): IOutcome[] {
    const outcomes = [];

    event.markets.forEach((marketObj: IMarket) => {
      marketObj.outcomes.forEach((outcomeObj: IOutcome) => {
        outcomeObj.marketRawHandicapValue = marketObj.rawHandicapValue;
        outcomeObj.priceType = this.definePriceType(marketObj, outcomeObj);
        outcomes.push(outcomeObj);
      });
    });

    return outcomes;
  }

  /**
   * Get outcomes / markets / events from events received from SS
   * @param {array} events
   * @return {array} outcomes
   */
  getOutcomes(eventsList: ISportEventEntity[]): {
    events: { [key: string]: ISportEvent },
    markets: { [key: string]: IMarket },
    outcomes: IOutcome[]
  } {
    const events = {};
    const markets = {};
    const outcomes = [];

    _.each(eventsList, (eventObj: ISportEventEntity) => {
      if (eventObj.event && eventObj.event.id) {
        events[eventObj.event.id] = eventObj.event;
      }

      _.each(eventObj.event && eventObj.event.children, (marketObj: IMarketEntity) => {
        if (marketObj.market && marketObj.market.id) {
          markets[marketObj.market.id] = marketObj.market;
        }

        _.each(marketObj.market && marketObj.market.children, (outcomeObj: IOutcomeEntity) => {
          if(outcomeObj.hasOwnProperty('outcome')){
            outcomeObj.outcome.marketRawHandicapValue = marketObj.market.rawHandicapValue;
            outcomeObj.outcome.priceType = this.definePriceType(marketObj.market, outcomeObj.outcome);
            outcomes.push(outcomeObj.outcome);
          }
         
        });
      });
    });

    return { events, markets, outcomes };
  }

  /**
   * Is add to betslip in process
   * @return {boolean}
   */
  isAddToBetslipInProcess(): boolean {
    return this.syncProcess.inProgress;
  }

  /**
   * Main add to betslip flow
   * @param {string} rawIds
   * @param {boolean} goToBetSlip redirect to betSlip page, redirect by default
   * @param {boolean} doNotRemove allow bet slip to remove bet when same outcome id is passed
   * @param {boolean} redirect
   * @param {boolean} isSyncWithNative fire event syncWithNative if true
   * @param {boolean} fromNative detect is function call from event syncBetSlipFromNative
   * @param {boolean} directLink detect if selections added via direct link
   */
  addToBetSlip(rawIds: string, goToBetSlip: boolean = true, doNotRemove: boolean = true, redirect: boolean = true,
    isSyncWithNative: boolean = true, fromNative: boolean = false, directLink = false, racingPostGTM?: any,trackingModule?: string): Observable<{}> {
    if (this.toteBetslipService.isToteBetPresent()) {
      this.router.navigate(['/']);
      return this.betslipService.showBetslipLimitationPopup();
    }
    const ids = _.uniq(rawIds.split(',')).join();
    this.syncProcess.inProgress = true;
    // prevent router reload at SESSION_LOGIN if adding by deeplink
    if (redirect) {
      this.userService.set({isRedirecting: true});
    }

    // if overask in progress we can not add/remove bets to betslip
    if (this.overaskService.isInProcess) {
      this.overaskService.showOveraskInProgressNotification();
      this.syncProcess.inProgress = false;
      return;
    }

    const idsForProcess: Observable<string[] | string> = fromNative ? observableOf(ids) : this.checkMaxBetsAmount(ids);
    const add = _.partial(this.addSelectionsToBetSlip, goToBetSlip, doNotRemove, redirect, isSyncWithNative);

    this.storageService.set('betIds', ids);
    return idsForProcess.pipe(
      switchMap(this.getEvents.bind(this)),
      map((res: { SSResponse: ISSResponse }) => {
        this.gtmTrackAddToBetSlip(res, false, racingPostGTM, trackingModule);
        return res;
      }),
      concatMap(this.buildSelections.bind(this)),
      map((selections: Partial<IBetSelection>[]) => {
        if (directLink) {
          this.handleDirectLinkOutcome(selections);
        }

        return this.sortSelectionBasedOnIds(ids, selections);
      }),
      mergeMap(add.bind(this)),
      catchError((error) => {
        if (!this.showMaxBetsErr) {
          this.router.navigate(['/betslip', 'unavailable']);
          return EMPTY;
        }

        if (redirect) {
          this.router.navigate(['/']);
        }
        this.showMaxStakeDialog();
        return EMPTY;
      }),
      finalize(() => {
        this.syncProcess.inProgress = false;
      }));
  }

  reuseSelections(outcomeIds: string[], receipts: IBetDetail[], location?: string, goToBetSlip?: boolean): Observable<null> {
    this.syncProcess.inProgress = true;
    const navigateToBetSlip = goToBetSlip? goToBetSlip : false;

    if (this.overaskService.isInProcess) {
      this.overaskService.showOveraskInProgressNotification();
      this.syncProcess.inProgress = false;
      return;
    }

    this.storageService.set('betIds', outcomeIds.join(','));

    return this.getEvents(outcomeIds).pipe(
      map((res: { SSResponse: ISSResponse }) => {
        this.gtmTrackAddToBetSlip(res, true, false, undefined, location);
        return res;
      }),
      map((res: { SSResponse: ISSResponse }) => {
        return this.buildSelectionsFromBetReceipts(res, receipts, location);
      }),
      mergeMap((selections: IBetSelection[]) => {
        return this.addSelectionsToBetSlip(navigateToBetSlip, true, false, false, selections);
      }),
      catchError((error) => {
        console.warn('Error In Reuse Selection ', error);
        if(!_.isNumber(error)) {
          this.router.navigate(['/betslip', 'unavailable']);
        }
        return EMPTY;
      }),
      finalize(() => {
        this.syncProcess.inProgress = false;
      })
    );
  }

  /**
   * Synchronizes selection to betslip.
   * @param {string} outcomeId
   * @param {string} type
   * @param {string} userStake
   * @param {boolean} userEachWay
   * @param {IPrice} price
   * @param {boolean} isVirtual
   * @param {int} eventId
   * @param {boolean} isOutright
   * @param {boolean} isSpecial
   * @param {IGtmEvent} GTMObject
   * @return {Promise}
   */
  syncToBetslip({ outcomeId,
                  type,
                  userStake,
                  userEachWay,
                  price,
                  isVirtual,
                  eventId,
                  isOutright,
                  isSpecial,
                  GTMObject
                }: IBetSelection): Observable<Object> {
    // Show Betslip Limitation Popup BMA-28466
    if (this.toteBetslipService.isToteBetPresent()) {
      return this.betslipService.showBetslipLimitationPopup();
    }
    // if overask in progress we can not add/remove bets to betslip
    this.syncProcess.inProgress = true;

    if (this.overaskService.isInProcess) {
      this.overaskService.showOveraskInProgressNotification();
      this.syncProcess.inProgress = false;
      return observableOf(null);
    }

    const add = _.partial(this.addSelectionsToBetSlip, false, false, false, true);

    this.storageService.set('betIds', outcomeId);
    const eventsDataObservable$ = this.getEvent(outcomeId);
    this.betslipStorageService.setEventToBetslipObservable = eventsDataObservable$;

    return eventsDataObservable$.pipe(
      map((response: ISportEvent[]) => {
          if (!response.length) {
            return;
          }
          const event = response[0],
            outcomes = this.getOutcomesFromQuickBetEvent(event),
            eventIsLive = event.rawIsOffCode === 'Y' || (event.rawIsOffCode === '-' && event.isStarted);

          const details = BetslipBetDataUtils.outcomeDetails(
            event,
            event.markets[0],
            outcomes[0]);
          if (type === 'simple') {
            const outcome = outcomes[0],
              outcomePrice = outcome.prices[0],
              handicap = this.getOutcomeHandicap(outcome, outcomePrice);
            return [{
              userStake,
              userEachWay,
              outcomes,
              handicap,
              price: price || outcomePrice,
              eventIsLive, // solution for indicate in-play event,
              isVirtual,
              eventId,
              isOutright,
              isSpecial,
              GTMObject,
              details
            }];
          }

          if (type === 'scorecast') {
            this.normalizeScorecastOutcomes(outcomeId, outcomes);
          }

          return [{
            userStake,
            userEachWay,
            outcomes,
            handicap: undefined,
            price,
            type: type.toUpperCase(),
            eventIsLive, // solution for indicate in-play event
            isVirtual,
            eventId,
            isOutright,
            isSpecial,
            GTMObject
          }];
        }),
        mergeMap(add.bind(this)));
  }

  private gtmTrackAddToBetSlip(response: { SSResponse: ISSResponse }, isReuse: boolean, racingPostGTM?: any, trackingModule?: string, location?: string): void {
    let tracking: IGtmOrigin;
    if (!isReuse) {
      tracking = this.getBannerTracking;
      this.gtmTrackingService.restoreTracking(tracking);
    }

    const events = response.SSResponse.children.filter(({ event }) => {
      return event && event.children;
    });

    const markets = events.reduce((sum, { event }) => {
      event.children.forEach((market) => {
        market._gtm = {
          name: event.name,
          category: String(event.categoryId),
          variant: String(event.typeId),
          dimension60: String(event.id),
          dimension62: event.isStarted ? 1 : 0,
          dimension63: event.isYourCallBet === 'true' ? 1 : 0
        };
      });
      return sum.concat(event.children);
    }, []);

    const products = markets.reduce((sum, marketData) => {
      if (!marketData.market.children) {
        return sum;
      }
      const marketProds = marketData.market.children.map(({ outcome }) => {
        if(outcome) {
        if (isReuse) {
          let reuseBetOriginData = this.storageService.get('reuseBetSelections');
          tracking = this.gtmTrackingService.getBetOrigin(outcome.id);
          tracking.location = location;
          tracking.betType = "reuse";
          if (reuseBetOriginData && !reuseBetOriginData[outcome.id]) { 
            reuseBetOriginData[outcome.id] = tracking
          } else if(!reuseBetOriginData){
            reuseBetOriginData = {};
            reuseBetOriginData[outcome.id] = tracking;
          }
          this.storageService.set('reuseBetSelections', reuseBetOriginData);
        }
        
        if (!!trackingModule)
          tracking.module = trackingModule;

        const marketsTracking = Object.assign({
          brand: marketData.market.name,
          dimension61: outcome.id,
          dimension64: tracking.location,
          dimension65: tracking.module,
          dimension166: isReuse? 'reuse' : 'normal'
        }, marketData._gtm);
        if (racingPostGTM && Object.keys(racingPostGTM).length) {
          marketsTracking.dimension64 = racingPostGTM.location;
          marketsTracking.dimension65 = racingPostGTM.module;
          marketsTracking.dimesnion86 = racingPostGTM.dimension86; // Odds Boost
          marketsTracking.dimesnion87 = racingPostGTM.dimension87; // Stream Active
          marketsTracking.dimension88 = racingPostGTM.dimension88; // Stream_ID
          marketsTracking.quantity = racingPostGTM.quantity;
        }
        return marketsTracking;
      }
      });
      delete marketData._gtm;
      return sum.concat(marketProds);
    }, []);

    const gtmObj = {
      eventAction: isReuse ? 'reuse selection' : 'add to betslip',
      eventLabel: 'success',
      event: 'trackEvent',
      eventCategory: 'betslip',
      ecommerce: {
        add: {
          products
        }
      }
    };

    this.gtmService.push('trackEvent', Object.assign({}, gtmObj));
  }

  /**
   * Sort event markets according to the order of outcomes in request.
   * As they were originally sorted and passed by Scorecast component.
   * Markets with non-matched outcome ids are moved in the end of the list, keeping relative order (fallback case).
   * Reason: OB sometimes has different order of First GoalScorer and Correct Score component.
   */
  private normalizeScorecastOutcomes(originalOutcomeIds, eventOutcomes): void {
    const outcomeIds = [].concat(originalOutcomeIds).map(String),
      orderMap = eventOutcomes.reduce((result: { [k: number]: number }, outcome, outcomeIndex: number) => {
        const idIndex = outcomeIds.indexOf(outcome.id.toString());
        result[outcome.id] = idIndex >= 0 ? idIndex : outcomeIndex + outcomeIds.length + eventOutcomes.length;
        return result;
      }, {});

    eventOutcomes.sort((o2, o1) => orderMap[o2.id] - orderMap[o1.id]);
  }

  private get getBannerTracking(): IGtmOrigin {
    return {
      module: 'banner',
      location: this.location.path()
    };
  }

  private set getBannerTracking(value: IGtmOrigin){}

  /**
   * Gets event data from SS
   * @param {string | string[]} ids array
   * @returns {promise} events responce
   */
  private getEvents(ids: string | string[]): Observable<{ SSResponse: ISSResponse }> {
    return observableFrom(this.siteServerRequestHelperService.getEventsByOutcomes({
      outcomesIds: ids, isValidFzSelection: this.isValidSelection && this.userService.status
    }));
  }

  /**
   * Method to check if fanzone selection is valid 
   * @param rawIds - outcome ids
   * @returns - is valid selection
   */
  isValidOutcome(outcomeIds): Observable<boolean> {
    const outcomesIds = _.uniq(outcomeIds.split(',')).join();
    return observableFrom(this.siteServerRequestHelperService.getEventsByOutcomes({
      outcomesIds: outcomesIds, isValidFzSelection: true
    })).pipe(map((outcomesResponse) => {
      const fzStorage = this.fanzoneStorageService.get('fanzone') || {};
      const outcomes = this.betslipService.mapOutComes(outcomesResponse);
      this.filteredOutcomeIds = outcomes.map((outcome) => {
        if ((!outcome.teamExtIds && !outcome.hasOwnProperty('isDisplayed')) || this.checkIfFzSelection(outcome, fzStorage)) { 
          return outcome.id
        }
      }).filter((outcome)=> !!outcome);
      return (Object.keys(fzStorage).length && outcomes.some((outcome) => (outcome.teamExtIds && outcome.teamExtIds.replace(',','') === fzStorage.teamId) && outcome.isFanzoneMarket));
    }));
  }

  private checkIfFzSelection(outcome, fzStorage): boolean {
    return outcome.teamExtIds && outcome.isFanzoneMarket && 
    (!this.userService.status || (Object.keys(fzStorage).length && outcome.teamExtIds.replace(',','') !== fzStorage.teamId));
  }

  /**
   * Gets event data from SS after add to betslip from quickbet
   * @param {string | string[]} ids array
   * @returns {promise} events responce
   */
  private getEvent(ids: string | number[]): Observable<ISportEvent[]> {
    this.siteServerService.isValidFzSelection = true;
    return observableFrom(this.siteServerService.getEventsByOutcomeIds({ outcomesIds: ids, racingFormOutcome: true }));
  }

  /*
   * Builds selections from ss responce
   * @param {object} SS responce
   * @return {array} selections
   */
  private buildSelections(response: { SSResponse: ISSResponse }): Observable<Partial<IBetSelection>[]> {
    if (_.every(response.SSResponse.children, (eventObj: ISportEventEntity) => !eventObj.event)) {
      return throwError('Selection fot found in SiteServe');
    }
    const { events, markets, outcomes } = this.getOutcomes(response.SSResponse.children),
      eventIsLive = this.isLiveEvent(response); // in case of multiple events checks status of only first event

    return observableOf(outcomes.map((outcome: IOutcome) => {
      const price = this.getOutcomePrice(outcome),
        handicap = this.getOutcomeHandicap(outcome, price),
        isSuspended = events[outcome.eventId || markets[outcome.marketId].eventId].eventStatusCode === 'S' ||
          markets[outcome.marketId].marketStatusCode === 'S',
        details = <IOutcomeDetails>BetslipBetDataUtils.outcomeDetails(
          events[outcome.eventId || markets[outcome.marketId].eventId],
          markets[outcome.marketId],
          outcome);

      return {
        outcomes: [outcome],
        handicap,
        price,
        eventIsLive, // solution for indicate in-play event,
        isSuspended,
        details
      };
    }));
  }

  private sortSelectionBasedOnIds(ids: string, selections: Partial<IBetSelection>[]): Partial<IBetSelection>[] {
    return _.map(ids.split(','), (id: string) => {
      return _.find(selections, (selection: Partial<IBetSelection>) => {
        selection.GTMObject = {
          eventAction: 'add to betslip',
          tracking: this.getBannerTracking
        };
        return selection.outcomes[0].id === id;
      });
    }).filter((el: Partial<IBetSelection>) => el);
  }

  /**
   * Check whether event is live or not
   * @param rawSSResponse
   * @returns {boolean|string}
   */
  private isLiveEvent(rawSSResponse: { SSResponse: ISSResponse }): boolean {
    const event = rawSSResponse.SSResponse.children[0].event;
    return event.rawIsOffCode === 'Y' || (event.rawIsOffCode === '-' && event.isStarted);
  }

  private registerSelection(selection: IBetSelection, doNotRemove: boolean, isSyncWithNative: boolean): Observable<void> {
    return this.betslipService.toggleSelection(selection, doNotRemove, isSyncWithNative).pipe(map(() => {
      this.pubsub.publishSync(this.pubsub.API.BETSLIP_COUNTER_UPDATE, this.betslipService.count());
      this.pubsub.subscribe('addToBetSlipByOutcomeIdFactory', this.pubsub.API.ADDTOBETSLIP_PROCESS_FINISHED, () => {
        this.syncProcess.inProgress = false;
      });
    }));
  }

  /**
   * Add selection to Betslip storage
   * @param {boolean} goToBetSlip
   * @param {boolean} doNotRemove
   * @param {boolean} redirect
   * @param {boolean} isSyncWithNative
   * @param {Array} selections
   */
  private addSelectionsToBetSlip(goToBetSlip: boolean, doNotRemove: boolean, redirect: boolean, isSyncWithNative,
                                 selections: IBetSelection | IBetSelection[]): Observable<any> {
    let observableSelections: Observable<any>;
    // constant for timeouts logic beyond
    const timeout = 1000;

    if ((selections as IBetSelection[]).length) {
      observableSelections = observableForkJoin(_.map((selections as IBetSelection[]), (selection: IBetSelection) => {
        return this.registerSelection(selection, doNotRemove, isSyncWithNative);
      }));
    } else {
      observableSelections = this.registerSelection((selections as IBetSelection), doNotRemove, isSyncWithNative);
    }

    return observableSelections.pipe(map(() => {

        if (redirect) {
          this.router.navigate(['/'])
            .then(() => this.userService.set({ isRedirecting: false }));
        }

      if (goToBetSlip && this.deviceService.isMobile) {
        // send data customer is deeplinked into the betslip overlay on Mobile
        this.gtmService.push('trackPageview', { virtualUrl: '/betslip-receipt' });

          // timeout to finish redirect before opening betslip.
          this.windowRef.nativeWindow.setTimeout(() => {
            this.pubsub.publish(this.pubsub.API['show-slide-out-betslip'], true);
          }, timeout);
        }

        // show error popUp in case user tried to add more stakes than allowed
        if (this.showMaxBetsErr) {
          // timeout to sync with timeout in logic above for finishing redirection to betslip
          setTimeout(() => {
            this.showMaxStakeDialog();
          }, timeout);
        }
      }),
      map(() => this.pubsub.publishSync(this.pubsub.API.BETSLIP_UPDATED)));
  }

  /**
   * Check if max bets amount are not exceeded
   * @param {string} ids - selection id's
   * return {array}
   */
  private checkMaxBetsAmount(ids: string): Observable<string[]> {
    return this.cmsService.getSystemConfig().pipe(
      map((config: ISystemConfig) => {
        this.maxBets = config.Betslip.maxBetNumber;
        const newBets = ids.split(','),
          betsInBetsLip = this.betslipService.count(),
          totalBets = betsInBetsLip + newBets.length;

        // if we have more bets then max allowed show dialog
        if (totalBets > this.maxBets) {
          this.showMaxBetsErr = true;
        }

        // remove excessive new bets
        return newBets.slice(0, (this.maxBets - betsInBetsLip));
      }));
  }

  /**
   * Checks what type of price is in given outcome. Outcome will have "SP" price type if one of next conditions will be met,
   * otherwise "LP" price type will be returned.
   *   - "priceTypeCodes" of outcome's market does not include "LP" code;
   *   - outcome does not have available prices;
   *   - outcome is of "Unnamed favourites" type.
   *
   * @param {Object} marketEntity
   * @param {Object} outcomeEntity
   * @return {string}
   */
  private definePriceType(marketEntity: IMarket, outcomeEntity: IOutcome): string {
    const isFavourite = ['unnamed favourite', 'unnamed 2nd favourite'].indexOf(outcomeEntity.name.toLowerCase()) > -1;
    return marketEntity.priceTypeCodes.indexOf('LP') === -1 ||
    !outcomeEntity.children || isFavourite ? 'SP' : 'LP';
  }

  /**
   * Retrieves prices from outcome response.
   * @param {Object} outcome
   * @return {Object}
   */
  private getOutcomePrice(outcome: IOutcome): IOutputPrice {
    const price = outcome.children && outcome.children[0] && outcome.children[0].price;
    return _.extend(price || {}, { priceType: outcome.priceType });
  }

  /**
   * Retrieves handicap data from outcome response.
   * @param {Object} outcome
   * @param {Object=} price
   * @return {Object}
   */
  private getOutcomeHandicap(outcome: IOutcome, price: IOutcomePrice): IHandicapOutcome {
    return outcome.marketRawHandicapValue && {
      type: outcome.outcomeMeaningMajorCode,
      raw: price && (price.handicapValueDec || '').replace(/,/g, '')
    };
  }

  private buildSelectionsFromBetReceipts(
    response: { SSResponse: ISSResponse },
    receipts: IBetDetail[],
    location?: string
  ): Partial<IBetSelection>[] {
    if (response.SSResponse.children.every((eventObj: ISportEventEntity) => !eventObj.event)) {
      return [];
    }

    const { events, markets, outcomes } = this.getOutcomes(response.SSResponse.children);
    const eventIsLive = this.isLiveEvent(response);

    const complexTypeMap = {
      SF: 'FORECAST',
      RF: 'FORECAST_COM',
      CF: 'FORECAST_COM',
      TC: 'TRICAST',
      CT: 'TRICAST_COM',
      SC: 'SCORECAST'
    };

    const singlesIds = {};
    const selections: Partial<IBetSelection>[] = [];

    const singles = [];
    const multiples = [];
    receipts.forEach((receipt: IBetDetail) => {
      receipt.betType === 'SGL' ? singles.push(receipt) : multiples.push(receipt);
    });

    singles.forEach((receipt: IBetDetail) => {
      const leg = receipt.leg[0];
      const complexType = complexTypeMap[leg.legSort];

      const selOutcomes = leg.part.map((part: IBetDetailLegPart) => {
        return outcomes.find((_outcome: IOutcome) => _outcome.id === this.getOutComeId(part));
      });

      singlesIds[this.getSelectionId(complexType, selOutcomes)] = true;

      const price = complexType === complexTypeMap.SC ? this.parseReceiptPrices(receipt.odds) : this.getOutcomePrice(selOutcomes[0]);
      const handicap = this.getOutcomeHandicap(selOutcomes[0], price);

      const GTMObject = leg.eventEntity ? this.formGTMObject(leg.eventEntity, markets, selOutcomes[0], location, eventIsLive) : undefined;

      selections.push({
        outcomes: selOutcomes,
        handicap,
        price,
        eventIsLive,
        type: complexType,
        isFCTC: receipt.isFCTC,
        GTMObject,
        details: !receipt.isFCTC ? <IOutcomeDetails>BetslipBetDataUtils.outcomeDetails(
          events[selOutcomes[0].eventId || markets[selOutcomes[0].marketId].eventId],
          markets[selOutcomes[0].marketId],
          selOutcomes[0]) : undefined
      });
    });

    multiples.forEach((receipt: IBetDetail) => {
      receipt.leg.forEach((leg: IBetDetailLeg) => {
        const selOutcomes = outcomes.filter((outcome: IOutcome) => outcome.id === this.getOutComeId(leg.part[0]));
        const selectionId = this.getSelectionId('SGL', selOutcomes);
        const isLive = leg.part[0].event.rawIsOffCode === 'Y' || (leg.part[0].event.rawIsOffCode === '-' && leg.part[0].event.isStarted);
        if (singlesIds[selectionId]) {
          return;
        }

        singlesIds[selectionId] = true;

        const price = this.getOutcomePrice(selOutcomes[0]);
        const handicap = this.getOutcomeHandicap(selOutcomes[0], price);

        const GTMObject = leg.eventEntity ? this.formGTMObject(leg.eventEntity, markets, selOutcomes[0], location, eventIsLive) : undefined;

        selections.push({
          outcomes: selOutcomes,
          handicap,
          price,
          eventIsLive: isLive,
          GTMObject
        });
      });
    });

    return selections;
  }

  private formGTMObject(eventEntity: ISportEvent, markets: { [key: string]: IMarket }, selectedOutcome: IOutcome, location: string, eventIsLive: boolean) {
    const GTMObject = {
      eventAction: 'reuse selection',
      categoryID: eventEntity && String(eventEntity.categoryId),
      typeID: eventEntity && String(eventEntity.typeId),
      eventID: eventEntity && String(eventEntity.id),
      selectionID: eventEntity && String(eventEntity.id)
    };

    const tracking = this.gtmTrackingService.getBetOrigin(selectedOutcome.id);
    tracking.location = location;
    tracking.betType = 'reuse';

    GTMObject['tracking'] = tracking;
    GTMObject['betData'] = {
      name: eventEntity.originalName || eventEntity.name,
      category: String(eventEntity.categoryId),
      variant: String(eventEntity.typeId),
      brand: eventEntity.markets[0].marketName || eventEntity.markets[0].name,
      dimension60: String(eventEntity.id),
      dimension61: selectedOutcome.id,
      dimension62: eventIsLive ? 1 : 0,
      dimension63: this.isByB(eventEntity) ? 1 : 0,
      dimension64: tracking.location,
      dimension65: tracking.module,
      dimension177: markets[selectedOutcome.marketId].isSCAvailable ? 'show': 'No show',
      dimension180: tracking.module === 'next races' && eventEntity.categoryId == '39' ? 'virtual' : 'normal'

    };
    return GTMObject
  }

  private getOutComeId(legPart: IBetDetailLegPart): string | IOutcome {
    return Array.isArray(legPart.outcome) ? legPart.outcomeId : legPart.outcome
  }

  private getSelectionId(type: string, outcomes: IOutcome[]): string {
    return `${type || 'SGL'}|${outcomes.map((outcome: IOutcome) => outcome.id).join('|')}`;
  }

  private parseReceiptPrices(odds: IBetOdds): IOutcomePrice {
    const oddsParts = odds.frac.split('/');

    return {
      priceDec: odds.dec,
      priceDen: +oddsParts[1],
      priceNum: +oddsParts[0],
      priceType: 'LP'
    };
  }

  private showMaxStakeDialog() {
    this.dynamicComponentLoader.loadModule(this.modulePath).then((moduleRef) => {
      const componentFactory = moduleRef.componentFactoryResolver.resolveComponentFactory(MaxStakeDialogComponent);
      this.dialogService.openDialog(DialogService.API.betslip.maxStakeDialog, componentFactory, true, {
        text: this.maxBets
      });
    });
    this.showMaxBetsErr = false;
  }

  private handleDirectLinkOutcome(selections: Partial<IBetSelection>[]) {
    const delay = 2000;
    let suspSelectionsCount = 0;

    selections.forEach((selection: Partial<IBetSelection>) => {
      if (selection.isSuspended || selection.outcomes.some((outcome: IOutcome) => outcome.outcomeStatusCode === 'S')) {
        suspSelectionsCount++;
      }
    });

    if (suspSelectionsCount) {
      setTimeout(() => {
        this.pubsub.publishSync(this.pubsub.API.BS_SHOW_SUSP_OVERLAY);
      }, delay);
    }
  }

  private isByB(event): boolean {
    return event && this.env && this.env.BYB_CONFIG
      && String(this.env.BYB_CONFIG.HR_YC_EVENT_TYPE_ID) === String(event.typeId);
  }
}
