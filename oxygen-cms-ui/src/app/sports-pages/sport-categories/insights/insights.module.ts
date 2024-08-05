import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {InsightsRoutingModule} from './insights-routing.module';
import { SharedModule } from '@app/shared/shared.module';
import { InsightsService } from './insights.service';
import { InsightsComponent } from './inisghts-tab/insights.component';
import { PopularBetFiltersCreateComponent } from './popular-bet-filters-create/popular-bet-filters-create.component';
import { SportTabPopularBetsComponent } from './sport-tab-popular-bets/sport-tab-popular-bets.component';
@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    InsightsRoutingModule,
  ],
  declarations: [
    InsightsComponent,
    PopularBetFiltersCreateComponent,
    SportTabPopularBetsComponent,  
  ],
  providers: [
    InsightsService
  ],
})
export class InsightsModule { }
