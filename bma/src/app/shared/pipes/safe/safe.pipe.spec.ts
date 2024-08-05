import { SafePipe } from './safe.pipe';

describe('SafePipe', () => {
  let pipe;

  let sanitizer;

  beforeEach(() => {
    sanitizer = {
      bypassSecurityTrustHtml: jasmine.createSpy('bypassSecurityTrustHtml'),
      bypassSecurityTrustUrl: jasmine.createSpy('bypassSecurityTrustUrl'),
      bypassSecurityTrustResourceUrl: jasmine.createSpy('bypassSecurityTrustResourceUrl')
    };

    pipe = new SafePipe(sanitizer);
  });

  it('should call bypassSecurityTrustHtml', () => {
    pipe.transform('html string', 'html');
    expect(sanitizer.bypassSecurityTrustHtml).toHaveBeenCalledWith('html string');
  });

  it('should call bypassSecurityTrustUrl', () => {
    pipe.transform('url string', 'url');
    expect(sanitizer.bypassSecurityTrustUrl).toHaveBeenCalledWith('url string');
  });

  it('should call bypassSecurityTrustResourceUrl', () => {
    pipe.transform('resourceUrl string', 'resourceUrl');
    expect(sanitizer.bypassSecurityTrustResourceUrl).toHaveBeenCalledWith('resourceUrl string');
  });

  it('should return false for wrong type', () => {
    const result = pipe.transform('html', 'htmla');
    expect(result).toEqual(false);
  });
});


