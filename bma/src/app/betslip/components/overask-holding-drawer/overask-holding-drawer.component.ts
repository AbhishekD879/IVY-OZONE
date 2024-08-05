import { ChangeDetectionStrategy, Component, Input } from '@angular/core';

@Component({
  selector: 'overask-holding-drawer',
  templateUrl: './overask-holding-drawer.component.html',
  styleUrls: ['./overask-holding-drawer.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class OveraskHoldingDrawerComponent {
  @Input() title: string;
  @Input() topMessage: string;
  @Input() bottomMessage: string;
  @Input() maxStake: number;
  @Input() currencySymbol: string;
  @Input() relativeToParent = false;
}
