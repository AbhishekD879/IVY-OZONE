import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { GamingOverlayComponent } from '@lazy-modules/gamingOverlay/components/gaming-overlay.component';
import { SharedModule } from '@sharedModule/shared.module';
//import { CasinoPlatformLoaderModule } from '@casinocore/loader';

@NgModule({
  //imports: [SharedModule, CasinoPlatformLoaderModule],
  imports: [SharedModule],
  declarations: [GamingOverlayComponent],
  exports: [GamingOverlayComponent],
  providers: [],
  schemas: [NO_ERRORS_SCHEMA]
})
export class GamingOverlayModule {
  static entry = GamingOverlayComponent;
}
