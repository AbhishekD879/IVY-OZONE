import {  Component } from '@angular/core';
import { trigger, transition, style, animate, state, keyframes } from '@angular/animations';
import {FiveASideEntryListOverlayComponent
    as AppFiveASideEntryListOverlayComponent
} from '@app/fiveASideShowDown/components/fiveASideEntry/fiveASideEntryListOverlay/fiveaside-entrylist-overlay.component';
@Component({
  selector: 'fiveaside-entrylist-overlay',
  templateUrl: './fiveaside-entrylist-overlay.component.html',
  styleUrls: ['./fiveaside-entrylist-overlay.component.scss'],
  animations:[trigger('overlay', [
    state('in', style({ transform: 'translateY(0)' })),
    transition('void => *', [
      animate(
        300,
        keyframes([
          style({ opacity: 1, transform: 'translateY(800px)', offset: 0 }),
          style({ opacity: 1, transform: 'translateY(400px)', offset: 0.5 }),
          style({ opacity: 1, transform: 'translateY(0)', offset: 1.0 })
        ])
      )
    ])
  ])]
})
export class FiveASideEntryListOverlayComponent extends AppFiveASideEntryListOverlayComponent {
}
