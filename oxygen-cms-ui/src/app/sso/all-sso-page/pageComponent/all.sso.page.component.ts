import {Component, OnInit} from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {CSVGeneratorService} from '@app/client/private/services/csv.generator.service';
import {SsoCreateComponent} from '../createSsoDialog/sso.create.component';
import {SsoApiService} from '../../service/sso.api.service';
import {SsoPage} from '@app/client/private/models/ssopage.model';
import {AppConstants} from '@app/app.constants';
import {DataTableColumn} from '@app/client/private/models/dataTableColumn';
import {ActiveInactiveExpired} from '@app/client/private/models/activeInactiveExpired.model';
import {Router} from '@angular/router';
import {Order} from '@app/client/private/models/order.model';

@Component({
  selector: 'all-sso-page',
  templateUrl: './all.sso.page.component.html',
  styleUrls: ['./all.sso.page.component.scss'],
  providers: [
    CSVGeneratorService
  ]
})
export class AllSsoPageComponent implements OnInit {
  ssoPagesData: Array<SsoPage>;
  getDataError: string;
  searchField: string = '';
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Title',
      property: 'title',
      link: {
        hrefProperty: 'id'
      },
      type: 'link'
    },
    {
      name: 'Open Link',
      property: 'openLink'
    },
    {
      name: 'Show on IOS',
      property: 'showOnIOS',
      type: 'boolean'
    },
    {
      name: 'Show on Android',
      property: 'showOnAndroid',
      type: 'boolean'
    },
    {
      name: 'Target IOS',
      property: 'targetIOS'
    },
    {
      name: 'Target Android',
      property: 'targetAndroid'
    }
  ];

  searchableProperties: Array<string> = [
    'title',
    'openLink'
  ];

  constructor(
    public snackBar: MatSnackBar,
    private dialogService: DialogService,
    private dialog: MatDialog,
    private ssoApiService: SsoApiService,
    private router: Router
  ) {}

  /**
   * Create new SSO page.
   */
  createSsoPage(): void {
    const dialogRef = this.dialog.open(SsoCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      data: {
        ssoData: this.ssoPagesData
      }
    });

    dialogRef.afterClosed().subscribe(newSsoPage => {
      if (newSsoPage) {
        this.ssoApiService.postNewSsoPage(newSsoPage)
          .map(data => data.body)
          .subscribe((page: SsoPage) => {
            if (page) {
              this.ssoPagesData.push(page);
              this.router.navigate([`/sso-page/${page.id}`]);
            }
          });
      }
    });
  }

  /**
   * Het amount of Active/Inactive elements.
   * @return {{active:number, inactive:number}}
   */
  get ssoPagesAmount(): ActiveInactiveExpired {
    const activePromos = this.ssoPagesData && this.ssoPagesData.filter(ssoPage => ssoPage.disabled === false);
    const activePromosAmount = activePromos && activePromos.length;
    const inactivePromosAmount = this.ssoPagesData.length - activePromosAmount;

    return {
      active: activePromosAmount,
      inactive: inactivePromosAmount
    };
  }

  /**
   * handle deleting ssoPage
   * @param {SsoPage} ssoPage
   */
  removeHandler(ssoPage: SsoPage) {
    this.dialogService.showConfirmDialog({
      title: 'Remove SsoPage',
      message: 'Are You Sure You Want to Remove ssoPage?',
      yesCallback: () => {
        this.sendRemoveRequest(ssoPage);
      }
    });
  }

  /**
   * Send DELETE API request
   * @param {SsoPage} ssoPage
   */
  sendRemoveRequest(ssoPage: SsoPage) {
    this.ssoApiService.deleteSsoPage(ssoPage.id)
      .subscribe((data: any) => {
        this.ssoPagesData.splice(this.ssoPagesData.indexOf(ssoPage), 1);
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'SsoPage is Removed.'
        });
      });
  }


  /**
   * Handle reorder of data items.
   */
  reorderHandler(newOrder: Order) {

    this.ssoApiService.postNewSsoPagesOrder(newOrder)
      .subscribe((data: any) => {
        this.snackBar.open('NEW SSO PAGES ORDER SAVED!!', 'OK!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }

  ngOnInit() {
    this.ssoApiService.getSsoPagesData()
      .map(data => data.body)
      .subscribe((data: SsoPage[]) => {
        this.ssoPagesData = data;
      }, error => {
        this.getDataError = error.message;
      });
  }
}
