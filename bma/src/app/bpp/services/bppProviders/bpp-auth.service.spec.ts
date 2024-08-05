
import { of as observableOf,  Observable } from 'rxjs';
import { BppAuthService } from '@app/bpp/services/bppProviders/bpp-auth.service';
import environment from '@environment/oxygenEnvConfig';

describe('BPP Auth Service', () => {
  let service: BppAuthService,
    httpServiceStub;

  beforeEach(() => {
    httpServiceStub = {
      post: jasmine.createSpy().and.returnValue(observableOf(null))
    };

    service = new BppAuthService(httpServiceStub);
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
    expect(service['apiEndpoint']).toBe(environment.BPP_ENDPOINT);
  });

  it('should validate', () => {
    const body = { username: 'joe', token: '12345' };

    service['postData'] = jasmine.createSpy().and.returnValue(observableOf(null));
    const result = service.validate(body);

    expect(service['postData']).toHaveBeenCalledWith(`auth/user`, body);
    expect(result).toEqual(jasmine.any(Observable));
  });

  it('should post data', () => {
    const url = `auth/user`,
      body = { username: 'joe', token: '12345' },
      result = service['postData'](url, body);

    expect(httpServiceStub.post).toHaveBeenCalledWith(`${environment.BPP_ENDPOINT}/${url}`, body, {
      withCredentials: true
    });
    expect(result).toEqual(jasmine.any(Observable));
  });

  afterEach(() => {
    service = null;
  });
});
