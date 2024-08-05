import {
  OutrightsSportTabComponent
} from '@sb/components/outrightsSportTab/outrights-sport-tab.component';
import { fakeAsync, tick } from '@angular/core/testing';

describe('#OutrightsSportTabComponent', () => {
  let component: OutrightsSportTabComponent;
  let sportTabsService, pubSubService, routingHelper, slpSpinnerStateService;

  const event = { id: 21312 } as any;

  beforeEach(() => {
    slpSpinnerStateService = {
      handleSpinnerState: jasmine.createSpy('handleSpinnerState')
    };
    sportTabsService = {
      deleteEvent: jasmine.createSpy('deleteEvent'),
      eventsBySections: jasmine.createSpy('eventsBySections')
    };

    pubSubService = {
      subscribe: jasmine.createSpy('subscribe'),
      unsubscribe: jasmine.createSpy('unsubscribe'),
      API: {
        RELOAD_COMPONENTS: 'RELOAD_COMPONENTS',
        DELETE_EVENT_FROM_CACHE: 'DELETE_EVENT_FROM_CACHE'
      }
    };
    routingHelper = {
      formEdpUrl: jasmine.createSpy('formEdpUrl')
    };
    component = new OutrightsSportTabComponent(sportTabsService, pubSubService, routingHelper, slpSpinnerStateService);

    component.sport = {
      getByTab: jasmine.createSpy('getByTab').and.returnValue(Promise.resolve([]))
    } as any;
  });

  it('#eventURL - should go to EDP', () => {
    component.eventURL(event);
    expect(routingHelper.formEdpUrl).toHaveBeenCalledWith(event);
  });

  it('#ngOnInit', fakeAsync(() => {
    pubSubService.subscribe.and.callFake((param1, param2, cb) => cb(param1, param2));

    component.ngOnInit();
    tick();

    expect(pubSubService.subscribe).toHaveBeenCalledTimes(1);
    expect(slpSpinnerStateService.handleSpinnerState).toHaveBeenCalled();
    expect(pubSubService.subscribe).toHaveBeenCalledWith(
      'OutrightsSportTabComponent', 'DELETE_EVENT_FROM_CACHE', jasmine.any(Function));
    expect(sportTabsService.deleteEvent).toHaveBeenCalledWith(jasmine.any(String), jasmine.any(Array));
  }));

  it('#ngOnDestroy', () => {
    component.ngOnDestroy();
    expect(pubSubService.unsubscribe).toHaveBeenCalledWith('OutrightsSportTabComponent');
  });

  it('trackById', () => {
    const result = component.trackById(1, {typeId: 'test'} as any);

    expect(result).toBe('test');
  });

  describe('loadOutrightData', () => {
    it('should call sport.getByTab', fakeAsync(() => {
      component['loadOutrightData']();
      tick();

      expect(component.sport.getByTab).toHaveBeenCalled();
      expect(component.isResponseError).toBeFalsy();
    }));

    it('should call sportTabsService.eventsBySections if there are events', fakeAsync(() => {
      component.sport.getByTab = jasmine.createSpy('getByTab').and.returnValue(Promise.resolve([
        {id: 0}, {id: 1}
      ]));

      component['loadOutrightData']();
      tick();

      expect(component['sportTabsService'].eventsBySections).toHaveBeenCalled();
    }));

    it('should not call sportTabsService.eventsBySections if there are no events', fakeAsync(() => {
      component['loadOutrightData']();
      tick();

      expect(sportTabsService.eventsBySections).not.toHaveBeenCalled();
    }));

    it('should call sport.getByTab and handle error', fakeAsync(() => {
      component.sport.getByTab = jasmine.createSpy('getByTab').and.returnValue(Promise.reject({error: ''}));
      component['loadOutrightData']();
      tick();

      expect(component.isResponseError).toBeTruthy();
    }));

  });
});
