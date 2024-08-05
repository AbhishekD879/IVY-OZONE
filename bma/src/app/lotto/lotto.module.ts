import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { FormsModule } from '@angular/forms';


import { SharedModule } from '@sharedModule/shared.module';

import { SimpleFiltersService } from '@ss/services/simple-filters.service';
import { LottoRoutingModule } from './lotto-routing.module';
import { LottoMainComponent } from './components/lottoMain/lotto-main.component';
import { LottoSegmentPageComponent } from '@lottoModule/components/lottoSegmentPage/lotto-segment-page.component';
import { NumberSelectorComponent } from './components/numberSelector/number-selector.component';
import { LottoNumberSelectorComponent } from './components/lottoNumberSelectorDialog/lotto-number-selector-dialog.component';
import { SiteServerLottoService } from './services/siteServerLotto/site-server-lotto.service';
import { BuildLotteriesService } from './services/buildLotteries/build-lotteries.service';
import { LottoReceiptService } from './services/lottoReceipt/lotto-receipt.service';
import { LottoResultsService } from './services/lottoResults/lotto-results.service';
import { MainLottoService } from './services/mainLotto/main-lotto.service';
import { SegmentDataUpdateService } from './services/segmentDataUpdate/segment-data-update.service';
import { AsyncScriptLoaderService } from '../core/services/asyncScriptLoader/async-script-loader.service';
import { LinesummaryComponent } from '@lottoModule/components/linesummary/linesummary.component';
import { LottoInfoDialogComponent } from './components/lottoInfoDialog/lotto-info-dialog.component';
 

@NgModule({
  declarations: [
    LottoMainComponent,
    LottoSegmentPageComponent,
    NumberSelectorComponent,
    LottoNumberSelectorComponent,
    LinesummaryComponent,
    LottoInfoDialogComponent
  ],
  imports: [

    SharedModule,
    FormsModule,
    LottoRoutingModule
  ],
  exports: [
    LottoMainComponent,
    LottoSegmentPageComponent,
    NumberSelectorComponent,
    LottoNumberSelectorComponent,
    LinesummaryComponent
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
