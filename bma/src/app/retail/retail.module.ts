import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { BetFilterComponent } from '@platform/retail/components/betFilter/bet-filter.component';


import { SharedModule } from '@sharedModule/shared.module';
import { RetailRoutingModule } from '@app/retail/retail-routing.module';
import { RetailPageComponent } from '@platform/retail/components/retailPage/retail-page.component';
import { ShopLocatorComponent } from '@app/retail/components/shopLocator/shop-locator.component';
import { BetFilterDialogComponent } from '@app/retail/components/betFilterDialog/bet-filter-dialog.component';
import { BetTrackerComponent } from '@app/retail/components/betTracker/bet-tracker.component';
import { RetailRunService } from '@app/retail/services/retailRun/retail-run.service';
import { RetailMenuComponent } from '@app/retail/components/retailMenu/retail-menu.component';
import {
  FootballFilterConfirmDialogComponent
} from '@app/retail/components/footballFilterConfirmDialog/football-filter-confirm-dialog.component';
import { RetailOverlayComponent } from '@app/retail/components/retailOverlay/retail-overlay.component';
import { AsyncScriptLoaderService } from '../core/services/asyncScriptLoader/async-script-loader.service';

@NgModule({
  imports: [
    SharedModule,

    FormsModule,
    HttpClientModule,
    ReactiveFormsModule,
    RetailRoutingModule,
  ],
  declarations: [
    RetailPageComponent,
    ShopLocatorComponent,
    BetFilterComponent,
    BetTrackerComponent,
    BetFilterDialogComponent,
    RetailMenuComponent,
    FootballFilterConfirmDialogComponent,
    RetailOverlayComponent,
  ],
  exports: [
    BetFilterDialogComponent,
    RetailMenuComponent,
    FootballFilterConfirmDialogComponent,
    RetailOverlayComponent,
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class RetailModule {
  static entry = { RetailMenuComponent, RetailOverlayComponent, BetTrackerComponent };
  constructor(private retailRunService: RetailRunService,private asls: AsyncScriptLoaderService) {
    this.retailRunService.run();
    this.asls.loadCssFile('assets-retail.css', true, true).subscribe();
  }
}
