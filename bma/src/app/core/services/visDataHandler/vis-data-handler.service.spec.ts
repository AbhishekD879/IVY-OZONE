import { of as observableOf } from 'rxjs';
import { pubSubApi } from '@core/services/communication/pubsub/pubsub-api.constant';
import { VisDataHandlerService } from './vis-data-handler.service';

describe('VisDataHandlerService', () => {
  let service: VisDataHandlerService;

  let eventFactory;
  let visEventService;
  let cmsService;
  let pubSubService;
  let route;
  let routingState;

  const eventEntity = {
    id: '123456',
    categoryId: '13',
    eventIsLive: true
  };

  beforeEach(() => {
    eventFactory = {
      getEvent: jasmine.createSpy().and.returnValue(Promise.resolve(eventEntity))
    };
    visEventService = {
      checkForEventsWithAvailableVisualization: jasmine.createSpy().and.returnValue(observableOf({})),
      checkPreMatchWidgetAvailability: jasmine.createSpy().and.returnValue(observableOf({}))
    };
    cmsService = {
      getSystemConfig: jasmine.createSpy().and.returnValue(observableOf({
        VisualisationConfig: {
          timeout: 1000,
          footballId: '13',
          tennisId: '14'
        }
      }))
    };
    pubSubService = {
      publish: jasmine.createSpy(),
      API: pubSubApi
    };
    route = {
      snapshot: {}
    };
    routingState = {
      getRouteParam: jasmine.createSpy().and.returnValue('123456')
    };

    service = new VisDataHandlerService(
      eventFactory,
      visEventService,
      cmsService,
      pubSubService,
      route,
      routingState
    );
  });

  describe('init', () => {
    it('no event', (done) => {
      service.init().subscribe((res) => {
        expect(eventFactory.getEvent).toHaveBeenCalledTimes(1);
        expect(eventFactory.getEvent).toHaveBeenCalledWith('123456');
        expect(cmsService.getSystemConfig).toHaveBeenCalled();
        res.subscribe(() => {
          expect(visEventService.checkForEventsWithAvailableVisualization).toHaveBeenCalledTimes(1);
          expect(visEventService.checkPreMatchWidgetAvailability).toHaveBeenCalledTimes(1);
          expect(pubSubService.publish).toHaveBeenCalledTimes(1);
          expect(pubSubService.publish).toHaveBeenCalledWith(pubSubService.API.DISPLAY_WIDGET, [{ name: 'match-centre' }]);
          done();
        });
      });
    });

    it('with event', (done) => {
      service.init(<any>eventEntity).subscribe((res) => {
        expect(eventFactory.getEvent).not.toHaveBeenCalled();
        expect(cmsService.getSystemConfig).toHaveBeenCalled();
        done();
      });
    });

    it('with event, but not vis', (done) => {
      eventEntity.categoryId = '15';
      service.init(<any>eventEntity).subscribe(() => {}, (res) => {
        expect(res).toEqual('Not football or tennis vis');
        done();
      });
    });
  });

  describe('getVisEndpoint', () => {
    it('getVisEndpoint (football)', () => {
      eventEntity.categoryId = '15';
      service['getVisEndpoint'](<any>{ categoryId: '13' }).subscribe(data => {
        expect(data.visEndpoint).not.toBeUndefined();
      });
    });

    it('with event, but not vis (tennis)', () => {
      eventEntity.categoryId = '14';
      service['getVisEndpoint'](<any>{ categoryId: '14' }).subscribe(data => {
        expect(data.visEndpoint).not.toBeUndefined();
      });
    });

    it('with event, but not vis (disabled)', () => {
      service['cmsService'].getSystemConfig = () => observableOf({
        VisualisationConfig: {
          timeout: 1000,
          footballId: '13',
          tennisId: '14',
          disabled: true
        }
      });
      eventEntity.categoryId = '14';
      service['getVisEndpoint'](<any>{ categoryId: '14' }).subscribe(data => {
        expect(data.visEndpoint).toBeUndefined();
      });
    });
  });
});
