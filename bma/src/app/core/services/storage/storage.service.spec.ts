import { StorageService } from './storage.service';

describe('StorageService', () => {
  let service: StorageService;
  let windowRef;

  beforeEach(() => {
    windowRef = {
      document: {
        cookie: ''
      },
      nativeWindow: {
        location: {
          href: 'https://bma-tst1.coral.co.uk'
        },
        localStorage: {
          removeItem: jasmine.createSpy('local.removeItem')
        },
        sessionStorage: {
          removeItem: jasmine.createSpy('session.removeItem')
        }
      }
    };
    service = new StorageService(windowRef);
  });

  it('init', () => {
    expect(service).toBeDefined();
  });

  describe('get method', () => {
    it('should get value stored in the cookie collection', () => {
      service.isSupported = false;

      const actualResult = service.get('test');

      expect(actualResult).toEqual('');
    });

    it('should get value stored in the local storage collection', () => {
      service.isSupported = true;
      windowRef.nativeWindow.localStorage.getItem = jasmine.createSpy('').and.returnValue('null');
      const actualResult = service.get('test');

      expect(actualResult).toEqual(null);
    });

    it('should get value stored in the local storage collection and parse it', () => {
      service.isSupported = true;
      windowRef.nativeWindow.localStorage.getItem = jasmine.createSpy('').and.returnValue('true');
      const actualResult = service.get('test');

      expect(actualResult).toEqual(true);
    });

    it('should get value stored in the local storage and try parse it', () => {
      service.isSupported = true;
      windowRef.nativeWindow.localStorage.getItem = jasmine.createSpy('').and.returnValue('[{}}]');
      const actualResult = service.get('test');

      expect(actualResult).toEqual(null);
    });
  });

  describe('set method', () => {
    it('should set value to the local storage', () => {
      service.isSupported = true;
      windowRef.nativeWindow.localStorage.setItem = jasmine.createSpy();
      const actualResult = service.set('testKey', 'testValue');

      expect(actualResult).toBeTruthy();
    });

    it('should set undefined value as null to the local storage', () => {
      const key = 'testKey';
      service.isSupported = true;
      windowRef.nativeWindow.localStorage.setItem = jasmine.createSpy();
      const actualResult = service.set('testKey', undefined);
      expect(service['webStorage'].setItem).toHaveBeenCalledWith(`${service['prefix']}${key}`, null);
      expect(actualResult).toBeTruthy();
    });

    it('should set value to the cookies', () => {
      service.isSupported = false;

      const actualResult = service.set('testKey', 'testValue');

      expect(actualResult).toBeFalsy();
    });
  });

  describe('remove method', () => {
    it('should remove value from localStorage', () => {
      service.isSupported = true;

      const actualResult = service.remove('test');

      expect(actualResult).toEqual(true);
    });

    it('should remove value from cookies', () => {
      service.isSupported = false;

      const actualResult = service.remove('test');

      expect(actualResult).toEqual(false);
    });
  });

  describe('isJsonObject method', () => {
    it('should check if value is object - negative case with ("string" string)', () => {
      const actualResult = service['isJsonObject']('test');

      expect(actualResult).toBeFalsy();
    });

    it('should check if value is object - negative case with ("number" string)', () => {
      const actualResult = service['isJsonObject']('555');

      expect(actualResult).toBeFalsy();
    });

    it('should check if value is object - negative case with ("boolean" string)', () => {
      const actualResult = service['isJsonObject']('true');

      expect(actualResult).toBeFalsy();
    });

    it('should check if value is object - positive case', () => {
      const actualResult = service['isJsonObject']('{}');

      expect(actualResult).toBeTruthy();
    });
  });

  describe('setCookie method', () => {
    it('should set not secure cookie', () => {
      service.setCookie('testKey', 'testValue');

      expect(windowRef.document.cookie.indexOf('testKey=testValue;') >= 0).toBeTruthy();
      expect(windowRef.document.cookie.indexOf('path=/; domain=.coral.co.uk') >= 0).toBeTruthy();
      expect(windowRef.document.cookie.indexOf('secure') >= 0).toBeFalsy();
    });

    it('should not set cookie when value is not defined', () => {
      service.setCookie('testKey', undefined);

      expect(windowRef.document.cookie.indexOf('testKey=testValue;') >= 0).toBeFalsy();
      expect(windowRef.document.cookie.indexOf('path=/; domain=.coral.co.uk') >= 0).toBeFalsy();
      expect(windowRef.document.cookie).toBe('');
    });

    it('should set cookie when value is array', () => {
      const value = ['1', '2'];
      service.setCookie('testKey', value);

      expect(windowRef.document.cookie.indexOf(`testKey=${encodeURIComponent(JSON.stringify(value))}`) >= 0).toBeTruthy();
      expect(windowRef.document.cookie.indexOf('path=/; domain=.coral.co.uk') >= 0).toBeTruthy();
      expect(windowRef.document.cookie.indexOf('secure') >= 0).toBeFalsy();
    });

    it('should set cookie when value is object', () => {
      const value = { key: 'value' };
      service.setCookie('testKey', value);

      expect(windowRef.document.cookie.indexOf(`testKey=${encodeURIComponent(JSON.stringify(value))}`) >= 0).toBeTruthy();
      expect(windowRef.document.cookie.indexOf('path=/; domain=.coral.co.uk') >= 0).toBeTruthy();
      expect(windowRef.document.cookie.indexOf('secure') >= 0).toBeFalsy();
    });

    it('should set cookie when domain name is not defined', () => {
      service.setCookie('testKey', 'testValue', undefined);

      expect(windowRef.document.cookie.indexOf('testKey=testValue;') >= 0).toBeTruthy();
      expect(windowRef.document.cookie.indexOf('path=/; domain=.coral.co.uk') >= 0).toBeTruthy();
      expect(windowRef.document.cookie.indexOf('secure') >= 0).toBeFalsy();
    });

    it('should set secure cookie', () => {
      service.setCookie('testKey', 'testValue', '.coral.co.uk', 5, true);

      expect(windowRef.document.cookie.indexOf('testKey=testValue;') >= 0).toBeTruthy();
      expect(windowRef.document.cookie.indexOf('path=/; domain=.coral.co.uk') >= 0).toBeTruthy();
      expect(windowRef.document.cookie.indexOf('secure') >= 0).toBeTruthy();
    });

    it('should not set secure cookie if http', () => {
      service['windowRefService'].nativeWindow.location.href = 'http://bma-tst1.coral.co.uk';
      service.setCookie('testKey', 'testValue', '.coral.co.uk', 5, true);

      expect(windowRef.document.cookie.indexOf('secure') >= 0).toBeFalsy();
    });

    it('should set cookie with default expiry time that is one year', () => {
      service.setCookie('testKey', 'testValue');

      expect(windowRef.document.cookie.indexOf('testKey=testValue;') >= 0).toBeTruthy();
      expect(windowRef.document.cookie.indexOf('path=/; domain=.coral.co.uk') >= 0).toBeTruthy();
      expect(windowRef.document.cookie.indexOf(new Date().getFullYear() + 1) >= 0).toBeTruthy();
    });
  });

  describe('checkSupport', () => {
    it('should return true', () => {
      service['storageType'] = 'sessionStorage';
      windowRef.nativeWindow.sessionStorage.setItem = jasmine.createSpy();
      const supported = service['checkSupport']();

      expect(supported).toBe(true);
    });

    it('should return false as error will be thrown', () => {
      service['storageType'] = 'sessionStorage' as any;
      windowRef.nativeWindow.sessionStorage.setItem = jasmine.createSpy('').and.throwError('err');

      const supported = service['checkSupport']();

      expect(supported).toBe(false);
    });
  });

  it('#setPrefix should add period to the prefix', () => {
    service['setPrefix']('TST');
    expect(service['prefix']).toBe('TST.');
  });

  it('#deriveKey should add prefix to the key', () => {
    service['prefix'] = 'TST.';
    const key = service['deriveKey']('test');
    expect(key).toBe('TST.test');
  });

  it('#init should set storageType, prefix and isSupported properties', () => {
    service['init']();
    expect(service['storageType']).toBeDefined();
    expect(service['prefix']).toBeDefined();
    expect(service['isSupported']).toBeDefined();
  });
});
