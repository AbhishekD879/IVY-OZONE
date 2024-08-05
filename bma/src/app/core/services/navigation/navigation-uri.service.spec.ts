import { NavigationUriService } from './navigation-uri.service';

describe('NavigationUriService', () => {
  let service: NavigationUriService;

  const externalUrl = 'https://gaming.coral.co.uk/';
  const internalUrl = '/tennis';
  const internalAbsoluteUrl = 'https://test-domain.com/tennis';

  beforeEach(() => {
    const windowRefService = {
      nativeWindow: {
        location: {
          origin: 'https://my-domain.com'
        }
      }
    } as any;

    service = new NavigationUriService(
      windowRefService
    );
  });

  it('link is internal if is relative', () => {
    expect(service.origin).toBe('https://my-domain.com');
  });

  describe('isInternalUri', () => {

    it('link is internal if is relative', () => {
      spyOn(service, 'isAbsoluteUri').and.returnValue(false);

      expect(service.isInternalUri('')).toBe(true);
      expect(service.isInternalUri()).toBe(true);
    });

    it('link is internal if absolute but refers to same origin', () => {
      spyOn(service, 'isAbsoluteUri').and.returnValue(true);
      spyOn(service, 'isSameOriginUri').and.returnValue(true);

      expect(service.isInternalUri('')).toBe(true);
    });

    it('link is external if absolute and refers to different origin', () => {
      spyOn(service, 'isAbsoluteUri').and.returnValue(true);
      spyOn(service, 'isSameOriginUri').and.returnValue(false);

      expect(service.isInternalUri('')).toBe(false);
    });
  });

  describe('isAbsoluteUri', () => {

    it('should check that link is absolute (based on protocol)', () => {
      expect(service.isAbsoluteUri(externalUrl)).toBe(true);
    });

    it('should check that internal link is still absolute (based on protocol)', () => {
      expect(service.isAbsoluteUri(internalAbsoluteUrl)).toBe(true);
    });

    it('should check that relative link is a such (no protocol)', () => {
      expect(service.isAbsoluteUri(internalUrl)).toBe(false);
      expect(service.isAbsoluteUri()).toBe(false);
    });
  });

  describe('isSameOriginUri', () => {

    it('should detect same origin', () => {
      expect(service.isSameOriginUri('https://my-domain.com/tab')).toBe(true);
    });

    it('should detect different origin', () => {
      expect(service.isSameOriginUri('https://google.com/tab')).toBe(false);
      expect(service.isSameOriginUri()).toBe(false);
    });
  });
});
