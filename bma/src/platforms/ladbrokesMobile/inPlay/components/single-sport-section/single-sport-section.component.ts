import { Component, ChangeDetectionStrategy } from '@angular/core';
import { SingleSportSectionComponent } from '@app/inPlay/components/singleSportSection/single-sport-section.component';

@Component({
  selector: 'single-sport-section',
  templateUrl: 'single-sport-section.component.html',
  styleUrls: [
    '../../../../../app/inPlay/components/singleSportSection/single-sport-section.component.scss',
    './single-sport-section.component.scss'
  ],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class LadbrokesSingleSportSectionComponent extends SingleSportSectionComponent { }

