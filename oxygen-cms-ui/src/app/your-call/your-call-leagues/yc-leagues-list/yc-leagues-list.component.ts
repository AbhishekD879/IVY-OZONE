import {Component, OnInit} from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import {HttpResponse} from '@angular/common/http';

import {DialogService} from '@app/shared/dialog/dialog.service';
import {YourCallAPIService} from '../../service/your-call.api.service';
import {YourCallLeague} from '../../../client/private/models';
import {YcLeaguesCreateComponent} from '../yc-leagues-create/yc-leagues-create.component';
import {AppConstants} from '@app/app.constants';
import {DataTableColumn} from '@app/client/private/models/dataTableColumn';
import {ActiveInactiveExpired} from '@app/client/private/models/activeInactiveExpired.model';
import {Router} from '@angular/router';
import {Order} from '@app/client/private/models/order.model';

@Component({
  selector: 'yc-leagues-list',
  templateUrl: './yc-leagues-list.component.html',
  styleUrls: ['./yc-leagues-list.component.scss']
})
export class YcLeaguesListComponent implements OnInit {
  leaguesData: Array<YourCallLeague>;
  getDataError: string;
  searchField: string = '';
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'League Title',
      property: 'name',
      link: {
        hrefProperty: 'id'
      },
      type: 'link'
    },
    {
      name: 'Type ID',
      property: 'typeId'
    },
    {
      name: 'Enabled for BYB',
      property: 'enabled',
      type: 'boolean'
    },
    {
      name: 'Enabled for 5 A Side',
      property: 'activeFor5aSide',
      type: 'boolean'
    }
  ];

  filterProperties: Array<string> = [
    'name'
  ];

  constructor(
    public snackBar: MatSnackBar,
    private dialogService: DialogService,
    private dialog: MatDialog,
    private leaguesAPIService: YourCallAPIService,
    private router: Router
  ) {
  }

  get leaguesAmount(): ActiveInactiveExpired {
    const activeLeagues = this.leaguesData && this.leaguesData.filter(league => league.enabled);
    const activeLeaguesAmount = activeLeagues && activeLeagues.length;
    const inactiveLeaguesAmount = this.leaguesData.length - activeLeaguesAmount;

    return {
      active: activeLeaguesAmount,
      inactive: inactiveLeaguesAmount
    };
  }

  ngOnInit(): void {
    this.leaguesAPIService.getLeaguesList()
      .subscribe((data: any) => {
        this.leaguesData = data.body;
      }, error => {
        this.getDataError = error.message;
      });
  }

  createLeague(): void {
    const dialogRef = this.dialog.open(YcLeaguesCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      data: {}
    });

    dialogRef.afterClosed().subscribe(newLeague => {
      if (newLeague) {
        this.leaguesAPIService.createLeague(newLeague)
          .map((yourCallLeague: HttpResponse<YourCallLeague>) => {
            return yourCallLeague.body;
          })
          .subscribe((yourCallLeague: YourCallLeague) => {
            if (yourCallLeague) {
              this.leaguesData.push(yourCallLeague);
              this.router.navigate([`/yc/yc-leagues/${yourCallLeague.id}`]);
            }
          });
      }
    });
  }

  /**
   * handle deleting league
   * @param {YourCallLeague} league
   */
  removeLeague(league: YourCallLeague): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove YourCall League',
      message: 'Are You Sure You Want to Remove YourCall League?',
      yesCallback: () => {
        this.sendRemoveRequest(league);
      }
    });
  }

  /**
   * Send DELETE API request
   * @param {YourCallLeague} league
   */
  sendRemoveRequest(league: YourCallLeague): void {
    this.leaguesAPIService.deleteLeague(league.id)
      .subscribe((data: any) => {
        this.leaguesData.splice(this.leaguesData.indexOf(league), 1);
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'YourCall League is Removed.'
        });
      });
  }

  reorderHandler(newOrder: Order): void {
    this.leaguesAPIService.postNewLeaguesOrder(newOrder)
      .subscribe(() => {
        this.snackBar.open('YourCall Leagues Order Saved!', 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
    });
  }
}
