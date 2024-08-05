import { ReceiptEditComponent } from './receipt-edit.component';
import { of } from 'rxjs';

describe('ReceiptEditComponent', () => {
  let component: ReceiptEditComponent;
  let snackBar;
  let activatedRoute;
  let router;
  let apiClientService;
  let globalLoaderService;
  let dialogService;
  let betReceiptMobileBannerService;

  beforeEach(() => {
    snackBar = {};
    activatedRoute = {
      params: of({ type: 'mobile' })
    };
    router = {};
    apiClientService = {
      betReceiptMobileBanner: () => betReceiptMobileBannerService
    };
    globalLoaderService = {
      showLoader: jasmine.createSpy('showLoader'),
      hideLoader: jasmine.createSpy('hideLoader')
    };
    dialogService = {};
    betReceiptMobileBannerService = {
      getById: jasmine.createSpy('getById').and.returnValue(of({ body: {} }))
    };

    component = new ReceiptEditComponent(
      snackBar, activatedRoute, router, apiClientService, globalLoaderService, dialogService
    );
    component.actionButtons = {
      extendCollection: jasmine.createSpy('extendCollection')
    };
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(betReceiptMobileBannerService.getById).toHaveBeenCalled();
  });
});
