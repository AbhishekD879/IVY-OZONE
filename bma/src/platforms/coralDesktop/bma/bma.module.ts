import { FormsModule } from '@angular/forms';
import { APP_INITIALIZER, NgModule, NO_ERRORS_SCHEMA } from '@angular/core';


import { DesktopModule } from '@coralDesktop/desktop/desktop.module';
import { SharedModule } from '@sharedModule/shared.module';


import { ContactUsComponent } from '@bmaModule/components/contactUs/contact-us.component';
import { NotFoundComponent } from '@bmaModule/components/404/404.component';
import { InplayLiveStreamModule } from '@inPlayLiveStream/inplay-live-stream.module';
import { BmaRunService } from '@bmaModule/services/bmaRunService/bma-run.service';
import { BmaInit } from '@bmaModule/services/bmaRunService/bma-init';
import { LocaleService } from '@coreModule/services/locale/locale.service';
import { StaticComponent } from '@bmaModule/components/static/static.component';
import * as criticalLangData from '@localeModule/translations/en-US/critical-lang-data';
import { DesktopLiveStreamWrapperComponent } from '@coralDesktop/bma/components/liveStream/live-stream-wrapper.component';

// Vanilla desktop overrides
import { DesktopBmaMainComponent } from '@coralDesktop/bma/components/bmaMain/bma-main.component';
import { DesktopHomeComponent } from '@coralDesktop/bma/components/home/home.component';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';


@NgModule({
  imports: [
    SharedModule,

    FormsModule,
    DesktopModule,
    InplayLiveStreamModule,
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
    DesktopHomeComponent,
    NotFoundComponent,
    StaticComponent,
    DesktopBmaMainComponent,
    DesktopLiveStreamWrapperComponent,
  ],
  exports: [
    ContactUsComponent,
    NotFoundComponent,
    StaticComponent,
    DesktopBmaMainComponent,
    DesktopLiveStreamWrapperComponent,
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class BmaModule {
  constructor(private localeService: LocaleService,private asls: AsyncScriptLoaderService) {
    this.localeService.setLangData(criticalLangData);
    this.asls.loadCssFile('assets-racing.css', true, true).subscribe();
    
  }
}
