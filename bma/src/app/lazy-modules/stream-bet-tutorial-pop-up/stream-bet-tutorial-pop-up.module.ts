import { CommonModule } from "@angular/common";
import { NgModule, NO_ERRORS_SCHEMA } from "@angular/core";
import { SharedModule } from "@sharedModule/shared.module";
import { StreamBetTutorialPopUpComponent } from "@lazy-modules/stream-bet-tutorial-pop-up/stream-bet-tutorial-pop-up/stream-bet-tutorial-pop-up.component";


@NgModule({
    imports: [
        CommonModule,
        SharedModule
    ],
    declarations: [
        StreamBetTutorialPopUpComponent
    ],
    exports: [
        StreamBetTutorialPopUpComponent
    ],
    schemas: [NO_ERRORS_SCHEMA]
})
export class StreamBetTutorialPopUpModule {
    static entry = StreamBetTutorialPopUpComponent;
}