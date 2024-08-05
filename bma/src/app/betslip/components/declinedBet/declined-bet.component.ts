import { ChangeDetectionStrategy, Component, Input } from '@angular/core';
import { IOutcome } from '@core/models/outcome.model';

@Component({
  selector: 'declined-bet',
  templateUrl: 'declined-bet.component.html',
  styleUrls: ['declined-bet.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class DeclinedBetComponent {
  @Input() selectionName?: string;
  @Input() fctcData?: {outcomes: IOutcome[], lines: number, modifire: string};
  @Input() stakeMultiplier?: string;
  @Input() marketName: string;
  @Input() eventName?: string;

  constructor( ) { }
}
