import { trigger, transition, style, animate } from '@angular/animations';
import { Component } from '@angular/core';
import {
  FiveASideMultiEntryProgressComponent
    as AppFiveASideMultiEntryProgressComponent
} from '@app/fiveASideShowDown/components/fiveASideEntry/fiveASideMultiEntryProgress/fiveaside-multientry-progress.component';
@Component({
  selector: 'fiveaside-multientry-progress',
  templateUrl: './fiveaside-multientry-progress.component.html',
  styleUrls: ['./fiveaside-multientry-progress.component.scss'],
  animations: [trigger('myInsertMultiRemoveTrigger', [
    transition(':enter', [style({ marginLeft: '0%' }), animate(1000)])
  ])]
})
export class FiveASideMultiEntryProgressComponent extends AppFiveASideMultiEntryProgressComponent {
}
