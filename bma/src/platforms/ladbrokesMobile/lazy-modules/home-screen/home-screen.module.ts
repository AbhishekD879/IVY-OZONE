import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { SharedModule } from '@sharedModule/shared.module';
import { HomeScreenComponent } from '@shared/components/homeScreen/home-screen.component';

@NgModule({
    imports: [
        SharedModule
    ],
    providers: [],
    declarations: [
        HomeScreenComponent
    ],
    exports: [
        HomeScreenComponent
    ],
    schemas: [NO_ERRORS_SCHEMA]
})
export class HomeScreenModule {
    static entry = HomeScreenComponent;
}