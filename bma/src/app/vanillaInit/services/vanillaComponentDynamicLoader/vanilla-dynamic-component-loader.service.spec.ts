import {
  VanillaDynamicComponentLoaderService
} from '@vanillaInitModule/services/vanillaComponentDynamicLoader/vanilla-dynamic-component-loader.service';
import { Subject } from 'rxjs';
import { UserLoginEvent } from '@frontend/vanilla/core';

describe('VanillaDynamicComponentLoaderService', () => {
  let service: VanillaDynamicComponentLoaderService;

  let user;
  let headerService;

  beforeEach(() => {
    user = { 
      isAuthenticated: true,
      events: new Subject()
    };
    headerService = {
      _inner : {
        dynamicComponentsRegistry : {
          registerLazyComponent: jasmine.createSpy('registerLazyComponent')
        }
      },
      setHeaderComponent: jasmine.createSpy(),
      whenReady : {
        subscribe: jasmine.createSpy('subscribe').and.callFake(cb => cb())
      }
    };

    service = new VanillaDynamicComponentLoaderService(user, headerService);
  });

  it('#init should call correct methods', () => {
    const event = new UserLoginEvent();
    service['addComponentsToVanillaHeader'] = jasmine.createSpy();
    service.init();
    user.events.next(event);
    expect(service['addComponentsToVanillaHeader']).toHaveBeenCalledTimes(2);
  });

  it('#addComponetsToVanillaHeader should call correct methods when user is authenticated', () => {
    service['addComponentsToVanillaHeader']();
    expect(headerService['_inner']['dynamicComponentsRegistry'].registerLazyComponent)
      .toHaveBeenCalledWith('HEADER',"mybets",jasmine.any(Function));
    expect(headerService['_inner']['dynamicComponentsRegistry'].registerLazyComponent)
      .toHaveBeenCalledWith('HEADER','betslip', jasmine.any(Function));
  });

  it('#addComponetsToVanillaHeader should call correct methods when user isn\'t authenticated', () => {
    user.isAuthenticated = false;
    service = new VanillaDynamicComponentLoaderService(user, headerService);
    service['addComponentsToVanillaHeader']();
    headerService.whenReady.subscribe(() => {
    expect(headerService['_inner']['dynamicComponentsRegistry'].registerLazyComponent)
      .toHaveBeenCalledWith('HEADER','betslip',jasmine.any(Function));
  });
});
});
