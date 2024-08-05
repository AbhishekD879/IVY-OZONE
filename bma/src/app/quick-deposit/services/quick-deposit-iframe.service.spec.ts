import { QuickDepositIframeService } from '@app/quick-deposit/services/quick-deposit-iframe.service';
import { of } from 'rxjs';

describe('QuickDepositIframeService', () => {
  let service: QuickDepositIframeService;

  let windowRef;
  let userService;
  let sanitizer;
  let device;
  let cashierResourceService;
  let cashierService;

  const enabled = of(true);

  beforeEach(() => {
    windowRef = {
      nativeWindow: {
        clientConfig: {
          vnCashier: {
            host: 'host'
          }
        }
      }
    };
    userService = {
      ssoToken: 'token',
      username: 'name'
    };
    sanitizer = {
      bypassSecurityTrustResourceUrl: jasmine.createSpy().and.callFake((param) => param)
    };
    device = {
      viewType: 'mobile'
    };
    cashierResourceService = {
      quickDepositEnabled: jasmine.createSpy().and.returnValue(enabled)
    };
    cashierService = {
      goToCashierDeposit: jasmine.createSpy()
    };

    service = new QuickDepositIframeService(
      windowRef,
      userService,
      sanitizer,
      device,
      cashierResourceService,
      cashierService
    );
  });

  it('should return correct url', () => {
    const expectedUrl = 'host/cashierapp/cashier.html?userId=cl_name&brandId=CORAL&'
      + 'productId=SPORTSBOOK&channelId=MW&langId=en&sessionKey=token&stake=10&estimatedReturn=500#/';
    const url = service.getUrl(10, 500);
    expect(url).toBe(expectedUrl);
  });

  it('#isEnabled', () => {
    const result = service.isEnabled();
    expect(result).toBe(enabled);
    expect(cashierResourceService.quickDepositEnabled).toHaveBeenCalled();
  });

  it('#redirectToDepositPage', () => {
    service.redirectToDepositPage();
    expect(cashierService.goToCashierDeposit).toHaveBeenCalledWith(jasmine.objectContaining({}));
  });
});
