import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { LeavingCasinoDialogComponent } from './components/LeavingCasinoDialog/leaving-casino-info-dialog.component';
import { SharedModule } from '@sharedModule/shared.module';
import { CasinoGoToSportsComponent } from './components/casinoGoToSports/casino-goto-sports-button.component';
import { CasinoMyBetsFiveASideComponent } from './components/casinoMyBetsFiveASideButton/casino-mybets-five-a-side-button.component';
import { CasinoMyBetsFiveasideBetHeaderComponent } from './components/casinoMyBetsFiveASideBetHeader/casino-mybets-fiveaside-bet-header.component';
import { FiveASideShowDownApiModule } from '@app/fiveASideShowDown/fiveASideShowDown-api.module';

@NgModule({
  imports: [SharedModule, FiveASideShowDownApiModule],
  declarations: [CasinoGoToSportsComponent, 
                 LeavingCasinoDialogComponent,
                 CasinoMyBetsFiveASideComponent,
                 CasinoMyBetsFiveasideBetHeaderComponent
              ],
  exports: [CasinoGoToSportsComponent,
            LeavingCasinoDialogComponent,
            CasinoMyBetsFiveASideComponent,
            CasinoMyBetsFiveasideBetHeaderComponent
          ],
  providers: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class CasinoMyBetsIntegrationModule {
  static entry = { CasinoGoToSportsComponent,
                   LeavingCasinoDialogComponent,
                   CasinoMyBetsFiveASideComponent,
                   CasinoMyBetsFiveasideBetHeaderComponent
                };
}
