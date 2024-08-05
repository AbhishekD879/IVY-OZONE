import { Component, OnInit,ChangeDetectionStrategy } from '@angular/core';
import {
  FiveASideEntryDetailsComponent
    as AppFiveASideEntryDetailsComponent
} from '@app/fiveASideShowDown/components/fiveASideEntry/fiveASideEntryDetails/fiveaside-entry-details.component';
@Component({
  selector: 'fiveaside-entry-details',
  templateUrl: './fiveaside-entry-details.component.html',
  styleUrls: ['./fiveaside-entry-details.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FiveASideEntryDetailsComponent extends AppFiveASideEntryDetailsComponent implements OnInit {
}
