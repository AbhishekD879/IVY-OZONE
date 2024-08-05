import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { DesktopModule } from '@desktopModule/desktop.module';
import { SharedModule } from '@sharedModule/shared.module';
import { SbModule } from '@sbModule/sb.module';
import { OlympicsRunService } from '@app/olympics/services/olympics-run.service';
import { OlympicsRoutingModule } from '@olympicsModule/olympics-route.module';

// Overridden app components
import { OlympicsPageComponent } from '@coralDesktop/olympics/components/olympicsPage/olympics-page.component';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';

@NgModule({
  imports: [
    SbModule,
    SharedModule,
    DesktopModule,
    OlympicsRoutingModule
  ],
  declarations: [
    // Overridden app components
    OlympicsPageComponent
  ],
  exports: [
    // Overridden app components
    OlympicsPageComponent
  ],
  providers: [
    OlympicsRunService
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class OlympicsModule {
  constructor(private asls: AsyncScriptLoaderService,private olympicsRunService: OlympicsRunService) {
    this.olympicsRunService.run();
      this.asls.loadCssFile('assets-olympics.css', true, true).subscribe();
  }
}
