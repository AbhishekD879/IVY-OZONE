import { WidgetsPageComponent } from './widgets.page.component';
import { of } from 'rxjs';

describe('WidgetsPageComponent', () => {
  let component: WidgetsPageComponent;
  let widgetsAPIService, snackBar;

  beforeEach(() => {
    widgetsAPIService = {
      getWidgetsData: jasmine.createSpy('getWidgetsData').and.returnValue(of({ body: 'test' }))
    };
    snackBar = {};
    component = new WidgetsPageComponent(
      widgetsAPIService, snackBar
    );

    component.ngOnInit();
  });

  it('should call getWidgetsData', () => {
    expect(widgetsAPIService.getWidgetsData).toHaveBeenCalled();
  });
});
