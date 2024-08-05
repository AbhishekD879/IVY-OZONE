import { fakeAsync, tick } from '@angular/core/testing';
import { LocaleService } from './locale.service';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import * as bma from '@localeModule/translations/en-US/bma.lang';

describe('LocaleService', () => {

  let service: LocaleService;
  const coreToolsService = new CoreToolsService();

  beforeEach(() => {
    service = new LocaleService(coreToolsService);
    service.setLangData(bma);
  });

  it('should get correct locale', () => {
    expect(service.getLocale()).toBe('en-US');
  });

  it('should set correct locale', () => {
    service.setLocale('ua-UA');
    expect(service.getLocale()).toBe('ua-UA');
  });

  it('should get correct string by token', () => {
    expect(service.getString('bma.showPassword' )).toBe('Show');
    expect(service.getString('bma.fakeToken')).toBe('KEY_NOT_FOUND');
  });

  it('should apply substitutions', () => {
    expect(service.applySubstitutions('Show %1 %2', ['param1', 'param2'] )).toBe('Show param1 param2');
    expect(service.applySubstitutions('Show {variable}', {variable: 'value'})).toBe('Show value');
  });

  it('should return load Subject', () => {
    expect(service.isTranslationModuleLoaded).toBe(service['isTranslationLoaded']);
    expect(service.isTranslationModuleLoaded.value).toEqual(false);
  });

  it('should complete Subject and set true value', fakeAsync(() => {
    service.translationLoadComplete();

    tick();

    expect(service.isTranslationModuleLoaded.isStopped).toEqual(true);
    expect(service.isTranslationModuleLoaded.value).toEqual(true);
  }));

  it('setLangData should call deepMerge method', () => {
    coreToolsService.deepMerge = jasmine.createSpy('deepMerge');

    service.setLangData('test' as any);

    expect(coreToolsService.deepMerge).toHaveBeenCalledTimes(1);
  });
});
