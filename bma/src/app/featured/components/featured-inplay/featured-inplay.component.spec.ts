import * as _ from 'underscore';
import { FeaturedInplayComponent } from '@featured/components/featured-inplay/featured-inplay.component';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { of as observableOf } from 'rxjs';
import { SimpleChanges } from '@angular/core';
import { fakeAsync, tick } from '@angular/core/testing';
import { ISportInstanceMap } from '@app/core/services/cms/models/sport-instance.model';

describe('FeaturedInplayComponent', () => {
  let component: FeaturedInplayComponent;

  let localeService,
    gtmService,
    sportEventHelperService,
    pubSubService,
    routingHelperService,
    sportsConfigService,
    sportsConfigHelperService,
    changeDetectorRef;

  const expectedSportConfigs: ISportInstanceMap = {
    'someCategoryName': {
      sportConfig: {
        config: {
          name: 'someCategoryName',
          path: 'football',
          request: {
            categoryId: '16',
            dispSortName: 'MR',
            marketTemplateMarketNameIntersects: 'Match Betting'
          },
        }
      },
    } as any,
    'basketball': {
      sportConfig: {
        config: {
          name: 'basketball',
          path: 'basketball',
          request: {
            categoryId: '6',
            dispSortName: 'HH',
            marketTemplateMarketNameIntersects: 'Match Betting'
          },
        }
      }
    } as any
  };

  beforeEach(() => {
    localeService = {
      getString: jasmine.createSpy().and.returnValue('tranlation')
    };
    gtmService = {
      push: jasmine.createSpy()
    };
    sportEventHelperService = {
      isFootball: jasmine.createSpy()
    };
    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: pubSubApi
    };
    routingHelperService = {
      formInplayUrl: jasmine.createSpy()
    };
    sportsConfigService = {
      getSports: jasmine.createSpy('getSports').and.returnValue(observableOf(expectedSportConfigs))
    };
    sportsConfigHelperService = {
      getSportConfigName: jasmine.createSpy('getSportConfigName')
    };

    changeDetectorRef = {
      detectChanges: jasmine.createSpy('detectChanges'),
      markForCheck: jasmine.createSpy('markForCheck')
    };

    component = new FeaturedInplayComponent(
      localeService,
      gtmService,
      sportEventHelperService,
      pubSubService,
      routingHelperService,
      sportsConfigService,
      sportsConfigHelperService,
      changeDetectorRef
    );

    component.module = {
      totalEvents: 228
    } as any;
  });

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOnInit', () => {
    it('should be single sport', () => {
      component.sportName = 'football';
      component.ngOnInit();
      expect(component.isSingleSportView).toBeTruthy();
    });

    it('should listen DELETE_EVENT_FROM_CACHE', () => {
      component.ngOnInit();
      expect(pubSubService.subscribe).toHaveBeenCalled();
    });

    it('should call remove event and render on event', () => {
      component['sportsConfigSubscription'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;
      component.removeEvent = jasmine.createSpy();
      component['render'] = jasmine.createSpy();
      pubSubService.subscribe.and.callFake((p1, p2, cb) => cb());
      component.ngOnInit();
      expect(component['sportsConfigSubscription'].unsubscribe).toHaveBeenCalled();
      expect(component.removeEvent).toHaveBeenCalled();
      expect(component['render']).toHaveBeenCalled();
    });

    it('should be multiple sport', () => {
      expect(component.isSingleSportView).toBeFalsy();
    });

    it('should set titles', () => {
      component.ngOnInit();
      expect(component.title).toBeDefined();
      expect(component.seeAllTitle).toBeDefined();
      expect(localeService.getString).toHaveBeenCalledTimes(2);
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });

    it('should call render fn', () => {
      component['render'] = jasmine.createSpy();
      component.ngOnInit();
      expect(component['render']).toHaveBeenCalled();
    });

    it('should subscribe on event remove event', () => {
      component.ngOnInit();
      expect(pubSubService.subscribe).toHaveBeenCalled();
    });
  });

  describe('#ngOnChanges', () => {
    it('should call render', () => {
      component['sportsConfigSubscription'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;
      component['render'] = jasmine.createSpy();
      component.ngOnChanges({ module: {} } as any);
      expect(component['sportsConfigSubscription'].unsubscribe).toHaveBeenCalled();
      expect(component['render']).toHaveBeenCalled();
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });

    it('should not call render', () => {
      component['sportsConfigSubscription'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;
      component['render'] = jasmine.createSpy();
      component.ngOnChanges({} as SimpleChanges);
      expect(component['sportsConfigSubscription'].unsubscribe).not.toHaveBeenCalled();
      expect(component['render']).not.toHaveBeenCalled();
    });

    it('should call setSeeAllTitle', () => {
      component['setSeeAllTitle'] = jasmine.createSpy();
      component.ngOnChanges({ eventsCount: {} } as any);

      expect(component['setSeeAllTitle']).toHaveBeenCalled();
    });

    it('should not call setSeeAllTitle', () => {
      component['setSeeAllTitle'] = jasmine.createSpy();
      component.ngOnChanges({} as SimpleChanges);

      expect(component['setSeeAllTitle']).not.toHaveBeenCalled();
    });
  });

  describe('#ngOnDestroy', () => {
    it('should unsubscribe connect', () => {
      component.ngOnDestroy();
      expect(pubSubService.unsubscribe).toHaveBeenCalled();
    });

    it('should unsubscribe from sports config', () => {
      component['sportsConfigSubscription'] = {
        unsubscribe: jasmine.createSpy('unsubscribe')
      } as any;
      component.ngOnDestroy();

      expect(component['sportsConfigSubscription'].unsubscribe).toHaveBeenCalled();
    });
  });

  describe('#getTitle', () => {
    it('should use sport segment', () => {
      component.isSingleSportView = false;
      const sportSegment = {
        categoryName: 'categoryName'
      } as any;
      const typeSegment = {
        typeName: 'typeName'
      } as any;
      component.getTitle(sportSegment, typeSegment);
      expect(component.getTitle(sportSegment, typeSegment)).toEqual(sportSegment.categoryName);
    });

    it('should use type segment', () => {
      component.isSingleSportView = true;
      const sportSegment = {
        categoryName: 'categoryName'
      } as any;
      const typeSegment = {
        typeName: 'typeName'
      } as any;
      expect(component.getTitle(sportSegment, typeSegment)).toEqual(typeSegment.typeName);
    });
  });

  describe('#getSelectedMarket', () => {
    it('should return primary football market', () => {
      sportEventHelperService.isFootball.and.returnValue(true);
      const event = {
        primaryMarkets: [
          { name: 'somePrimaryMarket' }
        ]
      } as any;
      const marketName = component.getSelectedMarket(event);
      expect(marketName).toEqual('somePrimaryMarket');
    });

    it('should return simple market for other events', () => {
      const event = {
        markets: [
          { name: 'someSimpleMarket' }
        ]
      } as any;
      const marketName = component.getSelectedMarket(event);
      expect(marketName).toEqual('someSimpleMarket');
    });
  });

  describe('*ngFor tracking', () => {
    it('should track by id', () => {
      const eventEntity: any = {
        id: 1
      };
      expect(component.trackById(1, eventEntity)).toBe(1);
    });

    it('should track by key and events count', () => {
      const renderItem: any = {
        football: [{} as any, {} as any]
      };
      expect(component.trackByKey(1, renderItem.football)).toBe(1);
    });
  });

  describe('#sendGTM', () => {
    it('should send EDP GTM', () => {
      component.isSingleSportView = true;
      component.sendGTM();
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
        'eventCategory': 'in-play module ',
        'eventAction': 'sportpage',
        'eventLabel': 'see all'
      }));
    });

    it('should send home page GTM', () => {
      component.sendGTM();
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', jasmine.objectContaining({
        'eventCategory': 'in-play module ',
        'eventAction': 'homepage',
        'eventLabel': 'see all'
      }));
    });
  });

  describe('#removeEvent', () => {
    it('should remove event from module', () => {
      component.module.data = [{
        categoryName: 'someCategoryName',
        eventsByTypeName: [{
          typeName: 'someTypeName',
          events: [{ id: 1 }, { id: 2 }]
        }]
      }] as any;
      component.removeEvent(1);
      expect(component.module.data[0].eventsByTypeName[0].events.length).toBe(1);
      expect(changeDetectorRef.markForCheck).toHaveBeenCalled();
    });

    it('should not remove event from module', () => {
      component.module.data = [{
        categoryName: 'someCategoryName',
        eventsByTypeName: [{
          typeName: 'someTypeName',
          events: [{ id: 1 }, { id: 2 }]
        }]
      }] as any;
      component.removeEvent(3);
      expect(component.module.data[0].eventsByTypeName[0].events.length).toBe(2);
    });
  });

  describe('#render', () => {
    beforeEach(() => {
      component.module.data = [{
        categoryName: 'someCategoryName',
        eventsByTypeName: [{
          typeName: 'someTypeName',
          events: [{ event: 1 } as any]
        }]
      }] as any;
    });

    it('should define renderData and trackingKeys', () => {
      component['render']();
      expect(component.renderData).toBeDefined();
      expect(component.trackingKeys).toBeDefined();
    });

    it('should build render data for SPL page', () => {
      component.isSingleSportView = true;
      component['render']();
      expect(component.renderData['someTypeName']).toEqual([{ event: 1 } as any]);
      expect(component.trackingKeys).toEqual(['someTypeName']);
    });

    it('should build render data for home page', () => {
      component.isSingleSportView = false;
      component['render']();
      expect(component.renderData['someCategoryName']).toEqual([{ event: 1 } as any]);
      expect(component.trackingKeys).toEqual(['someCategoryName']);
    });

    it('should merge events for home page', () => {
      component.module.data = _.clone(component.module.data);
      component.module.data.push({
        categoryName: 'someCategoryName',
        eventsByTypeName: [{
          typeName: 'someOtherTypeName',
          events: [{ event: 2 } as any]
        }]
      } as any);
      component.isSingleSportView = false;
      component['render']();
      expect(component.renderData['someCategoryName']).toEqual([{ event: 1 }, { event: 2 }]);
      expect(component.trackingKeys).toEqual(['someCategoryName']);
    });

    it('should get sport config for SPL page', fakeAsync(() => {
      sportsConfigHelperService.getSportConfigName.and.returnValue('someCategoryName');
      sportsConfigService.getSports.and.returnValue(observableOf(expectedSportConfigs));
      component.isSingleSportView = true;
      component.sportName = 'someCategoryName';
      component['render']();
      expect(sportsConfigService.getSports).toHaveBeenCalledWith(['someCategoryName']);
      tick();
      expect(component.sports['someTypeName']).toEqual(expectedSportConfigs['someCategoryName']);
    }));

    it('should get sport config for home page', fakeAsync(() => {
      component.module.data = [{
        categoryName: 'someCategoryName',
        eventsByTypeName: [{
          typeName: 'someTypeName',
          events: [{ event: 1 } as any]
        }]
      }, {
          categoryName: 'basketball',
          eventsByTypeName: [{
            typeName: 'some basketball type',
            events: [{ event: 2 } as any]
          }]
        }] as any;
      sportsConfigHelperService.getSportConfigName.and.returnValues('someCategoryName', 'basketball');
      sportsConfigService.getSports.and.returnValue(observableOf(expectedSportConfigs));
      component.isSingleSportView = false;
      component['render']();
      expect(sportsConfigService.getSports).toHaveBeenCalledWith(['someCategoryName', 'basketball']);
      tick();
      expect(component.sports['someCategoryName']).toEqual(expectedSportConfigs['someCategoryName']);
      expect(component.sports['basketball']).toEqual(expectedSportConfigs['basketball']);
    }));
  });

  describe('#routingHelperService', () => {
    it('should build inplay URL for sport', () => {
      component.sportName = 'football';
      component.buildInplayUrl();
      expect(routingHelperService.formInplayUrl).toHaveBeenCalledWith('football');
    });

    it('should build inplay URL', () => {
      component.buildInplayUrl();
      expect(routingHelperService.formInplayUrl).toHaveBeenCalledWith('');
    });
  });

  it('should use OnPush strategy', () => {
    expect(FeaturedInplayComponent['__annotations__'][0].changeDetection).toBe(0);
  });
});
