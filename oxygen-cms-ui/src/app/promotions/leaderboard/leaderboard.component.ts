import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpResponse } from '@angular/common/http';
import { ApiClientService } from '@app/client/private/services/http';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { TableColumn } from '@app/client/private/models/table.column.model';
import { PromotionsLeaderboard } from '@app/client/private/models/promotions-leaderboard.model';

@Component({
  selector: 'app-leaderboard',
  templateUrl: './leaderboard.component.html',
  styleUrls: ['./leaderboard.component.scss']
})

export class LeaderboardComponent implements OnInit {
  public searchField: string = '';
  public leaderboard: [];
  public isLoading: boolean = false;
  public leaderboards: PromotionsLeaderboard[];
  filterProperties: Array<string> = [
    'name'
  ];
  dataTableColumns: Array<TableColumn> = [
    {
      name: 'Name',
      property: 'name',
      link: {
        hrefProperty: 'id',
        path: '/promotions/leaderboard/'
      },
      type: 'link'
    },
    {
      name: 'Nav group IDs',
      property: 'navGIds'
    },
    {
      name: 'Last Updated At',
      property: 'updatedAt',
      type: 'date'
    },
    {
      name: 'Enabled',
      property: 'status',
      type: 'boolean'
    }
  ];
  constructor(
    public router: Router,
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService
  ) { }

  ngOnInit(): void {
    this.globalLoaderService.showLoader();
    this.isLoading = true;
    this.apiClientService
      .promotionLeaderboardService()
      .findAllByBrand()
      .finally(() => {
        this.hideSpinner();
      })
      .map((data: HttpResponse<PromotionsLeaderboard[]>) => {
        return data.body;
      }).subscribe((leaderboard: PromotionsLeaderboard[]) => {
        this.leaderboards = leaderboard;
      });
  }

  /**
  * Remove leaderboard
  * @param - {PromotionsLeaderboard} leaderboard
  * @returns - {void}
  */
  removeLeaderboard(leaderboard: PromotionsLeaderboard): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove Static Block',
      message: `Are You Sure You Want to Remove Leaderboard ${leaderboard.name}`,
      yesCallback: () => {
        this.apiClientService
          .promotionLeaderboardService()
          .remove(leaderboard.id)
          .subscribe(() => {
            this.leaderboards.splice(this.leaderboards.indexOf(leaderboard), 1);
            this.dialogService.showNotificationDialog({
              title: 'Remove Completed',
              message: 'Leaderboard is Removed.'
            });
          });
      }
    });
  }

  private hideSpinner(): void {
    this.isLoading = false;
    this.globalLoaderService.hideLoader();
  }
}
