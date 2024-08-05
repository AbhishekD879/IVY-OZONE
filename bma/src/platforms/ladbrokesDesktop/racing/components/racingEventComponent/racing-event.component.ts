import {
  LadbrokesRacingEventComponent as RacingEventComponent
} from '@ladbrokesMobile/racing/components/racingEventComponent/racing-event.component';
import { OnInit, Component } from '@angular/core';

import * as _ from 'underscore';
import { IRacingPostVerdict } from '@racing/models/racing-post-verdict.model';
import { IStreamsCssClasses } from '@core/models/streams-css-classes.model';

import environment from '@environment/oxygenEnvConfig';

@Component({
  templateUrl: 'racing-event.component.html',
  styleUrls: ['./racing-event.component.scss'],
  selector: 'racing-event'
})
export class DesktopRacingEventComponent extends RacingEventComponent implements OnInit {
  racingPostVerdictData: IRacingPostVerdict;
  cssClassesForStreams: IStreamsCssClasses = {
    iGameMedia: '',
    otherProviders: 'live-column watch-live'
  };
  defaultLiveCommentaryUrl: string = environment.LIVE_COMMENTARY_URL;
  showSpinnerInDropdown: boolean;
  readonly MARKETS_CONTAINER: string = '.markets-container';

  ngOnInit() {
    super.ngOnInit();
    if (this.eventEntity && _.has(this.eventEntity.racingFormEvent, 'overview')) {
      this.racingPostSummary = this.eventEntity.racingFormEvent.overview;
    }
    if (this.eventEntity) {
      this.racingPostVerdictData = this.eventEntity.racingPostVerdict;
    }
  }

  formatEventTerms(str: string): string {
    return str
      .replace(/ODDS/ig, '')
      .replace(/Each Way:/ig, 'E/W')
      .replace(/- places/ig, 'Places');
  }

  formatAntepostTerms(str: string): string {
    const newStr = str
      .replace(/(odds)/ig, '')
      .replace(/Each Way:/ig, 'E/W')
      .replace(/(- places)/ig, 'Places')
      .replace(/\d+\/\d+( odds)/ig, match => {
        return `${match}`;
      });
    return newStr.replace(/[0-9]+(?!.*[0-9])/, match => `${match}`);
  }

  openLiveCommentary(): void {
    const sportChannel = this.sportName === 'horseracing' ? 'horses' : 'greyhound';
    const liveCommentaryUrl = (this.liveCommentary && this.liveCommentary[this.sportName]) ||
                              `${this.defaultLiveCommentaryUrl}&channel=${sportChannel}`;


    this.windowRef.nativeWindow.open(liveCommentaryUrl, 'liveCommentary',
    'width=400,height=275,screenX=50,left=50,screenY=50,top=50');
  }
}
