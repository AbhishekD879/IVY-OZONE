import { ChangeDetectionStrategy, Component, Input, OnInit } from '@angular/core';
import { VirtualSharedService } from '@shared/services/virtual/virtual-shared.service';
import { RaceOutcomeDetailsService } from '@core/services/raceOutcomeDetails/race-outcome-details.service';
import { IOutcome } from '@core/models/outcome.model';
import { ISportEvent } from '@core/models/sport-event.model';

@Component({
  selector: 'race-silk',
  templateUrl: './race-silk.component.html',
  styleUrls: ['./race-silk.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class RaceSilkComponent implements OnInit {
  @Input() eventEntity: ISportEvent;
  @Input() outcomeEntity: IOutcome;
  @Input() isStreamBet: boolean;

  isVirtual: boolean = false;
  isGreyhound: boolean = false;
  isGeneric: boolean = false;
  isUKorIRE: boolean = false;

  constructor(
    private virtualSharedService: VirtualSharedService,
    private raceOutcomeDetailsService: RaceOutcomeDetailsService
  ) {
  }

  ngOnInit() {
    this.chooseSilkType();
  }

  /**
   * Choose the right silk type using input data.
   * Does it in mutually exclusive manner. There can be only one right silk type.
   */
  private chooseSilkType(): void {
    if (this.virtualSharedService.isVirtual(this.eventEntity.categoryId)) {
      this.isVirtual = true;
      return;
    }

    if (this.raceOutcomeDetailsService.isGreyhoundSilk(this.eventEntity, this.outcomeEntity)) {
      this.isGreyhound = true;
    }

    if (this.raceOutcomeDetailsService.isGenericSilk(this.eventEntity, this.outcomeEntity) || (this.isStreamBet && this.getDefaultSilk())) {
      this.isGeneric = true;
    }

    if (this.outcomeEntity.racingFormOutcome && this.outcomeEntity.racingFormOutcome.silkName) {
      this.isUKorIRE = true;
    }
  }

  getDefaultSilk(): boolean {
    return !this.outcomeEntity.racingFormOutcome && this.eventEntity.categoryId.toString() === '21';
  }
}
