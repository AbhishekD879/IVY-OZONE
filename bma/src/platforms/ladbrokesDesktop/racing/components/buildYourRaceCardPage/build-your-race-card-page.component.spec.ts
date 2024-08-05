import { BuildYourRaceCardPageComponent } from './build-your-race-card-page.component';
import { of } from 'rxjs';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';

describe('LadbrokesBuildYourRaceCardPageComponent', () => {
  let component: BuildYourRaceCardPageComponent;
  let buildYourRaceCardPageService;
  let routingState;
  let route;
  let router;
  let routingHelperService,
  pubSubService;

  beforeEach(() => {
    buildYourRaceCardPageService = {
      getEvents: jasmine.createSpy().and.returnValue( of({}).toPromise() ),
      subscribeForUpdates: jasmine.createSpy(),
      unSubscribeForUpdates: jasmine.createSpy()
    };
    routingState = {
      getRouteParam: jasmine.createSpy()
    };
    route = {};
    router = {};
    routingHelperService = {
      formSportUrl: jasmine.createSpy('formSportUrl').and.returnValue(of(''))
    };
    pubSubService = {
      API: pubSubApi,
      publish: jasmine.createSpy('publish'),
      subscribe: jasmine.createSpy('subscribe').and.callFake((subscriber, method, cb ) => {
        if (method === 'EMA_UNSAVED_ON_EDP') {
          cb(true);
        } else if (method === 'SUSPEND_IHR_EVENT_OR_MRKT') {
          cb('555', {fcMktAvailable: 'N', tcMktAvailable: 'N', originalName: 'Win or Each Way'});
        }
      }),
    };

    component = new BuildYourRaceCardPageComponent(buildYourRaceCardPageService, routingState, route, router, routingHelperService, pubSubService);
  });

  describe('onInit', () => {
    it('should save subscription', () => {
      component.ngOnInit();
      expect(component['eventsSubscription']).toBeDefined();
    });
    it('should set fc/tc delta in event', () => {
      component.events = [{id: '555'}] as any;
      component.ngOnInit();
      expect(component.events[0].delta).toEqual({fcMktAvailable: 'N', tcMktAvailable: 'N', updateEventId: '555', originalName: 'Win or Each Way'});
    });
  });

  describe('onDestroy', () => {
    it('should unsubscribe subscriptions', () => {
      component.ngOnInit();
      spyOn(component['eventsSubscription'], 'unsubscribe');
      component.ngOnDestroy();
      expect(component['eventsSubscription'].unsubscribe).toHaveBeenCalled();
    });

    it('should not call unsubscribe', () => {
      component.ngOnDestroy();
      expect(component['eventsSubscription']).toBeUndefined();
    });
  });

});
