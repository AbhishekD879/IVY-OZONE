import { NgModule, NO_ERRORS_SCHEMA } from "@angular/core";
import { CommonModule } from "@angular/common";
import { SharedModule } from "@sharedModule/shared.module";
import { RacingStatusComponent} from "@ladbrokesMobile/lazy-modules/racingStatus/components/racing-status.component";

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