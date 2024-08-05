import { of, throwError } from 'rxjs';
import { StaticComponent } from './static.component';

describe('StaticComponent', () => {
  let component: StaticComponent;
  let cmsService;
  let routingState;
  let route;

  beforeEach(() => {
    cmsService = {
      getStaticBlock: jasmine.createSpy().and.returnValue(of({
        title: 'as'
      }))
    };
    routingState = {
      getRouteParam: jasmine.createSpy().and.returnValue('static')
    };
    route = {
      snapshot: {}
    };
    component = new StaticComponent(cmsService, route, routingState);
  });

  it('should create component instance', () => {
    expect(component).toBeTruthy();
  });

  it('#ngOnInit', () => {
    component.hideSpinner = jasmine.createSpy();
    component.ngOnInit();
    expect(component.content).toEqual(<any>{
      title: 'as'
    });
    expect(component.hideSpinner).toHaveBeenCalled();
    expect(cmsService.getStaticBlock).toHaveBeenCalledWith('static', null);
    expect(routingState.getRouteParam).toHaveBeenCalledWith('static-block', route.snapshot);
  });

  it('ngOnInit error', () => {
    cmsService.getStaticBlock.and.returnValue(throwError('error'));
    component.ngOnInit();
    expect(component.state.error).toBeTruthy();
  });
});
