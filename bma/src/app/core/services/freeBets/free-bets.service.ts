import {
  from as observableFrom,
  combineLatest as observableCombineLatest,
  of as observableOf,
  mergeMap,
  Observer,
  Observable,
  throwError,
  BehaviorSubject,
  Subject
} from 'rxjs';

import { shareReplay, concatMap, catchError, map } from 'rxjs/operators';
import { IFreeBet } from '@betslip/services/freeBet/free-bet.model';
import environment from '@environment/oxygenEnvConfig';
import { Injectable} from '@angular/core';
import * as _ from 'underscore';

import {
  IFreeBetState,
  IFreeBetBetslipFormat,
  IStoreFreeBets,
  IFreebetLink,
  IFreebetCategory,
  IFreebetBetLevelMap
} from '@core/services/freeBets/free-bets.model';
import {
  IFreebetToken,
  IAccountFreebetsResponse,
  IFreebetGroup,
  IAccFreebetsResponseModel
} from '@app/bpp/services/bppProviders/bpp-providers.model';
import { ISportEvent } from '@core/models/sport-event.model';
import { FreeBetsDialogComponent } from '@shared/components/freeBetsDialog/free-bets-dialog.component';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { BppService } from '@app/bpp/services/bpp/bpp.service';
import { TimeService } from '@core/services/time/time.service';
import { SessionService } from '@authModule/services/session/session.service';
import { StorageService } from '@core/services/storage/storage.service';
import { UserService } from '@core/services/user/user.service';
import { ModuleExtensionsStorageService } from '@core/services/moduleExtensionsStorage/module-extensions-storage.service';
import { SiteServerService } from '@core/services/siteServer/site-server.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { IMarket } from '@core/models/market.model';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { IClassModel } from '@core/models/class.model';
import { ICategory } from '@core/models/category.model';
import { IEventClassModel } from '@core/models/ss-get-events-by-type-response.model';
import { IMarketEntity } from '@core/models/market-entity.model';
import { IGroupedOutcome } from '@shared/models/scorecast.model';
import { LocaleService } from '@core/services/locale/locale.service';
import { DeviceService } from '@core/services/device/device.service';
import { SportsConfigHelperService } from '@sb/services/sportsConfig/sport-config-helper.service';

@Injectable()
export class FreeBetsService {
  static BET_LEVELS = ['SELECTION', 'MARKET', 'EVENT', 'TYPE', 'CLASS'];
  static EVENT_LEVELS = ['SELECTION', 'MARKET', 'EVENT'];

  public isFRFreeBets: BehaviorSubject<any> = new BehaviorSubject({} as IFreebetToken);
  private freebetsGroup$: Subject<IFreebetGroup> = new Subject();
  private freeBetsState: IFreeBetState;
  private closestExpiringFreeBet: IFreebetToken;
  private readonly title = 'freeBetsFactory';
  
  constructor(
    protected siteServerService: SiteServerService,
    protected modulesExtensionsStorage: ModuleExtensionsStorageService,
    protected user: UserService,
    protected pubsubService: PubSubService,
    protected storage: StorageService,
    protected sessionService: SessionService,
    protected timeService: TimeService,
    protected bppService: BppService,
    protected nativeBridge: NativeBridgeService,
    protected dialogService: DialogService,
    protected routingHelperService: RoutingHelperService,
    protected filtersService: FiltersService,
    protected locale: LocaleService,
    protected deviceService: DeviceService,
    protected sportsConfigHelperService: SportsConfigHelperService
  ) {
    this.freeBetsState = this.getInitFreebetsState();

    this.pubsubService.subscribe('freeBetsFactory', this.pubsubService.API.STORE_FREEBETS_ON_REFRESH, () => {
      this.getFreeBets(true).subscribe();
    });

    this.pubsubService.subscribe(this.title, this.pubsubService.API.STORE_FREEBETS, (data: IStoreFreeBets & {isPageRefresh?: boolean}) => {
      return data ? this.store(this.user.username, data, data.isPageRefresh) : this.getFreeBets().subscribe();
    });

    /**
     * Clear freebets state after user logs out.
     */
    this.pubsubService.subscribe(this.title, this.pubsubService.API.SESSION_LOGOUT, () => {
      this.unsetfreeBetstate();
      this.onFreeBetUpdated(this.freeBetsState);
      this.pubsubService.publish(this.pubsubService.API.NOTIFICATION_HIDE);
    });
  }

  getFreeBet(freeBetId: string): Observable<IFreebetToken> {
    return this
      .getFreeBets().pipe(
      concatMap((freeBets: IFreebetToken[]) => {
        const freeBet = _.findWhere(freeBets, { freebetTokenId: freeBetId });
        return freeBet ? observableOf(freeBet) : throwError(freeBet);
      }),
      concatMap((freeBet: IFreebetToken) => {
        return this.getFreeBetWithBetNowLink(freeBet);
      }),
      catchError(err => {
        // eslint-disable-next-line no-console
        console.info(`No freebet available by ID ${freeBetId}`, err);
        return throwError(freeBetId);
      }));
  }

  /**
   * @param isSessionRefresh - passed to method when login session is refreshed. sleep or reload page
   */
  getFreeBets(isSessionRefresh?: boolean, isFreeRide?: boolean): Observable<IFreebetToken[]> {
    return this.user.isInShopUser() ? observableOf([]) : observableFrom(this.sessionService.whenProxySession()).pipe(
      concatMap(() => this.processFreebetsRequest(isSessionRefresh, isFreeRide)));
  }

  getFreeBetsData(): IFreebetToken[] {
    const freeBetsStorage: string = this.storage.get(`freeBets-${this.user.username}`);
    return  _.isString(freeBetsStorage) ? JSON.parse(freeBetsStorage) : [];
  }

  getFreeBetsSum(): string {
    const freeBetsData: IFreebetToken[] = this.getFreeBetsData();
    const sum =  _.reduceRight(_.pluck(freeBetsData, 'freebetTokenValue'), (item, num) => {
      return Number(item) + Number(num);
    }, 0).toFixed(2);

    return this.filtersService.currencyPosition(sum, this.user.currencySymbol);
  }

  showFreeBetsInfo(): Observable<void> {
    return Observable.create((observer: Observer<void>) => {
      const hideFreeBetsForUser: boolean = this.storage.get(`hideFreeBetsFor${this.user.username}`);
      const freeBetsData = this.getFreeBetsData();
      this.pubsubService.publish('FREEBET_UPDATE_LOGIN',[freeBetsData]);
      const freeBetsSum = this.getFreeBetsSum();

      if (!hideFreeBetsForUser && freeBetsData.length && this.storage.getCookie('sportsbookToken')) {
        this.storage.set(`hideFreeBetsFor${this.user.username}`, true);
        this.pubsubService.publish(this.pubsubService.API.USER_INTERACTION_REQUIRED);
        this.dialogService.openDialog(
          DialogService.API.freeBetsDialog,
          FreeBetsDialogComponent,
          false, {
            freeBetsSum,
            currencySymbol:this.user.currencySymbol,
            freeBetsData: _.each(freeBetsData, (item: IFreebetToken) => {
              const expDate = item.freebetTokenExpiryDate,
                tempDate = new Date(expDate.replace(/-/g, '/'));
              item.freebetTokenExpiryDate = this.timeService.formatByPattern(tempDate, 'dd/MM/yyyy');
            }),
            onBeforeClose: () => {
              observer.next(null);
              observer.complete();
            }
          }
        );
      } else {
        observer.next(null);
        observer.complete();
      }
    });
  }

  /**
   * Perfroms check if free bet icon should be displayed.
   * @param event
   * @return {boolean}
   */
  isFreeBetVisible(event: ISportEvent): boolean {
    // Free bet icon should not be visible for anonymous user
    if (!this.user.status) {
      return false;
    }

    return _.some(this.freeBetsState.data, (freeBet: IFreebetToken) => {
      if (freeBet.tokenPossibleBet) {
        const freeBetId = Number(freeBet.tokenPossibleBet.betId);
        const { id, typeId, classId, categoryId, markets } = event;

        return {
          SELECTION: _.some(markets,
            (marketEntity: IMarket) => _.some(marketEntity.outcomes, outcomeEntity => freeBetId === Number(outcomeEntity.id))),
          MARKET: _.some(markets, (marketEntity: IMarket) => freeBetId === Number(marketEntity.id)),
          EVENT: freeBetId === id,
          TYPE: freeBetId === Number(typeId),
          CLASS: freeBetId === classId,
          CATEGORY: freeBetId === Number(categoryId)
        }[freeBet.tokenPossibleBet.betLevel] || false;
      }

      return false;
    });
  }

  store(username: string, params: IStoreFreeBets, isPageRefresh?: boolean): void {
    const storageFreeBets: string = this.storage.get(`freeBets-${username}`),
      freeBetsData: string = _.isString(storageFreeBets) ? storageFreeBets : JSON.stringify(storageFreeBets);

    if (params.error) {
      // eslint-disable-next-line no-console
      console.info('Freebets server error:', params.error);
      this.unsetfreeBetstate();
      this.freeBetsState.freeBetFanzoneData =[];
    } else {
      if (params.data) {
        _.each(params.data, (item: IFreebetToken) => this.enhanceFreeBetItem(item));
        params.data = this.sortByExpiryDate(params.data);
      }

      if (params &&
          params.data &&
          params.data.length > 0 &&
          freeBetsData &&
          freeBetsData !== 'null' &&
          _.isEqual(
            JSON.parse(freeBetsData).map((a: IFreebetToken) => a.freebetTokenId).sort((a, b) => a < b ? -1 : a > b ? 1 : 0),
            params.data.map((a: IFreebetToken) => a.freebetTokenId).sort((a, b) => a < b ? -1 : a > b ? 1 : 0)
          )
      ) {
        this.storage.set(`hideFreeBetsFor${username}`, true);
        this.setFreeBetsState(params.data);
      } else if (params.data) {
        const frFreebets = params.data.find(bet => {
            return bet.tokenPossibleBetTags && bet.tokenPossibleBetTags.tagName && bet.tokenPossibleBetTags.tagName == 'FRRIDE';
          }
        );
        if (frFreebets) {
          this.isFRFreeBets.next(frFreebets);
        }
        const updatedFreeBets = params.data.filter(bet => {
          return (bet.tokenPossibleBetTags && bet.tokenPossibleBetTags.tagName) ? bet.tokenPossibleBetTags.tagName !== 'FRRIDE' : bet;
        });
        this.storage.set(`freeBets-${username}`, JSON.stringify(updatedFreeBets));
        this.storage.remove(`hideFreeBetsFor${username}`);
        this.setFreeBetsState(updatedFreeBets);
      } else {
        this.storage.remove(`freeBets-${username}`);
        this.unsetfreeBetstate();
        this.freeBetsState.freeBetFanzoneData =[];
      }
    }
    this.onFreeBetUpdated(this.freeBetsState, isPageRefresh);
  }
  private unsetfreeBetstate() {
    this.freeBetsState.available = false;
    this.freeBetsState.data = [];
    this.freeBetsState.betTokens = [];
    this.freeBetsState.fanZone = [];
}

  getFreeBetInBetSlipFormat(id: string): IFreebetToken | IFreeBetBetslipFormat | IFreeBet {
    const freeBetsStorage: string = this.storage.get(`freeBets-${this.user.username}`),
      freeBetsData = _.isString(freeBetsStorage) ? JSON.parse(freeBetsStorage) : [],
      freeBet: IFreebetToken = _.findWhere(freeBetsData, { freebetTokenId: id });

    return freeBet ? {
      expiry: `${freeBet.freebetTokenExpiryDate.replace(/\s/g, 'T')}.000Z`,
      id: freeBet.freebetTokenId,
      offerName: `${freeBet.freebetOfferName} `,
      value: freeBet.freebetTokenValue,
      type: freeBet.freebetTokenType
    } : undefined;
  }

  getFreeBetsState(): IFreeBetState {
    return this.freeBetsState;
  }

  getOddsBoostsWithCategories(oddsBoosts: IFreebetToken[]): Observable<IFreebetToken[]> {
    const observables = [];
    const boostsByBetLevels = _.groupBy(oddsBoosts, (boost: IFreebetToken) => {
      return boost.tokenPossibleBet ? boost.tokenPossibleBet.betLevel : 'ANY';
    });

    _.each(boostsByBetLevels, (freeBets: IFreebetToken[], level: string) => {
      const uniqLevelIDs = this.getUniqBetIds(freeBets);
      if (FreeBetsService.BET_LEVELS.indexOf(level) > -1) {
        observables.push(this.getLevelEventsDataByIDs(level, uniqLevelIDs));
      } else if (level === 'CATEGORY') {
        observables.push(this.getCategoriesDataByIDs(uniqLevelIDs));
      } else {
        observables.push(observableOf({}));
      }
    });

    return observableCombineLatest(observables).pipe(map((data: IFreebetBetLevelMap[]) => {
      const levelsData = _.extend({}, ...data);

      _.each(oddsBoosts, (boost: IFreebetToken) => {
        if (boost.tokenPossibleBet && levelsData[boost.tokenPossibleBet.betLevel] &&
          levelsData[boost.tokenPossibleBet.betLevel][boost.tokenPossibleBet.betId]) {
          const category = levelsData[boost.tokenPossibleBet.betLevel][boost.tokenPossibleBet.betId];
          boost.categoryId = category.categoryId;
          boost.categoryName = category.categoryName;
          boost.betNowLink = category.betNowLink;
        } else {
          boost.betNowLink = this.getBetNowLink({categoryId: undefined});
        }
      });
      return oddsBoosts;
    }));
  }

  getCategoriesDataByIDs(uniqIDs: string[]): Observable<IFreebetBetLevelMap> {
    const CATEGORY = {};
    return observableFrom(this.siteServerService.getCategories(uniqIDs)).pipe(concatMap((data: ICategory[]) => {
      _.each(data, (category: ICategory) => {
        CATEGORY[category.id] = this.getEventData(category.id, category.name);
      });
      return observableOf({ CATEGORY });
    }));
  }

  getLevelEventsDataByIDs(betlevel: string, uniqIDs: Array<string>): Observable<IFreebetBetLevelMap> {
    const levelEventMap = {};
    return observableFrom(this.siteServerService.getData(betlevel, uniqIDs, true)).pipe(
    concatMap((data: Array<{}>) => {
      _.each(data, (sportEvent: IEventClassModel) => {
        let eventIds;
        const levelData = this.getIds(sportEvent);

        levelEventMap[betlevel] = levelEventMap[betlevel] || {};

        if (betlevel === 'TYPE') {
          eventIds = sportEvent.class.children.map((event: IClassModel) => event.type.id);
        } else if (betlevel === 'SELECTION') {
          eventIds = this.getSelectionOutcomeIds(sportEvent);
        } else if (betlevel === 'MARKET') {
          eventIds = sportEvent.event.children.map((market: IMarketEntity) => market.market.id);
        } else {
          eventIds = [levelData.id];
        }
        _.each(eventIds, (id: string) => {
          levelEventMap[betlevel][id] = this.getEventData(
            Number(levelData.categoryId),
            levelData.categoryName,
            levelData.eventData
          );
        });
      });
      return observableOf(levelEventMap);
    }));
  }

  getFreeBetWithBetNowLink(freeBet: IFreebetToken): Observable<IFreebetToken> {
    const tokenPossibleBet = freeBet.tokenPossibleBet || { betId: null, betLevel: null };
    const tokenPossibleBets = freeBet.tokenPossibleBets || [];
    if(tokenPossibleBets.length > 1) {
      tokenPossibleBets.forEach(list => {
        if(['any', 'any_sports'].includes(list.betLevel.toLocaleLowerCase())) {
          freeBet.betNowLink = '/';
        }
      });
      if(freeBet.betNowLink === '/') {
        return observableOf(freeBet);
      }
    }
    const { betId, betLevel } = tokenPossibleBet;
    freeBet.betNowLink = '/';
    if(betLevel === 'ANY_POOLS') {
      freeBet.betNowLink = '/horse-racing';
      return observableOf(freeBet);
    }

    if (betId && _.indexOf(FreeBetsService.BET_LEVELS, betLevel) > -1) {
      return observableFrom(this.siteServerService.getData(betLevel, [betId], false)).pipe(
        concatMap((data: ISportEvent[]) => {
          return data ? observableOf(this.getBetNowLink(this.getIds(data))) :
            throwError(`Can not fetch event ${betId}`);
        }),
        map((betNowLink: string) => {
          freeBet.betNowLink = betNowLink;
          return freeBet;
        }),
        catchError(error => {
          // eslint-disable-next-line no-console
          console.info(`Error loading Events by ${betLevel} for bet ${betId}`, error);
          return observableOf(freeBet);
        }));
    } else if (betLevel === 'CATEGORY') {
      freeBet.betNowLink = this.getBetNowLink({ categoryId: betId });
    }

    return observableOf(freeBet);
  }

  getFreeBetAvailableMessage(): string {
    return this.locale.getString('bma.freebetsAvailableMessage');
  }

  getHideFreeBetIDs(): string[] {
    const hideFreeBetIDs: string = this.storage.get(`hideFreeBetIDs-${this.user.username}`);
    return _.isString(hideFreeBetIDs) ? JSON.parse(hideFreeBetIDs) : [];
  }

  getBetLevelName(betId: string, betLevel: string,freebetTokenDisplayText?:string,hasDisplayText:boolean=true): Observable<any> {
    if (freebetTokenDisplayText && hasDisplayText) {
      return observableOf(freebetTokenDisplayText);
    }
    else if (FreeBetsService.BET_LEVELS.includes(betLevel)) {
      return observableFrom(this.siteServerService.getData(betLevel, [betId], false)).pipe(
        map((data: any) => {
          if (FreeBetsService.EVENT_LEVELS.includes(betLevel)) {
            return data.event.name;
          } else if (betLevel === 'TYPE') {
            return data.class.children[0].type.name;
          } else {
            return data.class.name;
          }
        })
      );
    } else if (betLevel === 'CATEGORY') {
      return observableFrom(this.siteServerService.getCategories([betId])).pipe(
        map((data: ICategory[]) => {
          return data[0].name;
        })
      );
    } else if(betLevel === 'ANY_POOLS') {
        return observableOf(freebetTokenDisplayText);
    }

    return observableOf('');
  }

  /**
   * Groups freebets based on sport name.
   * To find out sport name we need to make SS Api call.
   * @param freebets {IFreebetToken[]}
   * @returns observable
   */

  groupByName(freebets: IFreebetToken[],hasDisplayText:boolean=true): Observable<IFreebetGroup> {
    const observables = [];
    const betIDS = {toteClassId: '321',horseRacing: '223',hrCategory: '21'}
    const allSports = this.locale.getString('sb.allSports');  
    const fbIds = _.groupBy(freebets, (freeBet: IFreebetToken) => {
    let betId: string | number = '', betLevel = '';
    if(freeBet.tokenPossibleBets && freeBet.tokenPossibleBets.length > 0) { 
      let betLevelId;
      const list = [];
      freeBet.tokenPossibleBets.forEach(item => {
        betId = item.betId;
        betLevel = item.betLevel;
        if((betLevel=== 'CLASS' && (betId === betIDS.toteClassId || betId === betIDS.horseRacing)) || (betId === '' && betLevel === 'ANY_POOLS') || (betId === betIDS.hrCategory && betLevel === 'CATEGORY')) {
          betLevelId = 'ANY_POOLS';
        } else {
          betLevelId = betId;
        }
        list.push(freeBet.freebetTokenDisplayText ? freeBet.freebetTokenDisplayText : betLevelId)
      })
      return list;
    }
  });
    _.each(fbIds, (fbList: IFreebetToken[]) => {
      let betId: string | number = '', betLevelVal = '';
    if(fbList[0].tokenPossibleBets && fbList[0].tokenPossibleBets.length > 0) { 
      betId = fbList[0].tokenPossibleBets[0].betId;
      betLevelVal = fbList[0].tokenPossibleBets[0].betLevel;
    }
      const betLevel = betId ? betLevelVal : betLevelVal === 'ANY_POOLS' ? betLevelVal : 'ANY';
      const name = fbList[0] && fbList[0].tokenPossibleBets[0] && fbList[0].tokenPossibleBets[0].name ? fbList[0].tokenPossibleBets[0].name : '';
      const freebetText=  fbList[0] && fbList[0].freebetTokenDisplayText ? fbList[0].freebetTokenDisplayText : name;
      observables.push(this.getBetLevelName(betId.toString(), betLevel,freebetText,hasDisplayText));
    });
    const groupedFreebets: IFreebetGroup = {};
    return observableCombineLatest(observables).pipe(
      mergeMap(names => {
        const betIds = Object.keys(fbIds);
        names.forEach((name, index) => {
          name === '' && (name = allSports);
          groupedFreebets[name] = !!groupedFreebets[name] ? [...groupedFreebets[name], ...fbIds[betIds[index]]] : fbIds[betIds[index]];
        });
        return observableOf(groupedFreebets);
      }));
  }

  /**
   * @param {string} [categoryName]
   * @return {*}  {boolean}
   * @memberof FreeBetsService
   */
     public isBetPack(categoryName?: string) : boolean {
      return categoryName?.replace(/ /g, '').toUpperCase() === this.locale.getString('bs.betTokenSp');
    }

  /**
   * check is fanzone freebet
   * @param {string} categoryName
   * @returns {boolean}
   */
    public isFanzone(categoryName?: string) : boolean {
      return categoryName?.replace(/ /g, '').toUpperCase() === this.locale.getString('bs.fanZoneSp');
    }

  protected enhanceFreeBetItem(item: IFreebetToken): IFreebetToken {
    if (item.freebetTokenExpiryDate) {
      const tempDate = new Date(item.freebetTokenExpiryDate.replace(/-/g, '/'));
      const timeDifferent = this.timeService.compareDate(item.freebetTokenExpiryDate);
      if (timeDifferent > 7) {
        item.usedBy = this.timeService.formatByPattern(tempDate, 'dd/MM/yyyy');
      } else {
        item.expires = `${timeDifferent} day${timeDifferent > 1 ? 's' : ''}`;
      }
    }
    item.freeBetType = this.getFreeBetType(item);
    return item;
  }
  /** 
   * @param item 
   * @returns {string} freeBetType
   */
  public getFreeBetType(item:IFreebetToken):string{
    const freeBetOfferCategory =item.freebetOfferCategories && item.freebetOfferCategories.freebetOfferCategory;
    switch (true) {
      case this.isBetPack(freeBetOfferCategory):
        return this.locale.getString('bma.betToken');
      case this.isFanzone(freeBetOfferCategory):
        return this.locale.getString('bma.fanZone');
      case !item.freebetOfferCategories:
      default:
        return this.locale.getString('bma.freeBet');
    }
  }
  private sortByExpiryDate(freeBetsArray: IFreebetToken[]): IFreebetToken[] {
    return freeBetsArray
      .sort((a, b) => {
        const aFb = Date.parse(a.freebetTokenExpiryDate.replace(/\s/g, 'T')),
          bFb = Date.parse(b.freebetTokenExpiryDate.replace(/\s/g, 'T'));

        return aFb - bFb;
      });
  }

  private getSelectionOutcomeIds(sportEvent: IEventClassModel): string[] {
    return [].concat(...sportEvent.event.children.map((market: IMarketEntity) => {
      return market.market.children.map((outcome: IGroupedOutcome) => outcome.outcome.id);
    }));
  }

  private getEventData(id: number, name: string, eventData?: ISportEvent): IFreebetCategory {
    return {
      categoryId: Number(id),
      categoryName: name,
      betNowLink: this.getBetNowLink({categoryId: String(id), eventData: eventData})
    };
  }

  private getUniqBetIds(freeBets: IFreebetToken[]): string[] {
    return _.chain(freeBets)
            .filter(bet => !!bet.tokenPossibleBet)
            .uniq(false, bet => String(bet.tokenPossibleBet.betId))
            .map(bet => String(bet.tokenPossibleBet.betId))
            .value();
  }

  private getBetNowLink({ categoryId, eventData }: IFreebetLink): string {
    let betNowLink = '/';

    if (categoryId) {
      if (eventData) {
        betNowLink += this.routingHelperService.formEdpUrl(eventData);
      } else {
        this.sportsConfigHelperService.getSportPathByCategoryId(Number(categoryId)).subscribe((sportPath: string) => {
          betNowLink += this.getSportlink(categoryId, sportPath);
        });
      }
    }

    return betNowLink;
  }

  private getSportlink(categoryId: string, sportPath: string): string {
    const outOfSportCategories = ['horseracing', 'greyhound'];
    const outOfSportCategory = _.some(outOfSportCategories, (sport: string) =>  {
      return environment.CATEGORIES_DATA.racing[sport].id === categoryId;
    });
    return outOfSportCategory ? `${sportPath}` : `sport/${sportPath}`;
  }

  private getIds(betData): { categoryId: string; eventData: ISportEvent; id: string; categoryName: string } {
    const eventData = betData && betData.event;
    const classData = (betData && betData.class) || {};
    const { categoryId, categoryName, id } = eventData || classData;

    return { id, categoryId, categoryName, eventData };
  }

  private processFreebetsRequest(isSessionRefresh?: boolean, isFreeRide?: boolean): Observable<IFreebetToken[]> {
    // on page refresh get freebets from main request with all freebets data.
    const method = isSessionRefresh ? 'allAccountFreebets' : 'accountFreebets';

    // SPORTS param passed to get correct filtered freebets in response
    return this.bppService.send(method, 'SPORTS').pipe(
      shareReplay(1),
      map((body: IAccountFreebetsResponse) => {
        const freeBets = body.response.model.freebetToken;
        _.each(freeBets, (item: IFreebetToken) => this.enhanceFreeBetItem(item));

        this.store(this.user.username, { data: freeBets, error: null }, isSessionRefresh);
        this.pubsubService.publish('FREEBET_UPDATE_LOGIN',[this.freeBetsState.data]);
        return this.freeBetsState.freeBetFanzoneData;
      }));
  }

  public getAccLimitFreeBetReq(): Observable<IAccFreebetsResponseModel> {
    const method = 'accountFreebetsWithLimits';
    // SPORTS param passed to get correct filtered freebets in response
    return this.bppService.send(method, 'SPORTS').pipe(
      shareReplay(1),
      map((body: IAccountFreebetsResponse) => {
       const toteBetPacks = [];
       body.response.model.freebetToken && body.response.model.freebetToken.forEach(freeBet => {
          if((freeBet.tokenPossibleBet.betLevel === 'ANY_POOLS' || freeBet.tokenPossibleBet.betLevel ==='ANY') && (freeBet.freebetOfferCategories && freeBet.freebetOfferCategories.freebetOfferCategory === 'Bet Pack')) {
            toteBetPacks.push(freeBet);
           }
         });
         this.storage.set('toteBetPacks', toteBetPacks);
        return body.response.model;
      }));
  }


  private getInitFreebetsState(): IFreeBetState {
    const state = {
      available: false,
      data: []
    };
    const freeBetsStorage: string = this.storage.get(`freeBets-${this.user.username}`);

    if (freeBetsStorage) {
      const freeBetsData = _.isString(freeBetsStorage) ? JSON.parse(freeBetsStorage) : freeBetsStorage;
      state.available = freeBetsData.length > 0;
      state.data = freeBetsData;
      this.onFreeBetUpdated(state, true);
    }

    return state;
  }

  private onFreeBetUpdated(freeBetsState: IFreeBetState, isPageRefresh?: boolean): void {
    this.nativeBridge.onFreeBetUpdated(!!freeBetsState.available, freeBetsState.data);
    this.pubsubService.publish(this.pubsubService.API.FREEBETS_UPDATED, [freeBetsState, isPageRefresh]);
  }

  private setFreeBetsState(data: IFreebetToken[]): void {
    this.freeBetsState.data = data.filter((fb => {return ((!fb.freebetOfferCategories) || (!this.isBetPack(fb && fb.freebetOfferCategories && fb.freebetOfferCategories.freebetOfferCategory) && !this.isFanzone(fb && fb.freebetOfferCategories && fb.freebetOfferCategories.freebetOfferCategory))) }));
    this.freeBetsState.betTokens = data.filter(fb => this.isBetPack(fb.freebetOfferCategories?.freebetOfferCategory));
    this.freeBetsState.fanZone = data.filter(fb => this.isFanzone(fb.freebetOfferCategories?.freebetOfferCategory));
    this.freeBetsState.freeBetFanzoneData = data.filter((fb => {return ((!fb.freebetOfferCategories) || !this.isBetPack(fb && fb.freebetOfferCategories && fb.freebetOfferCategories.freebetOfferCategory)) }));
    this.freeBetsState.available = this.freeBetsState.freeBetFanzoneData.length > 0;
  }
}
