import { AfterViewInit, Component, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges } from '@angular/core';
import { Sort } from '@angular/material/sort';
import { SortableTableService } from '@app/client/private/services/sortable.table.service';
import { TableColumn } from '@app/client/private/models/table.column.model';
import { TableLink } from '@app/client/private/models/table.link.model';
import * as _ from 'lodash';
import { DataTableColumn } from '@app/client/private/models/dataTableColumn';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { Observable, of as observableOf } from 'rxjs';
import { map } from 'rxjs/operators';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AppConstants } from '@app/app.constants';
import { BigCompetitionAPIService } from '@app/sports-pages/big-competition/service/big-competition.api.service';
import { DatePipe } from '@angular/common';

/**
 * Custom table
 */
@Component({
  selector: 'cms-data-table',
  templateUrl: './cms.data.table.component.html',
  styleUrls: ['./cms.data.table.component.scss'],
  providers: [
    SortableTableService, BigCompetitionAPIService,
    DatePipe

  ]
})
export class CMSDataTableComponent implements OnInit, AfterViewInit, OnChanges {
  /**
   * Data to bew viewed in table
   * @type {any[]}
   */
  @Input() potTableData: Array<any> = [];

  @Input() customTableData: Array<any> = [];

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
   * Actions array.
   * Cureently hardcoded and supported only "remove" action.
   * @type {any[]}
   */
  @Input() actions: Array<string> = [];

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
   * Enable table data pagination, if provided. Specifies number of element on page.
   */
  @Input() paginationLimit: number;

  /**
   * Reflects currently shown page number. Initial value can be set externally.
   */
  @Input() paginationIndex: number = 0;
   /**
   * Reflects currently changed values in dataTOReorder.
   */
   @Input() updatingPopularTimeFilters?: boolean;

  /**
   * Clone data item callback,
   * if Action "clone" provided.
   * @type {EventEmitter<any>}
   */
  @Output() onCloneTableElement = new EventEmitter();

  /**
   * Remove data item callback,
   * if Action "remove" provided.
   * @type {EventEmitter<any>}
   */
  @Output() onRemoveTableElement = new EventEmitter();

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
  @Input() addTable: boolean;
  @Input() sportId: number;
  @Output() removeMarket = new EventEmitter();
  @Output() addMarketsToList = new EventEmitter();
  @Output() addList = new EventEmitter();
  @Input() showMarketSwitcher: boolean;
  @Input() popularBetsMarketSwitcher: boolean;
  @Output() addNewBybToList = new EventEmitter();
  @Input() isAddRowValue: boolean;
  @Input() expandedDetails: any;
  @Input() isAddTable: boolean;
  @Output() removeBybRow = new EventEmitter();
  @Input() cmsDatatable: boolean;
  @Input() validateNumberOrder: boolean = false;
  @Input() disableButtons: boolean = false;
  title: string;
  eventId: string;
  marketId: string;
  createdBy: string;
  createdAt: string;
  location: string;
  callApiforSave: Boolean = false;
  @Input() showaddButton: Boolean=true;
  @Input() insightsDatatable:boolean;
  @Input() savedSuccessFully: boolean;
  orderCheck:boolean=true;

  tableUniqueClass: string = _.uniqueId('reorder_');
  isSorted: boolean = false;
  isFiltered: boolean = true;
  paginationStart: number = 0;
  paginationRange: Array<void> = [];
  sorting: Sort;
  marketName = '';
  displayName = '';
  updatedName: string;
  isLineEdit = { 'show': false, 'title': '' };
  sportsWithMultiMarkets = [1, 6, 30, 31];

  constructor(
    protected sortableTableService: SortableTableService,
    protected sanitizer: DomSanitizer,
    protected snackBar: MatSnackBar,
    protected bigCompetitionApiService: BigCompetitionAPIService,
    protected datePipe: DatePipe
  ) { }
  ngAfterViewInit() {
    if (this.reorder) {
      this.addReorderingToTable();
    }
    this.orderCheck =this.expandedDetails?.every((val)=> val.saved);
  }

  @Input() competionList1: any = [];
  ngOnInit() {
    if (this.customTableColumns.length === 0 && this.customTableData.length > 0) {
      this.createDefaultColumnTables();
    }

    if (this.savedSuccessFully && this.cmsDatatable) {
      let ele: any = document.getElementById('addbtn') as HTMLElement;
      ele && ele.scrollIntoView();
    }
  }

  ngOnChanges(changes: SimpleChanges) {
    if ((changes.filterString && !changes.filterString.firstChange) ||
      (changes.paginationLimit && !changes.paginationLimit.firstChange)) {
      this.paginationIndex = 0;
    }
    // Added this condition for popular bets, Backed in last and Event starts In filter tables to update the data in sortable create
    if(changes.updatingPopularTimeFilters && changes.updatingPopularTimeFilters.currentValue){
      this.addReorderingToTable();
    }
  }

  /**
   * Clone element
   * @param {any} dataElement
   */
  cloneDataElement(dataElement: any) {
    this.onCloneTableElement.emit(dataElement);
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

  get selectedRows(): string[] {
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

  // ToDo: getter should converted into plain subject, which is streaming customTableData only on sort/filter/pagination actions
  // ToDo: but some pages still may mutate input data directly, thus rely on permanent change detection
  // get filtered, sorted, paginated data
  get dataElementsList(): Observable<Array<any>> {
    return observableOf(this.customTableData?.slice()).pipe(
      map(list => this.filterTable(list)),
      map(list => this.sortTable(list)),
      map(list => this.paginateTable(list)),
    );
  }

  /**
   * Add drag-n-drop reorder functionality to table
   */
  addReorderingToTable() {
    const self = this;
    this.sortableTableService.addSorting({
      dataToReorder: self.cmsDatatable ? self.expandedDetails : self.customTableData,
      mainSelector: `.custom-table.${this.tableUniqueClass} tbody`,
      handlerSelector: '.drag-handler',
      onReorderEnd(data, indexOfDraggedElement) {
        //emit reordered data for market switcher table
        if (self.showMarketSwitcher) {
          const newOrder = [];
          this.dataToReorder.map(element => {
            newOrder.push({
              'templateMarketName': element.templateMarketName,
              'title': element.title
            });
          });
          self.onElementsOrder.emit(newOrder);
        }
         //PopularBets reordering here//
         else if(self.popularBetsMarketSwitcher) {
          const popularBetsnewOrder = [];
          this.dataToReorder.map(element => {
            popularBetsnewOrder.push({
              'displayName': element.displayName,
              'isEnabled': element.isEnabled,
              'isTimeInHours': element.isTimeInHours, 
              'isDefault': element.isDefault, 
              'time': element.time
            });
          });
          self.onElementsOrder.emit(popularBetsnewOrder);
        } else if (self.cmsDatatable) {
          let orderData: any = this.dataToReorder;
          const newOrder = {
            id: orderData[indexOfDraggedElement].id,
            order: orderData.map(element => element.id),
          };
          self.onElementsOrder.emit(newOrder);
        }
        // emit reordered data.
        else {
          const newOrder = {
            order: self.customTableData.map(element => element.id),
            id: self.customTableData[indexOfDraggedElement].id
          };
          self.onElementsOrder.emit(newOrder);
        }
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
  getLinkMapping(row: any, link?: TableLink): string {
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
    return 'mapping/' + resultingLink;
  }

  isActiveColumn(dataElement: any, column: DataTableColumn): boolean {
    return (dataElement[column.property] && !column.isReversed) || (column.isReversed && !dataElement[column.property]);
  }

  isValidDate(dateString) {
    const date = new Date(dateString);
    return !isNaN(date.getTime());
  }

  getHtmlString(html: string): SafeHtml {
    const cleanHTML = html.replace(/\\\//g, '');
    return this.sanitizer.bypassSecurityTrustHtml(cleanHTML);
  }

  getNestedValue(dataElement: any, property: string) {
    return _.get(dataElement, property);
  }

  /**
   * Apply pagination index, validation forces valid pagination range limits.
   * @param pageIndex
   */
  goToPage(pageIndex: number): void {
    const lastIndex = this.paginationRange.length - 1;
    this.paginationIndex = pageIndex < 0 || lastIndex < 0 ? 0 : pageIndex > lastIndex ? lastIndex : pageIndex;
  }

  private filterTable(list: Array<any>): Array<any> {
    this.isFiltered = !!(this.filterProperties.length > 0 && this.filterString && this.filterString.length > 0);
    return this.isFiltered ? this.filterList(list) : list;
  }

  private filterList(list: Array<any>): Array<any> {
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

  private sortTable(list: Array<any>): Array<any> {
    this.isSorted = !!(this.sorting && this.sorting.active && this.sorting.direction);
    return this.isSorted ? this.sortList(list) : list;
  }
  private sortList(list: Array<any>): Array<any> {
    const toLowerCase = s => typeof s === 'string' ? s.toLowerCase() : s;

    return list.sort((A, B) => {
      const direction = this.sorting.direction === 'asc' ? 1 : -1,
        a = toLowerCase(A[this.sorting.active]),
        b = toLowerCase(B[this.sorting.active]);

      return (a < b ? -1 : 1) * direction;
    });
  }

  private paginateTable(list: Array<any>): Array<any> {
    return this.paginationLimit ? this.paginateList(list) : list;
  }

  private paginateList(list: Array<any>): Array<any> {
    this.paginationRange = new Array(this.paginationLimit ? Math.ceil(list.length / this.paginationLimit) : 0);
    this.goToPage(this.paginationIndex); // keep current index in valid range, when number of table entries decrease dynamically
    this.paginationStart = this.paginationIndex * this.paginationLimit;
    return list.slice(this.paginationStart, this.paginationStart + this.paginationLimit);
  }

  /**
   * Handle edit and save icons
   * @param data
   * @param mode
   * findIndex to find the postion of row which is supposed to edit
   */
  editInLine(data, mode): void {
    if (mode && this.updatedName) {
      this.isLineEdit = { 'show': false, 'title': '' };
      if (this.customTableData.findIndex(i => i.title === this.updatedName) === -1) {
        const a = this.customTableData.findIndex(i => i.templateMarketName === data.templateMarketName);
        this.customTableData[a].title = this.updatedName;
        this.onElementsOrder.emit(this.customTableData);
      } else {
        this.snackBar.open(`Duplicate record exist!`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      }
    } else {
      this.isLineEdit = { 'show': true, 'title': data.title };
      this.updatedName = data.title;
    }
  }

  /**
   * Emit- Remove market data in market switcher table
   */
  removeNewMarket(): void {
    this.removeMarket.emit(false);
    this.clearRowData();
  }

  /**
     * @param marketName
     * @param displayName
     * @param aggregated
     * Emit- Newly added market data in market switcher table
     * findIndex to check if no duplicate marketName and displayName exists
     */


  saveNewBybMarket(rowData, type: any): void {
    this.showtoolTip = [];
    this.expandedDetails.forEach(data => {
      data.saved = true
      data.showDate = false;
    });
    if (type == 'save') {
      rowData.saved = true;
      rowData.showDate = false;
      this.sendAddNewByb(rowData, type);
      this.showaddButton = true;
    } else {
      rowData.saved = false;
      this.showaddButton = false;
      rowData.showDate = true;
      this.setDayTime(rowData);
    }
    this.orderCheck =this.expandedDetails?.every((val)=> val.saved);
    this.showtoolTip = this.competionList1.filter(list => rowData.locations.includes(list.id)).map(values => values.name)
  }

  removeBybRowRecord(row, ind): void {
    this.showaddButton = true;
    if (row.id == '') {
      this.expandedDetails.splice(ind, 1);
    }
    this.removeBybRow.emit(row);
    this.clearrowData();
  }

  clearrowData(): void {
    this.title = '';
    this.eventId = '';
    this.marketId = '';
    this.createdBy = '';
    this.createdAt = '';
    this.location = '';
  }

  /**
   * @param marketName
   * @param displayName
   * Emit- Newly added market data in market switcher table
   * findIndex to check if no duplicate marketName and displayName exists
   */
  addMarket(marketName, displayName,aggregated): void {
    if (marketName && displayName) {
      let markets = marketName.toLowerCase().split(',');
      let isMultipleMarketAllowed = this.sportsWithMultiMarkets.indexOf(this.sportId) > -1;
      let maxAllowedMarket = isMultipleMarketAllowed ? 3 : 1;
      aggregated = markets.length > 1;
      if (markets.length <= maxAllowedMarket) {
        const toFindDuplicates = markets => markets.filter((item, index) => markets.indexOf(item) !== index)
        const duplicateElementa = toFindDuplicates(markets);
        if (duplicateElementa.length >= 1) {
          this.snackBar.open(`Duplicate market exist!`, 'Ok!', {
            duration: AppConstants.HIDE_DURATION,
          });
          return;
        }else{
        let isValidMarket = false;
        for (let market of markets) {
          if (!this.customTableData) {
            isValidMarket = true;
          } else if (this.customTableData.findIndex(i => i.templateMarketName.replace(', ', ',').toLowerCase().split(',').indexOf(market.trim()) > -1 || i.title === displayName) === -1) {
            isValidMarket = true;
          } else {
            isValidMarket = false;
            break;
          }
        }
        if (isValidMarket) {
          this.sendAddMarket(marketName, displayName,aggregated);
        }
        else {
          this.snackBar.open(`Duplicate record exist!`, 'Ok!', {
            duration: AppConstants.HIDE_DURATION,
          });
        }
      }
      }
      else {
        if (isMultipleMarketAllowed) {
          this.snackBar.open(`Not more than three markets`, 'Ok!', {
            duration: AppConstants.HIDE_DURATION,
          });
        } else {
          this.snackBar.open(`Not applicable for this sports`, 'Ok!', {
            duration: AppConstants.HIDE_DURATION,
          });
        }
      }
    }
  }

  /**
   * Clear Row data after adding market in market switcher table
   */
  clearRowData(): void {
    this.marketName = '';
    this.displayName = '';
  }

  /**
   * 
   * @param marketName 
   * @param displayName 
   * Emit Add Market
   */
  sendAddMarket(marketName, displayName,aggregated): void {
    this.addMarketsToList.emit({
      'templateMarketName': marketName,
      'title': displayName,
      'aggregated': aggregated
    });
    this.clearRowData();
  }

  /**
 * 
 * @param marketName 
 * @param displayName 
 * Emit Add Market
 */
  sendAddNewByb(rowData, type): void {
    let locationIds: any = [];
    let savedData: any = [];
    this.competionList1.forEach(val => {
      if (rowData.locations.includes(val.id)) {
        locationIds.push(val.id);
      }
    })
    rowData.locations = locationIds;
    let savedDataObj = {
      'title': rowData.title,
      'eventId': rowData.eventId,
      'marketId': rowData.marketId,
      'displayFrom': rowData.displayFrom,
      'displayTo': rowData.displayTo,
      'locations': rowData.locations,
      'fromTime': rowData.fromTime,
      'toTime': rowData.toTime,
      id: rowData.id,
      type: type,
      sortOrder: rowData.sortOrder,
      'todateChange': rowData.todateChange,
      'fromdateChange': rowData.fromdateChange,
      toSeconds:rowData.toSeconds,
      fromSeconds:rowData.fromSeconds


    };
    savedData.push(savedDataObj)
    this.addNewBybToList.emit({ data: savedData, type: 0 });
    this.clearRowData();
  }

  addRow(type: any) {
    this.showtoolTip = [];
    let saveddata: any = this.expandedDetails.filter(val => !val.saved);
    if (type == 0) {
      this.showaddButton = false;
    }
    this.addList.emit({ data: saveddata, type: type });
  }

  showtoolTip: any = [];
  getCheckList(rowData: any) {
    this.showtoolTip = [];
    this.showtoolTip = this.competionList1.filter(list => rowData.locations.includes(list.id)).map(values => values.name)
  }

  getdata(data, eve: any, type) {
    let date = new Date();
    if (type == 'to') {
      let datee: any = new Date().toISOString().split('T');
      data['toTime'] = datee[1];
      data['todateChange'] = true;
      data['toSeconds'] = date.getSeconds() < 10 ? '0' + date.getSeconds().toString() : date.getSeconds().toString();
    } else {
      let datee: any = new Date().toISOString().split('T');
      data['fromTime'] = datee[1];
      data['fromdateChange'] = true;
      data['fromSeconds'] = date.getSeconds() < 10 ? '0' + date.getSeconds().toString() : date.getSeconds().toString();
    }
  }

  setDayTime(rowData) {
    const date = new Date(rowData.displayFrom1);
    const date1 = new Date(rowData.displayTo1)
    rowData.displayFrom = this.fromdateSelection(date);
    rowData.displayTo = this.fromdateSelection(date1);
  }

  fromdateSelection(date: Date): string {
    const year = date.getFullYear();
    const month = this.pad(date.getMonth() + 1);
    const day = this.pad(date.getDate());
    const hours = this.pad(date.getHours());
    const minutes = this.pad(date.getMinutes());
    return `${year}-${+(month) < 10 ? '0' + month : month}-${+(day) < 10 ? '0' + day : day}T${+(hours) < 10 ? '0' + hours : hours}:${+(minutes) < 10 ? '0' + minutes : minutes}`;
  }

  pad(n: number) {
    return n < 0 ? '0' + n : '' + n;
  }



}
