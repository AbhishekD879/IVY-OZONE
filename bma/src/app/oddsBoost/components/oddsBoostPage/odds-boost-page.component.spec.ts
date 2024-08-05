import { of as observableOf, throwError } from 'rxjs';
import { OddsBoostPageComponent } from './odds-boost-page.component';
import { discardPeriodicTasks, fakeAsync, flush, tick } from '@angular/core/testing';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('OddsBoostPageComponent', () => {
  const title = 'oddsBoost';

  let component: OddsBoostPageComponent;
  let userService;
  let oddsBoostService;
  let cmsService;
  let localeService;
  let sessionStatusCallback;
  let domSanitizer;
  let pubSubService;
  let windowRefService;
  let changeDetector;
  let gtmService;
  let timeService;

  beforeEach(() => {
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe').and.callFake((file, method, callback) => {
        if (method !== 'STORE_FREEBETS') {
          sessionStatusCallback = callback;
        }
      }),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      publish: jasmine.createSpy('publish'),
      API: pubSubApi
    };
    userService = {
      status: true
    };
    oddsBoostService = {
      getOddsBoostTokens: jasmine.createSpy('getOddsBoostTokens').and.returnValue(observableOf([{
        freebetTokenExpiryDate: new Date().toISOString(),
        freebetTokenStartDate: new Date().toISOString()
      }]))
    };
    cmsService = {
      getOddsBoost: jasmine.createSpy('getOddsBoost').and.returnValue(observableOf({
        termsAndConditionsText: 'terms',
        loggedInHeaderText: 'in',
        loggedOutHeaderText: 'out'
      })),
      getSportCategoryById: jasmine.createSpy('getSportCategoryById').and.returnValue(observableOf({ svgId: 'sport-icon-1' }, { svgId: null }))

    };
    localeService = {
      getString: jasmine.createSpy().and.returnValue('Odds Boost')
    };
    domSanitizer = {
      bypassSecurityTrustHtml: jasmine.createSpy()
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    changeDetector = {
      detectChanges: jasmine.createSpy().and.returnValue('detectChanges')
    };
    timeService = {
      findDifferenceBetweenUTCAndBST: jasmine.createSpy().and.returnValue('findDifferenceBetweenUTCAndBST'),
      dateToString: jasmine.createSpy().and.returnValue('dateToString')
    }


    component = new OddsBoostPageComponent(
      pubSubService,
      userService,
      oddsBoostService,
      cmsService,
      localeService,
      domSanitizer,
      windowRefService,
      changeDetector,
      gtmService,
      timeService
    );
    spyOn(component, 'showSpinner').and.callThrough();
    spyOn(component, 'hideSpinner').and.callThrough();
  });

  it('constructor', () => {
    expect(component).toBeDefined();
    expect(pubSubService.subscribe).toHaveBeenCalledWith(
      title, [pubSubService.API.SUCCESSFUL_LOGIN, pubSubService.API.SESSION_LOGOUT], jasmine.any(Function)
    );
  });

  it('should get oddsboost on init', () => {
    component.ngOnInit();
    expect(cmsService.getOddsBoost).toHaveBeenCalled();
    expect(oddsBoostService.getOddsBoostTokens).toHaveBeenCalled();
  });

  it('should not get oddsboost on init if not logged in', () => {
    userService.status = false;
    sessionStatusCallback();
    component.ngOnInit();
    expect(oddsBoostService.getOddsBoostTokens).not.toHaveBeenCalled();
    expect(component.hideSpinner).toHaveBeenCalled();
  });

  it('should show spinner on init and hide on get odds boost success', fakeAsync(() => {
    userService.status = true;
    sessionStatusCallback();
    component.ngOnInit();
    expect(component.showSpinner).toHaveBeenCalled();
    expect(oddsBoostService.getOddsBoostTokens).toHaveBeenCalled();
    tick();
    flush();
    discardPeriodicTasks();
    expect(component.hideSpinner).toHaveBeenCalled();
  }));

  it('should hide spinner when getOddBoostToken api fails', () => {
    component['oddsBoostService'].getOddsBoostTokens = jasmine.createSpy().and.returnValue(throwError(new Error('Fake error')));
    component.ngOnInit();
    expect(component.hideSpinner).toHaveBeenCalled();
  });

  it('should open login dialog', () => {
    component.openLoginDialog();
    expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.OPEN_LOGIN_DIALOG, jasmine.objectContaining(
      {
        moduleName: 'oddsboost'
      }
    ));
  });

  it('should subscribe login/logout events', () => {
    userService.status = false;
    sessionStatusCallback();
    expect(component.isLoggedIn).toBe(false);

    userService.status = true;
    sessionStatusCallback();
    expect(component.isLoggedIn).toBe(true);
  });

  it('setUpcomingBoostTimer', () => {
    component['getNextUpcomingBoost'] = jasmine.createSpy().and.returnValue({});
    component.upcomingBoosts = [{}] as any;
    component['setUpcomingBoostTimer']();
    expect(component['getNextUpcomingBoost']).toHaveBeenCalled();
  });

  it('setUpcomingBoostTimer no upcoming boosts', () => {
    component['getNextUpcomingBoost'] = jasmine.createSpy();
    component.upcomingBoosts = [] as any;
    component['setUpcomingBoostTimer']();
    expect(component['getNextUpcomingBoost']).not.toHaveBeenCalled();
  });

  describe('@ngOnDestroy', () => {
    beforeEach(() => {
      component.ngOnInit();
    });
    it('should unbind subscriptions if oddsBoostSubscription was defined', () => {
      spyOn<any>(component['oddsBoostSubscription'], 'unsubscribe');
      component.ngOnDestroy();
      expect(component['oddsBoostSubscription'].unsubscribe).toHaveBeenCalled();
      expect(pubSubService.unsubscribe).toHaveBeenCalled();
    });

    it('should not unsubscibe oddsBoostSubscription if not defined', () => {
      component['oddsBoostSubscription'] = null;
      component['availableCountDown'] = {
        unsubscribe : () => true
      } as any;
      component.ngOnDestroy();
      expect(component['oddsBoostSubscription']).toBeFalsy();
      expect(pubSubService.unsubscribe).toHaveBeenCalled();
    });

    it('should not unsubscibe oddsBoostSubscription if not defined', () => {
      component['oddsBoostSubscription'] = null;
      component.ngOnDestroy();
      expect(component['oddsBoostSubscription']).toBeFalsy();
      expect(pubSubService.unsubscribe).toHaveBeenCalled();
    });
  });

  it('getContent shoud show error', () => {
    spyOn(component, 'showError');
    cmsService.getOddsBoost.and.returnValue(throwError(null));
    component['getContent']();
    expect(component.showError).toHaveBeenCalledTimes(1);
  });

  it('getNextUpcomingBoost', () => {
    const tokens: any = [
      { freebetTokenStartDate: '2020-04-08T13:20:00.000Z' },
      { freebetTokenStartDate: '2020-04-08T13:10:00.000Z' },
    ];
    expect(component['getNextUpcomingBoost'](tokens)).toEqual(tokens[1]);
  });

  it('should call sortOddsboostTokensInSpecificOrder with converted tokens data', () => {
    const tokensData = { '1': [{ categoryId: '1', categoryName: 'Football' }] } as any;
    spyOn(component, 'loadSvg');
    spyOn(component, 'sortOddsboostTokensInSpecificOrder');
    component.filterOddsboostTokens(tokensData as any);
    expect(component.sortOddsboostTokensInSpecificOrder).toHaveBeenCalledWith([{ categoryId: '1', categoryName: 'Football' }] as any);
    expect(component.loadSvg).toHaveBeenCalledWith(tokensData);
  });

  it('should sort oddsboost tokens in specific order', () => {
    const tokensData = [{ categoryId: '3', categoryName: 'Cricket' }, { categoryId: '1', categoryName: 'Football' }, { categoryId: '2', categoryName: 'Horse Racing' }];
    component.sortOddsboostTokensInSpecificOrder(tokensData as any);
    expect(component.sortedTokensArr).toEqual([{ categoryId: '1', categoryName: 'Football' }, { categoryId: '2', categoryName: 'Horse Racing' }, { categoryId: '3', categoryName: 'Cricket' }] as any);
  });

  it('should call sendGTMData method if isDefaultPillOnLoad is true', () => {
    component.isDefaultPillOnLoad = true;
    const pillName = { value: 1, name: 'All', id: '', type: 'sport', active: false };
    spyOn(component, 'sendGTMData');
    component.onSelectonOfSportPill(pillName);
    expect(component.sendGTMData).toHaveBeenCalledWith(pillName.name);
    expect(component.isDefaultPillOnLoad).toBeTrue();
  });

  it('should not call sendGTMData method if isDefaultPillOnLoad is false', () => {
    component.isDefaultPillOnLoad = false;
    const pillName = { value: 1, name: 'All', id: '', type: 'sport', active: false };
    spyOn(component, 'sendGTMData');
    component.onSelectonOfSportPill(pillName);
    expect(component.sendGTMData).not.toHaveBeenCalled();
    expect(component.isDefaultPillOnLoad).toBeTrue();
  });

  it('should send GTM data on load"', () => {
    const value = 'load';
    const gtmData = {
      event: 'contentView',
      'component.CategoryEvent': 'odds boost',
      'component.LabelEvent': 'oddset',
      'component.ActionEvent': 'load',
      'component.PositionEvent': component.isActive ? 'available' : 'upcoming',
      'component.LocationEvent': 'upcoming-' + component.upcomingBoosts.length,
      'component.EventDetails': 'available-' + component.availableBoosts.length,
      'component.URLClicked': 'not applicable'
    }
    component.sendGTMData(value);
    expect(component.gtmService.push).toHaveBeenCalledWith('contentView', gtmData);
  });

  it('should send GTM data on click when isActive is true', () => {
    const value = 'click';
    const isActive = true;
    const gtmData = {
      event: 'Event.Tracking',
      'component.CategoryEvent': 'odds boost',
      'component.LabelEvent': 'oddset',
      'component.ActionEvent': value,
      'component.PositionEvent': component.isActive ? 'available' : 'upcoming',
      'component.LocationEvent': 'not applicable',
      'component.EventDetails': value,
      'component.URLClicked': 'not applicable'
    }
    component.isActive = isActive;
    component.sendGTMData(value);
    expect(component.gtmService.push).toHaveBeenCalledWith('Event.Tracking', gtmData);
  });

  it('should send GTM data with correct "component.PositionEvent" value when isActive is false', () => {
    const value = 'click';
    const isActive = false;
    const gtmData = {
      event: 'Event.Tracking',
      'component.CategoryEvent': 'odds boost',
      'component.LabelEvent': 'oddset',
      'component.ActionEvent': value,
      'component.PositionEvent': 'upcoming',
      'component.LocationEvent': 'not applicable',
      'component.EventDetails': value,
      'component.URLClicked': 'not applicable'
    };
    component.isActive = isActive;
    component.sendGTMData(value);
    expect(component.gtmService.push).toHaveBeenCalledWith(gtmData.event, gtmData);
  });

  it('should send GTM data on click if available', () => {
    const value = 'available';
    const gtmData = {
      event: 'Event.Tracking',
      'component.CategoryEvent': 'odds boost',
      'component.LabelEvent': 'oddset',
      'component.ActionEvent': 'click',
      'component.PositionEvent': 'upcoming',
      'component.LocationEvent': 'not applicable',
      'component.EventDetails': value,
      'component.URLClicked': 'not applicable'
    }
    component.sendGTMData(value);
    expect(component.gtmService.push).toHaveBeenCalledWith('Event.Tracking', gtmData);
  });

  it('should send GTM data on click if available', () => {
    const value = 'upcoming';
    const gtmData = {
      event: 'Event.Tracking',
      'component.CategoryEvent': 'odds boost',
      'component.LabelEvent': 'oddset',
      'component.ActionEvent': 'click',
      'component.PositionEvent': 'available',
      'component.LocationEvent': 'not applicable',
      'component.EventDetails': value,
      'component.URLClicked': 'not applicable'
    }
    component.sendGTMData(value);
    expect(component.gtmService.push).toHaveBeenCalledWith('Event.Tracking', gtmData);
  });

  describe('filterOddsboostTokensForSport', () => {
    it('ceteory items null', () => {
      const val = [{ categoryId: '1' }, { categoryId: '2' }, {}];
      component.filterOddsboostTokensForSport(val as any);
    })
    it('ceteory items null', () => {
      const val = [{ categoryId: null }];
      component.filterOddsboostTokensForSport(val as any)
    })
  })

  describe('sorting', () => {
    it('should sort tokens in specific order when all categories exist', () => {
      const reqTokensData = [
        { categoryName: 'Horse Racing' },
        { categoryName: 'A-Z' },
        { categoryName: 'Football' },
        { categoryName: 'All' },
      ];
      component.sortOddsboostTokensInSpecificOrder(reqTokensData as any);
      expect(component.sortedTokensArr[0].categoryName).toEqual('All');
      expect(component.sortedTokensArr[1].categoryName).toEqual('Football');
      expect(component.sortedTokensArr[2].categoryName).toEqual('Horse Racing');
      expect(component.sortedTokensArr[3].categoryName).toEqual('A-Z');
    });

    it('should sort tokens in specific order when categoryName as undefined', () => {
      const reqTokensData = [
        { categoryName: 'Horse Racing' },
        { categoryName: undefined },
        { categoryName: 'Football' },
        {}
      ];
      component.sortOddsboostTokensInSpecificOrder(reqTokensData as any);
      expect(component.sortedTokensArr[0].categoryName).toEqual(undefined);
      expect(component.sortedTokensArr[1].categoryName).toEqual(undefined);
      expect(component.sortedTokensArr[2].categoryName).toEqual('Football');
    });

    it('should sort tokens based on categoryName when indexA is -1 and indexB is -1', () => {
      const reqTokensData = [
        { categoryName: 'XYZ' },
        { categoryName: 'ABC' },
      ];
      component.sortOddsboostTokensInSpecificOrder(reqTokensData as any);
      expect(component.sortedTokensArr.length).toEqual(reqTokensData.length);
      expect(component.sortedTokensArr[0].categoryName).toEqual('ABC');
      expect(component.sortedTokensArr[1].categoryName).toEqual('XYZ');
    });

    it('should sort tokens based on categoryName when indexA is -1 and indexB is not -1', () => {
      const reqTokensData = [
        { categoryName: 'XYZ' },
        { categoryName: 'Horse Racing' },
      ];
      component.sortOddsboostTokensInSpecificOrder(reqTokensData as any);
      expect(component.sortedTokensArr.length).toEqual(reqTokensData.length);
      expect(component.sortedTokensArr[0].categoryName).toEqual('Horse Racing');
      expect(component.sortedTokensArr[1].categoryName).toEqual('XYZ');
    });

    it('should sort tokens based on categoryName when indexA is not -1 and indexB is -1', () => {
      const reqTokensData = [
        { categoryName: 'Football' },
        { categoryName: 'ABC' },
      ];
      component.sortOddsboostTokensInSpecificOrder(reqTokensData as any);
      expect(component.sortedTokensArr.length).toEqual(reqTokensData.length);
      expect(component.sortedTokensArr[0].categoryName).toEqual('Football');
      expect(component.sortedTokensArr[1].categoryName).toEqual('ABC');
    });

    it('should filter sport pills from oddsboost tokens', () => {
      const sortedTokensData = [
        { categoryId: '1', categoryName: 'Football' },
        { categoryId: '2', categoryName: 'Horse Racing' },
        { categoryId: '3', categoryName: 'A-Z' },
        { categoryId: '4', categoryName: 'Cricket' },
      ];
      component.filterSportPillsFromOddsboostTokens(sortedTokensData as any);
      expect(component.sportPills.length).toEqual(5);
      expect(component.sportPills[0].name).toEqual('All');
      expect(component.sportPills[0].active).toBeTruthy();
      expect(component.sportPills[1].name).toEqual('Football');
      expect(component.sportPills[1].active).toBeFalsy();
      expect(component.sportPills[2].name).toEqual('Horse Racing');
      expect(component.sportPills[2].active).toBeFalsy();
      expect(component.sportPills[3].name).toEqual('A-Z');
      expect(component.sportPills[3].active).toBeFalsy();
    });

    it('should filter sport pills from oddsboost tokens and set default pill if "All" pill is not present', () => {
      const sortedTokensData = [
        { categoryName: 'Football', categoryId: '1' },
        { categoryName: 'Horse Racing', categoryId: '2' },
        { categoryName: 'Tennis', categoryId: '3' },
        { categoryName: 'Football', categoryId: '1' },
      ];
      component.filterSportPillsFromOddsboostTokens(sortedTokensData as any);
      expect(component.sportPills.length).toEqual(4);
      expect(component.sportPills[0].name).toEqual('All');
      expect(component.sportPills[0].active).toBeTrue();
    });

    it('should filter sport pills from oddsboost tokens and keep existing "All" pill if present', () => {
      const sortedTokensData = [
        { categoryName: 'All', categoryId: '' },
        { categoryName: 'Football', categoryId: '1' },
        { categoryName: 'Horse Racing', categoryId: '2' },
        { categoryName: 'Tennis', categoryId: '3' },
        { categoryName: 'Football', categoryId: '1' },
      ];
      component.filterSportPillsFromOddsboostTokens(sortedTokensData as any);
      expect(component.sportPills.length).toEqual(4);
      expect(component.sportPills[0].name).toEqual('All');
      expect(component.sportPills[0].active).toBeFalse();
    });

    it('should select a specific sport pill and call filterOddsboostTokensForSport', () => {
      const selectedPill = { value: 2, name: 'Horse Racing', id: '2', type: 'sport', active: false };
      spyOn(component, 'filterOddsboostTokensForSport');
      component.sortedTokensArr = [
        { categoryName: 'Football', categoryId: '1' },
        { categoryName: 'Horse Racing', categoryId: '2' },
        { categoryName: 'Tennis', categoryId: '3' },
      ] as any;
      component.onSelectonOfSportPill(selectedPill);
      expect(selectedPill.active).toBeTrue();
      expect(component.sportPills.every((pill) => pill.active === (pill.id === selectedPill.id))).toBeTrue();
      expect(component.filterOddsboostTokensForSport).toHaveBeenCalledWith([
        { categoryName: 'Horse Racing', categoryId: '2' },
      ] as any);
    });
  });

  it('should set nextAvailableBoostDate when isActive is true', () => {
    component.isActive = true;

    const event = '2023-07-06T10:30:00';

    component.leastTimeToken(event);

    expect(component.nextAvailableBoostDate).toEqual(new Date(event));
    expect(component.nextUpcomingBoostDate).toBeUndefined();
  });

  it('should set nextUpcomingBoostDate when isActive is false', () => {
    component.isActive = false;

    const event = '2023-07-06T10:30:00';

    component.leastTimeToken(event);

    expect(component.nextUpcomingBoostDate).toEqual(new Date(event));
    expect(component.nextAvailableBoostDate).toBeUndefined();
  });

  it('should set isActive to true when availableBoosts has items and upcomingBoosts is empty', () => {
    component.availableBoosts = [
      { freebetTokenId: 'token1' },
      { freebetTokenId: 'token2' },
    ] as any;
    component.upcomingBoosts = [];

    component.oddsBoostTokens();

    expect(component.isActive).toBe(true);
    expect(component.noTokens).toBe(true);
  });

  it('should set isActive to false when availableBoosts is empty and upcomingBoosts has items', () => {
    component.availableBoosts = [];
    component.upcomingBoosts = [
      { freebetTokenId: 'token3' },
      { freebetTokenId: 'token4' },
    ] as any;

    component.oddsBoostTokens();

    expect(component.isActive).toBe(false);
    expect(component.noTokens).toBe(true);
  });

  it('should set noTokens to false when both availableBoosts and upcomingBoosts are empty', () => {
    component.availableBoosts = [];
    component.upcomingBoosts = [];

    component.oddsBoostTokens();

    expect(component.isActive).toBe(true);
    expect(component.noTokens).toBe(false);
  });

  it('should set oddsBoostToken when oddsBoostToken is null', () => {
    component.isActive = true;
    component.oddsBoostToken = null;
    component.dateExpiryCountMap.clear();

    const oddsBoosts = {
      freebetTokenStartDate: '2023-07-06T10:00:00',
      freebetTokenExpiryDate: '2023-07-06T12:00:00',
      categoryName: 'Basketball',
    } as any;

    component.findTimer(oddsBoosts);

    expect(component.oddsBoostToken).toEqual(oddsBoosts);
    expect(component.dateExpiryCountMap.get(oddsBoosts.freebetTokenExpiryDate)).toBe(1);
  });

  it('should set date to "freebetTokenStartDate" when isActive is false', () => {
    component.isActive = false;

    const oddsBoosts = {
      freebetTokenStartDate: '2023-07-06T10:00:00',
      freebetTokenExpiryDate: '2023-07-06T12:00:00',
      categoryName: 'Basketball',
    } as any;

    spyOn(component.dateExpiryCountMap, 'get');
    spyOn(component.dateExpiryCountMap, 'set');

    component.findTimer(oddsBoosts);

    expect(component.dateExpiryCountMap.get).toHaveBeenCalledWith(oddsBoosts.freebetTokenStartDate);
    expect(component.dateExpiryCountMap.set).toHaveBeenCalled();
  });

  it('should update oddsBoostToken when oddsBoostStartDate is earlier than nextBoostStartDate', () => {
    component.isActive = true;
    component.oddsBoostToken = {
      freebetTokenStartDate: '2023-07-06T14:00:00',
      freebetTokenExpiryDate: '2023-07-06T16:00:00',
      categoryName: 'Basketball',
    } as any;

    component.dateExpiryCountMap.clear();
    component.dateExpiryCountMap.set(component.oddsBoostToken.freebetTokenExpiryDate, 1);

    const oddsBoosts = {
      freebetTokenStartDate: '2023-07-06T10:00:00',
      freebetTokenExpiryDate: '2023-07-06T12:00:00',
      categoryName: 'Football',
    } as any;

    component.findTimer(oddsBoosts);

    expect(component.oddsBoostToken).toEqual(oddsBoosts);
    expect(component.dateExpiryCountMap.get(oddsBoosts.freebetTokenExpiryDate)).toBe(1);
  });

  it('should not update oddsBoostToken when oddsBoostStartDate is later than nextBoostStartDate', () => {
    component.isActive = true;
    component.oddsBoostToken = {
      freebetTokenStartDate: '2023-07-06T10:00:00',
      freebetTokenExpiryDate: '2023-07-06T12:00:00',
      categoryName: 'Basketball',
    } as any;

    component.dateExpiryCountMap.clear();
    component.dateExpiryCountMap.set(component.oddsBoostToken.freebetTokenExpiryDate, 1);

    const oddsBoosts = {
      freebetTokenStartDate: '2023-07-06T14:00:00',
      freebetTokenExpiryDate: '2023-07-06T16:00:00',
      categoryName: 'Football',
    } as any;

    component.findTimer(oddsBoosts);

    expect(component.oddsBoostToken).not.toEqual(oddsBoosts);
    expect(component.dateExpiryCountMap.get(oddsBoosts.freebetTokenExpiryDate)).toBe(1);
  });

  it('should update the count in dateExpiryCountMap when expiryTokens > 1', () => {
    component.isActive = true;
    component.oddsBoostToken = {
      freebetTokenStartDate: '2023-07-06T10:00:00',
      freebetTokenExpiryDate: '2023-07-06T12:00:00',
      categoryName: 'Basketball',
    } as any;

    const oddsBoosts = {
      freebetTokenStartDate: '2023-07-06T10:00:00',
      freebetTokenExpiryDate: '2023-07-06T12:00:00',
      categoryName: 'Football',
    } as any;

    component.dateExpiryCountMap.set(oddsBoosts.freebetTokenExpiryDate, 2);

    component.findTimer(oddsBoosts);

    expect(component.dateExpiryCountMap.get(oddsBoosts.freebetTokenExpiryDate)).toBe(3);
  });

  it('should set nextSport to empty string and sameExpiry to expiryTokens when expiryTokens > 1', () => {
    component.oddsBoostToken = {
      freebetTokenStartDate: '2023-07-06T10:00:00',
      freebetTokenExpiryDate: '2023-07-06T12:00:00',
      categoryName: 'Basketball',
    } as any;

    component.dateExpiryCountMap.set(component.oddsBoostToken.freebetTokenExpiryDate, 3);
    component.tokenCount();

    expect(component.nextSport).toBe('');
    expect(component.sameExpiry).toBe(3);
  });

  it('should set nextSport to empty string and sameExpiry to expiryTokens when expiryTokens > 1 (based on freebetTokenStartDate)', () => {
    component.oddsBoostToken = {
      freebetTokenStartDate: '2023-07-06T10:00:00',
      freebetTokenExpiryDate: '2023-07-06T12:00:00',
      categoryName: 'Basketball',
    } as any;

    component.dateExpiryCountMap.set(component.oddsBoostToken.freebetTokenStartDate, 3);

    component.tokenCount();

    expect(component.nextSport).toBe('');
    expect(component.sameExpiry).toBe(3);
  });

  it('should set nextSport to categoryName or "MultiSport" and sameExpiry to 0 when expiryTokens <= 1', () => {
    component.oddsBoostToken = {
      freebetTokenStartDate: '2023-07-06T10:00:00',
      freebetTokenExpiryDate: '2023-07-06T12:00:00',
      categoryName: 'Basketball',
    } as any;

    component.dateExpiryCountMap.set(component.oddsBoostToken.freebetTokenExpiryDate, 1);
    component.tokenCount();

    expect(component.nextSport).toBe('Basketball');
    expect(component.sameExpiry).toBe(0);
  });

  it('should set nextSport to "MultiSport" and sameExpiry to 0 when categoryName is not available', () => {
    component.oddsBoostToken = {
      freebetTokenStartDate: '2023-07-06T10:00:00',
      freebetTokenExpiryDate: '2023-07-06T12:00:00',

    } as any;

    component.dateExpiryCountMap.set(component.oddsBoostToken.freebetTokenExpiryDate, 1);

    component.tokenCount();

    expect(component.nextSport).toBe('MultiSport');
    expect(component.sameExpiry).toBe(0);
  });

  it('should call expireTokenInfo when token has expired (isActive is true)', () => {
    const now = new Date('2023-07-06T10:30:00');
    jasmine.clock().install();
    jasmine.clock().mockDate(now);

    const oddBoost = {
      freebetTokenId: 'token1',
      freebetTokenStartDate: new Date('2023-07-05T10:00:00'),
      freebetTokenExpiryDate: new Date('2023-07-06T10:00:00'),
    } as any;

    spyOn(component, 'expireTokenInfo');

    component.isActive = true;

    component.checkTokenDate(oddBoost);

    expect(component.expireTokenInfo).toHaveBeenCalledWith({
      freebetTokenId: 'token1',
      tokenExpire: true,
    });

    jasmine.clock().uninstall();
  });

  it('should call expireTokenInfo when token has expired (isActive is false)', () => {
    const now = new Date('2023-07-06T10:30:00');
    jasmine.clock().install();
    jasmine.clock().mockDate(now);

    const oddBoost = {
      freebetTokenId: 'token1',
      freebetTokenStartDate: new Date('2023-07-05T10:00:00'),
      freebetTokenExpiryDate: new Date('2023-07-06T10:00:00'),
    } as any;

    spyOn(component, 'expireTokenInfo');

    component.isActive = false;

    component.checkTokenDate(oddBoost);

    expect(component.expireTokenInfo).toHaveBeenCalledWith({
      freebetTokenId: 'token1',
      tokenExpire: true,
    });

    jasmine.clock().uninstall();
  });

  it('should update expireTokenDetails with tokenExpire', () => {
    const event = {
      freebetTokenId: 'token1',
      tokenExpire: new Date('2023-07-06T10:30:00'),
    } as any;

    component.expireTokenInfo(event);

    expect(component.expireTokenDetails['token1']).toEqual(event.tokenExpire);
  });

  it('should update expireTokenDetails with multiple tokenExpire values', () => {
    const event1 = {
      freebetTokenId: 'token1',
      tokenExpire: new Date('2023-07-06T10:30:00'),
    } as any;

    const event2 = {
      freebetTokenId: 'token2',
      tokenExpire: new Date('2023-07-07T12:00:00'),
    } as any;

    component.expireTokenInfo(event1);
    component.expireTokenInfo(event2);

    expect(component.expireTokenDetails['token1']).toEqual(event1.tokenExpire);
    expect(component.expireTokenDetails['token2']).toEqual(event2.tokenExpire);
  });

  it('should call loadSvg ', () => {
    const tokensData = {
      category1: [
        { id: 1, name: 'Token 1' },
        { id: 2, name: 'Token 2' },
      ],
      category2: [
        { id: 3, name: 'Token 3' },
      ],
    } as any;
    component.oddsBoostToken = null;



    spyOn(component, 'findTimer');
    spyOn(component, 'checkTokenDate');
    spyOn(component, 'tokenCount');

    const result = component.loadSvg(tokensData);

    expect(component.oddsBoostToken).toBeNull();
    expect(cmsService.getSportCategoryById).toHaveBeenCalled();
    expect(result).toBe(tokensData);
    expect(component.findTimer).toHaveBeenCalledWith(tokensData['category1'][0]);
    expect(component.checkTokenDate).toHaveBeenCalledWith(tokensData['category1'][0]);
    expect(component.tokenCount).toHaveBeenCalled();
  });
  it('should call loadSvg if no svgId  ', () => {
    cmsService = {
      getSportCategoryById: jasmine.createSpy('getSportCategoryById').and.returnValue(observableOf(null))
    };
    component = new OddsBoostPageComponent(
      pubSubService,
      userService,
      oddsBoostService,
      cmsService,
      localeService,
      domSanitizer,
      windowRefService,
      changeDetector,
      gtmService,
      timeService
    );
    const tokensData = {
      category1: [
        { id: 1, name: 'Token 1' },
        { id: 2, name: 'Token 2' },
      ],
      category2: [
        { id: 3, name: 'Token 3' },
      ],
    } as any;
    component.oddsBoostToken = null;

    spyOn(component, 'findTimer');
    spyOn(component, 'checkTokenDate');
    spyOn(component, 'tokenCount');

    const result = component.loadSvg(tokensData);

    expect(component.oddsBoostToken).toBeNull();
    expect(cmsService.getSportCategoryById).toHaveBeenCalled();
    expect(result).toBe(tokensData);
    expect(component.findTimer).toHaveBeenCalledWith(tokensData['category1'][0]);
    expect(component.checkTokenDate).toHaveBeenCalledWith(tokensData['category1'][0]);
    expect(component.tokenCount).toHaveBeenCalled();
  });

  describe('availableTokens', () => {
    it('', fakeAsync(() => {
      component.startingAvailbleTokenNumber = 1;
      component.availableTokens(1);
      flush();
      tick(2000)
      discardPeriodicTasks()
    }))
    it('', fakeAsync(() => {
      component.startingAvailbleTokenNumber = 1;
      component.availableTokens(2);
      flush();
      tick(2000)
      discardPeriodicTasks()
    }))
  })

  describe('disabledBoostIcon', () => {
    it('should set enabled to true and then false after a delay', fakeAsync(() => {
      component.enabled = false;
      component.isLoggedIn = true;
      component.disabledBoostIcon();
      expect(component.enabled).toBe(true);
      tick(3000);
      expect(component.enabled).toBe(false);
    }));

    it('should not set enabled to true if both enabled and isLoggedIn are false', () => {
      component.enabled = true;
      component.isLoggedIn = true;
      component.disabledBoostIcon();
      expect(component.enabled).toBe(true);
    });
  });


  describe('getOddsBoosts', () => {
    it('validDate false' ,() => {
      component.isActive = false;
      component.timerStart = '00:00:01'
      component.validDate({
        freebetTokenExpiryDate: new Date(),
        freebetTokenStartDate: new Date()})
    })

    it('validDate true' ,() => {
      component.isActive = true;
      component.timerStart = '00:00:01'
      component.validDate({freebetTokenExpiryDate: new Date()})
    })
  })

  describe('padnumber', () => {
    it('`0${number}' ,() => {
      const retVal = component.padNumber(5)
      expect(retVal).toBe('05')
    })
  })

  describe('getOddsBoosts', () => {
    it('getOddsBoosts' ,fakeAsync(() => {
      spyOn(component, 'resolvedTimeZone').and.returnValue('Europe/Gibraltar');
      spyOn(component, 'unsubscribeOddsBoost');
      component.getOddsBoosts()
      tick(1000);
    }))

    it('getOddsBoosts' ,fakeAsync(() => {
      spyOn(component, 'resolvedTimeZone').and.returnValue('Europe/Gibraltar');
      spyOn(component, 'unsubscribeOddsBoost');
      (timeService.findDifferenceBetweenUTCAndBST as jasmine.Spy).and.returnValue(undefined);
      component.getOddsBoosts()
      tick(1000);
    }))
  })
});
