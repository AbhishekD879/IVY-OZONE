import { ProxyHeadersService } from '@app/bpp/services/proxyHeaders/proxy-headers.service';

describe('Proxy Headers Service', () => {
  let service: ProxyHeadersService,
    userServiceStub;

  beforeEach(() => {
    userServiceStub = {
      bppToken: null
    };

    service = new ProxyHeadersService(userServiceStub);
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
    expect(service['token']).toBe('');
  });

  it('shouldn\'t generate bpp auth header token', () => {
    expect(service['token']).toBe('');
    expect(service.generateBppAuthHeaders()).toBe('');
  });

  it('should generate bpp auth header token', () => {
    expect(service['token']).toBe('');
    userServiceStub.bppToken = '12345';
    expect(service.generateBppAuthHeaders()).toBe('12345');
    expect(service['token']).toBe('12345');
  });

  afterEach(() => {
    service = null;
  });
});
