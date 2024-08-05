import { CommonModule } from '@angular/common';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { FreebetSignpostingComponent } from '@lazy-modules/signposting/components/freebet-signposting/freebet-signposting.component';
import { SharedModule } from '@sharedModule/shared.module';
@NgModule({
  imports: [CommonModule, SharedModule],
  providers: [],
  exports: [FreebetSignpostingComponent],
  declarations: [
    FreebetSignpostingComponent
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class SignpostingModule {
  static entry = FreebetSignpostingComponent;
}