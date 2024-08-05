import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { BetFinderComponent } from '@app/bf/components/betFinder/bet-finder.component';
import { BetFinderResultComponent } from '@app/bf/components/betFinderResult/bet-finder-result.component';
import { BetFinderHelperService } from '@app/bf/services/bet-finder-helper.service';
import { SharedModule } from '@sharedModule/shared.module';
import * as bf from '@localeModule/translations/en-US/bf.lang';
import { LocaleService } from '@core/services/locale/locale.service';

// Overridden app components
import { DesktopBetFinderComponent } from '@ladbrokesDesktop/bf/components/betFinder/bet-finder.component';
import { DesktopBetFinderResultComponent } from '@ladbrokesDesktop/bf/components/betFinderResults/bet-finder-result.component';
import { AsyncScriptLoaderService } from '@core/services/asyncScriptLoader/async-script-loader.service';

@NgModule({
  imports: [ SharedModule, FormsModule ],
  declarations: [
    // Overridden app components
    DesktopBetFinderComponent,
    DesktopBetFinderResultComponent,

    BetFinderComponent,
    BetFinderResultComponent
  ],
  providers: [
    BetFinderHelperService,
  ],
  exports: [
    // Overridden app components
    DesktopBetFinderComponent,
    DesktopBetFinderResultComponent,

    BetFinderComponent,
    BetFinderResultComponent
  ],
  schemas: [NO_ERRORS_SCHEMA]
})

export class BetFinderModule {
  constructor(private localeService: LocaleService,private asls: AsyncScriptLoaderService) {
    this.localeService.setLangData(bf);
      this.asls.loadCssFile('assets-betfinder.css', true, true).subscribe();
  }
}
