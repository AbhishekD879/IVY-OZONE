import { DeviceService } from './device.service';
import environment from '@environment/oxygenEnvConfig';
import * as _ from 'underscore';

describe('DeviceService', () => {
  let service: DeviceService;
  let windowRef;
  let storage;
  let pubSubService;
  let document;

  beforeEach(() => {
    windowRef = {
      nativeWindow: window
    };
    storage = {
      get: jasmine.createSpy('get'),
      set: jasmine.createSpy('set')
    };
    pubSubService = {
      API: {
        DEVICE_VIEW_TYPE_CHANGED_NEW: 'DEVICE_VIEW_TYPE_CHANGED_NEW'
      },
      publish: jasmine.createSpy('publish')
    };
    document = {};
  });

  describe('DeviceService', () => {
    beforeEach(() => {
      service = new DeviceService(windowRef, storage, pubSubService, document);
    });
    it('constructor', () => {
      expect(service).toBeDefined();
    });

    it('should check if touch device', () => {
      expect(service.isTouch()).toBe(false);
    });

    it('should check if isDesktopSafari device', () => {
      service.isDesktop = true;
      service.browserName = 'Chrome';

      expect(service.isDesktopSafari).toBeFalsy();

      service.isDesktop = false;
      service.browserName = 'Chrome';

      expect(service.isDesktopSafari).toBeFalsy();

      service.isDesktop = true;
      service.browserName = 'Safari';

      expect(service.isDesktopSafari).toBeTruthy();
    });

    describe('isOnline', () => {
      it('should check if device online', () => {
        service.setOnline(true);
        expect(service.isOnline()).toBe(true);
      });

      it('should set device online status', () => {
        service.setOnline(false);
        expect(service.isOnline()).toBe(false);
      });

      it('should take value from this.navigator.onLine', () => {
        service['isDeviceOnline'] = undefined;
        spyOn(service['navigator'], 'onLine').and.returnValue(true);

        expect(service.isOnline()).toBe(true);
      });

      it('should take value from this.navigator.onLine', () => {
        service['isDeviceOnline'] = true;
        spyOn(service['navigator'], 'onLine').and.returnValue(undefined);

        expect(service.isOnline()).toBe(true);
      });
  
    });

    describe('isMobileOnly', () => {
      it('should check if device is mobile only', () => {
        expect(service.isMobileOnly).toBe(false);
      });

      it('should check for touch devices', () => {
        service['windowRef'] = {
          nativeWindow: {
            innerWidth: 300
          }
        } as any;
        service.mobileWidth = 340;
        service['document'] = {
          ontouchstart: jasmine.createSpy('ontouchstart')
        };

        expect(service.isMobileOnly).toBeTruthy();
      });
    });

    it('should check if browser is safari', () => {
      expect(service.isSafari).toBe(false);
    });

    it('should check device is mobile by user agent, vendor', () => {
      expect(service.performProviderIsMobile(false, 'android')).toBe(true);
      expect(service.performProviderIsMobile(true, 'android')).toBe(false);
      expect(service.performProviderIsMobile(true, 'symbian')).toBe(true);
      expect(service.performProviderIsMobile(false, 'symbian')).toBe(true);
      expect(service.performProviderIsMobile(true, 'test')).toBe(false);
      expect(service.performProviderIsMobile(false, 'test')).toBe(false);
    });

    describe('performProviderIsMobile', () => {
      /* eslint-disable max-len */
      const userAgentsMobile = {
        android: 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Mobile Safari/537.36',
        samsungS8Plus: 'Mozilla/5.0 (Linux; Android 9; SM-G955F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.90 Mobile Safari/537.36',
        iPhoneX: 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
        iPhoneSafari: 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1',
        symbian: 'symbian'
      };

      const userAgentsTablet = {
        iPad: 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1',
        iPadSafari: 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Mobile/15E148 Safari/604.1',
        iPadPro: 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1',
        samsungTab: 'Mozilla/5.0 (Linux; Android 4.4.4; SM-T560) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.90 Safari/537.36',
      };
      /* eslint-enable max-len */

      describe('should return True if onlyMobile', () => {
        Object.keys(userAgentsMobile).forEach((device: string) => {
          it(device, () => expect(service.performProviderIsMobile(true, userAgentsMobile[device])).toBe(true));
        });
      });

      describe('should return False if onlyMobile', () => {
        Object.keys(userAgentsTablet).forEach((device: string) => {
          it(device, () => expect(service.performProviderIsMobile(true, userAgentsTablet[device])).toBeFalsy());
        });
      });

      describe('should return True if onlyMobile equal false', () => {
        Object.keys(userAgentsTablet).forEach((device: string) => {
          it(device, () => expect(service.performProviderIsMobile(false, userAgentsTablet[device])).toBeTruthy());
        });

        Object.keys(userAgentsMobile).forEach((device: string) => {
          it(device, () => expect(service.performProviderIsMobile(false, userAgentsMobile[device])).toBeTruthy());
        });
      });

      describe('use agent', () => {
        it(`should use navigator.userAgent if No param userAgentName`, () => {
          service['navigator'] = { userAgent: userAgentsMobile.android };
        });

        it(`should use navigator.userAgent if device is ipad`, () => {
          service['navigator'] = { userAgent: 'ipad' };
        });
        it(`should use navigator.userAgent if device is macintosh`, () => {
          service['navigator'] = { userAgent: 'macintosh' };
        });

        it(`should use navigator.vendor if No param userAgentName and navigator.userAgent`, () => {
          service['navigator'] = {
            userAgent: null,
            vendor: userAgentsMobile.android
          };
        });

        it(`should use navigator.opera if No userAgentName and navigator.userAgent and navigator.vendor`, () => {
          service['navigator'] = {
            userAgent: null,
            vendor: null,
          };
          service['windowRef'].nativeWindow.opera = userAgentsMobile.android;
        });

        afterEach(() => expect(service.performProviderIsMobile()).toBeTruthy());
      });
    });

    describe('freeBetChannel', () => {
      it('should get desktop free bet channel', () => {
        expect(service.freeBetChannel).toBe('MI');
      });

      it('should get Android free bet channel', () => {
        service['detectWrapper'] = jasmine.createSpy('detectWrapper').and.returnValue(true);
        service['device'].os.name = 'Android';

        expect(service.freeBetChannel).toBe('Mz');
      });

      it('should get iOS free bet channel', () => {
        service['detectWrapper'] = jasmine.createSpy('detectWrapper').and.returnValue(true);
        service['device'].os.name = 'iOS';

        expect(service.freeBetChannel).toBe('My');
      });

      it('should get mobile free bet channel', () => {
        service['detectWrapper'] = jasmine.createSpy('detectWrapper').and.returnValue(true);
        service['device'].device.type = 'mobile';

        expect(service.freeBetChannel).toBe('M');
      });
    });

    describe('samsungUAFix', () => {
      let device;
      let os;
      let ua;

      beforeEach(() => {
        device = {
          model: null,
          type: 'mobile'
        };
        os = {
          name: 'Android'
        };
        ua = 'Mozilla/5.0 (Linux; Android 7.0; SM-T713) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36';
      });

      it('should set device.vendor and device.model', () => {
        service['samsungUAFix']({ device, os, ua });

        expect(device.vendor).toEqual('Samsung');
        expect(device.model).toBe('SM-T713');
      });

      it('should not set device.vendor and device.model', () => {
        service['samsungUAFix']({
          device,
          os,
          ua: 'Mozilla/5.0 (Linux; Android 7.0)'
        });

        expect(device.vendor).not.toEqual('Samsung');
        expect(device.model).not.toBe('SM-T713');
      });

      it('should not set device.vendor and device.model', () => {
        device.vendor = null;
        device.model = null;
        spyOn(_, 'last');

        service['samsungUAFix']({ device, os, ua: '' });

        expect(device.vendor).toBeNull();
        expect(device.model).toBeNull();
        expect(_.last).not.toHaveBeenCalled();
      });
    });

    it('should subscribe to resize events', () => {
      service.viewType = 'mobile';
      service.isMobile = false;
      window.dispatchEvent(new Event('resize'));
      expect(pubSubService.publish).toHaveBeenCalled();
    });

    it('should subscribe to orientationchange events', () => {
      service.viewType = 'mobile';
      service.isMobile = false;
      window.dispatchEvent(new Event('orientationchange'));
      expect(pubSubService.publish).toHaveBeenCalled();
    });

    describe('getRequestPlatform', () => {
      it('should return "desktop"', () => {
        environment['CURRENT_PLATFORM'] = 'desktop';

        expect(service['getRequestPlatform']('tablet')).toEqual('desktop');
      });

      it('should return "tablet"', () => {
        environment['CURRENT_PLATFORM'] = 'mobile';

        expect(service['getRequestPlatform']('tablet')).toEqual('tablet');
      });
    });

    describe('getDeviceData', () => {
      it('should return ""', () => {
        service['device'] = {
          device: {
            vendor: 'Microsoft',
            model: 'Lumia 520'
          }
        };

        service['getDeviceData']();
      });

      it('should return "Mobile Unknown"', () => {
        service['device'] = {
          device: {
            type: 'mobile'
          }
        };

        expect(service['getDeviceData']()).toEqual('Mobile Unknown');
      });

      it('should return "Unknown Device"', () => {
        service['device'] = {
          device: {}
        };

        expect(service['getDeviceData']()).toEqual('Unknown Device');
      });

      it('should return "iPhone"', () => {
        service['device'] = {
          device: {
            model: 'iPhone'
          }
        };
        spyOn(service, 'getiPhoneDevice' as any).and.callThrough();

        expect(service['getDeviceData']()).toEqual('iPhone');
        expect(service['getiPhoneDevice']).toHaveBeenCalled();
      });

      it('should return "Samsung"', () => {
        service['device'] = {
          device: {
            vendor: 'Samsung',
            model: 'GM-300'
          }
        };
        spyOn(service, 'getSamsungDevice' as any).and.callThrough();

        expect(service['getDeviceData']()).toEqual('Samsung GM-300');
        expect(service['getSamsungDevice']).toHaveBeenCalled();
      });
    });

    describe('buildSamsungVersionMap', () => {
      it('should init samsungVersionMap if empty', () => {
        service['samsungVersionMap'] = null;

        service['buildSamsungVersionMap']();

        expect(service['samsungVersionMap']).toBeDefined();
      });

      it('should not init samsungVersionMap if defined', () => {
        spyOn(_, 'each');
        service['samsungVersionMap'] = {};

        service['buildSamsungVersionMap']();

        expect(_.each).not.toHaveBeenCalled();
      });
    });

    describe('getSamsungDevice', () => {
      it('should return "Samsung"', () => {
        expect(service['getSamsungDevice']('T-850')).toBe('Samsung');
      });

      it('should return parsed samsung device', () => {
        service['getSamsungDevice']('Samsung Galaxy SM-G93');
      });
    });

    describe('getiPhoneDevice', () => {
      let nativeWindow;
      beforeEach(() => {
        nativeWindow = {
          devicePixelRatio: 1,
          screen: {
            width: 480,
            height: 320
          }
        };
      });

      it('should return "iPhone 2g/3g/3gs"', () => {
        nativeWindow.screen = { width: 320, height: 480 };
        service['windowRef'] = { nativeWindow } as any;

        expect(service['getiPhoneDevice']()).toEqual('iPhone 2g/3g/3gs');
      });

      it('should return "iPhone 2g/3g/3gs"', () => {
        nativeWindow.screen = { width: 480, height: 320 };
        service['windowRef'] = { nativeWindow } as any;

        expect(service['getiPhoneDevice']()).toEqual('iPhone 2g/3g/3gs');
      });

      it('should return "iPhone 4"', () => {
        nativeWindow.screen = { width: 960, height: 640 };
        service['windowRef'] = { nativeWindow } as any;

        expect(service['getiPhoneDevice']()).toEqual('iPhone 4');
      });

      it('should return "iPhone 4"', () => {
        nativeWindow.screen = { width: 640, height: 960 };
        service['windowRef'] = { nativeWindow } as any;

        expect(service['getiPhoneDevice']()).toEqual('iPhone 4');
      });

      it('should return "iPhone 5"', () => {
        nativeWindow.screen = { width: 640, height: 1136 };
        service['windowRef'] = { nativeWindow } as any;

        expect(service['getiPhoneDevice']()).toEqual('iPhone 5');
      });

      it('should return "iPhone 5"', () => {
        nativeWindow.screen = { width: 1136, height: 640 };
        service['windowRef'] = { nativeWindow } as any;

        expect(service['getiPhoneDevice']()).toEqual('iPhone 5');
      });

      it('should return "iPhone 6"', () => {
        nativeWindow.screen = { width: 750, height: 1334 };
        service['windowRef'] = { nativeWindow } as any;

        expect(service['getiPhoneDevice']()).toEqual('iPhone 6');
      });

      it('should return "iPhone 6"', () => {
        nativeWindow.screen = { width: 1334, height: 750 };
        service['windowRef'] = { nativeWindow } as any;

        expect(service['getiPhoneDevice']()).toEqual('iPhone 6');
      });

      it('should return "iPhone 6 Plus"', () => {
        nativeWindow.screen = { width: 1242, height: 2208 };
        service['windowRef'] = { nativeWindow } as any;

        expect(service['getiPhoneDevice']()).toEqual('iPhone 6 Plus');
      });

      it('should return "iPhone 6 Plus"', () => {
        nativeWindow.screen = { width: 2208, height: 1242 };
        service['windowRef'] = { nativeWindow } as any;

        expect(service['getiPhoneDevice']()).toEqual('iPhone 6 Plus');
      });

      it('should return "iPhone"', () => {
        nativeWindow.screen = { width: 750, height: 1792 };
        nativeWindow.devicePixelRatio = undefined;
        service['windowRef'] = { nativeWindow } as any;

        expect(service['getiPhoneDevice']()).toEqual('iPhone');
      });
    });

    describe('getFullDeviceName', () => {
      it('should get device name', () => {
        service['getFullDeviceName']('LG', 'LG Nexus');
      });

      it('should get composed device name', () => {
        service['getFullDeviceName']('Samsung', 'GM-300');
      });
    });

    describe('getUuid', () => {
      it('should get uuid from storage', () => {
        const uuid = '12345678-1234-4321-1234-123456789000';
        (service['storage'].get as jasmine.Spy).and.returnValue(uuid);

        expect(service['getUuid']()).toEqual(uuid);
      });

      it('should create and return new uuid', () => {
        (service['storage'].get as jasmine.Spy).and.returnValue(undefined);

        service['getUuid']();

        expect(service['storage'].get).toHaveBeenCalled();
        expect(service['storage'].set).toHaveBeenCalledWith('uuid', jasmine.any(String));
      });
    });

    describe('getSoftSerial', () => {
      it('should get soft serial from storage', () => {
        const softSerial = 123456;
        (service['storage'].get as jasmine.Spy).and.returnValue(softSerial);

        expect(service['getSoftSerial']()).toEqual(softSerial);
      });

      it('should create and return new soft serial', () => {
        (service['storage'].get as jasmine.Spy).and.returnValue(undefined);

        service['getSoftSerial']();

        expect(service['storage'].get).toHaveBeenCalled();
        expect(service['storage'].set).toHaveBeenCalledWith('softSerial', jasmine.any(String));
      });
    });

    describe('getStrictViewType', () => {
      it('should return "tablet"', () => {
        spyOn(service, 'getViewType' as any).and.returnValue('landscapeTablet');

        expect(service['getStrictViewType']()).toEqual('tablet');
      });

      it('should return "mobile"', () => {
        spyOn(service, 'getViewType' as any).and.returnValue('mobile');

        expect(service['getStrictViewType']()).toEqual('mobile');
      });


      it('should return "desktop"', () => {
        spyOn(service, 'getViewType' as any).and.returnValue('desktop');

        expect(service['getStrictViewType']()).toEqual('desktop');
      });
    });
  });

  describe('getViewType', () => {
    it('should return "mobile"', () => {
      service.isMobile = true;

      expect(service['getViewType']()).toEqual('mobile');
    });

    it('should return "tablet"', () => {
      service.isMobile = false;
      service['windowRef'] = {
        nativeWindow: {
          innerWidth: 800
        }
      } as any;

      expect(service['getViewType']()).toEqual('tablet');
    });

    it('should return "landscapeTablet"', () => {
      service.isMobile = false;
      service['windowRef'] = {
        nativeWindow: {
          innerWidth: 1024
        }
      } as any;

      expect(service['getViewType']()).toEqual('landscapeTablet');
    });

    it('should return "desktop"', () => {
      service.isMobile = false;
      service['windowRef'] = {
        nativeWindow: {
          innerWidth: 1048
        }
      } as any;

      expect(service['getViewType']()).toEqual('desktop');
    });
  });

  describe('getDeviceViewType', () => {
    it('should return object with tablet: true', ()=>{
      service['windowRef'] = {
        nativeWindow: {
          innerWidth: 800
        }
      } as any;

      expect(service['getDeviceViewType']().mobile).toBeFalsy();
      expect(service['getDeviceViewType']().tablet).toBeTruthy();
      expect(service['getDeviceViewType']().desktop).toBeFalsy();
    });
    it('should return object with desktop: true', ()=>{
      service['windowRef'] = {
        nativeWindow: {
          innerWidth: 1024
        }
      } as any;

      expect(service['getDeviceViewType']().mobile).toBeFalsy();
      expect(service['getDeviceViewType']().tablet).toBeTruthy();
      expect(service['getDeviceViewType']().desktop).toBeFalsy();
    });
  });

  it(`isMobile should be Truthy  if tablet has shorter width than mobileWidth`, () => {
    const userAgent = 'Mozilla/5.0 (Linux; Android 7.0; SM-T713) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36';
    const windowStub: any = { nativeWindow: { innerWidth: 683, navigator: { userAgent }, addEventListener: jasmine.createSpy() } };
    service = new DeviceService(windowStub, storage, pubSubService, document);

    expect(service.isMobile).toBeTruthy();
  });
  describe('isRobot', () => {
    it('it should return true if userAgent is Googlebot', () => {
      const userAgent = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)';
      service['navigator'] = { userAgent };
      expect(service['isRobot']()).toBeTruthy();
    });
    it('it should return flase if userAgent is not Googlebot', () => {
      const userAgent = 'Mozilla/5.0 (Linux; Android 7.0; SM-T713) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36';
      service['navigator'] = { userAgent };
      expect(service['isRobot']()).toBeFalsy();
    });
    it('it should return flase if navigator is null', () => {
      service['navigator'] = null;
      expect(service['isRobot']()).toBeFalsy();
    });
    it('it should return flase if navigator.userAgent is null', () => {
      service['navigator'] = { userAgent: null };
      expect(service['isRobot']()).toBeFalsy();
    });
  });
  describe('getDeviceBrowserName', () => {
    beforeEach(() => {
      service = new DeviceService(windowRef, storage, pubSubService, document);
    });
    it('returns null', () => {
      service['device'] = { };      
      expect(service['getDeviceBrowserName']()).toBeUndefined();
    });
    it('returns undefined browser name', () => {
      service['device'].browser = { }; 
      expect(service['getDeviceBrowserName']()).toBeUndefined();
    });
  });
});
