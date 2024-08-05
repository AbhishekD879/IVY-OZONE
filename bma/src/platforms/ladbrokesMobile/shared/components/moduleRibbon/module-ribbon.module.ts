import { CommonModule } from '@angular/common';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { LadbrokesModuleRibbonComponent } from './module-ribbon.component';

@NgModule({
    imports: [
        SharedModule, CommonModule
    ],
    providers: [
    ],
    declarations: [
        LadbrokesModuleRibbonComponent
    ],
    exports: [
        LadbrokesModuleRibbonComponent
    ],
    schemas: [NO_ERRORS_SCHEMA]
})
export class RibbonModule {
    static entry = LadbrokesModuleRibbonComponent;
}