import { ChangeDetectionStrategy, Component, Input, OnInit } from '@angular/core';
import { ISportEvent } from '@core/models/sport-event.model';
import { IOutcome } from '@core/models/outcome.model';

@Component({
  selector: 'gh-silk',
  template: '<div class="gh-silk" [ngClass]="greyhoundClass" data-crlat="gh-silk"></div>',
  styleUrls: ['gh-silk.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class GhSilkComponent implements OnInit {
  @Input() event: ISportEvent;
  @Input() outcome: IOutcome;
  @Input() postPickSilk: number = 0;    // for racing-post-pick component usage

  greyhoundClass: string;

  ngOnInit(): void {
    this.greyhoundClass = this.postPickSilk ?
      `runner-deflt-gh${this.postPickSilk}` : `runner${this.getCountryFlag()}-gh${this.outcome.runnerNumber}`;
  }

  private getCountryFlag(): string {
    const flag = this.event.typeFlagCodes.split(',').find((v: string) => v === 'US' || v === 'AU');
    return flag ? `-${flag.toLowerCase()}` : '-deflt';
  }
}
