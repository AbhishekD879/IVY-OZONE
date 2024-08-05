import { DesktopBmaMainComponent } from './components/bmaMain/bma-main.component';
import { FormsModule } from '@angular/forms';
import { APP_INITIALIZER, NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { DesktopModule } from '@ladbrokesDesktop/desktop/desktop.module';
import { SharedModule } from '@sharedModule/shared.module';
import { FavouritesModule } from '@favouritesModule/favourites.module';
import { ContactUsComponent } from '@app/bma/components/contactUs/contact-us.component';
import { LogoutResolver } from '@app/vanillaInit/services/logout/logout.service';
import { DesktopHomeComponent } from '@ladbrokesDesktop/bma/components/home/home.component';
import { NotFoundComponent } from '@bma/components/404/404.component';
import { BmaRunService } from '@bma/services/bmaRunService/bma-run.service';
import { BmaInit } from '@bma/services/bmaRunService/bma-init';
import { LocaleService } from '@core/services/locale/locale.service';
import { StaticComponent } from '@bma/components/static/static.component';
import * as criticalLangData from '@ladbrokesDesktop/lazy-modules/locale/en-US/critical-lang-data';
import { DesktopLiveStreamWrapperComponent } from '@ladbrokesDesktop/bma/components/liveStream/live-stream-wrapper.component';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';

@NgModule({
  imports: [
    SharedModule,

    FormsModule,
    FavouritesModule,
    DesktopModule,
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
    ContactUsComponent,
    DesktopHomeComponent,
    DesktopBmaMainComponent,
    NotFoundComponent,
    StaticComponent,
    DesktopLiveStreamWrapperComponent,
  ],
  exports: [
    ContactUsComponent,
    DesktopBmaMainComponent,
    NotFoundComponent,
    StaticComponent,
    DesktopLiveStreamWrapperComponent
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class BmaModule {
  constructor(private localeService: LocaleService,private asls: AsyncScriptLoaderService) {
    this.localeService.setLangData(criticalLangData);
    this.asls.loadCssFile('assets-racing.css', true, true).subscribe();
  }
}
