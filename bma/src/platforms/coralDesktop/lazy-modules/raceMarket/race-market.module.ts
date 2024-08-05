import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from '@sharedModule/shared.module';
import { RaceMarketComponent } from './race-market.component';


@NgModule({
    declarations: [
        RaceMarketComponent
    ],
    imports: [
        CommonModule,
        SharedModule
    ],
    exports: [RaceMarketComponent],
    providers: [],
    schemas: [NO_ERRORS_SCHEMA]
})
export class RaceMarketModule {
    static entry = RaceMarketComponent;
}