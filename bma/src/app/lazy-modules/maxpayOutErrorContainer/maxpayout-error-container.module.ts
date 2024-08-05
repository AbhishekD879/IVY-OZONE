import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { MaxpayoutErrorContainerComponent } from './maxpayout-error-container.component';
import { MaxPayOutErrorService } from './services/maxpayout-error.service';

@NgModule({
    imports: [
        SharedModule
    ],
    providers: [],
    exports: [],
    declarations: [
        MaxpayoutErrorContainerComponent
    ],
    schemas: [NO_ERRORS_SCHEMA]
})
export class MaxpayoutErrorContainerModule {
    constructor(private maxPayOutErrorService: MaxPayOutErrorService) {}
    static entry = MaxpayoutErrorContainerComponent;
}
