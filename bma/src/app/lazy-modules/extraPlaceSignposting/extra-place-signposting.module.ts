import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { ExtraPlaceSignpostingComponent } from './components/extra-place-signposting.component';

@NgModule({
    imports: [
        SharedModule
    ],
    providers: [],
    exports: [ExtraPlaceSignpostingComponent],
    declarations: [
        ExtraPlaceSignpostingComponent
    ],
    schemas: [NO_ERRORS_SCHEMA]
})
export class ExtraPlaceSignpostingModule {
    static entry = ExtraPlaceSignpostingComponent;
}
