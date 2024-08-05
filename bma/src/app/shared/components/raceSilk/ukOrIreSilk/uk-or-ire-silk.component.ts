import { ChangeDetectionStrategy, Component, Input, OnInit } from '@angular/core';
import { ISilkStyleModel } from '@core/services/raceOutcomeDetails/silk-style.model';
import { RaceOutcomeDetailsService } from '@core/services/raceOutcomeDetails/race-outcome-details.service';
import { ISportEvent } from '@core/models/sport-event.model';
import { IOutcome } from '@core/models/outcome.model';

@Component({
  selector: 'uk-or-ire-silk',
  templateUrl: './uk-or-ire-silk.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class UkOrIreSilkComponent implements OnInit {
  @Input() eventEntity: ISportEvent;
  @Input() outcomeEntity: IOutcome;
  @Input() isStreamBet: boolean;
  silkClass: ISilkStyleModel;

  constructor(
    private raceOutcomeDetailsService: RaceOutcomeDetailsService
  ) {
  }

  ngOnInit() {
    this.silkClass = this.raceOutcomeDetailsService.getSilkStyle(this.eventEntity.markets[0], this.outcomeEntity,'', false, this.isStreamBet);
  }
}
