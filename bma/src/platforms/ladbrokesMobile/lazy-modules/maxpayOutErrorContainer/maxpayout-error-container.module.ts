import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { LadbrokesMaxpayoutErrorContainerComponent } from './maxpayout-error-container.component';

@NgModule({
    imports: [
        SharedModule
    ],
    providers: [],
    exports: [],
    declarations: [
        LadbrokesMaxpayoutErrorContainerComponent
    ],
    schemas: [NO_ERRORS_SCHEMA]
})
export class MaxpayoutErrorContainerModule {
    static entry = LadbrokesMaxpayoutErrorContainerComponent;
}
