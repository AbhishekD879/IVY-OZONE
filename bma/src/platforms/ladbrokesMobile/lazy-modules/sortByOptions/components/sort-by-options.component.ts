import { Component } from '@angular/core';
import { SortByOptionsComponent as AppSortByOptionsComponent } from '@lazy-modules/sortByOptions/components/sort-by-options.component';

@Component({
  selector: 'sort-by-options',
  templateUrl: './sort-by-options.component.html',
  styleUrls: ['./sort-by-options.component.scss']
})
export class SortByOptionsComponent extends AppSortByOptionsComponent {}
