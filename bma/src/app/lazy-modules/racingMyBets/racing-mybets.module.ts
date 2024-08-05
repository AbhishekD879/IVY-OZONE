import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RacingMyBetsComponent } from './components/racing-mybets.component';
import { SharedModule } from '@sharedModule/shared.module';

@NgModule({
  imports: [CommonModule, SharedModule],
  declarations: [RacingMyBetsComponent],
  exports: [RacingMyBetsComponent],
  providers: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class RacingMybetsModule {
  static entry = RacingMyBetsComponent;
}
