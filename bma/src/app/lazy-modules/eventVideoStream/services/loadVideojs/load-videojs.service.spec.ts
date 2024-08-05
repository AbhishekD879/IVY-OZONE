
import { of as observableOf } from 'rxjs';
import { LoadVideoJSService } from './load-videojs.service';
describe('LoadVideoJSService', () => {
  let service: LoadVideoJSService;

  let asyncScriptLoader;

  beforeEach(() => {
    asyncScriptLoader = {
      loadJsFile: jasmine.createSpy().and.returnValue(observableOf({})),
      loadCssFile: jasmine.createSpy().and.returnValue(observableOf({}))
    };

    service = new LoadVideoJSService(asyncScriptLoader);
  });

  it('loadScripts', () => {
    service.loadScripts().subscribe();
    expect(asyncScriptLoader.loadJsFile).toHaveBeenCalledTimes(2);
    expect(asyncScriptLoader.loadCssFile).toHaveBeenCalledTimes(1);
  });
});
