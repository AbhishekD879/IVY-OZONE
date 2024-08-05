import { CommonModule } from "@angular/common";
import { NgModule, NO_ERRORS_SCHEMA } from "@angular/core";
import { RacingStatusComponent } from "@lazy-modules/racingStatus/components/racing-status.component";
import { SharedModule } from "@sharedModule/shared.module";

@NgModule({
    imports: [
        CommonModule,
        SharedModule
    ],
    declarations: [
        RacingStatusComponent
    ],
    exports: [
        RacingStatusComponent
    ],
    schemas: [NO_ERRORS_SCHEMA]
})
export class RacingStatusModule {
    static entry = RacingStatusComponent;
}