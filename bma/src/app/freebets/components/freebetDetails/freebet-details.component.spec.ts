import { throwError, of } from 'rxjs';
import { FreebetDetailsComponent } from './freebet-details.component';
import { fakeAsync, tick } from '@angular/core/testing';

describe('FreebetDetailsComponent', () => {
  let component: FreebetDetailsComponent;
  let filtersService;
  let userService;
  let router;
  let freebetsService;
  let route;
  let routingState;
  let coreToolsService;
  let freeBet: any;
  beforeEach(() => {
    freeBet = {
      freebetTokenValue: '123'
    };
    filtersService = {
      setCurrency: jasmine.createSpy('setCurrency').and.returnValue('123')
    };
    userService = {
      currencySymbol: jasmine.createSpy('currencySymbol'),
      status: false
    };
    router = {
      navigate: jasmine.createSpy('navigate')
    };
    freebetsService = {
      getFreeBet: jasmine.createSpy('getFreeBet').and.returnValue(of(freeBet))
    };
    route = {
      snapshot: {}
    };
    routingState = {
      getRouteParam: jasmine.createSpy()
    };
    coreToolsService = {
      deepClone: jasmine.createSpy().and.callFake((data) => data)
    };

    component = new FreebetDetailsComponent(
      filtersService,
      userService,
      router,
      freebetsService,
      route,
      routingState,
      coreToolsService
    );
  });

  it('constructor', () => {
    expect(component).toBeTruthy();
  });

  describe('#ngOnInit', () => {
    it('ngOnInit success', fakeAsync(() => {
      component.hideSpinner = jasmine.createSpy();

      component.ngOnInit();
      tick();

    expect(routingState.getRouteParam).toHaveBeenCalledWith('betId', route.snapshot);
    expect(freebetsService.getFreeBet).toHaveBeenCalled();
    expect(component.hideSpinner).toHaveBeenCalled();
    expect(component.item).toBe(freeBet);
    expect(filtersService.setCurrency).toHaveBeenCalled();
    expect(coreToolsService.deepClone).toHaveBeenCalledWith(freeBet);
  }));

    it('ngOnInit (get freebet fail)', fakeAsync(() => {
      freebetsService.getFreeBet.and.returnValue(throwError(null));
      component.hideSpinner = jasmine.createSpy();

      component.ngOnInit();
      tick();

      expect(routingState.getRouteParam).toHaveBeenCalledWith('betId', route.snapshot);
      expect(freebetsService.getFreeBet).toHaveBeenCalled();
      expect(component.hideSpinner).toHaveBeenCalled();
    }));

    it('ngOnInit (get freebet fail) no user status', () => {
      freebetsService.getFreeBet.and.returnValue(throwError(null));
      userService.status = true;
      component.hideSpinner = jasmine.createSpy();

      component.ngOnInit();

      expect(routingState.getRouteParam).toHaveBeenCalledWith('betId', route.snapshot);
      expect(freebetsService.getFreeBet).toHaveBeenCalled();
      expect(component.hideSpinner).toHaveBeenCalled();

      expect(component.state.error).toBeTruthy();
      expect(component.hideSpinner).toHaveBeenCalled();
      expect(router.navigate).not.toHaveBeenCalled();
    });
  });
});
