import { ChangeDetectionStrategy, Component, Input } from '@angular/core';

@Component({
  selector: 'fiveaside-spinner',
  template: ``,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FiveASideSpinnerComponent {
  @Input() marginTop: number;
  @Input() isLeaderBoard: boolean;
}
