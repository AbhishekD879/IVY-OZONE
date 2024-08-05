import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { RpgComponent } from '@lazy-modules/rpg/rpg.component';

import { SharedModule } from '@sharedModule/shared.module';

@NgModule({
  imports: [
    SharedModule
  ],
  providers: [],
  exports: [],
  declarations: [
    RpgComponent
  ],
  schemas: [ NO_ERRORS_SCHEMA ]
})
export class RpgModule {
  static entry = RpgComponent;
}
