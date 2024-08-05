import { fakeAsync, tick } from '@angular/core/testing';

import { DeferredLoaderService } from './deferred-loader.service';
import { MODULES_BY_PRIORITY, MODULES_LOADING_DELAY } from './deferred-loader.service.constant';

describe('DeferredLoaderService', () => {
  let
    service: DeferredLoaderService,
    dynamicLoaderService,
    pubSubService;

  beforeEach(() => {
    dynamicLoaderService = {
      loadModule: jasmine.createSpy('loadModule').and.returnValue(Promise.resolve())
    };
    pubSubService = {
      API: {
        APP_IS_LOADED: 'APP_IS_LOADED',
        DEFERRED_MODULES_LOADED: 'DEFERRED_MODULES_LOADED',
        RELOAD_COMPONENTS: 'RELOAD_COMPONENTS'
      },
      subscribe: jasmine.createSpy('subscribe').and.callFake((a, b, cb) => cb()),
      publish: jasmine.createSpy('publish')
    };

    service = new DeferredLoaderService(
      dynamicLoaderService,
      pubSubService
    );
    service['isLoaded'] = true;
  });

  it('should import delay', () => {
    expect(MODULES_LOADING_DELAY).toBe(100);
  });

  it('should use copy of constant', () => {
    expect(service.modulesToLoad).toEqual(MODULES_BY_PRIORITY);
    expect(service.modulesToLoad).not.toBe(MODULES_BY_PRIORITY);
  });

  it('should initialize lazyLoading on RELOAD_COMPONENTS event', () => {
    spyOn(service as any, 'lazyLoadModules');
    service['isLoaded'] = false;
    service.init();

    expect(pubSubService.subscribe).toHaveBeenCalledTimes(2);
  });

  it('should try to load all modules from list and trigger appropriate events', fakeAsync(() => {
    const modulesCount = MODULES_BY_PRIORITY.length;
    const firstModulePath = MODULES_BY_PRIORITY[0].path;
    service['lazyLoadModules']();
    tick(MODULES_LOADING_DELAY);

    expect(dynamicLoaderService.loadModule).toHaveBeenCalledTimes(modulesCount);
    expect(dynamicLoaderService.loadModule.calls.argsFor(0)[0]).toBe(firstModulePath.substring(0, firstModulePath.indexOf(':')));
    expect(pubSubService.publish).toHaveBeenCalledTimes(modulesCount + 1);
  }));
});
