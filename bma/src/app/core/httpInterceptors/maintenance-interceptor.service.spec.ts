import { MaintenanceInterceptor } from './maintenance-interceptor.service';
import { of, throwError } from 'rxjs';
import { HttpErrorResponse, HttpResponse } from '@angular/common/http';
import { ICrashDetails } from '@core/httpInterceptors/crash-details.model';
import environment from '@environment/oxygenEnvConfig';

describe('MaintenanceInterceptor', () => {
  let service: MaintenanceInterceptor;
  let device;
  let tempStorage;
  let route;
  let router;
  let awsService;
  let httpHandler;
  let crashMock;

  const patchCrashMock = (data: ICrashDetails): ICrashDetails => {
    return { ...crashMock, date: data.date, timestamp: data.timestamp };
  };

  beforeEach(() => {
    device = {};
    tempStorage = {
      set: jasmine.createSpy('set')
    };
    route = {
      params: {},
      snapshot: {}
    };
    router = {
      navigate: jasmine.createSpy('navigate')
    };
    awsService = {
      trackOxygenRequest: jasmine.createSpy('trackOxygenRequest'),
      getUniqueSubscriberName: jasmine.createSpy('getUniqueSubscriberName').and.returnValue(`awsFirSubscr_${new Date().getTime()}`)
    };
    httpHandler = {
      handle: jasmine.createSpy('handle').and.returnValue(of({ res: 'res' }))
    };
    crashMock = {
      params: {},
      segment: undefined,
      date: '',
      timestamp: 0,
      url: 'Internet Connection Lost',
      method: null,
      status: null,
      statusText: 'Internet connnection lost',
      device: {},
      environment: 'dev'
    };

    service = new MaintenanceInterceptor(
      device,
      tempStorage,
      route,
      router,
      awsService
    );
  });
  describe('intercept', () => {
    const req = { req: 'req' } as any;

    let errorResponse;

    beforeEach(() => {
      service['getResponseTime'] = jasmine.createSpy('getResponseTime').and.returnValue(10);
      errorResponse = { status: 0, statusText: 'statusText' };
    });

    it('success: should not call trackOxygenRequest', () => {
      service.intercept(req, httpHandler).subscribe();
      expect(awsService.trackOxygenRequest).not.toHaveBeenCalled();
    });

    it('success: should call trackOxygenRequest', () => {
      const response: HttpResponse<any> = new HttpResponse(<any>{ res: 'res' });

      httpHandler.handle = jasmine.createSpy('handle').and.returnValue(of(response));

      service.intercept(req, httpHandler).subscribe();
      expect(awsService.trackOxygenRequest).toHaveBeenCalledWith(req, response, jasmine.any(Number),service['subscriberName']);
      expect(service['getResponseTime']).toHaveBeenCalledWith(jasmine.any(Number));
    });

    it('error: trackOxygenRequest', () => {
      httpHandler.handle = jasmine.createSpy().and.returnValue(
        throwError(new HttpErrorResponse({}))
      );

      service.intercept(req, httpHandler).subscribe(() => { }, () => { });
      expect(awsService.trackOxygenRequest).toHaveBeenCalledWith({ req: 'req' }, jasmine.any(HttpErrorResponse),
      10,service['subscriberName']);
      expect(service['getResponseTime']).toHaveBeenCalledWith(jasmine.any(Number));
    });

    it('error: SITESERVER_ENDPOINT', () => {
      errorResponse.url = environment.SITESERVER_ENDPOINT;

      const crashDetailsMock: ICrashDetails = { ...crashMock, ...errorResponse };

      httpHandler.handle = jasmine.createSpy().and.returnValue(
        throwError(new HttpErrorResponse(errorResponse))
      );

      service['getCrashDetails'] = jasmine.createSpy('getCrashDetails').and.returnValue(crashMock);

      service.intercept(req, httpHandler).subscribe(() => { }, () => { });
      expect(service['getCrashDetails']).toHaveBeenCalled();
      expect(tempStorage.set).toHaveBeenCalledWith('crashDetails', crashDetailsMock);
      expect(router.navigate).not.toHaveBeenCalledWith(['/under-maintenance']);
    });

    it('error: CMS_ENDPOINT', () => {
      errorResponse.url = `${environment.SITESERVER_ENDPOINT}/${environment.CMS_ENDPOINT}`;

      httpHandler.handle = jasmine.createSpy().and.returnValue(
        throwError(new HttpErrorResponse(errorResponse))
      );

      service.intercept(req, httpHandler).subscribe(() => { }, () => { });
      expect(router.navigate).toHaveBeenCalledWith(['/under-maintenance']);
    });

    afterEach(() => {
      expect(httpHandler.handle).toHaveBeenCalledWith(req);
    });
  });

  it('getCrashDetails should return crash details', () => {
    const res: ICrashDetails = service['getCrashDetails']();

    expect(res).toEqual(patchCrashMock(res));
  });
});
