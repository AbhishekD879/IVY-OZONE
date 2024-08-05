import { NgModule, NO_ERRORS_SCHEMA } from "@angular/core";
import { SharedModule } from '@sharedModule/shared.module';
import { LadbrokesRaceCardContentComponent as RaceCardContentComponent} from "@ladbrokesMobile/lazy-modules/raceCard/raceCardContent/race-card-content.component";

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