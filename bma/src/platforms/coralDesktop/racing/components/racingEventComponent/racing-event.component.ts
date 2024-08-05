import { RacingEventComponent } from '@racing/components/racingEventComponent/racing-event.component';
import { OnInit, Component } from '@angular/core';
import * as _ from 'underscore';
import { IStreamsCssClasses } from '@core/models/streams-css-classes.model';
import { IRacingPostVerdict } from '@racing/models/racing-post-verdict.model';
import environment from '@environment/oxygenEnvConfig';

@Component({
  templateUrl: 'racing-event.component.html',
  styleUrls: ['racing-event.component.scss'],
  selector: 'racing-event'
})
export class DesktopRacingEventComponent extends RacingEventComponent implements OnInit {
  racingPostVerdictData: IRacingPostVerdict;
  cssClassesForStreams: IStreamsCssClasses = {
    iGameMedia: '',
    otherProviders: 'live-column watch-live'
  };
  typeNames: { name: string }[];
  isNotHorseRacing: boolean;
  racingPostSummary: string;
  readonly HORSE_RACING_CATEGORY_ID: string = environment.HORSE_RACING_CATEGORY_ID;
  ngOnInit() {
    super.ngOnInit();
    this.typeNames = this.racingTypeNames.map(item => ({ name: item }));

    if (this.eventEntity) {
      this.racingPostVerdictData = this.eventEntity.racingPostVerdict;
    }
    if (this.eventEntity && _.has(this.eventEntity.racingFormEvent, 'overview')) {
      this.racingPostSummary = this.eventEntity.racingFormEvent.overview;
    }
    this.isNotHorseRacing = !this.isRacingSpecialsCondition &&
      (!this.isAntepostMarket() || this.racingInMeeting.length > 0) &&
      this.eventEntity.categoryId === this.HORSE_RACING_CATEGORY_ID;
  }

  formatEventTerms(str: string): string {
    return str
      .replace(/\d+\/\d+( ODDS)/ig, match => {
        return `<strong>${match}</strong>`;
      });
  }
}
