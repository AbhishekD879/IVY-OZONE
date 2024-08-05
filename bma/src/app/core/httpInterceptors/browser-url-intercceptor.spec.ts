import { BrowserUrlInterceptor } from './browser-url-interceptor';

describe('BrowserUrlInterceptor', () => {
  let service: BrowserUrlInterceptor;

  let urlService;
  let req;
  let next;
  let productServiceMock;

  const deleteNativeExtraHeader = { delete: jasmine.createSpy().and.returnValue({}) };
  const deleteExtraHeader = { delete: jasmine.createSpy().and.returnValue(deleteNativeExtraHeader) };
  const deleteResult = { delete: jasmine.createSpy().and.returnValue(deleteExtraHeader) };
  const result = {
    delete: jasmine.createSpy().and.returnValue(deleteResult)
  };
  const clonedReq = {};

  beforeEach(() => {
    req = {
      url: 'url',
      clone: jasmine.createSpy().and.returnValue(clonedReq),
      headers: {
        delete: jasmine.createSpy().and.returnValue(result)
      }
    };
    next = {
      handle: jasmine.createSpy()
    };
    productServiceMock = {
      getMetadata: jasmine.createSpy().and.returnValue({ apiBaseUrl: 'protocol://portalhostname' })
    };
    urlService = {
      parse: jasmine.createSpy().and.callFake((param: string) => {
        if (param === req.url) {
          return { isSameHost: true, hostname: 'hostname' };
        } else if (param === productServiceMock.getMetadata().apiBaseUrl) {
          return { hostname: 'portalhostname' };
        }
      })
    };
    service = new BrowserUrlInterceptor(urlService, productServiceMock);
  });

  it('#intercept should call correct methods when is the same host but not same as portal apiBaseUrl', () => {
    service.intercept(req, next);
    expect(urlService.parse).toHaveBeenCalledWith(req.url);
    expect(productServiceMock.getMetadata).toHaveBeenCalledWith('portal');
    expect(urlService.parse).toHaveBeenCalledWith(productServiceMock.getMetadata().apiBaseUrl);
    expect(next.handle).toHaveBeenCalledWith(req);
  });

  it('#intercept should call correct methods when not the same host but same as portal apiBaseUrl', () => {
    urlService = {
      parse: jasmine.createSpy().and.callFake((param: string) => {
        if (param === req.url) {
          return { isSameHost: false, hostname: 'portalhostname' };
        } else if (param === productServiceMock.getMetadata().apiBaseUrl) {
          return { hostname: 'portalhostname' };
        }
      })
    };
    service = new BrowserUrlInterceptor(urlService, productServiceMock);
    service.intercept(req, next);
    expect(urlService.parse).toHaveBeenCalledWith(req.url);
    expect(productServiceMock.getMetadata).toHaveBeenCalledWith('portal');
    expect(urlService.parse).toHaveBeenCalledWith(productServiceMock.getMetadata().apiBaseUrl);
    expect(next.handle).toHaveBeenCalledWith(req);
  });

  it('#intercept should call correct methods when is not the same host and not same as portal apiBaseUrl', () => {
    urlService = {
      parse: jasmine.createSpy().and.callFake((param: string) => {
        if (param === req.url) {
          return { isSameHost: false, hostname: 'hostname' };
        } else if (param === productServiceMock.getMetadata().apiBaseUrl) {
          return { hostname: 'portalhostname' };
        }
      })
    };
    service = new BrowserUrlInterceptor(urlService, productServiceMock);
    service.intercept(req, next);
    expect(req.headers.delete).toHaveBeenCalledWith('X-Native-App');
    expect(result.delete).toHaveBeenCalledWith('x-bwin-browser-url');
    expect(req.clone).toHaveBeenCalledWith(jasmine.objectContaining({ headers: {} }));
    expect(next.handle).toHaveBeenCalledWith(clonedReq);
  });
});
