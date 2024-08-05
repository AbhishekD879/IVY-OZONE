import { CommonModule } from "@angular/common";
import { NgModule, NO_ERRORS_SCHEMA } from "@angular/core";
import { FloatingIhrMsgComponent } from "@lazy-modules/floating-ihr-msg/floating-ihr-msg.component";
import { SharedModule } from "@sharedModule/shared.module";

@NgModule({
    imports: [
        CommonModule,
        SharedModule
    ],
    declarations: [
        FloatingIhrMsgComponent
    ],
    exports: [
        FloatingIhrMsgComponent
    ],
    schemas: [NO_ERRORS_SCHEMA]
})
export class FloatingIhrMsgModule {
    static entry = FloatingIhrMsgComponent;
}