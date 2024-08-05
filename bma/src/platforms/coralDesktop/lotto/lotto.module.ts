import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { FormsModule } from '@angular/forms';


import { SharedModule } from '@sharedModule/shared.module';
import { DesktopModule } from '@desktopModule/desktop.module';

import { SimpleFiltersService } from '@ss/services/simple-filters.service';
import { SegmentDataUpdateService } from '@app/lotto/services/segmentDataUpdate/segment-data-update.service';
import { LottoResultsService } from '@app/lotto/services/lottoResults/lotto-results.service';
import { LottoReceiptService } from '@app/lotto/services/lottoReceipt/lotto-receipt.service';
import { MainLottoService } from '@app/lotto/services/mainLotto/main-lotto.service';
import { SiteServerLottoService } from '@app/lotto/services/siteServerLotto/site-server-lotto.service';
import { BuildLotteriesService } from '@app/lotto/services/buildLotteries/build-lotteries.service';
import { NumberSelectorComponent } from '@app/lotto/components/numberSelector/number-selector.component';
import { LottoSegmentPageComponent } from '@lottoModule/components/lottoSegmentPage/lotto-segment-page.component';
import { LottoNumberSelectorComponent } from '@lottoModule/components/lottoNumberSelectorDialog/lotto-number-selector-dialog.component';
import { LinesummaryComponent } from '@lottoModule/components/linesummary/linesummary.component';
// Desktop
import { LottoRoutingModule } from './lotto-routing.module';
import { DesktopLottoMainComponent } from '@coralDesktop/lotto/components/lottoMain/lotto-main.component';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';
import { LottoInfoDialogComponent } from '@app/lotto/components/lottoInfoDialog/lotto-info-dialog.component';

@NgModule({
  declarations: [
    LottoSegmentPageComponent,
    NumberSelectorComponent,
    LottoNumberSelectorComponent,
    LinesummaryComponent,

    // Overridden
    DesktopLottoMainComponent,
    LottoInfoDialogComponent
  ],
  imports: [

    SharedModule,
    FormsModule,
    LottoRoutingModule,
    DesktopModule,
  ],
  exports: [
    LottoSegmentPageComponent,
    NumberSelectorComponent,
    LottoNumberSelectorComponent,
    LinesummaryComponent,

    // Overridden
    DesktopLottoMainComponent,
  ],
  schemas: [ NO_ERRORS_SCHEMA ],
  providers: [
    BuildLotteriesService,
    SiteServerLottoService,
    MainLottoService,
    LottoReceiptService,
    LottoResultsService,
    SegmentDataUpdateService,
    SimpleFiltersService
  ],
})
export class LottoModule {
  constructor(private asls: AsyncScriptLoaderService) {
    this.asls.loadCssFile('assets-lotto.css', true, true).subscribe();
  }
}
