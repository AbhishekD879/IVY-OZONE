import { CommonModule } from "@angular/common";
import { NO_ERRORS_SCHEMA, NgModule } from "@angular/core";
import { SharedModule } from "@sharedModule/shared.module";
import { QuickSwitchPanelComponent } from "./quickSwitchPanel/quick-switch-panel.component";

@NgModule({
    imports: [
        CommonModule,
        SharedModule
    ],
    declarations: [
        QuickSwitchPanelComponent
    ],
    exports: [
        QuickSwitchPanelComponent
    ],
    schemas: [NO_ERRORS_SCHEMA]
})
export class LazyQuickSwitchModule {
    static entry = QuickSwitchPanelComponent;
}