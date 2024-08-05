import { LadbrokesBmaMainComponent } from './components/bmaMain/bma-main.component';
import { FormsModule } from '@angular/forms';
import { APP_INITIALIZER, NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SharedModule } from '@sharedModule/shared.module';
import { FavouritesModule } from '@favouritesModule/favourites.module';
import { BmaInit } from '@app/bma/services/bmaRunService/bma-init';
import { BmaRunService } from '@app/bma/services/bmaRunService/bma-run.service';
import { ContactUsComponent } from '@app/bma/components/contactUs/contact-us.component';
import { LogoutResolver } from '@app/vanillaInit/services/logout/logout.service';

import { HomeComponent } from '@app/bma/components/home/home.component';
import { NotFoundComponent } from '@bma/components/404/404.component';
import { LocaleService } from '@core/services/locale/locale.service';
import { StaticComponent } from '@bma/components/static/static.component';
import * as criticalLangData from '@ladbrokesMobile/lazy-modules/locale/translations/en-US/critical-lang-data';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';

@NgModule({
  imports: [
    SharedModule,

    FormsModule,
    FavouritesModule,
  ],
  providers: [
    BmaRunService,
    {
      provide: APP_INITIALIZER,
      useFactory: BmaInit,
      deps: [BmaRunService],
      multi: true
    },
    LogoutResolver
  ],
  declarations: [
    LadbrokesBmaMainComponent,
    ContactUsComponent,
    HomeComponent,
    NotFoundComponent,
    StaticComponent
  ],
  exports: [
    LadbrokesBmaMainComponent,
    ContactUsComponent,
    NotFoundComponent,
    StaticComponent
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class BmaModule {
  constructor(private localeService: LocaleService,private asls: AsyncScriptLoaderService) {
    this.localeService.setLangData(criticalLangData);
    this.asls.loadCssFile('assets-racing.css', true, true).subscribe();
  }
}
