import { WidgetPageComponent } from './widget.page.component';
import { of } from 'rxjs';

describe('PromotionsPageComponent', () => {
  let component: WidgetPageComponent;
  let dialogService, route, router, widgetsAPIService, apiClientService;


  beforeEach(() => {
    route = {
      snapshot: {
        paramMap: { get: jasmine.createSpy('get') }
      }
    };
    dialogService = {};
    router = {};
    widgetsAPIService = {
      getSingleWidgetData: jasmine.createSpy('getSingleWidgetData').and.returnValue(of({ body: 'test' }))
    };
    apiClientService = {};
    component = new WidgetPageComponent(
      dialogService, route, router, widgetsAPIService, apiClientService
    );

    component.ngOnInit();
  });

  it('should call getSingleWidgetData', () => {
    const data = 'test' as any;
    expect(widgetsAPIService.getSingleWidgetData).toHaveBeenCalled();
    expect(component.widget).toEqual(data);
  });
});
