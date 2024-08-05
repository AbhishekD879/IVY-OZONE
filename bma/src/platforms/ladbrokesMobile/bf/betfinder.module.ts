import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { BetfinderRoutingModule } from './betfinder-routing.module';
import { BetFinderHelperService } from '@app/bf/services/bet-finder-helper.service';
import { SharedModule } from '@sharedModule/shared.module';
import { LadbrokesMobileBetFinderComponent } from '@ladbrokesMobile/bf/components/betFinder/bet-finder.component';
import { LadbrokesMobileBetFinderResultComponent } from '@ladbrokesMobile/bf/components/betFinderResult/bet-finder-result.component';
import * as bf from '@app/lazy-modules/locale/translations/en-US/bf.lang';
import { LocaleService } from '@core/services/locale/locale.service';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';

@NgModule({
  imports: [ SharedModule, FormsModule, BetfinderRoutingModule ],
  declarations: [
    LadbrokesMobileBetFinderComponent,
    LadbrokesMobileBetFinderResultComponent
  ],
  providers: [
    BetFinderHelperService,
  ],
  exports: [
    LadbrokesMobileBetFinderComponent,
    LadbrokesMobileBetFinderResultComponent
  ],
  schemas: [NO_ERRORS_SCHEMA]
})

export class BetFinderModule {
  constructor(private localeService: LocaleService,private asls: AsyncScriptLoaderService) {
    this.localeService.setLangData(bf);
      this.asls.loadCssFile('assets-betfinder.css', true, true).subscribe();
  }
}
