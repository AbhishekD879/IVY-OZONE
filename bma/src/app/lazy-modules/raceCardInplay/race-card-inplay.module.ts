import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { RaceCardInplayComponent as  RaceCardInplay} from './race-card-inplay.component';

@NgModule({
  imports: [SharedModule],
  declarations: [RaceCardInplay],
  exports: [RaceCardInplay],
  providers: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class RaceCardInplayModule {
  static entry = RaceCardInplay;
}
