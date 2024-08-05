import { Component, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { CommandService } from '@core/services/communication/command/command.service';
import { StorageService } from '@core/services/storage/storage.service';

import { IBetSelection } from '@betslip/services/betSelection/bet-selection.model';

@Component({
  selector: 'betslip-counter',
  templateUrl: 'betslip-counter.component.html',
  styleUrls: ['betslip-counter.component.scss']
})
export class BetslipCounterComponent implements OnInit, OnDestroy {
  dsBetCounter: number;
  bsBetCounter: number;
  betCounter: number;

  constructor(private pubsubService: PubSubService,
              private commandService: CommandService,
              private storageService: StorageService,
              private changeDetectorRef: ChangeDetectorRef) {}

  ngOnInit(): void {
    this.dsBetCounter = 0;
    this.bsBetCounter = this.betsLength;
    this.setCounter(true);

    this.pubsubService.subscribe('betSlipCounter', this.pubsubService.API.BETSLIP_COUNTER_UPDATE, (count: number) => {
      this.bsBetCounter = count || this.betsLength;
      this.setCounter();
    });

    // TODO: should be removed after yourcall full integration
    if (this.storageService.get('dsBetslip')) {
      this.commandService.executeAsync(this.commandService.API.DS_READY, undefined, 0)
        .then(data => this.updateCounterWithDS(data));
    }

    this.pubsubService.subscribe('betSlipCounter', this.pubsubService.API.DS_BETSLIP_COUNTER_UPDATE, this.updateCounterWithDS.bind(this));
  }

  ngOnDestroy(): void {
    this.pubsubService.unsubscribe('betSlipCounter');
  }

  get betsLength(): number {
    const bets: IBetSelection[] = this.storageService.get('betSelections'),
      toteBet = this.storageService.get('toteBet');
    return (bets && bets.length) || +Boolean(toteBet) || 0;
  }
  set betsLength(value:number){}

  /**
   * Sets counter by adding betslip and digital sport selections.
   * @private
   */
  protected setCounter(calledOnInit: boolean = false): void {
    this.betCounter = this.bsBetCounter + this.dsBetCounter;
    this.changeDetectorRef.detectChanges();
  }

  /**
   * Updates counter after change in digital sports.
   * @param {number} count
   * @private
   */
  private updateCounterWithDS(count: number): void {
    // Use timeout here as betslip counter updates comes from iframe and we need to start digest
    // cycle after applying new counter value
    this.dsBetCounter = count;
    this.setCounter();
  }
}
