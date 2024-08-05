import { Component, ChangeDetectionStrategy } from '@angular/core';
import {
  FiveASideSpinnerComponent
    as AppFiveASideSpinnerComponent
} from '@app/fiveASideShowDown/components/fiveASideSpinner/fiveaside-spinner.component';

@Component({
  selector: 'fiveaside-spinner',
  templateUrl: './fiveaside-spinner.component.html',
  styleUrls: ['./fiveaside-spinner.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FiveASideSpinnerComponent extends AppFiveASideSpinnerComponent {
}
