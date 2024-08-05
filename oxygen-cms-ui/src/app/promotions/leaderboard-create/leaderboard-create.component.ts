import { AfterContentInit, AfterViewInit, Component, OnInit } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import { Router } from '@angular/router';
import { FormControl, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { BrandService } from '@app/client/private/services/brand.service';
import { SortableTableService } from '@app/client/private/services/sortable.table.service';
import { ApiClientService } from '@app/client/private/services/http/index';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { Leaderboard, ColumnsConfig, PromoLeaderboard } from '@app/client/private/models/promotions-leaderboard.model';
import { AppConstants } from '@app/app.constants';
import * as _ from 'lodash';

@Component({
  selector: 'app-leaderboard',
  templateUrl: './leaderboard-create.component.html',
  styleUrls: ['./leaderboard-create.component.scss'],
  providers: [SortableTableService]
})

export class LeaderboardCreateComponent implements OnInit, AfterContentInit, AfterViewInit {

  public breadcrumbsData: Breadcrumb[];
  isDisabledBtn: boolean = false;
  uploadBtn: boolean = true;
  tableUniqueClass: string = _.uniqueId('reorder_');
  id: string;
  styleArray = [
    { id: `leaderBoard-col-font-default-${this.brandService.brand}`, value: 'Default' },
    { id: 'leaderBoard-col-font-normal', value: 'Normal' },
    { id: 'leaderBoard-col-normal-background', value: 'Normal Font with Background' },
    { id: 'leaderBoard-col-font-bold', value: 'Bold Font' },
    { id: 'leaderBoard-col-bold-background', value: 'Bold Font with Background' },
  ];
  leaderboard: Leaderboard = {} as Leaderboard;
  columnsData: ColumnsConfig[] = [];
  name: FormControl;
  csvFile = new FormData();
  constructor(
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService,
    private router: Router,
    private brandService: BrandService,
    private snackBar: MatSnackBar,
    protected sortableTableService: SortableTableService
  ) {
    this.name = new FormControl('', [Validators.required]);
  }

  ngOnInit(): void {
    this.breadcrumbsData = [{
      label: `Leaderboard`,
      url: `/promotions/leaderboard`
    }, {
      label: 'Create Leaderboard',
      url: `/promotions/createLeaderboard/`
    }];
    this.leaderboard.columns = this.columnsData;
    this.leaderboard.brand = this.brandService.brand;
    this.leaderboard.topX =  "";
    this.uploadBtn = false;
  }

  ngAfterContentInit() {
    this.addReorderingToTable();
  }

  ngAfterViewInit() {
    this.addReorderingToTable();
  }

   /**
   * Add drag-n-drop reorder functionality to table
   * @returns - void
   */
  addReorderingToTable(): void {
    const self = this;
    this.sortableTableService.addSorting({
      dataToReorder: self.leaderboard?.columns,
      mainSelector: `.custom-table.${self.tableUniqueClass} tbody`,
      handlerSelector: '.drag-handler',
      onReorderEnd(data, indexOfDraggedElement) {
        const newOrder = {
          order: self.leaderboard.columns.map(element => element.originalName),
          id: self.leaderboard.columns[indexOfDraggedElement].originalName
        };
        self.reorderHandler(newOrder.order);
      }
    });
  }

  /**
   * Reorder leaderboard colums
   * @param - {string[]} newOrder
   * @returns - void
   */
  reorderHandler(newOrder): void {
    console.log('$$newoder', newOrder);
  }

  /**
  * Add new line item to Navigation childs
  * @param - null
  * @returns - void
  */
  addLeaderboardColumns(): void {
    if (this.leaderboard && this.leaderboard.columns && this.leaderboard?.columns.length >= 5) {
      this.dialogService.showNotificationDialog({
        title: `Columns Configuration`,
        message: `Maximum number of Columns Data that can be added is 5`
      })
    } else {
      this.leaderboard?.columns.push(new ColumnsConfig());
    }
  }

  /**
  * Remove the column item
  * @param - {number} i
  * @returns - void
  */
  removeColumnItem(i: number): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove Static Block',
      message: `Are you sure you want to remove this column`,
      yesCallback: () => {
        this.leaderboard.columns.splice(i, 1);
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'Column is Removed.'
        });
      }
    });
  }

  /**
  * Save all Columns Details 
  * @returns boolean
  */
  savecolumnsDetails(): boolean {
    let isValid = true;
    const occurrences = {};
    this.leaderboard.columns.find(col => {
      if (!col.originalName) {
        this.dialogService.showNotificationDialog({
          title: 'Column Config table',
          message: 'Please fill all the required columns in table'
        });
        isValid = false;
      } else if (occurrences[col.originalName]) {
        this.dialogService.showNotificationDialog({
          title: 'Column Config table',
          message: 'two colums having same original Name'
        });
        isValid = false;
      }
      occurrences[col.originalName] = true;
    })
    return isValid;

  }

  /**
  * Save LeaderboardChanges
  * @returns - void
  */
  saveLeaderboardChanges(): void {
    if (this.savecolumnsDetails()) {
      this.globalLoaderService.showLoader();
      this.apiClientService.promotionLeaderboardService().
        postNewLeaderboard(this.leaderboard)
        .map((leaderboard: HttpResponse<PromoLeaderboard>) => {
          return leaderboard.body;
        }).subscribe((data: PromoLeaderboard) => {
          this.globalLoaderService.hideLoader();
          this.leaderboard = data;
          this.id = data.id;
          this.finishLeaderboardCreation();
        })
    }
  }

  /**
 * Show the message on saving the Leaderboard
 * @returns - void
 */
  finishLeaderboardCreation(): void {
    const self = this;
    this.dialogService.showNotificationDialog({
      title: 'Save Completed',
      message: 'Leaderboard is Created and Stored.',
      closeCallback() {
        self.router.navigate([`promotions/leaderboard/${self.id}`]);
      }
    });
  }

  /**
   * Validate input with type of number to enter 
   * the number less than 999 and greator than 0
   * @returns boolean
   */
  validateMinandMaxValue(): boolean {
    return (this.leaderboard.topX <= 99) ? true : false;
  }

  /**
   * Updates topX value to 1 when entered 0
   * @returns boolean
   */
  updateTopXValue(): void {
    if (this.leaderboard.topX == 0) {
      this.leaderboard.topX = 1;
    } else if (this.leaderboard.topX < 0) {
      this.leaderboard.topX = this.leaderboard.topX * -1;
    }
  }
  
  /**
   * Validate uploaded file
   * @returns null
   */
  prepareToUploadFile(event): void {
    const file = event.target.files[0];
    const fileType = file.type;
    const supportedTypes = ['xlsx','xls','text/csv'];

    if (supportedTypes.indexOf(fileType) === -1) {
      this.dialogService.showNotificationDialog({
        title: 'Error. Unsupported file type.',
        message: 'Supported \"csv\".'
      });

      return;
    }
    this.uploadBtn = true;
    this.leaderboard.filePath = file.name;
    this.csvFile =  new FormData();
    this.csvFile.append('file', file);
  }

  /**
   * Validation for upload button
   * @returns boolean
   */
  checkValidity(): boolean {
    return this.leaderboard.filePath && this.uploadBtn;
  }

  /**
   * Input file 
   * @returns null
   */
  handleFileUpload(event) {
    const input = event.target.previousElementSibling.querySelector('input');
    input.click();
  }

  /**
   * Uploads file
   * @returns null
   */
  uploadFile() {
    this.globalLoaderService.showLoader();
    this.apiClientService.promotionLeaderboardService()
        .uploadCSVFile(this.csvFile)
        .subscribe(() => {
          this.globalLoaderService.hideLoader();
          this.snackBar.open('File Was Uploaded.', 'Ok!', {
            duration: AppConstants.HIDE_DURATION,
          });
        });
    this.uploadBtn = false;
  }
  
  /**
  * check if the form is valid
  * @returns boolean
  */
  public isValidForm(): boolean {
    return this.leaderboard && this.leaderboard.columns && this.leaderboard.columns.length > 0 && this.leaderboard?.name && this.leaderboard?.filePath?.length > 0;
  }
}
