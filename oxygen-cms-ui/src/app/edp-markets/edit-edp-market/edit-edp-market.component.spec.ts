import { of } from 'rxjs';
import { EditEdpMarketComponent } from './edit-edp-market.component';

describe('EditEdpMarketComponent', () => {
  let component: EditEdpMarketComponent;
  let activatedRoute;
  let router;
  let apiClientService;
  let globalLoaderService;
  let dialogService;
  let edpService;

  beforeEach(() => {
    activatedRoute = {
      params: of({})
    };
    router = {};
    apiClientService = {
      edp: () => edpService
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    dialogService = {};
    edpService = {
      getById: jasmine.createSpy('getById').and.returnValue(of({ body: {} }))
    };

    component = new EditEdpMarketComponent(
      activatedRoute, router, apiClientService, globalLoaderService, dialogService
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(edpService.getById).toHaveBeenCalled();
  });
});
