import { ITimeFormData } from '@core/models/time-form-data.model';
import { Component, Input } from '@angular/core';

@Component({
  selector: 'timeform-widget',
  templateUrl: './timeform-widget.component.html',
  styleUrls: ['./timeform-widget.component.scss']
})
export class TimeFormWidgetComponent {

  @Input() timeformData: ITimeFormData;

  trackByStar(index: number): number {
    return index;
  }

  trackByPosition(index: number, position: { greyHoundFullName: string; }): string {
    return `${index}${position.greyHoundFullName}`;
  }

  getTimeFormClass(greyhound: { positionPrediction: string; }): string {
    return `position-${greyhound.positionPrediction}`;
  }
}
