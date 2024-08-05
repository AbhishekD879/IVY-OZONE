import {AfterViewInit, Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {SortableTableService} from '@app/client/private/services/sortable.table.service';
import {TableColumn} from '@app/client/private/models/table.column.model';
import {TableLink} from '@app/client/private/models/table.link.model';
import * as _ from 'lodash';
import {DataTableColumn} from '@app/client/private/models/dataTableColumn';
import TimelineUtils from '@app/timeline/timeline-utils';
import { Sort } from '@angular/material/sort';

/**
 * Custom table
 */
@Component({
  selector: 'timeline-data-table',
  templateUrl: './timeline.data.table.component.html',
  styleUrls: ['./timeline.data.table.component.scss'],
  providers: [
    SortableTableService
  ]
})
export class TimelineDataTableComponent implements OnInit, AfterViewInit {
  isPublishable = TimelineUtils.isPublishable;
  isUnpublishable = TimelineUtils.isUnpublishable;

  /**
   * Data to bew viewed in table
   * @type {any[]}
   */
  @Input() customTableData: Array<any> = [];

  @Input() startingNumberOffset: number = 0;

  @Input() background: string = 'bg-teal';

  /**
   * Flag to add Drag-n-drop functionality
   * @type {boolean}
   */
  @Input() reorder: boolean = false;

  /**
   * Flag to identify if multy remove with checkboxes are rendered
   */
  @Input() multyRemove: boolean = false;

  /**
   * Emits event with ids to remove
   */
  @Output() onMultyRemove = new EventEmitter();


  /**
   * {
   *   name: 'Title',
   *   property: 'title'
   * }
   * @type {}[]
   */
  @Input() customTableColumns?: Array<TableColumn> = [];

  /**
   * data string to filter table data
   * @type {string}
   */
  @Input() filterString: string = '';

  @Input() filterProperties: Array<string> = [];

  /**
   * Array of field names, wich will be used in filtering logic.
   * @type {any[]}
   */
  @Input() filterField: Array<string> = [];

  /**
   * Enable remove checkbox callback if Action "remove" provided.
   */
  @Input() isRemoveCheckboxEnabled: (value: any) => boolean;

  /**
   * Remove data item callback,
   * if Action "remove" provided.
   * @type {EventEmitter<any>}
   */
  @Output() onRemoveTableElement = new EventEmitter();

  @Output() onPublishTableElement = new EventEmitter();
  @Output() onUnpublishTableElement = new EventEmitter();
  @Output() onApproveTableElement = new EventEmitter();
  @Output() onToDraftTableElement = new EventEmitter();

  /**
   * Edit data item callback,
   * if Action "onPageEdit" provided.
   * @type {EventEmitter<any>}
   */
  @Output() onPageEditTableElement = new EventEmitter();

  /**
   * Reorder data callback
   * @type {EventEmitter<any>}
   */
  @Output() onElementsOrder = new EventEmitter();

  tableUniqueClass: string = _.uniqueId('reorder_');
  isSorted: boolean = false;
  isFiltered: boolean = true;

  sorting: Sort;

  constructor(
    private sortableTableService: SortableTableService
  ) {
  }

  /**
   * Remove element
   * @param {any} dataElement
   */
  removeDataElement(dataElement: any) {
    this.onRemoveTableElement.emit(dataElement);
  }

  removeDataElements(): void {
    this.onMultyRemove.emit(this.selectedRows);
  }

  private get selectedRows(): string[] {
    return this.customTableData.filter(r => r.multyRowSelected).map(r => r.id);
  }

  /**
   * Edit element on page in pop-up
   * @param {any} dataElement
   */
  editDataElement(dataElement: any) {
    this.onPageEditTableElement.emit(dataElement);
  }

  /**
   * set sort parameters, while clicking on table headers
   * @param {Sort} sort
   */
  sortData(sort: Sort) {
    this.sorting = sort;
  }

  // TODO refactor this method
  // get filtered, sorted data
  get dataElementsList() {
    let editedList = [];

    // block for getting array of sorted elements
    if (this.sorting && this.sorting.active && this.sorting.direction) {
      this.isSorted = true;

      editedList = this.customTableData.slice();
      editedList = editedList.sort((a, b) => {
        const isAsc = this.sorting.direction === 'asc';

        return compare(a[this.sorting.active], b[this.sorting.active], isAsc);
      });
    } else {
      this.isSorted = false;
    }

    // block for getting filtered elements. could be sorted and filtered array
    if (this.filterProperties.length > 0 && this.filterString && this.filterString.length > 0) {
      this.isFiltered = true;

      if (editedList.length > 0) {
        editedList = this.filterTable(editedList);
      } else {
        editedList = this.filterTable(this.customTableData);
      }

    } else {
      this.isFiltered = false;

      // return based not filtered and not sorted data.
      if (editedList.length === 0)  {
        editedList = this.customTableData;
      }
    }

    return editedList;
  }


  /**
   * Add drag-n-drop reorder functionality to table
   */
  addReorderingToTable() {
    const self = this;
    this.sortableTableService.addSorting({
      dataToReorder: self.customTableData,
      mainSelector: `.custom-table.${this.tableUniqueClass} tbody`,
      handlerSelector: '.drag-handler',
      onReorderEnd(data, indexOfDraggedElement) {
        // emit reordered data.
        const newOrder = {
          order: self.customTableData.map(element => element.id),
          id: self.customTableData[indexOfDraggedElement].id
        };
        self.onElementsOrder.emit(newOrder);
      }
    });
  }

  /**
   * If user will not provide array of customTableColumns,
   * we will generate columns for each value in object.
   */
  createDefaultColumnTables() {
    const columnsNames = Object.keys(this.customTableData[0]);
    this.customTableColumns = columnsNames.map(columnName => {
      const column: TableColumn = {
        name: columnName,
        property: columnName
      };

      return column;
    });
  }

  ngAfterViewInit() {
    if (this.reorder) {
      this.addReorderingToTable();
    }
  }

  ngOnInit() {
     if (this.customTableColumns.length === 0 && this.customTableData.length > 0) {
        this.createDefaultColumnTables();
     }
  }

  getLink(row: any, link?: TableLink): string {
    let rowLink: TableLink = link;
    if (!link) {
      rowLink = this.customTableColumns.find((column) => {
        return !!column.link;
      }).link;
    }

    if (!rowLink) {
      return '';
    }

    let resultingLink = rowLink.path ? `${rowLink.path}/${row[rowLink.hrefProperty]}` : row[rowLink.hrefProperty];
    if (rowLink.sibling) {
      resultingLink = '../' + resultingLink;
    }
    return resultingLink;
  }

  private filterTable(list): any[] {
    return list.filter((item) => {
      let match = false;

      this.filterProperties.forEach(propertyName => {
         if (item[propertyName] && item[propertyName].toString().toLowerCase().indexOf(this.filterString.toLowerCase()) >= 0) {
           match = true;
         }
      });

      return match;
    });
  }

  isActiveColumn(dataElement: any, column: DataTableColumn): boolean {
    return (dataElement[column.property] && !column.isReversed) || (column.isReversed && !dataElement[column.property]);
  }

  isValidDate(dateString) {
    const date = new Date(dateString);
    return !isNaN(date.getTime());
  }

  public getHtmlString(html: string): string {
    return html.replace(/<(?:.|\n)*?>/gm, '');
  }

  public getNestedValue(dataElement: any, property: string) {
    return _.get(dataElement, property);
  }

  approve(dataElement: any) {
    this.onApproveTableElement.emit(dataElement);
  }

  toDraft(dataElement: any) {
    this.onToDraftTableElement.emit(dataElement);
  }

  publish(dataElement: any) {
    this.onPublishTableElement.emit(dataElement);
  }

  unpublish(dataElement: any) {
    this.onUnpublishTableElement.emit(dataElement);
  }
}

function compare(a, b, isAsc) {
  if (_.isString(a) && _.isString(b)) {
    a = a.toLowerCase();
    b = b.toLowerCase();
  }
  return (a < b ? -1 : 1) * (isAsc ? 1 : -1);
}
