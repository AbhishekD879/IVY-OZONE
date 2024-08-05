import { Component, OnInit } from '@angular/core';
import { DataTableColumn } from '@root/app/client/private/models';
import { ApiClientService } from '@app/client/private/services/http';
import { TopSportsConstants } from '@root/app/virtual-sports/top-sports/constants/top-sports.constants';
import { TopSportsInfo } from '@root/app/virtual-sports/top-sports/models/top-sports.model';
import { GlobalLoaderService } from '@root/app/shared/globalLoader/loader.service';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AppConstants } from '@root/app/app.constants';


@Component({
  selector: 'app-top-sports-list',
  templateUrl: './top-sports-list.component.html',
  styleUrls: ['./top-sports-list.component.scss']
})

export class TopSportsListComponent implements OnInit {

  public topSportsConstants: any = TopSportsConstants;
  public isLoading: boolean = false;
  public topSportsData: TopSportsInfo[] = [];
  public searchField: string = '';
  public searchableProperties: string[] = [
    'sportsName',
  ];
  public dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Title',
      property: 'sportsName',
      link: {
        hrefProperty: 'id'
      },
      type: 'link',
    },
    {
      name: 'Enabled',
      property: 'isTopSports',
    }
  ];

  /**
   * Constructor
   * @param apiClientService: ApiClientService
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
    this.loadTopSportsRecords();
  }

  /**
   * Load topSports records on load
   * @returns - {void}
  */
  private loadTopSportsRecords(): void {
    this.showHideSpinner();
    this.apiClientService.virtualHubTopSportsService().getAllTopSports().map((response: any) => response.body).subscribe(res => {
      this.topSportsData = res;
      this.showHideSpinner(false);
    }, error => {
      this.showHideSpinner(false);
      this.errorNotify(error);
    });
  }

  /**
   * Delete confirmation
   * @param topSportsInfo : TopSportsInfo
   * @returns - {void}
  */
  public removetopSports(topSportsData: TopSportsInfo): void {
    this.dialogService.showConfirmDialog({
      title: `Remove top sport`,
      message: `Are you sure you want to remove the top sport?`,
      yesCallback: () => {
        this.removeRequest(topSportsData);
      }
    });
  }

  /**
   * Service call to delete topSports
   * @param topSportsData : TopSportsInfo
   * @returns - {void}
  */
  private removeRequest(topSportsData: TopSportsInfo): void {
    this.showHideSpinner(true);
    this.apiClientService.virtualHubTopSportsService().deleteTopSports(topSportsData.id).subscribe((res) => {
      if (res) {
        this.loadTopSportsRecords();
        this.showHideSpinner(false);
        this.snackBar.open('topSports is Removed!', 'Ok!', {
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
