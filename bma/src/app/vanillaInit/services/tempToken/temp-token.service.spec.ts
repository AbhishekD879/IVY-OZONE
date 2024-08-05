import { of as observableOf, throwError as observableThrowError } from 'rxjs';
import { TempTokenService } from '@vanillaInitModule/services/tempToken/temp-token.service';

describe('TempTokenService', () => {
  let service: TempTokenService;

  let http;

  const response = {
    sessionToken: 'sessionToken'
  };
  const url = jasmine.stringMatching('en/coralsports/api/temporarytoken');

  beforeEach(() => {
    http = {
      get: jasmine.createSpy().and.returnValue(observableOf(response))
    };
    service = new TempTokenService(http);
  });

  it('should call get method of api service', () => {
    service.fetchTemporaryToken();
    expect(http.get).toHaveBeenCalledWith(url);
  });

  it('should call get method, call callback and set sessionToken', () => {
    const callback = jasmine.createSpy();
    service.getTemporaryToken(callback);
    expect(http.get).toHaveBeenCalledWith(url);
    expect(service.temporaryToken).toBe(response.sessionToken);
    expect(callback).toHaveBeenCalledWith(response);
  });

  it('should call get method and shouldn`t call callback', () => {
    const callback = jasmine.createSpy();
    service.getTemporaryToken();
    expect(http.get).toHaveBeenCalledWith(url);
    expect(service.temporaryToken).toBe(response.sessionToken);
    expect(callback).not.toHaveBeenCalled();
  });

  it('should not set token and call methods in case of error', () => {
    http.get = jasmine.createSpy().and.returnValue(observableThrowError(null));
    service.getTemporaryToken();
    expect(http.get).toHaveBeenCalledWith(url);
    expect(service.temporaryToken).toBeUndefined();
  });
});
