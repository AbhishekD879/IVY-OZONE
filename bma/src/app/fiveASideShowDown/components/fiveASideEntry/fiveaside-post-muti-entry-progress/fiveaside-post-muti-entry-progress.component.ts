import { animate, style, transition, trigger } from '@angular/animations';
import { Component } from '@angular/core';
import {
  FiveASideMultiEntryProgressComponent
} from '@app/fiveASideShowDown/components/fiveASideEntry/fiveASideMultiEntryProgress/fiveaside-multientry-progress.component';

@Component({
  selector: 'fiveaside-post-muti-entry-progress',
  template: ``,
  animations: [trigger('myInsertMultiRemoveTrigger', [
    transition(':enter', [style({ marginLeft: '0%' }), animate(1000)])
  ])]
})
export class FiveasidePostMutiEntryProgressComponent extends FiveASideMultiEntryProgressComponent {
}
