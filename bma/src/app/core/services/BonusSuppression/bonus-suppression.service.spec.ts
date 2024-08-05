import { TestBed } from '@angular/core/testing';
import { ISystemConfig } from '../cms/models';
import { of as observableOf } from 'rxjs';

import { BonusSuppressionService } from './bonus-suppression.service';
import { YellowFlagData } from '../user/yellow-flag.model';
import environment from '@environment/oxygenEnvConfig';

describe('BonusSuppressionService', () => {
  let service;
  let dialogService;
  let router;
  let cmsService, userService;

  const sysConfig: ISystemConfig = {
    BonusSupErrorMsg: {
      errorMsg: 'Permission Denied',
      url: '/'
    }
  };

  beforeEach(() => {
    TestBed.configureTestingModule({});

    dialogService = {
      openDialog: jasmine.createSpy('openDialog').and.returnValue(true),
      ids: { bonusSuppresionError: 'BonusSuppressionError' }
    };

    userService = {
      status: true
    };

    router = {
      navigate: jasmine.createSpy()
    };

    cmsService = {
      getSystemConfig: jasmine.createSpy().and.returnValue(observableOf(sysConfig)),
      getCMSYellowFlagInfo: jasmine.createSpy('getCMSYellowFlagInfo')
    };

    service = new BonusSuppressionService(dialogService, router, cmsService, userService)
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should navigate away to home page for RG Yellow flagged user', () => {
    service.navigateAwayForRGYellowCustomer();

    expect(dialogService.openDialog).toHaveBeenCalled();
    expect(router.navigate).toHaveBeenCalled();
  });

  describe('#getRedirectionURL', () => {
    it('getRedirectionURL if cms configured', () => {
      const sysConfigModified = Object.assign({}, sysConfig);
      sysConfigModified['BonusSupErrorMsg'] = {
        errorMsg: 'Permission Denied',
        url: '/'
      };
      cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig')
        .and.returnValue(observableOf(sysConfigModified));

      service.getRedirectionURL();

      expect(service.bonusSuppresionUrl).toEqual('/');
    });
    it('getRedirectionURL if cms not configured', () => {
      const sysConfigModified = Object.assign({}, sysConfig);
      sysConfigModified['BonusSupErrorMsg'] = undefined;
      cmsService.getSystemConfig = jasmine.createSpy('getSystemConfig')
        .and.returnValue(observableOf(sysConfigModified));

      service['getRedirectionURL']();

      expect(service.bonusSuppresionUrl).toEqual(service.homeURL);
    });
  });

  describe('#checkIfYellowFlagDisabled', () => {
    it('should properly check If User is yellow flag disabled #checkIfYellowFlagDisabled', () => {
      service.cmsYellowFlagInfo = YellowFlagData;
      cmsService.cmsYellowFlagInfo = YellowFlagData;
      environment.brand = 'ladbrokes';
      cmsService.getCMSYellowFlagInfo = jasmine.createSpy('getCMSYellowFlagInfo').and.returnValue(YellowFlagData);
      const result = service.checkIfYellowFlagDisabled('Promotions');
      expect(result).toEqual(true);
    });

    it('should properly check If User is not yellow flag disabled #checkIfYellowFlagDisabled', () => {
      service.cmsYellowFlagInfo = YellowFlagData;
      cmsService.cmsYellowFlagInfo = YellowFlagData;
      userService.status = false;
      cmsService.getCMSYellowFlagInfo = jasmine.createSpy('getCMSYellowFlagInfo').and.returnValue(YellowFlagData);
      const result = service.checkIfYellowFlagDisabled('1-2-Frees');
      expect(result).toEqual(true);
    });

    it('should return true if main module is present and subModules is enabled', () => {
      service.cmsYellowFlagInfo = YellowFlagData;
      cmsService.cmsYellowFlagInfo = YellowFlagData;
      environment.brand = 'bma';
      userService.status = true;
      cmsService.getCMSYellowFlagInfo = jasmine.createSpy('getCMSYellowFlagInfo').and.returnValue(YellowFlagData);
      const result = service.checkIfYellowFlagDisabled('Promotions');
      expect(result).toEqual(true);
    });

    it('should return false if main module and sub module is present', () => {
      service.cmsYellowFlagInfo = YellowFlagData;
      cmsService.cmsYellowFlagInfo = YellowFlagData;
      environment.brand = 'bma';
      userService.status = true;
      cmsService.getCMSYellowFlagInfo = jasmine.createSpy('getCMSYellowFlagInfo').and.returnValue(YellowFlagData);
      const result = service.checkIfYellowFlagDisabled('Promotions', 'Promotion Sub 1');
      expect(result).toEqual(false);
    });

    it('should return false if main module is present and sub module is not present', () => {
      service.cmsYellowFlagInfo = YellowFlagData;
      cmsService.cmsYellowFlagInfo = YellowFlagData;
      environment.brand = 'bma';
      userService.status = true;
      cmsService.getCMSYellowFlagInfo = jasmine.createSpy('getCMSYellowFlagInfo').and.returnValue(YellowFlagData);
      const result = service.checkIfYellowFlagDisabled('Promotions', 'Promotion Sub 4');
      expect(result).toEqual(true);
    });

    it('should return false if main module is not present', () => {
      service.cmsYellowFlagInfo = YellowFlagData;
      cmsService.cmsYellowFlagInfo = YellowFlagData;
      environment.brand = 'bma';
      userService.status = true;
      cmsService.getCMSYellowFlagInfo = jasmine.createSpy('getCMSYellowFlagInfo').and.returnValue(YellowFlagData);
      const result = service.checkIfYellowFlagDisabled('Unknown');
      expect(result).toEqual(true);
    });

    it('should return false if cmsYellowFlagInfo is null', () => {
      service.cmsYellowFlagInfo = null;
      cmsService.cmsYellowFlagInfo = null;
      environment.brand = 'bma';
      userService.status = true;
      cmsService.getCMSYellowFlagInfo = jasmine.createSpy('getCMSYellowFlagInfo').and.returnValue(null);
      const result = service.checkIfYellowFlagDisabled('Unknown');
      expect(result).toEqual(true);
    });

    it('should return false if main module is present and subModules are empty', () => {
      const res = [{
        'brand': 'bma',
        'moduleName': 'Promotions',
        'aliasModuleNames': 'Promotion Sub 1',
        'subModuleEnabled': false,
        'subModules': []
      },
      {
        'brand': 'bma',
        'moduleName': 'free-to-play',
        'aliasModuleNames': 'Promotion Sub 1',
      }];
      environment.brand = 'bma';
      userService.status = true;
      cmsService.getCMSYellowFlagInfo = jasmine.createSpy('getCMSYellowFlagInfo').and.returnValue(res);
      const result = service.checkIfYellowFlagDisabled('Promotions', 'Promotions 1');
      expect(result).toEqual(false);
    });

    it('should return false if main module is present and subModuleEnabled is false', () => {
      const res = [{
        'brand': 'bma',
        'moduleName': 'Promotions',
        'aliasModuleNames': 'Promotion Sub 1',
        'subModuleEnabled': false,
        'subModules': []
      },
      {
        'brand': 'bma',
        'moduleName': 'free-to-play',
        'aliasModuleNames': 'Promotion Sub 1',
      }];
      environment.brand = 'bma';
      userService.status = true;
      cmsService.getCMSYellowFlagInfo = jasmine.createSpy('getCMSYellowFlagInfo').and.returnValue(res);
      const result = service.checkIfYellowFlagDisabled('Promotions', 'Promotions 1');
      expect(result).toEqual(false);
    });
  });

  describe('#checkRGYSubmodules', () => {
    it('if submodule string does not exist', () => {
      const data = YellowFlagData[0];
      data.subModuleEnabled = false;
      const result = service.checkRGYSubmodules(data, undefined);
      expect(result).toEqual(true);
    });
    it('if subModuleEnabled is false', () => {
      const module = YellowFlagData[0];
      module.subModuleEnabled = false;
      const result = service.checkRGYSubmodules(module, 'Promotions');
      expect(result).toEqual(true);
    });
    it('if subModule lenth is 0', () => {
      const module = YellowFlagData[0];
      module.subModules = [];
      const result = service.checkRGYSubmodules(module, 'Promotions');
      expect(result).toEqual(true);
    });
    it('if subModule lenth is not 0', () => {
      const module = YellowFlagData[0];
      const result = service.checkRGYSubmodules(module, 'Promotions');
      expect(result).toEqual(true);
    });
  });

  describe('#clubAndCheck', () => {
    it('should return false', () => {
      const infoObj = {
        'brand': 'bma',
        'moduleName': 'Promotions',
        'aliasModuleNames': 'Promotion Sub 1',
        'subModuleEnabled': false,
        'subModules': []
      };

      const res = service['clubAndCheck'](infoObj, 'Promotion');
      expect(res).toBe(false);
    });
    it('should return true', () => {
      const infoObj = {
        'brand': 'bma',
        'moduleName': 'Promotions',
        'aliasModuleNames': 'Promotion Sub 1',
        'subModuleEnabled': false,
        'subModules': []
      };

      const res = service['clubAndCheck'](infoObj, 'Promotions');
      expect(res).toBe(true);
    });
  });
});
