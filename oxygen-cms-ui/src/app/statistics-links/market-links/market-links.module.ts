import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '../../shared/shared.module';
import { MarketLinksRoutingModule } from './market-links-routing.module';
import { StatisticLinksService } from '../service/statistic-links.service';
import { MarketLinksListComponent } from './market-links-list/market-links-list.component';
import { MarketLinksEditComponent } from './market-links-edit/market-links-edit.component';
import { MarketLinksCreateComponent } from './market-links-create/market-links-create.component';

@NgModule({
  imports: [
    CommonModule,
    SharedModule,
    MarketLinksRoutingModule
  ],
  declarations: [
    MarketLinksListComponent,
    MarketLinksEditComponent,
    MarketLinksCreateComponent
  ],
   providers: [
    StatisticLinksService
  ],
  entryComponents: [
    MarketLinksCreateComponent
  ]
})
export class MarketLinksModule { }
