import { Component } from '@angular/core';
import { ProgressBarComponent } from '../progressBar/progress-bar.component';

@Component({
    selector: 'byb-progress-bar',
    templateUrl: '../progressBar/progress-bar.component.html',
    styleUrls: ['../progressBar/progress-bar.component.scss']
  })

  export class BybProgressBarComponent extends ProgressBarComponent {

  /**
   * This method has been modified as its expected to behave differenly in Byb-selections and 5-A-side components.
   * So, this component has been created extending ProgressBarComponent for different implementation of calcProgress().
   *
   * @return {*}  {number}
   * @memberof BybProgressBarComponent
   */
  public calcProgress(): number {
    const { min, max, value } = this;

    if (value < min) {
      return 0;
    }

    if (value > max) {
      return 100;
    }

    if (min >= max) {
      return 0;
    }

    return 100 / (max - min) * (value - min);
  }
}
