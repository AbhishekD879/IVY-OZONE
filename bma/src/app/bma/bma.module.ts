import { FormsModule } from '@angular/forms';
import { APP_INITIALIZER, NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { FavouritesModule } from '@favouritesModule/favourites.module';

import { BmaInit } from '@bmaModule/services/bmaRunService/bma-init';
import { BmaRunService } from '@bmaModule/services/bmaRunService/bma-run.service';
import { ContactUsComponent } from '@bmaModule/components/contactUs/contact-us.component';
import { NotFoundComponent } from '@bmaModule/components/404/404.component';
import { LocaleService } from '@coreModule/services/locale/locale.service';
import { StaticComponent } from '@bmaModule/components/static/static.component';
import * as criticalLangData from '@localeModule/translations/en-US/critical-lang-data';

// Vanilla overrides
import { BmaMainComponent } from '@bmaModule/components/bmaMain/bma-main.component';
import { HomeComponent } from '@bmaModule/components/home/home.component';
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
  ],
  declarations: [
    ContactUsComponent,
    HomeComponent,
    NotFoundComponent,
    StaticComponent,
    BmaMainComponent
  ],
  exports: [
    ContactUsComponent,
    NotFoundComponent,
    StaticComponent,
    BmaMainComponent,
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class BmaModule {
  constructor(private localeService: LocaleService,private asls: AsyncScriptLoaderService) {
    this.localeService.setLangData(criticalLangData);
    this.asls.loadCssFile('assets-racing.css', true, true).subscribe();
  }
}
