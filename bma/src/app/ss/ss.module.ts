import { HttpClientModule } from '@angular/common/http';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SharedModule } from '@sharedModule/shared.module';
import { LoadByPortionsService } from '@ss/services/load-by-portions.service';
import { SimpleFiltersService } from '@ss/services/simple-filters.service';
import { SiteServerEventToOutcomeService } from '@ss/services/site-server-event-to-outcome.service';
import { SiteServerPoolService } from '@ss/services/site-server-pool.service';

@NgModule({
  imports: [
    HttpClientModule,
    SharedModule
  ],
  providers: [
    LoadByPortionsService,
    SimpleFiltersService,
    SiteServerPoolService,
    SiteServerEventToOutcomeService
  ],
  declarations: [],
  exports: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class SsModule {}
