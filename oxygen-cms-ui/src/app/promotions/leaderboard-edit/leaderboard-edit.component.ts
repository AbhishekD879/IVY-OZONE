import { Component, OnInit, ViewChild, AfterContentInit, AfterViewInit } from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { FormControl, Validators } from '@angular/forms';
import { HttpResponse } from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { SortableTableService } from '@app/client/private/services/sortable.table.service';
import { BrandService } from '@app/client/private/services/brand.service';
import { ApiClientService } from '@app/client/private/services/http/index';
import { ColumnsConfig, Leaderboard, PromoLeaderboard } from '@app/client/private/models/promotions-leaderboard.model';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { ActionButtonsComponent } from '@app/shared/action-buttons/action-buttons.component';
import { AppConstants } from '@app/app.constants';
import * as _ from 'lodash';

@Component({
  selector: 'app-leaderboard',
  templateUrl: './leaderboard-edit.component.html',
  styleUrls: ['./leaderboard-edit.component.scss'],
  providers: [SortableTableService]
})

export class LeaderboardEditComponent implements OnInit, AfterContentInit, AfterViewInit {
  public breadcrumbsData: Breadcrumb[];
  public isLoading: boolean = false;
  isDisabledBtn: boolean = false;
  uploadBtn: boolean = true;
  tableUniqueClass: string = _.uniqueId('reorder_');
  leaderboard: PromoLeaderboard;
  name: FormControl;
  isFileChanged: boolean = false;
  csvFile: FormData;
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;
  styleArray = [
    { id: `leaderBoard-col-font-default-${this.brandService.brand}`, value: 'Default' },
    { id: 'leaderBoard-col-font-normal', value: 'Normal' },
    { id: 'leaderBoard-col-normal-background', value: 'Normal Font with Background' },
    { id: 'leaderBoard-col-font-bold', value: 'Bold Font' },
    { id: 'leaderBoard-col-bold-background', value: 'Bold Font with Background' },
  ];
  constructor(
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService,
    private activatedRoute: ActivatedRoute,
    private dialogService: DialogService,
    private brandService: BrandService,
    private snackBar: MatSnackBar,
    private router: Router,
    protected sortableTableService: SortableTableService
  ) {
    this.isValidForm = this.isValidForm.bind(this);
    this.name = new FormControl('', [Validators.required]);
  }

  ngOnInit(): void {
    this.loadInitData();
    this.addReorderingToTable();
  }

  ngAfterContentInit() {
    this.addReorderingToTable();
  }

  ngAfterViewInit() {
    this.addReorderingToTable();
  }

  /**
  * load Inital Data
  * @param {boolean} isLoading
  * @returns - void
  */
  loadInitData(isLoading: boolean = true): void {
    this.globalLoaderService.showLoader();
    this.isLoading = isLoading;
    this.activatedRoute.params.subscribe((params: Params) => {
      this.apiClientService.promotionLeaderboardService().getLeaderboardById(params['id'])
        .map((leaderboard: HttpResponse<PromoLeaderboard>) => {
          return leaderboard.body;
        })
        .subscribe((data: PromoLeaderboard) => {
          this.leaderboard = data;
          this.uploadBtn = false;
          if (this.leaderboard) {
            Object.assign(this.leaderboard, {
              id: data.id,
              name: data.name,
              status: data.status,
              updatedAt: data.updatedAt
            })
          }
          this.globalLoaderService.hideLoader();
          this.isLoading = false;
          this.breadcrumbsData = [{
            label: `Promotions Leaderboard`,
            url: `/promotions/leaderboard`
          }, {
            label: this.leaderboard.name,
            url: `/promotions/leaderboard/${this.leaderboard.id}`
          }];
          this.addReorderingToTable();
        }, () => {
          this.globalLoaderService.hideLoader();
          this.isLoading = false;
          setTimeout(this.addReorderingToTable, 500);
        });
    });
  }

  /**
  * Add drag-n-drop reorder functionality to table
  */
  addReorderingToTable() {
    const self = this;
    this.sortableTableService.addSorting({
      dataToReorder: self.leaderboard?.columns,
      mainSelector: `.custom-table.${self.tableUniqueClass} tbody`,
      handlerSelector: '.drag-handler',
      onReorderEnd(data, indexOfDraggedElement) {
        const newOrder = {
          order: self.leaderboard.columns.map(element => element),
          id: self.leaderboard.columns[indexOfDraggedElement].originalName
        };
        self.reorderHandler(newOrder.order);
      }
    });
  }

  /**
   * Reorder leaderboard columns
   * @param {ColumnsConfig[]} 
   * @returns - void
   */
  reorderHandler(newOrder: ColumnsConfig[]): void {
    console.log('$$newoder', newOrder);
  }

  /**
   * Leaderbaord form validation
   * @param {Leaderboard} lb
   * @returns boolean
  */
  isValidForm(lb: Leaderboard): boolean {
    return lb && lb.columns && lb.columns.length > 0 && lb.filePath && lb.filePath.length > 0
      && lb.name && lb.filePath.length > 0
  }

  /**
  * Action handler for the action button
  * @param - {event}
  * @returns - void
  */
  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeLeaderboard();
        break;
      case 'save':
        this.saveLeaderboardChanges();
        break;
      case 'revert':
        this.revertLeaderboardChanges();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  /**
  * delete the leaderboard
  * @returns null
  */
  removeLeaderboard(): void {
    this.apiClientService.promotionLeaderboardService().remove(this.leaderboard.id).subscribe(() => {
      this.dialogService.showNotificationDialog({
        title: 'Remove Completed',
        message: 'Leaderboard is Removed.'
      });
      this.router.navigate(['/promotions/leaderboard'])
    });
  }

  /**
   * delete the leaderboard
   * @param - {number} i
   * @returns null
   */
  removeColumnItem(i: number) {
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
   * save the Column COnfiguration details
   * @returns boolean
   */
  saveColumnConfigDetails(): boolean {
    let isValid = true;
    const occurrences = {};
    this.leaderboard.columns.find(col => {
      if (!col.originalName) {
        this.dialogService.showNotificationDialog({
          title: 'Column Config table',
          message: 'Please fill the required columns in table'
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
   * Make PUT request to server to update
   * @returns - void
   */
  saveLeaderboardChanges(): void {
    if (this.saveColumnConfigDetails()) {
      this.globalLoaderService.showLoader();
      this.apiClientService.promotionLeaderboardService().
        updateLeaderboard(this.leaderboard, this.isFileChanged)
        .map((leaderboard: HttpResponse<PromoLeaderboard>) => {
          return leaderboard.body;
        }).subscribe((data: PromoLeaderboard) => {
          this.globalLoaderService.hideLoader();
          this.leaderboard = data;
          this.actionButtons.extendCollection(this.leaderboard);
          this.dialogService.showNotificationDialog({
            title: `Promotions Leaderboard`,
            message: `Promotions Leaderboard is Saved.`,
            closeCallback: () => {
                this.router.navigateByUrl('/', { skipLocationChange: true }).then(() =>
                this.router.navigate([`/promotions/leaderboard/${this.leaderboard.id}`]));
            }
          });
        })
    }
  }

  /**
   * revert the changes 
   * @returns - void
   */
  revertLeaderboardChanges(): void {
    this.loadInitData(false);
  }

  /**
   * updates the value if file is changed 
   * @returns - void
   */
  toggle(event): void {
    this.isFileChanged = event.checked
  }


  /**
   * Add new line item to Navigation childs
   * @param - null
   * @returns - void
   */
  addLeaderboardColumns(): void {
    if (this.leaderboard.columns.length >= 5) {
      this.dialogService.showNotificationDialog({
        title: `Columns Configuration`,
        message: `Maximum number of Columns Data that can be added is 5`
      })
    } else {
      this.leaderboard.columns.push(new ColumnsConfig());
    }
  }

  /**
   * Validate input with type of number to enter 
   * the number less than 999 and reator than 0
   * @returns boolean
   */
  validateMinandMaxValue(): boolean {
    return (this.leaderboard.topX <= 99) ? true : false;
  }

  /**
   * Updates topX value to 1 when entered 0
   * @returns null
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
  handleFileUpload(event): void {
    const input = event.target.previousElementSibling.querySelector('input');
    input.click();
  }

  /**
   * Uploads file
   * @returns null
   */
  uploadFile(): void {
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

}

