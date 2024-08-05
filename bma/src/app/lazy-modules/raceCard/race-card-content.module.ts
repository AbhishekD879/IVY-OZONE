import { NgModule, NO_ERRORS_SCHEMA } from "@angular/core";
import { RaceCardContentComponent } from "@app/lazy-modules/raceCard/raceCardContent/race-card-content.component";
import { SharedModule } from "@app/shared/shared.module";


@NgModule({
    imports: [SharedModule],
    providers: [],
    exports: [],
    declarations: [
        RaceCardContentComponent
    ],
    schemas: [NO_ERRORS_SCHEMA]
})

export class RaceCardContentModule {
    static entry = RaceCardContentComponent;
  }