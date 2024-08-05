import { Component, OnInit } from '@angular/core';
import { DataTableColumn } from '@root/app/client/private/models';
import { ApiClientService } from '@root/app/client/private/services/http';
import { SignpostingConstants } from '@root/app/signposting/constants/signposting.constants';
import { SignpostingInfo } from '@root/app/signposting/models/signposting.model';
import { GlobalLoaderService } from '@root/app/shared/globalLoader/loader.service';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AppConstants } from '@root/app/app.constants';

@Component({
  selector: 'app-freebet-signposting-list',
  templateUrl: './freebet-signposting-list.component.html',
  styleUrls: ['./freebet-signposting-list.component.scss']
})
export class FreebetSignpostingListComponent implements OnInit {

  public signpostingConstants: any = SignpostingConstants;
  public isLoading: boolean = false;
  public signpostData: SignpostingInfo[] = [];
  public searchField: string = '';
  public searchableProperties: string[] = [
    'title',
  ];
  public dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Title',
      property: 'title',
      link: {
        hrefProperty: 'id'
      },
      type: 'link',
    },
    {
      name: 'Enabled',
      property: 'isActive',
    }
  ];

  /**
   * Constructor
   * @param apiClientService : ApiClientService
   * @param globalLoaderService : GlobalLoaderService
   * @param snackBar : MatSnackBar
   * @param dialogService : DialogService
  */
  constructor(private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private snackBar: MatSnackBar,
    private dialogService: DialogService) { }

  /**
   * ngOnInit
  */
  ngOnInit(): void {
    this.loadSignpostingRecords();
  }

  /**
   * Load signposting records on load
   * @returns - {void}
  */
  private loadSignpostingRecords(): void {
    this.showHideSpinner();
    this.apiClientService.freebetSignpostingService().getAllSignpostings().map((response: any) => response.body).subscribe(res => {
      this.signpostData = res;
      this.showHideSpinner(false);
    }, error => {
      this.showHideSpinner(false);
      this.errorNotify(error);
    });
  }

  /**
   * Delete confirmation
   * @param signpostingData : SignpostingInfo
   * @returns - {void}
  */
  public removeSignposting(signpostingData: SignpostingInfo): void {
    this.dialogService.showConfirmDialog({
      title: `Remove Signposting`,
      message: `Are you sure you want to remove the signposting?`,
      yesCallback: () => {
        this.removeRequest(signpostingData);
      }
    });
  }

  /**
   * Service call to delete signposting
   * @param signpostingData : SignpostingInfo
   * @returns - {void}
  */
  private removeRequest(signpostingData: SignpostingInfo): void {
    this.showHideSpinner(true);
    this.apiClientService.freebetSignpostingService().deleteSignposting(signpostingData.id).subscribe((res) => {
      if (res) {
        this.loadSignpostingRecords();
        this.showHideSpinner(false);
        this.snackBar.open('Signposting is Removed!', 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      }
    }, error => {
      this.showHideSpinner(false);
      this.errorNotify(error);
    });
  }

  /**
   * Error notification
   * @returns - {void}
  */
  private errorNotify(error: any): void {
    this.dialogService.showNotificationDialog({
      title: 'Error',
      message: JSON.stringify(error)
    });
  }

  /**
   * To show or hide spinner
   * @param {boolean} toShow
   * @returns - {void}
  */
  private showHideSpinner(toShow: boolean = true): void {
    toShow ? this.globalLoaderService.showLoader() : this.globalLoaderService.hideLoader();
    this.isLoading = toShow;
  }
}
