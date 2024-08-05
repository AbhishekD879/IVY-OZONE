import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LadbrokesVirtualEntryPointBannerComponent as VirtualEntryPointBannerComponent } from './virtual-entry-point-banner.component';



@NgModule({
  declarations: [VirtualEntryPointBannerComponent],
  imports: [
    CommonModule
  ],
  exports: [VirtualEntryPointBannerComponent]
})
export class VirtualEntryPointBannerModule {
  static entry = VirtualEntryPointBannerComponent;
}
