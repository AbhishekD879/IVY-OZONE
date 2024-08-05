import { Component, Input, OnInit, OnDestroy } from '@angular/core';

import { OddsBoostService } from '@oddsBoostModule/services/odds-boost.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { OverAskService } from '@betslip/services/overAsk/over-ask.service';

@Component({
  selector: 'odds-boost-betslip-header',
  templateUrl: './odds-boost-betslip-header.component.html',
  styleUrls: ['./odds-boost-betslip-header.component.scss']
})
export class OddsBoostBetslipHeaderComponent implements OnInit, OnDestroy {
  @Input() boostDisabled: boolean;

  reboost: boolean;
  active: boolean;

  private readonly COMPONENT_NAME: string = 'OddsBoostBetslipHeaderComponent';

  constructor(
    protected oddsBoostService: OddsBoostService,
    protected pubSubService: PubSubService,
    protected overAskService: OverAskService
  ) {
  }

  ngOnInit(): void {
    this.active = this.oddsBoostService.getBoostActiveFromStorage();
    this.pubSubService.subscribe(this.COMPONENT_NAME, this.pubSubService.API.ODDS_BOOST_CHANGE, (active: boolean) => {
      this.active = active;
      this.reboost = false;
    });

    this.pubSubService.subscribe(this.COMPONENT_NAME, this.pubSubService.API.ODDS_BOOST_REBOOST, () => {
      this.reboost = this.active;
    });
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe(this.COMPONENT_NAME);
  }

  onBoostClick(): void {
    if (this.boostDisabled) {
      return;
    }

    if (this.oddsBoostService.hasSelectionsWithFreeBet() && !this.active) {
      this.oddsBoostService.showOddsBoostFreeBetDialog(false, 'betslip');
      return;
    }

    if (this.reboost) {
      this.pubSubService.publishSync(this.pubSubService.API.BETSLIP_UPDATED);
      this.pubSubService.publish(this.pubSubService.API.ODDS_BOOST_REBOOST_CLICK);
      this.oddsBoostService.sendEventToGTM('betslip', true);
      return;
    }

    if (this.oddsBoostService.canBoostSelections()) {
      const active = !this.active;
      this.pubSubService.publish(this.pubSubService.API.ODDS_BOOST_CHANGE, active);
      this.oddsBoostService.sendEventToGTM('betslip', active);
    } else {
      this.oddsBoostService.showOddsBoostSpDialog();
    }
  }

  get isAvailable(): boolean {
    return this.oddsBoostService.isOddsBoostBetslipHeaderAvailable();
  }
set isAvailable(value:boolean){}
  showInfoDialog(): void {
    this.oddsBoostService.showInfoDialog();
  }
}
