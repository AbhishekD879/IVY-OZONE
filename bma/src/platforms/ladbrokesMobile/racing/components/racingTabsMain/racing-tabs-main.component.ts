import { Component } from '@angular/core';
import { HorseracingService } from '@coreModule/services/racing/horseracing/horseracing.service';
import { GreyhoundService } from '@coreModule/services/racing/greyhound/greyhound.service';
import { of, from, Observable, zip } from 'rxjs';
import {
  RacingTabsMainComponent as AppRacingTabsMainComponent
} from '@app/racing/components/racingTabsMain/racing-tabs-main.component';
import { ISportEvent } from '@core/models/sport-event.model';

@Component({
    selector: 'racing-tabs-main-component',
    templateUrl: '../../../../../app/racing/components/racingTabsMain/racing-tabs-main.component.html'
})
export class RacingTabsMainComponent extends AppRacingTabsMainComponent {

  protected concatDataRequests(racingInstance: HorseracingService | GreyhoundService): Observable<[ISportEvent[], ISportEvent[]]> {
    return zip(from(racingInstance.getByTab(this.display, true)), of([] as ISportEvent[]));
  }
}
