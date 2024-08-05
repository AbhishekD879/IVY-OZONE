import { CommonModule } from '@angular/common';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { BetShareImageCardComponent } from './bet-share-image-card.component';
import { BetShareGTAService } from './services/bet-share-gta-tracking.service';
import { BetShareImageCardService } from './services/bet-share-image-card.service';

@NgModule({
  imports: [CommonModule, SharedModule],
  providers: [BetShareGTAService, BetShareImageCardService],
  exports: [BetShareImageCardComponent],
  declarations: [
    BetShareImageCardComponent
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class BetShareImageCardModule {
  static entry = BetShareImageCardComponent;
}