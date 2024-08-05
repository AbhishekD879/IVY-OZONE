import { UpgradeAccountProviderService } from '@app/retail/services/upgradeAccountProvider/upgrade-account-provider.service';
import { of as observableOf, Observable, throwError } from 'rxjs';
import environment from '@environment/oxygenEnvConfig';

describe('UpgradeAccountProviderService', () => {
  let service: UpgradeAccountProviderService, httpClient, infoDialogService, localeService;

  beforeEach(() => {
    httpClient = {
      post: jasmine.createSpy('post').and.returnValue(observableOf({})),
      get: jasmine.createSpy('get').and.returnValue(observableOf({})),
    };
    infoDialogService = jasmine.createSpyObj('infoDialogService', ['openOkDialog']);
    localeService = jasmine.createSpyObj('localeService', ['getString']);

    service = new UpgradeAccountProviderService(httpClient, infoDialogService, localeService);
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
  });
  describe('@getRequest should', () => {
    beforeEach(() => {
      service['token'] = '123';
      localeService.getString.and.returnValue('message');
    });

    it('show dialog with error if http throws error', () => {
      httpClient.post.and.returnValue(throwError({
          error: {
            text: 'Service failure'
          }
        })
      );
      service.getRequest('').subscribe();
      expect(httpClient.post).toHaveBeenCalledTimes(1);
      expect(localeService.getString).toHaveBeenCalledWith('app.serverError');
      expect(infoDialogService.openOkDialog).toHaveBeenCalledWith('message');
    });
    it('not show dialog with error if http throws error', () => {
      httpClient.post.and.returnValue(throwError({
          error: {}
        })
      );
      service.getRequest('').subscribe();
      expect(httpClient.post).toHaveBeenCalled();
      expect(localeService.getString).not.toHaveBeenCalled();
      expect(infoDialogService.openOkDialog).not.toHaveBeenCalledWith('message');
    });
    it('call getRequest if http returns Token is not valid', () => {
      httpClient.post.and.returnValue(observableOf({
          errorMessage: 'Token is not valid'
        }
      ));
      service.getRequest('').subscribe();
      expect(httpClient.post).toHaveBeenCalledTimes(2);
      expect(service['token']).toEqual('');
      expect(localeService.getString).not.toHaveBeenCalled();
      expect(infoDialogService.openOkDialog).not.toHaveBeenCalledWith();
    });
    it('handle 401 error', () => {
      const successHandler = jasmine.createSpy('successHandler');
      const errorHandler = jasmine.createSpy('errorHandler');
      httpClient.post.and.returnValue(throwError({
            status: 401
        })
      );
      service.getRequest('').subscribe(successHandler, errorHandler);
      expect(service['token']).toEqual('');
      expect(httpClient.post).toHaveBeenCalledTimes(2);
      expect(localeService.getString).not.toHaveBeenCalled();
      expect(infoDialogService.openOkDialog).not.toHaveBeenCalled();
      expect(successHandler).not.toHaveBeenCalled();
      expect(errorHandler).toHaveBeenCalled();
    });
    it('not show dialog with error if no exceptions', () => {
      httpClient.post.and.returnValue(observableOf({}));
      service.getRequest('').subscribe();

      expect(localeService.getString).not.toHaveBeenCalled();
      expect(infoDialogService.openOkDialog).not.toHaveBeenCalled();
    });
    it('should be called with params', () => {
      httpClient.post.and.returnValue(observableOf({}));
      service.getRequest('test', {param: 'param'}, 'cwa_api_index.php').subscribe();
      expect(httpClient.post).toHaveBeenCalledTimes(1);
      expect(localeService.getString).not.toHaveBeenCalled();
      expect(infoDialogService.openOkDialog).not.toHaveBeenCalled();
    });
    it('should handle if there is no web token', () => {
      service['getWebToken'] = jasmine.createSpy('getWebToken').and.returnValue(observableOf(undefined));

      service.getRequest('').subscribe(null, (error) => {
        expect(error).toEqual(jasmine.any(Error));
      });
    });
  });
  describe('@getCardRequest should', () => {
    it('should get card number by passing userinfo', () => {
      const params = { username: 'username', customerSessionId: 'customerSessionId' };
      const endpoint = `${environment.APOLLO.CARD_ENDPOINT}/${params.username}/token-id?api-key=`
      +`${environment.APOLLO.API_KEY}&locale=en-GB&tokenType=gvc`;
      httpClient.get.and.returnValue(observableOf({ body: { data: { token: '111' } } }));
      service['getCardRequest'](params).subscribe();
      expect(httpClient.get).toHaveBeenCalledWith(endpoint, {
        observe: 'response',
        headers: {
          'X-CLIENT-REQUEST-ID': params.customerSessionId.substring(12),
          'X-FORWARDED-FOR': params.customerSessionId.substring(12),
          'Authorization': `Bearer ${params.customerSessionId}`
        }
      });
    });
  });
  describe('getWebToken', () => {
    beforeEach(() => {
      service['token'] = '123';
    });
    it('should return token if it exist', () => {
      const errorHandler = jasmine.createSpy('errorHandler');
      service['getWebToken']().subscribe((res) => {
        expect(res).toEqual('123');
      }, errorHandler);
      expect(errorHandler).not.toHaveBeenCalled();
      expect(httpClient.post).not.toHaveBeenCalled();
    });
    it('should call http if token is empty', () => {
      const endpoint = `${environment.APOLLO.API_ENDPOINT}/${environment.APOLLO.CWA_ROUTE}/sessionwebtoken`;
      const retailCreds = { hash: 'MzFhNDYwNDhkZGJiNjdiYzZkYTI0ODMzZTRmNDAxNmEwMTliNzFmYTkzODc0NDY0MTJmMDRmOTZmZDk2N2M5YQ' };
      service['token'] = '';
      httpClient.post.and.returnValue(observableOf({data: { token: '111'}}));
      service['getWebToken']().subscribe((res) => {
        expect(res).toEqual(service['token']);
      });
      expect(httpClient.post).toHaveBeenCalledWith(endpoint, retailCreds);
    });
  });
  describe('all getRequest methods', () => {
    beforeEach(() => {
      spyOn(service, 'getRequest').and.returnValue(jasmine.any(Observable) as any);
    });
    it('upgradeAccount', () => {
      const userData = {} as any;
      const result = service.upgradeAccount(userData);

      expect(service.getRequest).toHaveBeenCalledWith('upgradeinshoptomultichannel', userData);
      expect(result).toEqual(jasmine.any(Observable));
    });
    it('authenticate', () => {
      const cardNo = '1111111111';
      const pin = 111;
      const result = service.authenticate(cardNo, pin);

      expect(service.getRequest).toHaveBeenCalledWith('authenticate', {cardNo, pin});
      expect(result).toEqual(jasmine.any(Observable));
    });
    it('isEligible', () => {
      const cardNumber = '1111111111';
      const pin = 111;
      const result = service.isEligible(cardNumber, pin);

      expect(service.getRequest).toHaveBeenCalledWith('isinshopeligibleforupgrade', {cardNumber, pin});
      expect(result).toEqual(jasmine.any(Observable));
    });
    it('getPlayerInfo', () => {
      const cardNumber = '1111111111';
      const result = service.getPlayerInfo(cardNumber);

      expect(service.getRequest).toHaveBeenCalledWith('getplayerinfo', {username: cardNumber});
      expect(result).toEqual(jasmine.any(Observable));
    });
  });
});
