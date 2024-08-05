import { of } from 'rxjs';
import { arcData } from '../test/arcUser.mock';
import { ArcUserService } from './arcUser.service';

describe('ArcUserService', () => {
  let service: ArcUserService,
    pubSubService,
    claimsService,
    userService,
    cmsService;
  beforeEach(() => {
    pubSubService = {
      API: {
        SESSION_LOGIN: 'SESSION_LOGIN',
        APP_IS_LOADED: 'APP_IS_LOADED',
        RELOAD_COMPONENTS: 'RELOAD_COMPONENTS'
      },
      subscribe: jasmine.createSpy('subscribe').and.callFake((a, b, callback) => callback()),
      publish: jasmine.createSpy('publish')
    };
    claimsService = {
      get: jasmine.createSpy('get').and.returnValue('2')
    };
    userService = {
      isAuthenticated: true
    };
    cmsService = {
      formArcData: jasmine.createSpy('formArcData').and.returnValue(of(arcData)),
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({
        ArcConfig: {
          enableArc: true
        }
      }))
    };
    service = new ArcUserService(pubSubService, claimsService, userService, cmsService);
  });
  it('constructor', () => {
    spyOn<any>(service, 'initialData');
    expect(pubSubService.subscribe).toHaveBeenCalled();
  });
  it('cms with undefined', () => {
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({}))
    };
    service = new ArcUserService(pubSubService, claimsService, userService, cmsService);
    spyOn<any>(service, 'initialData');
    expect(service['initialData']).not.toHaveBeenCalled();
  });
  it('cms with null', () => {
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of(null))
    };
    service = new ArcUserService(pubSubService, claimsService, userService, cmsService);
    spyOn<any>(service, 'initialData');
    expect(service['initialData']).not.toHaveBeenCalled();
  });
  it('cms with false', () => {
    cmsService = {
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({
        ArcConfig: {
          enableArc: false
        }
      }))
    };
    service = new ArcUserService(pubSubService, claimsService, userService, cmsService);
    spyOn<any>(service, 'initialData');
    expect(service['initialData']).not.toHaveBeenCalled();
  });
  describe('initialData', () => {
    it('should call arc cms -1', () => {
      spyOn<any>(service, 'fetchArcCms');
      service['initialData']();
      expect(service.fetchArcCms).toHaveBeenCalled();
    });
    it('should not call arc cms - 2', () => {
      spyOn<any>(service, 'fetchArcCms');
      userService.isAuthenticated = false;
      claimsService.get.and.returnValue(undefined);
      service['initialData']();
      expect(service.fetchArcCms).not.toHaveBeenCalled();
    });
    it('should not call arc cms -3', () => {
      spyOn<any>(service, 'fetchArcCms');
      userService.isAuthenticated = false;
      service.arcRiskBandLevel = claimsService.get.and.returnValue('1');
      service.arcPrimaryReason = claimsService.get.and.returnValue(undefined);
      service['initialData']();
      expect(service.fetchArcCms).not.toHaveBeenCalled();
    });
    it('should not call arc cms -4', () => {
      spyOn<any>(service, 'fetchArcCms');
      service.arcPrimaryReason = claimsService.get.and.returnValue('1');
      service.arcRiskBandLevel = claimsService.get.and.returnValue(undefined);
      service['initialData']();
      expect(service.fetchArcCms).not.toHaveBeenCalled();
    });
    it('should not call arc cms -5', () => {
      spyOn<any>(service, 'fetchArcCms');
      userService.isAuthenticated = false;
      service['initialData']();
      expect(service.fetchArcCms).not.toHaveBeenCalled();
    });
  });
  describe('fetchArcCms', () => {
    it('should fetchArcCms', () => {
      arcData.enabled = true;
      service.quickbet = true;
      service.fetchArcCms();
      expect(pubSubService.publish).toHaveBeenCalledWith('crossSellData', true);
      expect(pubSubService.publish).not.toHaveBeenCalledWith('QuickbetClose', true);
    });
    it('should not fetchArcCms', () => {
      arcData.enabled = false;
      arcData.sportsActions = [];
      service.fetchArcCms();
      expect(pubSubService.publish).not.toHaveBeenCalledWith('QuickbetClose', true);
    });
    it('when cross sell is disabled', () => {
      arcData.enabled = true;
      arcData.sportsActions = [{
        'action': 'Gaming cross sell removal',
        'messagingContent': '',
        'enabled': false
      }];
      service.fetchArcCms();
      expect(pubSubService.publish).toHaveBeenCalledWith('crossSellData', false);
    });
    it('when quickbet is disabled', () => {
      arcData.enabled = true;
      service.quickbet = false;
      arcData.sportsActions = [{
        'action': 'Quick bet removal',
        'messagingContent': '',
        'enabled': false
      }];
      service.fetchArcCms();
      expect(pubSubService.publish).not.toHaveBeenCalledWith('QuickbetClose', false);
    });
  });
});