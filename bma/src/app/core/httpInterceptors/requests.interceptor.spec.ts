import { fakeAsync, tick } from '@angular/core/testing';
import { throwError } from 'rxjs';

import { RequestsInterceptor } from '@core/httpInterceptors/requests.interceptor';

describe('RequestsInterceptor', () => {
  let interceptor: RequestsInterceptor;
  let injector;
  let errorLogger;

  beforeEach(() => {
    errorLogger = {
      errorLog: jasmine.createSpy('errorLog')
    };
    injector = {
      get: jasmine.createSpy('get').and.returnValue(errorLogger)
    };
    interceptor = new RequestsInterceptor(injector);
  });

  it('intercept', fakeAsync(() => {
    const request: any = {};
    const error = {};
    const next = {
      handle: jasmine.createSpy('handle').and.returnValue(throwError(error))
    };

    interceptor.intercept(request, next).subscribe(null, () => {});
    tick();

    expect(injector.get).toHaveBeenCalledTimes(1);
    expect(next.handle).toHaveBeenCalledWith(request);
    expect(errorLogger.errorLog).toHaveBeenCalledWith(error);
  }));
});
