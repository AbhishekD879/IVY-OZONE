import { Component, OnInit } from '@angular/core';
import {
  FiveASideEntryListComponent
    as AppFiveASideEntryListComponent
} from '@app/fiveASideShowDown/components/fiveASideEntry/fiveASideEntryList/fiveaside-entry-list.component';

@Component({
  selector: 'fiveaside-entry-list',
  templateUrl: './fiveaside-entry-list.component.html',
  styleUrls: ['./fiveaside-entry-list.component.scss']
})
export class FiveASideEntryListComponent extends AppFiveASideEntryListComponent implements OnInit {
}
