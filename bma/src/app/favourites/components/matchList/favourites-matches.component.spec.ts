import { fakeAsync, tick } from '@angular/core/testing';
import { FavouritesMatchesComponent } from '@app/favourites/components/matchList/favourites-matches.component';
import { of as observableOf, throwError } from 'rxjs';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';

describe('FavouritesMatchesComponent', () => {
  let component: FavouritesMatchesComponent,
    favouritesService,
    userService,
    favouritesMatchesService,
    filtersService,
    ngZone,
    pubSubService;

  beforeEach(fakeAsync(() => {
    favouritesService = {
      getFavouritesEventsIds: jasmine.createSpy('getFavouritesEventsIds').and.returnValue([1, 2, 4]),
      getFavourites: jasmine.createSpy('getFavourites').and.returnValue(observableOf({})),
      isUserLoggedIn: jasmine.createSpy('isUserLoggedIn'),
      getFavoritesText: jasmine.createSpy('getFavoritesText').and.returnValue(observableOf({})),
      add: jasmine.createSpy().and.returnValue(Promise.resolve({}))
    };
    userService = {
      username: ''
    };
    ngZone = {
      runOutsideAngular: jasmine.createSpy('runOutsideAngular').and.callFake((fn) => fn())
    };

    pubSubService = new PubSubService(ngZone);
    spyOn(pubSubService, 'publish').and.callThrough();
    spyOn(pubSubService, 'subscribe').and.callThrough();
    spyOn(pubSubService, 'unsubscribe').and.callThrough();

    favouritesMatchesService = {
      removeMatch: jasmine.createSpy('removeMatch').and.returnValue([ { id: '01' } ]),
      unSubscribeForUpdates: jasmine.createSpy('unSubscribeForUpdates'),
      subscribeForUpdates: jasmine.createSpy('subscribeForUpdates'),
      trimFinishedEvents:  jasmine.createSpy('trimFinishedEvents'),
      getFavouritesMatches:  jasmine.createSpy('getFavouritesMatches').and.returnValue(Promise.resolve({}))
    };
    filtersService = {
      orderBy: jasmine.createSpy('filtersService.orderBy')
    };
    component = new FavouritesMatchesComponent(
      favouritesService,
      userService,
      pubSubService,
      favouritesMatchesService,
      filtersService
    );

    component.hideError = jasmine.createSpy();
    component.hideSpinner = jasmine.createSpy();
    component.showError = jasmine.createSpy();
  }));

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOnInit', () => {
    it('bsTab = true, username = \'\', isWidgetColumn = widget', () => {
      component.bsTab = true;
      component.isWidgetColumn = 'widget';
      component.widget = '';
      component.addEventListeners = jasmine.createSpy('addEventListeners');

      component.ngOnInit();

      expect(component.addEventListeners).toHaveBeenCalledTimes(1);
      expect(component.isUserLoggedIn).toBeFalsy();
      expect(component.isBsTab).toEqual('bs');
      expect(component.title).toEqual('favouritesMatchesbswidget');
      expect(component.displayPageHeader).toBeFalsy();
      expect(favouritesService.getFavoritesText).toHaveBeenCalled();
    });

    it('bsTab = false, username = Nick, isWidgetColumn = undefined', () => {
      userService.username = 'Nick';
      component.bsTab = false;
      component.isWidgetColumn = undefined;
      component.widget = undefined;
      component.addEventListeners = jasmine.createSpy('addEventListeners');

      component.ngOnInit();

      expect(component.isBsTab).toEqual('');
      expect(component.isUserLoggedIn).toBeTruthy();
      expect(component.displayPageHeader).toBeTruthy();
      expect(favouritesService.getFavourites).toHaveBeenCalledWith('football');
    });
  });

  it('#init', fakeAsync(() => {
    component.isUserLoggedIn = true;
    component.orderMatches = jasmine.createSpy();
    favouritesService.getFavourites.and.returnValue(observableOf([]));
    favouritesMatchesService.getFavouritesMatches = jasmine.createSpy().and.returnValue(Promise.resolve([{id: 1}, {id: 2}]));

    component.init().subscribe(() => {
      expect(component.orderMatches).toHaveBeenCalled();
      expect(favouritesMatchesService.subscribeForUpdates).toHaveBeenCalled();
    });

    tick();
  }));

  it('#init error logged in', fakeAsync(() => {
    component.title = 'title';
    component.isUserLoggedIn = true;
    favouritesService.getFavourites.and.returnValue(throwError({type: `Wrong sport was passed or user is not logged in!`}));

    component.init().subscribe(() => {}, err => {
      expect(component.matches).toEqual([]);
      expect(component.applyingParams).toBeFalsy();
      expect(err).toEqual({type: `Wrong sport was passed or user is not logged in!`});
      expect(component.showError).toHaveBeenCalled();
      expect(component.hideSpinner).toHaveBeenCalled();
    });
    tick();
  }));

  it('#init error logged out', fakeAsync(() => {
    component.title = 'title';
    component.isUserLoggedIn = false;
    favouritesService.getFavoritesText.and.returnValue(throwError('error'));

    component.init().subscribe(() => {}, err => {
      expect(component.applyingParams).toBeFalsy();
      expect(err).toEqual('error');
    });
    tick();
  }));

  it('#ngOnDestroy', () => {
    component.title = 'title';
    component['getFavouritesSubscription'] = { unsubscribe: jasmine.createSpy() } as any;

    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('title');
    expect(favouritesMatchesService.unSubscribeForUpdates).toHaveBeenCalledTimes(1);
    expect(component['getFavouritesSubscription'].unsubscribe).toHaveBeenCalledTimes(1);
  });

  it('#trackById', () => {
    const event = { id: 1, categoryName : 'categoryName'} as any;
    const result = component.trackById(1, event);

    expect(result).toBe(1);
  });


  describe('addEventListeners', () => {
    it('EVENT_ADDED', fakeAsync(() => {
      component.title = 'title';
      spyOn(component, 'init').and.returnValue(observableOf());

      component.addEventListeners();
      pubSubService.publish('EVENT_ADDED');
      tick();

      expect(component.applyingParams).toEqual(true);
      expect(component.init).toHaveBeenCalled();
    }));

    it('SET_ODDS_FORMAT', fakeAsync(() => {
      component.title = 'title';
      spyOn(component, 'init').and.returnValue(observableOf());

      component.addEventListeners();
      pubSubService.publish('SET_ODDS_FORMAT');
      tick();

      expect(component.init).toHaveBeenCalled();
    }));

    it('EVENT_REMOVED', fakeAsync(() => {
      spyOn(component, 'removeEvent');

      component.addEventListeners();
      pubSubService.publish('EVENT_REMOVED', 1);
      tick();

      expect(component.removeEvent).toHaveBeenCalledWith(1);
    }));

    it('DELETE_EVENT_FROM_CACHE', fakeAsync(() => {
      const match = { id: 1, categoryName: 'categoryName1' };
      component.matches = [
        match, { id: 2, categoryName: 'categoryName2' }
      ] as any;

      component.addEventListeners();
      pubSubService.publish('DELETE_EVENT_FROM_CACHE', 1);
      tick();

      expect(favouritesService.add).toHaveBeenCalledWith(match, 'categoryname1', {});
    }));

    it('DELETE_EVENT_FROM_CACHE should NOT remove match if list of matches is undefined', fakeAsync(() => {
      component.matches = undefined;

      component.addEventListeners();
      pubSubService.publish('DELETE_EVENT_FROM_CACHE', 1);
      tick();

      expect(favouritesService.add).not.toHaveBeenCalled();
    }));

    it('DELETE_EVENT_FROM_CACHE should NOT remove match if match is not found in matches list', fakeAsync(() => {
      const match = { id: 1, categoryName: 'categoryName1' };
      component.matches = [
        match, { id: 2, categoryName: 'categoryName2' }
      ] as any;

      component.addEventListeners();
      pubSubService.publish('DELETE_EVENT_FROM_CACHE', 3);
      tick();

      expect(favouritesService.add).not.toHaveBeenCalled();
    }));

    it('SUCCESSFUL_LOGIN, SESSION_LOGIN, SESSION_LOGOUT', fakeAsync(() => {
      spyOn(component, 'init').and.returnValue(observableOf());

      component.addEventListeners();
      pubSubService.publish('SESSION_LOGIN', 1);
      tick();

      expect(component.init).toHaveBeenCalled();
    }));
  });

  it('#removeEvent', () => {
    const arr = [1, 2];
    component.matches = arr as any;
    spyOn(component, 'applyingParams' as any);
    spyOn(component, 'orderMatches');
    spyOn(component, 'updateData');

    component.removeEvent(1);

    expect(favouritesMatchesService.removeMatch).toHaveBeenCalledWith(arr, 1);
    expect(component.orderMatches).toHaveBeenCalled();
    expect(component.updateData).toHaveBeenCalled();
  });

  it('#showHeader', () => {
    component.matches = [
      {
        id: 1,
        isFinished: false,
        isDisplayed: true
      }
    ] as any;
    expect(component.showHeader).toBeTruthy();

    component.matches = [
      {
        id: 1,
        isFinished: true,
        isDisplayed: false
      }
    ] as any;
    expect(component.showHeader).toBeFalsy();
  });

  it('#updateData should call trimFinishedEvents if id is not specified and set matches', () => {
    const matches = [
      {
        isFinished: false,
        isDisplayed: true,
        marketsCount: 1,
        markets: [{
          outcomes: []
        }]
      }
    ];
    favouritesMatchesService.trimFinishedEvents = jasmine.createSpy('trimFinishedEvents').and.returnValue(matches);

    component.updateData();

    expect(component.matches).toEqual(matches);
  });

  it('#logIn', () => {
    component.widget = 'someWidget';
    component.logIn();

    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.OPEN_LOGIN_DIALOG, {moduleName: 'favouriteswidget'});
  });

  it('#logIn when favourites runs as NOT a widget', () => {
    component.logIn();

    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.OPEN_LOGIN_DIALOG, {moduleName: 'favourites'});
  });

  it('#removeAllFavourites', () => {
    component.matches = [
      {id: 1, categoryCode: 'CategoryCode1'}, {id: 2,  categoryCode: 'CategoryCode2'}
    ] as any;
    component.removeAllFavourites();

    expect(favouritesService.add).toHaveBeenCalledWith({id: 1, categoryCode: 'CategoryCode1'}, 'categorycode1');
    expect(favouritesService.add).toHaveBeenCalledWith({id: 2, categoryCode: 'CategoryCode2'}, 'categorycode2');
  });

  it('#orderMatches', () => {
    component.matches = [
      {id: 1}, {id: 2}
    ] as any;
    component.orderMatches();

    expect(filtersService.orderBy).toHaveBeenCalledWith([{id: 1}, {id: 2}], ['startTime']);
  });
});
