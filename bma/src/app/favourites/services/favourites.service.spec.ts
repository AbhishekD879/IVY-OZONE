import { FavouritesService } from './favourites.service';
import { of as observableOf, throwError } from 'rxjs';
import { ISystemConfig } from '@core/services/cms/models';
import { Deferred } from '@app/favourites/services/deferred.class';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { fakeAsync, tick } from '@angular/core/testing';

xdescribe('FavouritesService', () => {
  let service;

  let userService;
  let favouritesStorageService;
  let pubSubService;
  let cmsService;
  let deviceService;
  let gtmService;
  let timeService;
  let routingStateService;

  const favouritesStorage = {
    myusername: {
      football: {
        9783453: {
          id: 9783453,
          startTime: '2019-05-20T11:05:00Z',
          stored: 1558353162403
        },
        9783516: {
          id: 9783516,
          startTime: '2019-05-20T08:31:00Z',
          stored: 1558353293405
        }
      }
    }
  };

  const sysConfigData = {
    Favourites: {
      displayOnMobile: true,
      displayOnTablet: true,
      displayOnDesktop: true,
    },
    favoritesText: 'Test favourites text'
  };

  beforeEach(() => {
    userService = {
      username: 'myUserName'
    };

    favouritesStorageService = {
      get:  jasmine.createSpy('get').and.returnValue(favouritesStorage),
      store: jasmine.createSpy()
    };

    pubSubService = {
      API: pubSubApi,
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe'),
    };

    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(observableOf(sysConfigData)),
      checkFavouritesWidget: jasmine.createSpy('checkFavouritesWidget').and.returnValue(true)
    };

    deviceService = {};

    gtmService = {
      push: jasmine.createSpy()
    };

    timeService = {
      daysDifference: jasmine.createSpy().and.returnValue(10)
    };

    routingStateService = {
      getCurrentSegment: jasmine.createSpy().and.returnValue('inPlay'),
      getCurrentUrl: jasmine.createSpy().and.returnValue('/home')
    };

    service = new FavouritesService(
      userService,
      favouritesStorageService,
      pubSubService,
      cmsService,
      deviceService,
      gtmService,
      timeService,
      routingStateService
    );

    service.lastActionDefer = new Deferred();
  });

  it('addEventListeners', () => {
    pubSubService.subscribe.and.callFake((a, method, cb) => {
      if (method === 'SUCCESSFUL_LOGIN') {
        spyOn(service, 'callLastAction');
        cb();
        expect(service.callLastAction).toHaveBeenCalled();
      }
    });
    service.addEventListeners();

    expect(pubSubService.subscribe).toHaveBeenCalledWith('favouritesService', pubSubService.API.SUCCESSFUL_LOGIN, jasmine.any(Function));
  });

  it('getFavoritesText', () => {
    service.getFavoritesText().subscribe((res) => {
      expect(res).toBe('Test favourites text');
    });
  });

  describe('addHandlerMethod', () => {
    it('addHandlerMethod', fakeAsync(() => {
      const handlerMethodName = jasmine.createSpy('handlerMethodName').and.returnValue(Promise.resolve('eventIdMessage'));
      const actionMessage = 'added';

      service.addHandlerMethod(handlerMethodName, actionMessage, {event: {id: 1}} as any)
        .then(() => {
          expect(handlerMethodName).toHaveBeenCalled();
          expect(service.pubSubService.publish).toHaveBeenCalledWith(service.pubSubService.API.EVENT_ADDED);
        });
      tick();
    }));

    it('addHandlerMethod', fakeAsync(() => {
      const handlerMethodName = jasmine.createSpy('handlerMethodName').and.returnValue(Promise.resolve('eventIdMessage'));
      const actionMessage = 'removed';

      service.addHandlerMethod(handlerMethodName, actionMessage, {event: {id: 1}} as any)
        .then(() => {
          expect(handlerMethodName).toHaveBeenCalled();
          expect(service.pubSubService.publish).toHaveBeenCalledWith(service.pubSubService.API.EVENT_REMOVED, 'eventIdMessage');
        });
      tick();
    }));

    it('should reject listeners',  fakeAsync(() => {
      const handlerMethodName = jasmine.createSpy('handlerMethodName').and.returnValue(Promise.reject('Error'));

      service.rejectListeners = jasmine.createSpy('rejectListeners');
      service.syncToNative = jasmine.createSpy('syncToNative');

      service.addHandlerMethod(handlerMethodName, 'actionMessage', {event: {id: 1}} as any).catch(() => {
          tick();
          expect(service.rejectListeners).toHaveBeenCalled();
        });
    }));

    it('should not publish anything and sync to native',  fakeAsync(() => {
      const handlerMethodName = jasmine.createSpy('handlerMethodName').and.returnValue(Promise.resolve('eventIdMessage'));
      service.syncToNative = jasmine.createSpy('syncToNative');

      deviceService.isWrapper = true;
      service.addHandlerMethod(handlerMethodName, 'actionMessage', {event: {id: 1}, isSyncWithNative: true} as any).then(() => {
        tick();
        expect(pubSubService.publish).not.toHaveBeenCalled();
        expect(service.syncToNative).toHaveBeenCalled();
      });
    }));
  });

  describe('getUserName', () => {
    it('should return user name', () => {
      const userName = service.getUserName();

      expect(userName).toEqual('myusername');
    });

    it('should not return user name', () => {
      userService.username = null;
      const userName = service.getUserName();

      expect(userName).toEqual(null);
    });
  });

  describe('invokeAuthorizedAction', () => {
    const successesFunction = () => 'successesFunction';

    it('when user is logged in', () => {
      spyOn(service, 'isUserLoggedIn').and.returnValue(true);
      const actualResult = service.invokeAuthorizedAction(successesFunction);

      expect(actualResult).toEqual('successesFunction');
    });

    it('when user is not logged in', () => {
      spyOn(service, 'isUserLoggedIn').and.returnValue(false);
      const actualResult = service.invokeAuthorizedAction(successesFunction);

      expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.OPEN_LOGIN_DIALOG, { moduleName: 'favourites' });
      expect(actualResult).toEqual(service.lastActionDefer.promise);
    });
  });

  describe('getCount', () => {
    it('when user is logged in', () => {
      spyOn(service, 'isUserLoggedIn').and.returnValue(true);
      spyOn(service, 'removeExpired').and.returnValue({
        first: '',
        second: '',
      });
      const actualResult = service.getCount('football');

      expect(actualResult).toEqual(2);
    });

    it('when user is not logged in', () => {
      spyOn(service, 'isUserLoggedIn').and.returnValue(false);
      const actualResult = service.getCount('sportName');

      expect(actualResult).toEqual(0);
    });
  });

  it('generateFavouriteEvent', () => {
    const event = {
      id: '123',
      startTime: 'startTime',
      categoryId: 'categoryId',
      displayOrder: 1
    } as any;
    const expectedResult = {
      id: '123',
      startTime: 'startTime'
    };
    service.favouriteEventModel = [
      'id',
      'startTime'
    ];
    const actualResult = service.generateFavouriteEvent(event);

    expect(actualResult).toEqual(expectedResult);
  });

  describe('#addEventToStorage', () => {
    const event = {
      id: 9783454,
      startTime: '2019-05-20T09:31:00Z'
    } as any;
    const gaObject = {
      event: 'trackEvent',
      eventCategory: 'favourites',
      eventAction: 'add',
      eventLabel: 'favourite icon',
      location: 'home'
    };
    const data = Object.assign(favouritesStorage);
    data.myusername.football['9783454'] = {
      stored: Date.now(),
      id: 9783454,
      startTime: '2019-05-20T09:31:00Z'};

    beforeEach(() => {
      spyOn(service, 'buildPath');
    });

    it('should add event to storage', () => {
      const config = {
        sportName: 'football'
      };
      service.addEventToStorage(event, config);

      expect(service.buildPath).toHaveBeenCalledWith(favouritesStorage, 'myusername', 'football');
      expect(service.gtmService.push).toHaveBeenCalledWith('trackEvent', gaObject);
      expect(service.favouritesStorageService.store).toHaveBeenCalledWith(data);
    });

    it('ga object when there is location in the config', () => {
      const gaObject2 = Object.assign(gaObject);
      gaObject2.location = 'location';
      const config = {
        sportName: 'football',
        location: 'location',
        fromWhere: 'fromWhere'
      };
      service.addEventToStorage(event, config);

      expect(service.gtmService.push).toHaveBeenCalledWith('trackEvent', gaObject2);
    });
    it('return promise reject when no sportname', fakeAsync(() => {
      const config = {
        sportName: '',
        location: 'location',
        fromWhere: 'fromWhere'
      };
      const errorHandler = jasmine.createSpy('errorHandler');

      const actualResult = service.addEventToStorage(event, config);
      actualResult.catch(errorHandler);
      tick();
      expect(errorHandler).toHaveBeenCalledWith('Error while adding event: 9783454 to Favourites - unknown sport!');
    }));
  });


  describe('#removeEventToStorage', () => {
    const event = {
      id: 9783454,
      startTime: '2019-05-20T09:31:00Z'
    } as any;
    const gaObject = {
      event: 'trackEvent',
      eventCategory: 'favourites',
      eventAction: 'remove',
      eventLabel: 'favourite icon',
      location: 'home'
    };
    const data = Object.assign(favouritesStorage);
    data.myusername.football['9783454'] = {
      stored: Date.now(),
      id: 9783454,
      startTime: '2019-05-20T09:31:00Z'};

    it('should remove event from storage', () => {
      const config = {
        sportName: 'football'
      };
      service.removeEventFromStorage(event, config);

      expect(service.gtmService.push).toHaveBeenCalledWith('trackEvent', gaObject);
      expect(service.favouritesStorageService.store).toHaveBeenCalledWith(data);
    });

    it('ga object when there is location in the config', () => {
      const gaObject2 = Object.assign(gaObject);
      gaObject2.location = 'location';
      const config = {
        sportName: 'football',
        location: 'location',
        fromWhere: 'fromWhere'
      };
      service.removeEventFromStorage(event, config);

      expect(service.gtmService.push).toHaveBeenCalledWith('trackEvent', gaObject2);
    });

    it('return promise reject when no sportname', fakeAsync(() => {
      const config = {
        sportName: '',
        location: 'location',
        fromWhere: 'fromWhere'
      };
      const errorHandler = jasmine.createSpy('errorHandler');

      const actualResult = service.removeEventFromStorage(event, config);
      actualResult.catch(errorHandler);
      tick();
      expect(errorHandler).toHaveBeenCalledWith('Error while removing event: 9783454 from Favourites - unknown sport!');
    }));
  });

  it('getSegment', () => {
    routingStateService.getCurrentSegment = jasmine.createSpy('getCurrentSegment').and.returnValue('inPlay');
    routingStateService.getCurrentUrl = jasmine.createSpy('getCurrentUrl').and.returnValue('/in-play');
    expect(service.getSegment()).toBe('in play');
    expect(routingStateService.getCurrentSegment).toHaveBeenCalled();
    expect(routingStateService.getCurrentUrl).toHaveBeenCalled();

    routingStateService.getCurrentSegment = jasmine.createSpy('getCurrentSegment').and.returnValue('currentSegment');
    routingStateService.getCurrentUrl = jasmine.createSpy('getCurrentUrl').and.returnValue('/in-play');
    expect(service.getSegment()).toBe('unknown.location');

    routingStateService.getCurrentSegment = jasmine.createSpy('getCurrentSegment').and.returnValue('inPlay');
    routingStateService.getCurrentUrl = jasmine.createSpy('getCurrentUrl').and.returnValue('/home');
    expect(service.getSegment()).toBe('home');
    expect(routingStateService.getCurrentSegment).toHaveBeenCalled();
    expect(routingStateService.getCurrentUrl).toHaveBeenCalled();
  });

  it('#showFavourites should get system config and check favourites', () => {
    service.showFavourites().subscribe((config: ISystemConfig) => {
      expect(cmsService.getSystemConfig).toHaveBeenCalled();
      expect(cmsService.checkFavouritesWidget).toHaveBeenCalledWith(sysConfigData);
      expect(service.isFavouritesEnabled).toBeTruthy();
    });
  });

  it('#isFavourite reject', fakeAsync(() => {

    const errorHandler = jasmine.createSpy('errorHandler');

    const actualResult = service.isFavourite({id: '123123'}, 'football');
    actualResult.catch(errorHandler);
    tick();
    expect(errorHandler).toHaveBeenCalledWith
    ('Event id: 123123, - was not found in favourites or wrong sport was passed or user is not logged in.');
  }));

  it('#isFavourite resolve', fakeAsync(() => {
    const Handler = jasmine.createSpy('Handler');
    const actualResult = service.isFavourite({id: '9783453'}, 'football');
    actualResult.then(Handler);
    tick();
    expect(Handler).toHaveBeenCalled();
  }));

  it('#isUserAndEventsReady falsy ', () => {
    const event = {
      id: 9783454,
      startTime: '2019-05-20T09:31:00Z'
    } as any;
    const config = {
      sportName: '',
      location: 'location',
      fromWhere: 'fromWhere'
    };
    expect(service.isUserAndEventsReady(event, config)).toBeFalsy();
  });

  it('#isUserAndEventsReady falsy ', () => {
    const event = {} as any;
    const config = {
      sportName: 'football',
      location: 'location',
      fromWhere: 'fromWhere'
    };
    expect(service.isUserAndEventsReady(event, config)).toBeFalsy();
  });

  it('#isUserAndEventsReady truthy ', () => {
    const events = [{
      id: 9783454,
      startTime: '2019-05-20T09:31:00Z'
    }] as any;
    const config = {
      sportName: 'football',
      location: 'location',
      fromWhere: 'fromWhere'
    };
    service.listeners = {};
    expect(service.isUserAndEventsReady(events, config)).toBeTruthy();
  });

  it('#isUserAndEventsReady  ', () => {
    const events = [{
      id: 9783454,
      startTime: '2019-05-20T09:31:00Z'
    }] as any;
    const config = {
      sportName: 'football',
      location: 'location',
      fromWhere: 'fromWhere'
    };
    service.listeners = {};
    expect(service.isUserAndEventsReady(events, config)).toBeTruthy();
  });


  describe('@removeExpired', () => {
    let events;

    beforeEach(() => {
      events = { 1: { id: 1 }, 2: { id: 2 }, 3: { id: 3 } } as any;
      service.removeEventFromStorage = jasmine.createSpy();
      service.isExpired = jasmine.createSpy().and.callFake(event => !!(event.id % 2));
    });

    it('should remove expired event from storage', () => {
      service.removeExpired(events);
      expect(service.removeEventFromStorage).toHaveBeenCalled();
      expect(service.isExpired).toHaveBeenCalled();
      expect(events).toEqual({ 2: { id: 2 } });
    });

    it('should remove selection from favourite icon', () => {
      const a1 = jasmine.createSpyObj('listenerA1', ['resolve']),
        a2 = jasmine.createSpyObj('listenerA2', ['resolve']),
        b1 = jasmine.createSpyObj('listenerB1', ['resolve']);

      service.listeners = { 1: { 'a1': { promise: a1 }, 'a2': { promise: a2 } }, 2: { 'b1': { promise: b1 } } };
      service.removeExpired(events);
      expect(a1.resolve).toHaveBeenCalledWith('removed');
      expect(a2.resolve).toHaveBeenCalledWith('removed');
      expect(b1.resolve).not.toHaveBeenCalled();
    });
  });

  describe('isExpired', () => {
    it('when user is logged in', () => {
      service.expirationTime = 5;
      const actualResult = service.isExpired({startTime: 123} as any);

      expect(timeService.daysDifference).toHaveBeenCalledWith(123);
      expect(actualResult).toEqual(true);
    });
  });

  describe('@getFavouritesEventsIds', () => {
    it('should get favorites ids for football', () => {
      const result = service.getFavouritesEventsIds('football');
      expect(result).toEqual([9783453, 9783516]);
    });

    it('should get favorites ids for tennis', () => {
      const result = service.getFavouritesEventsIds('tennis');
      expect(result).toEqual([]);
    });

    it('should get favorites ids for other user', () => {
      userService.username = 'otherUserName';
      const result = service.getFavouritesEventsIds('football');
      expect(result).toEqual([]);
    });
  });

  it('getFavoritesText', () => {
    service.getFavoritesText();

    expect(cmsService.getSystemConfig).toHaveBeenCalled();
  });

  it('syncToNative', () => {
    service.getFavourites = jasmine.createSpy('getFavourites').and.returnValue(observableOf({}));
    service.syncToNative();
    expect(service.getFavourites).toHaveBeenCalledWith('football');
  });

  xit('syncToNative error', () => {
    service.getFavourites = jasmine.createSpy('getFavourites').and.returnValue(
      throwError({type: 'Wrong sport was passed or user is not logged in!'})
    );
    service.syncToNative();

    expect(pubSubService.publish).not.toHaveBeenCalled();
  });

  describe('@getFavourites', () => {
    beforeEach(() => {
      service.removeExpired = jasmine.createSpy('removeExpired').and.returnValue({
        9783453: {
        id: 9783453,
        startTime: '2019-05-20T11:05:00Z',
        stored: 1558353162403
      },
        9783516: {
        id: 9783516,
        startTime: '2019-05-20T08:31:00Z',
        stored: 1558353293405
      }});
    });

    it('returns favourites', () => {
      userService.username = 'myUserName';
      service.getFavourites('football').subscribe((result) => {
        expect(result).toEqual(
          [
            {
              id: 9783453,
              startTime: '2019-05-20T11:05:00Z',
              stored: 1558353162403
            },
            {
              id: 9783516,
              startTime: '2019-05-20T08:31:00Z',
              stored: 1558353293405
            }
          ]
        );
      });
    });

    it('no favourite events', () => {
      userService.username = 'user2';
      service.isUserLoggedIn = jasmine.createSpy().and.returnValue(true);

      service.getFavourites('football').subscribe((result) => {
        expect(result).toEqual([]);
      });
    });

    it('throw error', () => {
      service.isUserLoggedIn = jasmine.createSpy().and.returnValue(false);

      service.getFavourites().subscribe((result) => {}, (err) => {
        expect(err).toEqual({type: 'Wrong sport was passed or user is not logged in!'});
      });
    });
  });

  it('should buildPath',  () => {
    const config = {a: {}};

    service.buildPath(config, 'a', 'b', 'c');

    expect(config).toEqual({'a': {'b': {'c': {}}}});
  });

  xit('should resolveListeners', () => {
    service.removeListeners = jasmine.createSpy('removeListeners');
    service.listeners = {
      1: {
        '1': { promise: new Deferred()},
        '2': { promise: new Deferred()}
      }
    };
    Object.setPrototypeOf(service.listeners['1'], {'3': { promise: new Deferred()}});
    service.resolveListeners(1, 'message');

    expect(service.removeListeners).toHaveBeenCalledWith(1);
  });

  xit('should rejectListeners',  () => {
    service.removeListeners = jasmine.createSpy('removeListeners');
    service.listeners = {
      1: {
        '1': { promise: new Deferred()},
        '2': { promise: new Deferred()}
      }
    };
    Object.setPrototypeOf(service.listeners['1'], {'3': { promise: new Deferred()}});
    service.rejectListeners(1, 'message');

    expect(service.removeListeners).toHaveBeenCalledWith(1);
  });

  describe('countListener', () => {
    it('should write listener to countListeners object and resolve promise', () => {
      service.getCount = jasmine.createSpy('getCount');
      service.countListener('listenerName', true);

      expect(service.getCount).toHaveBeenCalledWith('football');
    });

    it('should write listener to countListeners object and not resolve promise', () => {
      service.getCount = jasmine.createSpy('getCount');
      service.countListener('listenerName', false);

      expect(service.getCount).not.toHaveBeenCalledWith('football');
    });
  });

  describe('isAllFavourite', () => {
    it('should return true', fakeAsync(() => {
      const successHandler = jasmine.createSpy('successHandler');
      const errorHandler = jasmine.createSpy('errorHandler');

      service.isFavourite = jasmine.createSpy('isFavourite').and.returnValue(Promise.resolve(true));
      service.isAllFavourite([{id: 1}, {id: 2}] as any, 'sportName').then(successHandler, errorHandler);
      tick();

      expect(service.isFavourite).toHaveBeenCalledTimes(2);
      expect(successHandler).toHaveBeenCalledWith(true);
    }));

    it('should return false', fakeAsync(() => {
      const successHandler = jasmine.createSpy('successHandler');
      const errorHandler = jasmine.createSpy('errorHandler');

      service.isFavourite = jasmine.createSpy('isFavourite').and.returnValue(Promise.reject(false));
      service.isAllFavourite([{id: 1}, {id: 2}] as any, 'sportName').then(successHandler, errorHandler);
      tick();

      expect(service.isFavourite ).toHaveBeenCalledTimes(2);
      expect(successHandler).toHaveBeenCalledWith(false);
    }));
  });


  it('should removeCountListener', () => {
    service.countListeners = {
      'listenerName': {}
    };
    service.removeCountListener('listenerName');

    expect(service.countListeners['listenerName']).toBeUndefined();
    expect(service.countListeners).toEqual({});
  });

  describe('gaLocationName', () => {
    it('should return location',  () => {
      const actualResult = service.gaLocationName('fromWhere', 'location');

      expect(actualResult).toEqual('location');
    });

    it('should rerturn location from locationNamesMap',  () => {
      service.locationNamesMap = {'fromWhere': 'fromWhere'};
      const actualResult = service.gaLocationName('fromWhere', null);

      expect(actualResult).toEqual('fromWhere');
    });
  });

  describe('add', () => {
    it('should add handler method and remove event from storage',  fakeAsync(() => {
      service.isFavourite = jasmine.createSpy('isFavourite').and.returnValue(Promise.resolve());
      service.addHandlerMethod = jasmine.createSpy('addHandlerMethod');
      service.add({}, 'sportName', {}).then(() => {
        tick();
        expect(service.addHandlerMethod).toHaveBeenCalled();
      });
    }));

    it('should add handler method and add event to storage',  fakeAsync(() => {
      service.isFavourite = jasmine.createSpy('isFavourite').and.returnValue(Promise.reject('Error'));
      service.addHandlerMethod = jasmine.createSpy('addHandlerMethod');
      service.add({}, 'sportName', {});
      tick();
      expect(service.addHandlerMethod).toHaveBeenCalled();
    }));
  });

  xdescribe('addEventsArray', () => {
    beforeEach(() => {
      service.isUserLoggedIn = jasmine.createSpy('isUserLoggedIn').and.returnValue(true);
      service.rejectListeners = jasmine.createSpy('rejectListeners');
      service.resolveListeners = jasmine.createSpy('resolveListeners');
      service.refreshCount = jasmine.createSpy('refreshCount');
      service.listeners = {
        1: {'1': new Deferred()}
      };
    });

    it('should throw error',  () => {
      service.listeners = null;
      service.isFavourite = jasmine.createSpy('isFavourite');

      service.addEventsArray([], {});

      expect(service.isFavourite).not.toHaveBeenCalled();
    });

    it('should map through events resolving them', fakeAsync(() => {
      service.isFavourite = jasmine.createSpy('isFavourite').and.returnValue(Promise.resolve({}));

      service.addEventsArray([{id: 1}, {id: 2}], {sportName: 'sportName'});
      tick();

      expect(service.isFavourite).toHaveBeenCalled();
      expect(service.rejectListeners).toHaveBeenCalledWith(1, 'Event id: 1 - is already in favourites!');
    }));

    it('should map through events rejecting them',  fakeAsync(() => {
      service.isFavourite = jasmine.createSpy('isFavourite').and.returnValue(Promise.reject('Error'));
      service.addEventToStorage = jasmine.createSpy('addEventToStorage').and.returnValue(Promise.resolve({}));

      service.addEventsArray([{id: 1}, {id: 2}], {sportName: 'sportName'});
      tick();

      expect(service.addEventToStorage).toHaveBeenCalledTimes(2);
      expect(service.resolveListeners).toHaveBeenCalled();
      expect(service.refreshCount).toHaveBeenCalledWith('sportName');
    }));

    it('should map through events rejecting them',  fakeAsync(() => {
      service.isFavourite = jasmine.createSpy('isFavourite').and.returnValue(Promise.reject('Error'));
      service.addEventToStorage = jasmine.createSpy('addEventToStorage').and.returnValue(Promise.reject('Error'));

      service.addEventsArray([{id: 1}, {id: 2}], {sportName: 'sportName'});
      tick();

      expect(service.resolveListeners).not.toHaveBeenCalled();
      expect(service.refreshCount).not.toHaveBeenCalledWith('sportName');
      expect(service.rejectListeners).toHaveBeenCalledWith(1, 'Error');
    }));
  });

  it('should refresh count and add listeners', () => {
    service.refreshCount = jasmine.createSpy('refreshCount');
    service.resolveListeners = jasmine.createSpy('resolveListeners');
    service.refreshCounterAndListeners({id: 1} as any, {sportName: 'sportName'}).then((data) => {
      expect(data).toEqual({event: {id: 1}, config: {sportName: 'sportName'}});
    });

    expect(service.refreshCount).toHaveBeenCalledWith('sportName');
    expect(service.resolveListeners).toHaveBeenCalledWith(1, 'removed');
  });

  describe('removeFavouritesFormArray', () => {
    beforeEach(() => {
      service.isFavourite = jasmine.createSpy('isFavourite').and.returnValue(Promise.resolve('Resolve'));
      service.removeEventFromStorage = jasmine.createSpy('removeEventFromStorage').and.returnValue(Promise.resolve('Resolve'));
      service.refreshCounterAndListeners = jasmine.createSpy('refreshCounterAndListeners').and.returnValue(Promise.resolve('Resolve'));
      service.rejectListeners = jasmine.createSpy('rejectListeners');
    });
    it('should remove events and refresh listeners counter', fakeAsync(() => {
      service.removeFavouritesFormArray({events: [{id: 1}], config: {sportName: 'sportName'}});
      tick();

      expect(service.isFavourite).toHaveBeenCalledWith({id: 1}, 'sportName');
      expect(service.removeEventFromStorage).toHaveBeenCalledWith({id: 1}, {sportName: 'sportName'});
      expect(service.refreshCounterAndListeners).toHaveBeenCalledWith({id: 1}, {sportName: 'sportName'});
      expect(service.rejectListeners).not.toHaveBeenCalledWith();
    }));

    it('should reject listeners', fakeAsync(() => {
      service.refreshCounterAndListeners = jasmine.createSpy('refreshCounterAndListeners').and.returnValue(Promise.reject('Error'));

      service.removeFavouritesFormArray({events: [{id: 1}], config: {sportName: 'sportName'}});
      tick();

      expect(service.isFavourite).toHaveBeenCalledWith({id: 1}, 'sportName');
      expect(service.removeEventFromStorage).toHaveBeenCalledWith({id: 1}, {sportName: 'sportName'});
      expect(service.refreshCounterAndListeners).toHaveBeenCalledWith({id: 1}, {sportName: 'sportName'});
      expect(service.rejectListeners).toHaveBeenCalledWith( 1, `Event not found in favourites!`);
    }));
  });

  describe('checkingUserAndData', () => {
    it('should check user', fakeAsync(() => {
      const successHandler = jasmine.createSpy('successHandler');
      const errorHandler = jasmine.createSpy('errorHandler');

      service.isUserAndEventsReady = jasmine.createSpy('isUserAndEventsReady').and.returnValue(Promise.resolve(true));
      service.checkingUserAndData([], {}).then(successHandler, errorHandler);
      tick();

      expect(service.isUserAndEventsReady).toHaveBeenCalledWith([], {});
      expect(successHandler).toHaveBeenCalled();
      expect(errorHandler).not.toHaveBeenCalled();
    }));

    it('should check user and return error message', fakeAsync(() => {
      const successHandler = jasmine.createSpy('successHandler');
      const errorHandler = jasmine.createSpy('errorHandler');
      service.isUserAndEventsReady = jasmine.createSpy('isUserAndEventsReady').and.returnValue(Promise.resolve(false));
      service.checkingUserAndData([], {}).then(successHandler, errorHandler);
      tick();

      expect(service.isUserAndEventsReady).toHaveBeenCalledWith([], {});
      expect(successHandler).not.toHaveBeenCalled();
      expect(errorHandler).toHaveBeenCalledWith(`Error while removing eventsArray from Favourites -
    no events passed or wrong sport was passed or user is not logged in or no
    listeners passed!`);
    }));
  });

  xdescribe('removeEventsArray', () => {
    it('should removeEventsArray', fakeAsync(() => {
      const successHandler = jasmine.createSpy('successHandler');
      const errorHandler = jasmine.createSpy('errorHandler');

      service.checkingUserAndData = jasmine.createSpy('checkingUserAndData').and.returnValue(Promise.resolve({}));
      service.removeFavouritesFormArray = jasmine.createSpy('removeFavouritesFormArray');

      service.removeEventsArray([], {}).then(successHandler, errorHandler);
      tick();

      expect(successHandler).toHaveBeenCalled();
      expect(errorHandler).not.toHaveBeenCalled();
      expect(service.removeFavouritesFormArray).toHaveBeenCalledWith({});
    }));

    it('should show error in console', fakeAsync(() => {
      const successHandler = jasmine.createSpy('successHandler');
      const errorHandler = jasmine.createSpy('errorHandler');

      service.checkingUserAndData = jasmine.createSpy('checkingUserAndData').and.returnValue(Promise.reject('Error'));

      service.removeEventsArray([], {}).then(successHandler, errorHandler);
      tick();

      expect(successHandler).toHaveBeenCalledWith('Error');
      expect(errorHandler).not.toHaveBeenCalledWith();
    }));
  });

  describe('registerListener', () => {
    it('should update listeners by event id', () => {
      service.listeners = {
        1: {
          'some': {},
          'properties': {}
        },
      };
      service.registerListener({id: 1} as any, '1');

      expect(service.listeners).toEqual({
        1: {
          'some': {},
          'properties': {},
          '1': jasmine.any(Object)
        },
      });
    });

    it('should create listeners by event id', () => {
      service.listeners = {
        1: {},
      };
      service.registerListener({id: 2} as any, '2');

      expect(service.listeners).toEqual({
        1: {},
        2: {
          '2': jasmine.any(Object)
        }
      });
    });
  });

  it('should deRegisterListener',  () => {
    service.listeners = {
      1: {
        'some': {},
        'properties': {},
        '1': jasmine.any(Object)
      },
    };

    service.deRegisterListener({id: 1} as any, '1');

    expect(service.listeners).toEqual({
      1: {
        'some': {},
        'properties': {}
      },
    });
  });

  describe('callLastAction', () => {
    it('should call last action and set it to null',  () => {
      service.lastAction = jasmine.createSpy('lastAction');
      service.refreshCount = jasmine.createSpy('refreshCount');

      service.callLastAction();

      expect(service.refreshCount).toHaveBeenCalledWith('football');
      expect(service.lastAction).toEqual(null);
    });

    it('should not call last action and set it to null', () => {
      service.refreshCount = jasmine.createSpy('refreshCount');
      service.lastAction = null;

      service.callLastAction();

      expect(service.refreshCount).toHaveBeenCalledWith('football');
    });
  });

  it('should refreshCount', () => {
    service.getCount = jasmine.createSpy('getCount');
    service.countListeners = {
      '1': { promise: new Deferred()}
    };
    Object.setPrototypeOf(service.countListeners, {'2': { promise: new Deferred()}});

    service.refreshCount('sportName');

    expect(service.getCount).toHaveBeenCalledTimes(1);
  });

  describe('syncFromNative', () => {
    it('should use football favorites', () => {
      service.isUserLoggedIn = jasmine.createSpy('isUserLoggedIn').and.returnValue(true);
      service.getUserFavourites = jasmine.createSpy('getUserFavourites').and.returnValue({});
      service.syncFromNative({});

      expect(service.isUserLoggedIn).toHaveBeenCalled();
      expect(service.getUserFavourites).toHaveBeenCalledWith({}, 'myusername');
    });

    it('should not have favorites if user isn\'t log in', () => {
      service.isUserLoggedIn = jasmine.createSpy('isUserLoggedIn').and.returnValue(false);
      service.syncFromNative({});

      expect(service.isUserLoggedIn).toHaveBeenCalled();
    });
  });

  it('getUserFavourites', () => {
    const actualResult = service.getUserFavourites({USERNAME: [1, 2, 3], abra: [4, 5], kadabra: [6]}, 'username');
    const expectedResult = [1, 2, 3];

    expect(actualResult).toEqual(expectedResult);
  });
});