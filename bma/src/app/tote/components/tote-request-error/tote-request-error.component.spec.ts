import { ToteRequestErrorComponent } from './tote-request-error.component';
import { TOTE_CONFIG } from '../../tote.constant';

describe('ToteRequestErrorComponent', () => {
  let component: ToteRequestErrorComponent, route, routingState;

  beforeEach(() => {
    route = {
      snapshot: {
        params: {}
      }
    };
    routingState = {
      getRouteParam: jasmine.createSpy('routingState.getRoutingParams').and.returnValue('test_param')
    };

    component = new ToteRequestErrorComponent(route, routingState);
    component.activeTab = {id: null};
  });

  it('ngOnInit no route params', () => {
    component.ngOnInit();

    expect(component.activeTab.id).toBe('tab-results');
  });

  it('ngOnInit with route params', () => {
    route.snapshot.params.sport = 'test_sport_param';
    component.ngOnInit();

    expect(routingState.getRouteParam).toHaveBeenCalled();
    expect(component.activeTab.id).toBe('tab-test_param');
  });

  it('ngOnInit with route params (default tote sport)', () => {
    routingState.getRouteParam.and.returnValue('');
    route.snapshot.params.sport = 'test_sport_param';
    component.ngOnInit();
    expect(component.activeTab.id).toBe(`tab-${TOTE_CONFIG.DEFAULT_TOTE_SPORT}`);
  });
});
