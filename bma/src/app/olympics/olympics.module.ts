import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SharedModule } from '@sharedModule/shared.module';
import { LazySportModule } from '@sbModule/sport/sport.module';
import { OlympicsRunService } from '@olympicsModule/services/olympics-run.service';
import { OlympicsPageComponent } from '@olympicsModule/components/olympicsPage/olympics-page.component';
import { OlympicsRoutingModule } from './olympics-route.module';
import { AsyncScriptLoaderService } from '../core/services/asyncScriptLoader/async-script-loader.service';

@NgModule({
  imports: [
    SharedModule,
    LazySportModule,
    OlympicsRoutingModule
  ],
  declarations: [
    OlympicsPageComponent
  ],
  exports: [
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
