import {Component, OnInit} from '@angular/core';
import {HttpResponse} from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';
import {Router} from '@angular/router';

import {DialogService} from '../../../shared/dialog/dialog.service';
import {ApiClientService} from '../../../client/private/services/http';
import {GlobalLoaderService} from '../../../shared/globalLoader/loader.service';
import {Football3DBanner} from '../../../client/private/models/football3dbanner.model';
import {BannersCreateComponent} from '../banners-create/banners-create.component';
import {AppConstants} from '../../../app.constants';
import {ActiveInactiveExpired} from '../../../client/private/models/activeInactiveExpired.model';
import {Order} from '../../../client/private/models/order.model';

@Component({
  selector: 'app-banners-list',
  templateUrl: './banners-list.component.html',
  styleUrls: ['./banners-list.component.scss']
})
export class BannersListComponent implements OnInit {

  public isLoading: boolean = false;
  public searchField: string = '';
  public banners: Football3DBanner[] = [];
  searchableProperties: string[] = [
    'name',
    'description'
  ];
  dataTableColumns: any[] = [
    {
      name: 'Name',
      property: 'name',
      link: {
        hrefProperty: 'id'
      },
      type: 'link'
    },
    {
      name: 'Description',
      property: 'description'
    },
    {
      name: 'Validity Period Start',
      property: 'validityPeriodStart',
      type: 'date'
    },
    {
      name: 'Validity Period End',
      property: 'validityPeriodEnd',
      type: 'date'
    }
  ];

  constructor(
    private snackBar: MatSnackBar,
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService,
    private router: Router,
  ) {
  }

  ngOnInit() {
    this.showHideSpinner();
    this.apiClientService
        .footballBannersService()
        .getFootball3DFootball3DBanners()
        .map((banners: HttpResponse<Football3DBanner[]>) => {
          return banners.body;
        }).subscribe((banners: Football3DBanner[]) => {
          this.banners = banners;
          this.showHideSpinner(false);
        }, () => {
          this.showHideSpinner(false);
        });
  }

  get bannersAmount(): ActiveInactiveExpired {
    const activePromos = this.banners && this.banners.filter(banner => banner.disabled === false);
    const activePromosAmount = activePromos && activePromos.length;
    const inactivePromosAmount = this.banners.length - activePromosAmount;

    return {
      active: activePromosAmount,
      inactive: inactivePromosAmount
    };
  }

  public reorderHandler(newOrder: Order): void {

    this.apiClientService
        .footballBannersService()
        .postNewFootball3DBannersOrder(newOrder)
        .subscribe(() => {
      this.snackBar.open('Football 3D Banners Order Saved!!', 'Ok!', {
        duration: AppConstants.HIDE_DURATION,
      });
    });
  }

  public createFootballBanner(): void {
    this.dialogService.showCustomDialog(BannersCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add New Football 3D Banner',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (football3DBanner: Football3DBanner) => {
        this.apiClientService.footballBannersService()
            .postNewFootball3DBanner(football3DBanner)
            .map((result: HttpResponse<Football3DBanner>) => {
              return result.body;
            })
            .subscribe((result: Football3DBanner) => {
              this.banners.push(result);
              this.router.navigate([`/banners/football-banners/${result.id}`]);
            }, () => {
              console.error('Can not create football 3d banners');
            });
      }
    });
  }

  public removeFootballBanner(banner: Football3DBanner): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove Football 3D Banner',
      message: 'Are You Sure You Want to Remove Football 3D Banner?',
      yesCallback: () => {
        this.banners = this.banners.filter((l) => {
          return l.id !== banner.id;
        });
        this.apiClientService.footballBannersService().deleteFootball3DBanner(banner.id).subscribe(() => {
          this.dialogService.showNotificationDialog({
            title: 'Remove Completed',
            message: 'Football 3D Banner is Removed.'
          });
        });
      }
    });
  }

  private showHideSpinner(toShow: boolean = true): void {
    toShow ? this.globalLoaderService.showLoader() : this.globalLoaderService.hideLoader();
    this.isLoading = toShow;
  }

}
