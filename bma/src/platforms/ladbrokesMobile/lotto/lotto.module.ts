import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { SharedModule } from '@sharedModule/shared.module';

import { SimpleFiltersService } from '@ss/services/simple-filters.service';
import { LottoRoutingModule } from '@app/lotto/lotto-routing.module';
import { LottoMainComponent } from '@app/lotto/components/lottoMain/lotto-main.component';
import { LottoSegmentPageComponent } from '@app/lotto/components/lottoSegmentPage/lotto-segment-page.component';
import { NumberSelectorComponent } from '@app/lotto/components/numberSelector/number-selector.component';
import { LottoNumberSelectorComponent } from '@lottoModule/components/lottoNumberSelectorDialog/lotto-number-selector-dialog.component';
import { SiteServerLottoService } from '@app/lotto/services/siteServerLotto/site-server-lotto.service';
import { BuildLotteriesService } from '@app/lotto/services/buildLotteries/build-lotteries.service';
import { LottoReceiptService } from '@app/lotto/services/lottoReceipt/lotto-receipt.service';
import { LottoResultsService } from '@app/lotto/services/lottoResults/lotto-results.service';
import { MainLottoService } from '@app/lotto/services/mainLotto/main-lotto.service';
import { SegmentDataUpdateService } from '@app/lotto/services/segmentDataUpdate/segment-data-update.service';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';
import { LinesummaryComponent } from '@app/lotto/components/linesummary/linesummary.component';
import { LottoInfoDialogComponent } from '@app/lotto/components/lottoInfoDialog/lotto-info-dialog.component';
import { InfoDialogService } from '@app/core/services/infoDialogService/info-dialog.service';

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
    SimpleFiltersService,
    InfoDialogService
  ],
})
export class LottoModule {
  constructor(private asls: AsyncScriptLoaderService) {
    this.asls.loadCssFile('assets-lotto.css', true, true).subscribe();
  }
}
