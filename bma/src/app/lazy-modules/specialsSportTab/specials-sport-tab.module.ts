import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SpecialsSportTabComponent } from './components/specials-sport-tab.component';
import { SharedModule } from '@sharedModule/shared.module';

@NgModule({
  imports: [SharedModule],
  declarations: [SpecialsSportTabComponent],
  exports: [SpecialsSportTabComponent],
  providers: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class SpecialsSportTabModule {
  static entry = SpecialsSportTabComponent;
}
