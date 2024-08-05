import { Component, Input } from '@angular/core';

@Component({
  selector: 'odds-boost-button',
  templateUrl: './odds-boost-button.component.html',
  styleUrls: ['./odds-boost-button.component.scss']
})
export class OddsBoostButtonComponent {
  @Input() disabled: boolean = false;

  oddsBoostLabel: string;
  enabledVal: boolean;
  canAnimate: boolean = false;
  boostedVal: boolean = false;

  private label: { [key: string]: string } = {
    ENABLED: 'oddsboost.boostButton.enabled',
    DISABLED: 'oddsboost.boostButton.disabled',
    REBOOST: 'oddsboost.boostButton.reboost'
  };

  @Input()
  set reboost(val: boolean) {
    if (val && this.enabledVal) {
      this.oddsBoostLabel = this.label['REBOOST'];
      this.boostedVal = false;
    }
  }

  @Input()
  set enabled(val: boolean) {
    this.enabledVal = val;

    if (val) {
      this.oddsBoostLabel = this.label['ENABLED'];
      this.canAnimate = true;
      this.boostedVal = true;
    } else {
      this.oddsBoostLabel = this.label['DISABLED'];
      this.boostedVal = false;
    }
  }
  get enabled(): boolean {
    return this.enabledVal;
  }
}
