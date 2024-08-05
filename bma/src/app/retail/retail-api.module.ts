import { NgModule } from '@angular/core';
import { RetailRunService } from '@app/retail/services/retailRun/retail-run.service';
import { BetFilterParamsService } from '@app/retail/services/betFilterParams/bet-filter-params.service';
import { RetailMenuService } from '@app/retail/services/retailMenu/retail-menu.service';

@NgModule({
  declarations: [],
  providers: [
    RetailRunService,
    BetFilterParamsService,
    RetailMenuService,
  ]
})
export class RetailApiModule {}
