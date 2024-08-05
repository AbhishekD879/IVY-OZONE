import { NgModule } from '@angular/core';
import { LocaleService } from '@core/services/locale/locale.service';
import * as appLangData from '@localeModule/translations/en-US/index';

@NgModule()
export class TranslationModule {
  constructor(private localeService: LocaleService) {
    localeService.setLangData(appLangData);
    this.localeService.translationLoadComplete();
  }
}
