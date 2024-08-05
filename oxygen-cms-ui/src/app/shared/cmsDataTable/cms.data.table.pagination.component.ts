import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'cms-data-table-pagination',
  templateUrl: './cms.data.table.pagination.component.html',
  styleUrls: ['./cms.data.table.pagination.component.scss']
})
export class CMSDataTablePaginationComponent {
  @Input() range: Array<void>;
  @Input() currentIndex: number;
  @Output() goToPage: EventEmitter<number> = new EventEmitter<number>();
}
