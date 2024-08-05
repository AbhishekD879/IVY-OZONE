import { Injectable } from '@angular/core';
import * as _ from 'underscore';

import { Deferred } from './deferred.class';
import { ISystemConfig } from '@core/services/cms/models';
import { ISportEvent } from '@core/models/sport-event.model';
import { IFavouritesConfig, IFavouritesText } from '@app/favourites/models/favourites-config.model';
import { TimeService } from '@core/services/time/time.service';
import { GtmService } from '@core/services/gtm/gtm.service';
import { DeviceService } from '@core/services/device/device.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { FavouritesStorageService } from '@app/favourites/services/favourites-storage.service';
import { UserService } from '@core/services/user/user.service';
import { RoutingState } from '@sharedModule/services/routingState/routing-state.service';
import { Observable, Subscription, of as observableOf, throwError } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable()
export class FavouritesService {

  favouriteEventModel: string[] = [
    'id',
    'startTime'
  ];
  isFavouritesEnabled: boolean;
  expirationTime: number = 0.5;
  lastAction = null;
  lastActionDefer = new Deferred();
  listeners: { [key: number]: { [key: string]: { promise: Deferred } } } = {};
  countListeners = {};
  locationNamesMap = {
    'bsreceipt': 'betslip receipt',
    'couponsDetails': 'football coupons',
    'eventMain': 'event page',
    'sport.eventMain.market': 'event page',
    'home': 'home',
    'inPlay': 'in play',
    'inPlay.allsports': 'in play',
    'inPlay.sport': 'in play',
    'sport.matches.tab': 'football matches',
    'sport.matches': 'football matches',
    'competitionTypeEvents': 'football competitions',
    'sport.display': 'football in play',
    'favourites': 'favourites page'
  };

  private readonly title = 'favouritesService';

  constructor(
    private userService: UserService,
    private favouritesStorageService: FavouritesStorageService,
    private pubSubService: PubSubService,
    private cmsService: CmsService,
    private deviceService: DeviceService,
    private gtmService: GtmService,
    private timeService: TimeService,
    private routingState: RoutingState,
  ) {
    this.addEventListeners();

    this.addEventToStorage = this.addEventToStorage.bind(this);
    this.removeEventFromStorage = this.removeEventFromStorage.bind(this);
    this.addEventsArray = this.addEventsArray.bind(this);
    this.removeEventsArray = this.removeEventsArray.bind(this);
  }

  /**
   * addEventListeners()
   */
  addEventListeners(): void {
    this.pubSubService.subscribe(this.title, this.pubSubService.API.SUCCESSFUL_LOGIN, () => {
      this.callLastAction();
    });
  }

  /**
   * getFavoritesText()
   * @returns {Observable<IFavouritesText>}
   */
  getFavoritesText(): Observable<IFavouritesText> {
    return this.cmsService.getSystemConfig().pipe(
      map((data: ISystemConfig) => data.favoritesText)
    );
  }

  /**
   * getUserName()
   * @returns {string}
   */
  getUserName(): string {
    return this.userService.username ? this.userService.username.toLowerCase() : null;
  }

  /**
   * invokeAuthorizedAction()
   * @param {Function} successesFunction
   * @returns {Promise<void>}
   */
  invokeAuthorizedAction(successesFunction: Function): Promise<void> {
    if (this.isUserLoggedIn()) {
      return successesFunction();
    }

    this.lastAction = successesFunction;
    this.pubSubService.publish(this.pubSubService.API.OPEN_LOGIN_DIALOG, { moduleName: 'favourites' });

    return this.lastActionDefer.promise;
  }

  /**
   * getCount()
   * @param {string} sportName
   * @returns {number}
   */
  getCount(sportName: string): number {
    const userName = this.getUserName(),
      data: Object = this.favouritesStorageService.get();

    let count = 0;

    if (this.isUserLoggedIn() && data[userName] && data[userName][sportName]) {
      count = Object.keys(this.removeExpired(data[userName][sportName])).length;
    }

    return count;
  }

  /**
   * buildPath()
   * @param {Object} config
   * @param {any[]} args
   */
  buildPath(config: Object, ...args: any[]) {
    const prop = args.shift();

    if (!config[prop]) {
      config[prop] = {};
    }

    if (args.length) {
      this.buildPath(config[prop], ...args);
    }
  }

  /**
   * generateFavouriteEvent()
   * @param {ISportEvent} event
   * @returns {ISportEvent}
   */
  generateFavouriteEvent(event: ISportEvent): Partial<ISportEvent> {
    const favouriteEvent = {};

    _.forEach(this.favouriteEventModel, modelProperty => {
      favouriteEvent[modelProperty] = event[modelProperty];
    });

    return favouriteEvent;
  }

  /**
   * addEventToStorage()
   * @param {ISportEvent} event
   * @param {IFavouritesConfig} config
   * @returns {Promise<number|string>}
   */
  addEventToStorage(event: ISportEvent, config: IFavouritesConfig): Promise<number | string> {
    const userName = this.getUserName(),
      data = this.favouritesStorageService.get();

    if (config.sportName) {
      this.buildPath(data, userName, config.sportName);

      data[userName][config.sportName][event.id] = _.extend(
        { stored: Date.now() }, this.generateFavouriteEvent(event)
      );

      this.pushGAState('add', this.gaLocationName(config.fromWhere, config.location));
      this.favouritesStorageService.store(data);

      return Promise.resolve(event.id);
    }

    return Promise.reject(`Error while adding event: ${event.id} to Favourites - unknown sport!`);
  }

  /**
   * removeEventFromStorage()
   * @param {ISportEvent} event
   * @param {IFavouritesConfig} config
   * @returns {Promise<number|string>}
   */
  removeEventFromStorage(event: ISportEvent, config: IFavouritesConfig): Promise<number | string> {
    const userName = this.getUserName(),
      data = this.favouritesStorageService.get();

    if (config.sportName) {
      delete data[userName][config.sportName][event.id];

      this.pushGAState('remove', this.gaLocationName(config.fromWhere, config.location));
      this.favouritesStorageService.store(data);

      return Promise.resolve(event.id);
    }

    return Promise.reject(`Error while removing event: ${event.id} from Favourites - unknown sport!`);
  }

  /**
   * resolveListeners()
   * @param {number} eventId
   * @param {string} message
   */
  resolveListeners(eventId: number, message: string): void {
    for (const id in this.listeners[eventId]) {
      if (this.listeners[eventId].hasOwnProperty(id)) {
        this.listeners[eventId][id].promise.resolve(message);
      }
    }

    this.removeListeners(eventId);
  }

  /**
   * rejectListeners()
   * @param {number} eventId
   * @param {string} message
   * @returns {Promise<string>}
   */
  rejectListeners(eventId: number, message: string): Promise<string> {
    for (const id in this.listeners[eventId]) {
      if (this.listeners[eventId].hasOwnProperty(id)) {
        this.listeners[eventId][id].promise.reject(message);
      }
    }

    this.removeListeners(eventId);
    return Promise.reject(message);
  }

  /**
   * removeListeners()
   * @param {number} eventId
   */
  removeListeners(eventId: number): void {
    delete this.listeners[eventId];
  }

  /**
   * isFavourite()
   * @param {ISportEvent} eventEntity
   * @param {sportName} sportName
   * @returns {Promise<void|string>}
   */
  isFavourite(eventEntity: ISportEvent, sportName: string): Promise<void | string> {
    const userName = this.getUserName(),
      data = this.favouritesStorageService.get(),
      isExistingFavouriteEvent = sportName && data[userName] && data[userName][sportName] && data[userName][sportName][eventEntity.id];

    if (this.isUserLoggedIn() && isExistingFavouriteEvent) {
      return Promise.resolve();
    }

    return Promise.reject(`Event id: ${eventEntity.id}, - was not found in favourites or wrong sport was passed or user is not logged in.`);
  }

  /**
   * isAllFavourite()
   * @param {ISportEvent[]} events
   * @param {string} sportName
   * @returns {Promise<any>}
   */
  isAllFavourite(events: ISportEvent[], sportName: string): Promise<any> {
    const promises = events.map(event => this.isFavourite(event, sportName)
      .then(() => true, () => false));

    return Promise.all(promises)
      .then(results => {
        return results.every(actionStatus => actionStatus);
      });
  }

  /**
   * isUserLoggedIn()
   * @returns {boolean}
   */
  isUserLoggedIn(): boolean {
    return !!this.getUserName();
  }

  /**
   * countListener()
   * @param {string} listenerName
   * @param {boolean} initRefresh
   * @returns {Promise<number>}
   */
  countListener(listenerName: string, initRefresh: boolean): Promise<number> {
    const deferred = new Deferred();

    if (initRefresh) {
      deferred.resolve(this.getCount('football'));
    }

    this.countListeners[listenerName] = { promise: deferred };

    return deferred.promise;
  }

  /**
   * removeCountListener()
   * @param {string} listenerName
   */
  removeCountListener(listenerName: string): void {
    delete this.countListeners[listenerName];
  }

  /**
   * gaLocationName()
   * @param {string} fromWhere
   * @param {string} location
   * @returns {string}
   */
  gaLocationName(fromWhere: string, location: string): string {
    const segmentName = this.getSegment();

    if (location) {
      return location;
    }

    return typeof fromWhere !== 'undefined' ? this.locationNamesMap[fromWhere] : segmentName;
  }

  /**
   * getSegment()
   * @return {string}
   */
  getSegment(): string {
    let segment = '';
    const homeSegment = 'home';
    const currentSegment = this.routingState.getCurrentSegment();
    const currentUrl = this.routingState.getCurrentUrl();
    const isHome = currentSegment.indexOf(homeSegment) >= 0 || currentUrl.startsWith(`/${homeSegment}`);

    if (isHome) {
      segment = this.locationNamesMap[homeSegment];
    } else {
      segment = this.locationNamesMap[currentSegment] || 'unknown.location';
    }

    return segment;
  }

  /**
   * pushGAState()
   * @param {string} action
   * @param {string} location
   */
  pushGAState(action: string, location: string): void {
    this.gtmService.push('trackEvent', {
      event: 'trackEvent',
      eventCategory: 'favourites',
      eventAction: action,
      eventLabel: 'favourite icon',
      location
    });
  }

  /**
   * add()
   * @param {ISportEvent} event
   * @param {string} sportName
   * @param {IFavouritesConfig} config
   * @returns {Promise<any>}
   */
  add(event: ISportEvent, sportName: string, config: IFavouritesConfig): Promise<any> {
    const eventConfig = _.extend({ sportName, isSyncWithNative: true, event }, config);

    return this.isFavourite(event, sportName)
      .then(() => this.addHandlerMethod(this.removeEventFromStorage, 'removed', eventConfig))
      .catch(() => this.addHandlerMethod(this.addEventToStorage, 'added', eventConfig));
  }

  /**
   * addHandlerMethod()
   * @param {Function} handlerMethodName
   * @param {string} actionMessage
   * @param {IFavouritesConfig} config
   * @returns {Promise<void>}
   */
  addHandlerMethod(handlerMethodName: Function, actionMessage: string, config: IFavouritesConfig): Promise<void> {
    return this.invokeAuthorizedAction(() => {
      this.resolveListeners(config.event.id, 'pending');

      return handlerMethodName(config.event, config)
        .then(eventIdMessage => {
          if (actionMessage === 'added') {
            this.pubSubService.publish(this.pubSubService.API.EVENT_ADDED);
          } else if (actionMessage === 'removed') {
            this.pubSubService.publish(this.pubSubService.API.EVENT_REMOVED, eventIdMessage);
          }

          this.refreshCount(config.sportName);
          this.resolveListeners(eventIdMessage, actionMessage);

          if (config.isSyncWithNative && this.deviceService.isWrapper) {
            this.syncToNative();
          }

          return Promise.resolve(eventIdMessage);
        }, err => {
          this.rejectListeners(config.event.id, err);
          return Promise.reject(err);
        });
    });
  }

  /**
   * addEventsArray()
   * @param {ISportEvent[]} events
   * @param {IFavouritesConfig} config
   * @returns {Promise<any>}
   */
  addEventsArray(events: ISportEvent[], config: IFavouritesConfig): Promise<any> {
    if (this.isUserLoggedIn() && events && events.length && config.sportName && this.listeners) {
      const promises = events.map(event =>
        this.isFavourite(event, config.sportName).then(() => {
            const message = `Event id: ${event.id} - is already in favourites!`;

            if (!this.listeners[event.id]) {
              console.warn(message);
            } else {
              this.rejectListeners(event.id, message);
            }

            return false;
          }, () => {
            return this.addEventToStorage(event, config).then(() => {
              this.refreshCount(config.sportName);
              this.resolveListeners(event.id, 'added');

              return true;
            }, error => {
              this.rejectListeners(event.id, error);
              return false;
            });
          }
        )
      );

      return Promise.all(promises);
    }

    return Promise.reject(`Error while adding eventsArray to Favourites - no events passed or wrong
    sport was passed or user is not logged in or no listeners passed!`);
  }

  /**
   * refreshCounterAndListeners()
   * @param {ISportEvent} event
   * @param {IFavouritesConfig} config
   * @returns {Promise<any>}
   */
  refreshCounterAndListeners(event: ISportEvent, config: IFavouritesConfig): Promise<any> {
    this.refreshCount(config.sportName);
    this.resolveListeners(event.id, 'removed');

    return Promise.resolve({ event, config });
  }

  /**
   * isUserAndEventsReady()
   * @param {ISportEvent} events
   * @param {IFavouritesConfig} config
   * @returns {boolean}
   */
  isUserAndEventsReady(events: ISportEvent[], config: IFavouritesConfig): boolean {
    return !!(this.isUserLoggedIn() && events && events.length && config.sportName && this.listeners);
  }

  /**
   * removeFavouritesFormArray()
   * @param data
   * @returns {Promise<any>}
   */
  removeFavouritesFormArray(data): Promise<any> {
    return Promise.all(data.events.map(event => this.isFavourite(event, data.config.sportName)
      .then(() => this.removeEventFromStorage(event, data.config))
      .then(() => this.refreshCounterAndListeners(event, data.config))
      .catch(error => {
        this.rejectListeners(event.id, `Event not found in favourites!`);
        return error;
      })));
  }

  /**
   * checkingUserAndData()
   * @param {ISportEvent[]} events
   * @param {IFavouritesConfig} config
   * @returns {Promise<any>}
   */
  checkingUserAndData(events: ISportEvent[], config: IFavouritesConfig): Promise<any> {
    const errorMessage = `Error while removing eventsArray from Favourites -
    no events passed or wrong sport was passed or user is not logged in or no
    listeners passed!`;

    return Promise.resolve(this.isUserAndEventsReady(events, config))
      .then(results => results ? Promise.resolve({ events, config }) : Promise.reject(errorMessage));
  }

  /**
   * removeEventsArray()
   * @param {ISportEvent[]} events
   * @param {IFavouritesConfig} config
   * @returns {Promise<any>}
   */
  removeEventsArray(events: ISportEvent[], config: IFavouritesConfig): Promise<any> {
    return this.checkingUserAndData(events, config)
      .then(data => this.removeFavouritesFormArray(data))
      .catch(error => {
        console.warn('Favourites error: ', error);
        return error;
      });
  }

  /**
   * Returns favourites from storage
   *
   * @param sportName
   * @returns {*}
   */
  getFavourites(sportName) {
    const userName = this.getUserName(),
      data = this.favouritesStorageService.get();

    if (this.isUserLoggedIn() && sportName) {

      if (data[userName] && data[userName][sportName]) {
        const events: Object = this.removeExpired(data[userName][sportName]);
        return observableOf(Object.keys(events).map(k => events[k]));
      }

      return observableOf([]);
    }

    return throwError({type: `Wrong sport was passed or user is not logged in!`});
  }

  /**
   * Returns favourites ids from storage
   *
   * @param sportName
   * @returns {*}
   */
  getFavouritesEventsIds(sportName: string): number[] {
    const userName = this.getUserName();
    const data = this.favouritesStorageService.get();

    if (data[userName] && data[userName][sportName]) {
      const events: Object = data[userName][sportName];
      return Object.keys(events).map(Number);
    }

    return [];
  }

  /**
   * removeExpired()
   * @param {ISportEvent[]} events
   * @returns {ISportEvent[]}
   */
  removeExpired(events: Object): Object {
    for (const event in events) {
      if (this.isExpired(events[event])) {
        this.removeEventFromStorage(events[event], { sportName: 'football' });
        _.forEach(this.listeners[event], (listener: Deferred) => { listener && listener.promise && listener.promise.resolve('removed'); });
        delete events[event];
      }
    }

    return events;
  }

  /**
   * isExpired()
   * @param {ISportEvent} event
   * @returns {boolean}
   */
  isExpired(event: ISportEvent): boolean {
    return this.timeService.daysDifference(event.startTime) > this.expirationTime;
  }

  /**
   * registerListener()
   * @param {ISportEvent} event
   * @param {string} id
   * @returns {Promise<void>}
   */
  registerListener(event: ISportEvent, id: string): Promise<string> {
    const deferred = new Deferred();

    if (!this.listeners[event.id]) {
      this.listeners[event.id] = {};
    }

    this.listeners[event.id][id] = { promise: deferred };

    return deferred.promise;
  }

  /**
   * deRegisterListener()
   * @param {ISportEvent} event
   * @param {string} id
   */
  deRegisterListener(event: ISportEvent, id: string): void {
    if (this.listeners?.[event.id]?.[id]) {
      if (this.listeners?.[event.id]?.[id]) {
        delete this.listeners[event.id][id];
      }
    }
  }

  /**
   * callLastAction()
   */
  callLastAction(): void {
    if (this.lastAction) {
      this.lastAction();
      this.lastAction = null;
    }

    this.refreshCount('football');
  }

  /**
   * refreshCount()
   * @param {string} sportName
   */
  refreshCount(sportName: string): void {
    for (const prop in this.countListeners) {
      if (this.countListeners.hasOwnProperty(prop)) {
        this.countListeners[prop].promise.resolve(this.getCount(sportName));
      }
    }
  }

  /**
   * syncToNative()
   * @returns {Subscription}
   */
  syncToNative(): Subscription {
    return this.getFavourites('football')
      .subscribe(favourites => {
        this.pubSubService.publish(this.pubSubService.API.SYNC_FAVOURITES_TO_NATIVE, favourites);
      },
      err => console.error('Failed to synchronize favourites: ', err)
      );
  }

  /**
   * syncFromNative()
   * @param {Object} nativeFavourites
   */
  syncFromNative(nativeFavourites: Object): void {
    const data = this.favouritesStorageService.get(),
      username = this.getUserName(),
      webFavourites = this.isUserLoggedIn() && data[username] ? data[username].football : [],
      nativeFavData = this.getUserFavourites(nativeFavourites, username),
      webFavouritesIds = _.pluck(webFavourites, 'id'),
      nativeFavouritesIds = _.pluck(nativeFavData, 'id'),
      toAdd = _.difference(nativeFavouritesIds, webFavouritesIds),
      toRemove = _.difference(webFavouritesIds, nativeFavouritesIds),
      toToggle = _.union(toAdd, toRemove);

    _.forEach(toToggle, id => {
      // @ts-ignore
      const { startTime } = _.findWhere(nativeFavData, { id }) || { startTime: null };
      // @ts-ignore
      this.add({ id, startTime }, 'football', false);
    });
  }

  /**
   * getUserFavourites()
   * @param {Object} nativeFavourites
   * @param {string} username
   * @returns {string[]}
   */
  getUserFavourites(nativeFavourites, username) {
    let favouritesList = [];

    _.forEach(nativeFavourites, (value: any[], key: string) => {
      if (username === key.toLowerCase()) {
        favouritesList = value;
      }
    });

    return favouritesList;
  }

  /**
   * showFavourites()
   * get system config and check if favourites are enabled
   */
  showFavourites(): Observable<boolean> {
    return this.cmsService.getSystemConfig()
      .pipe(map((systemConfig: ISystemConfig) => {
        this.isFavouritesEnabled = this.cmsService.checkFavouritesWidget(systemConfig);
        return this.isFavouritesEnabled;
      }));
  }
}
