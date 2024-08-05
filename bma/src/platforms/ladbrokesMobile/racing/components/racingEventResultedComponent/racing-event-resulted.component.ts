import { Component } from '@angular/core';
import { RacingEventResultedComponent } from '@racing/components/racingEventResultedComponent/racing-event-resulted.component';

@Component({
  selector: 'racing-event-resulted',
  templateUrl: '../../../../../app/racing/components/racingEventResultedComponent/racing-event-resulted.component.html',
  styleUrls: ['./racing-event-resulted.component.scss']
})
export class LadbrokesRacingEventResultedComponent extends RacingEventResultedComponent {

  formatAntepostTerms(str: string): string {
    const newStr = str
      .replace(/( - places)/ig, 'Places')
      .replace(/(odds|:)/ig, '')
      .replace(/([,])/ig, '-')
      .replace(/\d+\/\d+( odds)/ig, match => {
        return `${match}`;
      });
    return newStr.replace(/[0-9]+(?!.*[0-9])/, match => `${match}`);
  }
}
