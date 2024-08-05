import { RecapchaService } from './recapcha.service';

describe('RecapchaService', () => {
  let service : RecapchaService,
    windowRef

  beforeEach(() => {
    windowRef = {
      document: {
        createElement: jasmine.createSpy('createElement'),
        getElementById: jasmine.createSpy('createId'),
        body: {
          appendChild: jasmine.createSpy('appendChild')
        }
      }
    };
    service = new RecapchaService(windowRef);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('addscript',()=>{
  it('When element id = ! recaptcha-enterprise',()=>{
    windowRef.document.getElementById.and.returnValue(true);
    const mock: any = {};
    windowRef.document.createElement.and.returnValue(mock);
    service.addScript();
    expect(windowRef.document.createElement).not.toHaveBeenCalled();
    expect(windowRef.document.body.appendChild).not.toHaveBeenCalled();
  });
  
  it('When element id = recaptcha-enterprise',()=>{
    windowRef.document.getElementById.and.returnValue(false);
    const mock: any = {};
    windowRef.document.createElement.and.returnValue(mock);
    service.addScript();
    expect(windowRef.document.createElement).toHaveBeenCalledWith('script');
    expect(windowRef.document.body.appendChild).toHaveBeenCalled();
  });
  });
});
