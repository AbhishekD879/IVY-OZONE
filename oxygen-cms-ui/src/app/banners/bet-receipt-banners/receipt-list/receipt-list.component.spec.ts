import { ReceiptListComponent } from './receipt-list.component';
import { of } from 'rxjs';

describe('ReceiptListComponent', () => {
  let component: ReceiptListComponent;
  let activatedRoute;
  let router;
  let apiClientService;
  let globalLoaderService;
  let dialogService;
  let snackBar;
  let betReceiptMobileBannerService;

  beforeEach(() => {
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
    snackBar = {};
    betReceiptMobileBannerService = {
      findAllByBrand: jasmine.createSpy('findAllByBrand').and.returnValue(of({ body: {} }))
    };

    component = new ReceiptListComponent(
      activatedRoute, router, apiClientService, globalLoaderService, dialogService, snackBar
    );
  });

  it('ngOnInit', () => {
    component.ngOnInit();
    expect(betReceiptMobileBannerService.findAllByBrand).toHaveBeenCalled();
  });
});
