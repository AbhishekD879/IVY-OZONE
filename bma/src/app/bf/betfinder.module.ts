import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { BetfinderRoutingModule } from '@app/bf/betfinder-routing.module';
import { BetFinderComponent } from '@app/bf/components/betFinder/bet-finder.component';
import { BetFinderResultComponent } from '@app/bf/components/betFinderResult/bet-finder-result.component';
import { BetFinderHelperService } from '@app/bf/services/bet-finder-helper.service';
import { SharedModule } from '@sharedModule/shared.module';
import * as bf from '@localeModule/translations/en-US/bf.lang';
import { LocaleService } from '@core/services/locale/locale.service';
import { AsyncScriptLoaderService } from '../core/services/asyncScriptLoader/async-script-loader.service';

@NgModule({
  imports: [ SharedModule, FormsModule, BetfinderRoutingModule ],
  declarations: [
    BetFinderComponent,
    BetFinderResultComponent
  ],
  providers: [
    BetFinderHelperService,
  ],
  exports: [
    BetFinderComponent,
    BetFinderResultComponent
  ],
  schemas: [NO_ERRORS_SCHEMA]
})

export class BetFinderModule {
  constructor(private localeService: LocaleService,private asls: AsyncScriptLoaderService) {
    this.asls.loadCssFile('assets-betfinder.css', true, true).subscribe();
    this.localeService.setLangData(bf);
  }
}
