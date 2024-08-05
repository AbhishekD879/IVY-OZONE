import { CommonModule } from '@angular/common';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { VirtualEntryPointBannerComponent } from '@lazy-modules/virtualEntryPointBanner/virtual-entry-point-banner.component';

@NgModule({
    imports: [CommonModule, SharedModule],
    providers: [],
    exports: [VirtualEntryPointBannerComponent],
    declarations: [
        VirtualEntryPointBannerComponent
    ],
    schemas: [NO_ERRORS_SCHEMA]
})

export class VirtualEntryPointBannerModule {
    static entry = VirtualEntryPointBannerComponent;
}
