import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';

import { SbModule } from '@sbModule/sb.module';
import { SharedModule } from '@sharedModule/shared.module';
import { LazyEnhancedMultiplesTabRoutingModule } from '@lazy-modules/enhancedMultiplesTab/enhanced-multiples-tab-routing.module';

import { EnhancedMultiplesTabComponent } from '@lazy-modules-module/enhancedMultiplesTab/components/enhanced-multiples-tab.component';

@NgModule({
  imports: [
    SbModule,
    SharedModule,
    LazyEnhancedMultiplesTabRoutingModule
  ],
  declarations: [ EnhancedMultiplesTabComponent ],
  providers: [],
  exports: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class LazyEnhancedMultiplesTabModule {
  static entry = EnhancedMultiplesTabComponent;
}
