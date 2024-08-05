import {Component, OnInit} from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import {HttpResponse} from '@angular/common/http';

import {DialogService} from '../../../shared/dialog/dialog.service';
import {BybAPIService} from '../../service/byb.api.service';
import {BYBSwitcher} from '../../../client/private/models';
import {BYBSwitchersCreateComponent} from '../byb-switchers-create/byb-switchers-create.component';
import {AppConstants} from '../../../app.constants';
import {DataTableColumn} from '../../../client/private/models/dataTableColumn';
import {ActiveInactiveExpired} from '../../../client/private/models/activeInactiveExpired.model';
import {Router} from '@angular/router';
import {Order} from '../../../client/private/models/order.model';

@Component({
  selector: 'byb-switchers-list',
  templateUrl: './byb-switchers-list.component.html',
  styleUrls: ['./byb-switchers-list.component.scss']
})
export class BYBSwitchersListComponent implements OnInit {
  switchersData: Array<BYBSwitcher>;
  getDataError: string;
  searchField: string = '';
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Switcher Title',
      property: 'name',
      link: {
        hrefProperty: 'id'
      },
      type: 'link'
    },
    {
      name: 'Provider',
      property: 'provider'
    },
    {
      name: 'Default',
      property: 'default',
      type: 'boolean'
    },
    {
      name: 'Enabled',
      property: 'enabled',
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
    private bybSwitchersService: BybAPIService,
    private router: Router
  ) {
  }

  get switchersAmount(): ActiveInactiveExpired {
    const activeSwitchers = this.switchersData && this.switchersData.filter(switcher => switcher.enabled);
    const activeSwitchersAmount = activeSwitchers && activeSwitchers.length;
    const inactiveSwitchersAmount = this.switchersData.length - activeSwitchersAmount;

    return {
      active: activeSwitchersAmount,
      inactive: inactiveSwitchersAmount
    };
  }

  ngOnInit(): void {
    this.bybSwitchersService.getSwitchersList()
      .subscribe((data: any) => {
        this.switchersData = data.body;
      }, error => {
        this.getDataError = error.message;
      });
  }

  public createSwitcher(): void {
    const dialogRef = this.dialog.open(BYBSwitchersCreateComponent, {
      width: '700px',
      data: {}
    });

    dialogRef.afterClosed().subscribe(newSwitcher => {
      if (newSwitcher) {
        this.bybSwitchersService.createSwitcher(newSwitcher)
          .map((bybSwitcher: HttpResponse<BYBSwitcher>) => {
            return bybSwitcher.body;
          })
          .subscribe((bybSwitcher: BYBSwitcher) => {
            if (bybSwitcher) {
              this.switchersData.push(bybSwitcher);
              this.router.navigate([`/byb/byb-switchers/${bybSwitcher.id}`]);
            }
          });
      }
    });
  }

  /**
   * handle deleting Switcher
   * @param {BYBSwitcher} Switcher
   */
  public removeSwitcher(switcher: BYBSwitcher): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove BYB Switcher',
      message: 'Are You Sure You Want to Remove Switcher?',
      yesCallback: () => {
        this.sendRemoveRequest(switcher);
      }
    });
  }

  /**
   * Send DELETE API request
   * @param {BYBSwitcher} Switcher
   */
  public sendRemoveRequest(switcher: BYBSwitcher): void {
    this.bybSwitchersService.deleteSwitcher(switcher.id)
      .subscribe((data: any) => {
        this.switchersData.splice(this.switchersData.indexOf(switcher), 1);
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'BYB Switcher is Removed.'
        });
      });
  }

  public reorderHandler(newOrder: Order): void {

    this.bybSwitchersService.postNewSwitchersOrder(newOrder)
      .subscribe(() => {
        this.snackBar.open('BYB Switchers Order Saved!', 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }
}
