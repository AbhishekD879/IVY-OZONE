import { of } from 'rxjs';
import { MaxPayOutErrorService } from './maxpayout-error.service';

describe('MaxPayOutErrorService', () => {
  let service;
  let cmsService;

  beforeEach(() => {
    cmsService = {
      getFeatureConfig: jasmine.createSpy('getFeatureConfig').and.returnValue(of({
        enabled: true,
        title: 'MaxPayOut',
        link: 'https://coral.co.uk/',
        click: 'here'
      } as any)),
      getSystemConfig: jasmine.createSpy('getSystemConfig').and.returnValue(of({
        maxPayOut: {
          maxPayoutFlag: true
        }
      }))
    };
    service = new MaxPayOutErrorService(cmsService);
  });

  describe('constructor', () => {
    it('config is defined', () => {
      spyOn<any>(service, 'setMaxPayOutTooltip');
      expect(service.maxPayFlag).toBe(true);
    });
    it('config is undefined', () => {
      cmsService.getSystemConfig = jasmine.createSpy().and.returnValue(of({}));
      spyOn<any>(service, 'setMaxPayOutTooltip');
      service = new MaxPayOutErrorService(cmsService);
      expect(service.maxPayFlag).toBe(false);
    });
    it('config is undefined-2', () => {
      cmsService.getSystemConfig = jasmine.createSpy().and.returnValue(of({
        maxPayOut: null
      }));
      spyOn<any>(service, 'setMaxPayOutTooltip');
      service = new MaxPayOutErrorService(cmsService);
      expect(service.maxPayFlag).toBe(false);
    });
  });
    
  describe('setMaxPayOutTooltip', () => {
    it('setMaxPayOutTooltip if config defined', () => {
      service['setMaxPayOutTooltip']();
      expect(cmsService.getFeatureConfig).toHaveBeenCalled();
    });
    it('setMaxPayOutTooltip if config is undefined', () => {
      cmsService.getFeatureConfig = jasmine.createSpy().and.returnValue(of({}));
      service.maxPayOutTooltip = "";
      service['setMaxPayOutTooltip']();
      expect(service.maxPayOutTooltip).toBe('');
    });
    it('setMaxPayOutTooltip if enabled is false', () => {
      cmsService.getFeatureConfig = jasmine.createSpy().and.returnValue(of({ enabled: false }));
      service.maxPayOutTooltip = "";
      service['setMaxPayOutTooltip']();
      expect(service.maxPayOutTooltip).toBe('');
    });
  });
  describe('form maxPayOutTooltip', () => {
    it('length more than 50', () => {
      cmsService.getFeatureConfig = jasmine.createSpy().and.returnValue(of({
        enabled: true,
        title: 'Csfd ftd yugdygds uyudsf dyfy udyf navailablilitydafgfsgfsgfdsgsfdgfdgsd',
        link: 'https://coral.co.uk/',
        click: 'here'
      }));
      const text = 'Csfd ftd yugdygds uyudsf dyfy udyf navailablilitydafgfsgfsgfdsgsfdgfdgsd';
      service['setMaxPayOutTooltip']();
      expect(service.maxPayOutTooltip).toBe(`${text.substring(0, 50)}...`);
    });
  });
});

