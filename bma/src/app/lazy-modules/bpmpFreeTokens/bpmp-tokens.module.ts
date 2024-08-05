import { CommonModule } from '@angular/common';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { BpmpTokensProviderComponent } from '@lazy-modules/bpmpFreeTokens/components/bpmp-tokens.component';
import { SharedModule } from '@sharedModule/shared.module';
@NgModule({
  imports: [CommonModule, SharedModule],
  providers: [],
  exports: [],
  declarations: [
    BpmpTokensProviderComponent
  ],
  schemas: [NO_ERRORS_SCHEMA]
})
export class BpmpFreeBetTokensModule {
  static entry = BpmpTokensProviderComponent;
}
