
import { sportEventMock } from '@app/racing/components/racingEventMain/racing-event-main.component.mock';
import { RacingPanelComponent } from '@shared/components/racingPanel/racing-panel.component';
import { of as observableOf } from 'rxjs';

describe('RacingPanelComponent', () => {
  let component: RacingPanelComponent;
  let localeService, router, routingHelperService, seoDataService, pubsub, gtmService,lpAvailabilityService,activatedRoute;

  beforeEach(() => {
    routingHelperService = {
      formEdpUrl: jasmine.createSpy('formEdpUrl'),
      formResultedEdpUrl: jasmine.createSpy('formResultedEdpUrl')
    };
    localeService = {
      getString: jasmine.createSpy()
    };
    router = {
      navigateByUrl: jasmine.createSpy('navigateByUrl')
    };
    seoDataService = {
      eventPageSeo: jasmine.createSpy('eventPageSeo')
    };
    pubsub = {
      publish: jasmine.createSpy('publish')
    };
    gtmService = {
      push: jasmine.createSpy('push')
    };
    lpAvailabilityService = {
      check: jasmine.createSpy().and.returnValue(true)
    }
    activatedRoute = {
      params: observableOf({display: 'horseracing'}),
      snapshot: {
        paramMap: {
          get: jasmine.createSpy('get')
        }
      }
    };
    component = new RacingPanelComponent(
      localeService,
      router,
      routingHelperService,
      seoDataService,
      pubsub,
      gtmService,
      lpAvailabilityService,
      activatedRoute
    );
  });

  describe('#ngOnInit', () => {
    it('should set titleText => title = ""', () => {
      activatedRoute.params = observableOf({display: ''})
      component.title = '';
      component.ngOnInit();
      expect(component.titleText).toBe('');
    });

    it('should set titleText => title = "Greyville"', () => {
      activatedRoute.params = observableOf({display: 'greyhound'})
      component.title = 'greyhound';
      component.ngOnInit();
      expect(component.titleText).toBe('greyhound');
    });

    it('should set titleText => title = "Greyville (UK)"', () => {
      activatedRoute.params = observableOf({display: 'greyhound'})
      component.title = 'Greyville (UK)';
      component.ngOnInit();
      expect(component.titleText).toBe('Greyville <b>(UK)</b>');
    });

    it('should set titleText => title = "racing.event"', () => {
      activatedRoute.params = observableOf({display: 'greyhound'})
      component.title = 'racing.event';
      component.ngOnInit();
      expect(localeService.getString).toHaveBeenCalled();
    });

    it('should filter virtual events', () => {
      activatedRoute.params = observableOf({display: 'horseracing'})
      component.events = [{categoryId : '19'}, {categoryId : '39'}] as any;
      component.title = 'racing.event';
      component.ngOnInit();
      expect(component.events.length).toBe(1);
    });


      it('should check isLpAvailable', () => {
        const events: any = [{
          categoryId : '161',
          markets : [
           {isLpAvailable : true} 
          ]
        }] as any;
        const isEarlyPricesAvailable = component['isLpAvailable'](events);
         expect(isEarlyPricesAvailable).toEqual(true)
       });
  });
  it('should call hasResult', () => {
    component.raceType = 'horseracing';
    let events: any = [{
      correctedDayValue: 'racing.today',
      isResulted: false,
      isStarted: false,
      rawIsOffCode: 'N',
      markets: [
        { isLpAvailable: true }
      ]
    }] as any;
    let hasResult = component['hasResult'](events);
    expect(hasResult).toEqual(false);
    events  = [{
      correctedDayValue: 'racing.today',
      isResulted: false,
      isStarted: false,
      rawIsOffCode: 'Y',
      markets: [
        { isLpAvailable: true }
      ]
    }] as any;
    expect(component['hasResult'](events)).toEqual(true);
    events = [{
      correctedDayValue: 'racing.today',
      isResulted: true,
      isStarted: false,
      rawIsOffCode: 'Y',
      markets: [
        { isLpAvailable: true }
      ]
    }] as any;
    hasResult = component['hasResult'](events);
    expect(hasResult).toEqual(true);
  });

  it('should call earlySignPostTitle', () => {
    localeService.getString = jasmine.createSpy('getString').and.returnValue('Early Prices Available');
    expect(component.earlySignPostTitle()).toEqual('Early Prices Available');
  });

  describe("should call isEarlyPricesAvailable", () => {
    it('should check is early price available', () => {
      component.raceType = 'horseracing';
      const events: any = [{
        correctedDayValue: 'racing.today',
        isResulted: false,
        isStarted: false,
        rawIsOffCode: 'N',
        markets: [
          { isLpAvailable: true }
        ]
      }] as any;
      const isEarlyPricesAvailable = component['isEarlyPricesAvailable'](events);
      expect(isEarlyPricesAvailable).toEqual(false);
    });
    it('should check is early price available with eventStatusData', () => {
      component.raceType = 'horseracing';
      const events: any = [{
        id: 1234,
        correctedDayValue: 'racing.today',
        isStarted: false,
        isLiveNowEvent: false,
        isResulted: false,
        rawIsOffCode: 'N',
        markets: [
          { isLpAvailable: true }
        ]
      }] as any;
      component.eventStatusData['1234'] = {title: 'race off'}
      localeService.getString = jasmine.createSpy('getString').and.returnValue('race off');
      const isEarlyPricesAvailable = component['isEarlyPricesAvailable'](events);
      expect(isEarlyPricesAvailable).toEqual(false);
    });
    it('should check is early price available greyhound today', () => {
      component.raceType = 'greyhound';
      const events: any = [{
        correctedDayValue: 'racing.tomorrow', 
        correctedDay: 'sb.today',
        isResulted: false,
        isStarted: false,
        rawIsOffCode: 'N',
        markets: [
          { isLpAvailable: true }
        ]
      }] as any;
      const isEarlyPricesAvailable = component['isEarlyPricesAvailable'](events);
      expect(isEarlyPricesAvailable).toEqual(true);
    });
    it('should check is early price available greyhound tomorrow', () => {
      component.raceType = 'greyhound';
      const events: any = [{
        correctedDayValue: 'racing.tomorrow', 
        correctedDay: 'sb.tomorrow',
        isResulted: false,
        isStarted: false,
        rawIsOffCode: 'N',
        markets: [
          { isLpAvailable: true }
        ]
      }] as any;
      const isEarlyPricesAvailable = component['isEarlyPricesAvailable'](events);
      expect(isEarlyPricesAvailable).toEqual(true);
    });
  });          
  describe('#trackById', () => {
    it('should trackById if id is exist', () => {
      expect(component.trackById(1, { id: '234234' } as any)).toBe('1234234');
    });

    it('should trackById if id is not exist', () => {
      expect(component.trackById(1, {} as any)).toBe('1');
    });
  });

  describe('#goToEvent', () => {
    const event = {
      preventDefault: jasmine.createSpy()
    } as any;

    it('should navigate to event page for GH', () => {
      spyOn(component, 'formEdpUrl');
      component.showSwitcher = false;
      component.groupFlagText = 'France';
      const expectedObj = {
        eventAction: 'meetings',
        eventCategory: 'greyhounds',
        eventLabel: 'navigation – france',
        categoryID: '16',
        typeID: 1904,
        eventID: 9458938
      };
      const ghEvent = {
        sportEventMock, ...{categoryId: '16', typeId: 1904, id: 9458938}
      };
      component.goToEvent(ghEvent as any, event);
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', expectedObj);
    });

    it('should navigate to to event page', () => {
      spyOn(component, 'formEdpUrl');
      component.showSwitcher = false;
      component.groupFlagText = 'France';
      const expectedObj = {
        eventAction: 'meetings',
        eventCategory: 'horse racing',
        eventLabel: 'navigation – france',
        categoryID: '21',
        typeID: 1904,
        eventID: 9458938
      };
      component.goToEvent(sportEventMock as any, event);
      expect(pubsub.publish).toHaveBeenCalled();
      expect(gtmService.push).toHaveBeenCalledWith('trackEvent', expectedObj);
      expect(component.formEdpUrl).toHaveBeenCalledWith(sportEventMock as any);
      expect(router.navigateByUrl).toHaveBeenCalled();
      expect(event.preventDefault).toHaveBeenCalled();
    });

    it('should emit event to Func is it is exist', () => {
      Object.defineProperty(component.clickFunction, 'observers', { value: [''] });
      spyOn(component.clickFunction, 'emit');
      component.goToEvent({} as any, event);

      expect(component.clickFunction.emit).toHaveBeenCalled();
      expect(router.navigateByUrl).not.toHaveBeenCalled();
      expect(event.preventDefault).toHaveBeenCalled();
    });

  });

  describe('goToSeo', () => {
    it('should create seo ', () => {
      routingHelperService.formEdpUrl.and.returnValue('url');
      component.goToSeo(({id: '1'} as any));
      expect(routingHelperService.formEdpUrl).toHaveBeenCalledWith({ id: '1' });
      expect(seoDataService.eventPageSeo).toHaveBeenCalledWith({ id: '1' },'url');
    });
  });

  describe('#formEdpUrl', () => {
    it('tote flow', () => {
      component.isTote = true;
      const url = component.formEdpUrl({
        id: 1
      } as any);
      expect(url).toEqual('/tote/event/1');
      expect(routingHelperService.formResultedEdpUrl).not.toHaveBeenCalled();
    });
    it('not tote flow', () => {
      component.formEdpUrl({
        id: 1
      } as any);
      expect(routingHelperService.formResultedEdpUrl).toHaveBeenCalledWith({ id: 1 }, '');
    });

    it('not tote flow with origin', () => {
      component.origin = 'origin';
      component.formEdpUrl({
        id: 1
      } as any);
      expect(routingHelperService.formResultedEdpUrl).toHaveBeenCalledWith({ id: 1 }, '?origin=origin');
    });
  });

  describe('#handleOutput', () => {
    it('should assign removeEventnameId an event.value', () => {
      const event = {output: 'removeEventNameEmitter', value: '12345'};
      component.handleOutput(event);
      expect(component.removeEventnameId).toBe('12345');
    });
    it('should assign eventStatusData with status', () => {
      const event = {output: 'eventStatusUpdate', value: {id: '1234', data: {title: 'race off'}}};
      component.handleOutput(event);
      expect(component.eventStatusData['1234'].title).toBe('race off');
    });
  });
});
