import { LocaleInterceptor } from './locale-interceptor.service';
import environment from '@environment/oxygenEnvConfig';

describe('LocaleInterceptor', () => {
  let service: LocaleInterceptor;
  let req;
  let next;

  beforeEach(() => {
    req = {
      clone: jasmine.createSpy(),
      url: '',
    };
    next = {
      handle: jasmine.createSpy()
    };
    service = new LocaleInterceptor();
  });

  it('intercept', () => {
    service.intercept(req, next);
    expect(next.handle).toHaveBeenCalledTimes(1);
    expect(next.handle).toHaveBeenCalledWith(req);
  });

  it('intrcept when ss', () => {
    req.url = `${environment.SITESERVER_ENDPOINT}/health-check`;
    service.intercept(req, next);
    expect(req.clone).toHaveBeenCalledWith({ url: `${req.url}?translationLang=en&responseFormat=json` });
  });

  it('intrcept when ss', () => {
    req.url = `${environment.SITESERVER_ENDPOINT}/health-check?simple-filter=category=12`;
    service.intercept(req, next);
    expect(req.clone).toHaveBeenCalledWith({ url: `${req.url}&translationLang=en&responseFormat=json` });
  });

  it('intrcept when ss commentary', () => {
    req.url = `${environment.SITESERVER_COMMENTARY_ENDPOINT}/health-check?simple-filter=category=12`;
    service.intercept(req, next);
    expect(req.clone).toHaveBeenCalledWith({ url: `${req.url}&translationLang=en&responseFormat=json` });
  });
});
