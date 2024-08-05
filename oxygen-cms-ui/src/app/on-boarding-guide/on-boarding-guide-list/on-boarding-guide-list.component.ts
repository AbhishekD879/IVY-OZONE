import {Component, OnInit} from '@angular/core';
import {DataTableColumn} from '@app/client/private/models/dataTableColumn';
import {OnBoardingGuide} from '@app/client/private/models/onBoardingGuide';
import {ApiClientService} from '@app/client/private/services/http';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {Router} from '@angular/router';
import {ActiveInactiveExpired} from '@app/client/private/models/activeInactiveExpired.model';
import {Order} from '@app/client/private/models/order.model';
import {AppConstants} from '@app/app.constants';
import { MatSnackBar } from '@angular/material/snack-bar';
import {HttpResponse} from '@angular/common/http';
import {OnBoardingGuideCreateComponent} from '@app/on-boarding-guide/on-boarding-guide-create/on-boarding-guide-create.component';

@Component({
  selector: 'app-on-boarding-guide-list',
  templateUrl: './on-boarding-guide-list.component.html'
})
export class OnBoardingGuideListComponent implements OnInit {
  onBoardingGuide: Array<OnBoardingGuide>;
  getDataError: string;
  searchField: string = '';
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Name',
      property: 'guideName',
      link: {
        hrefProperty: 'id'
      },
      type: 'link'
    },
    {
      name: 'Path',
      property: 'guidePath',
      width: 3
    },
    {
      name: 'Enabled',
      property: 'enabled',
      type: 'boolean'
    }
  ];

  filterProperties: Array<string> = [
    'guideName'
  ];

  constructor(
    public snackBar: MatSnackBar,
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService,
    public router: Router
  ) { }

  ngOnInit(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.onBoardingGuide()
      .getOnBoardingGuides()
      .map((data: any) => {
        return data.body;
      })
      .subscribe((data: OnBoardingGuide[]) => {
        this.onBoardingGuide = data;
        this.globalLoaderService.hideLoader();
      }, (error) => {
        this.onBoardingGuide = [];
        this.globalLoaderService.hideLoader();
      });
  }

  createOnBoardingGuide() {
    this.dialogService.showCustomDialog(OnBoardingGuideCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add On Boarding Guide',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (onBoardingGuide: OnBoardingGuide) => {
        this.globalLoaderService.showLoader();
        this.apiClientService.onBoardingGuide()
          .postNewOnBoardingGuide(onBoardingGuide)
          .map((response: HttpResponse<OnBoardingGuide>) => {
            return response.body;
          })
          .subscribe((data: OnBoardingGuide) => {
            this.onBoardingGuide.push(data);
            this.globalLoaderService.hideLoader();
            this.router.navigate([`/on-boarding-guide/${data.id}`]);
          }, error => {
            console.error(error.message);
            this.globalLoaderService.hideLoader();
          });
      }
    });
  }

  get onBoardingGuideAmount(): ActiveInactiveExpired {
    const onBoardingGuides = this.onBoardingGuide && this.onBoardingGuide.filter(obg => obg.enabled === true);
    const onBoardingGuideAmount = onBoardingGuides && onBoardingGuides.length;
    const inactiveOnBoardingGuideAmountAmount = this.onBoardingGuide.length - onBoardingGuideAmount;

    return {
      active: onBoardingGuideAmount,
      inactive: inactiveOnBoardingGuideAmountAmount
    };
  }

  removeOnBoardingGuide(onBoardingGuide: OnBoardingGuide) {
    this.dialogService.showConfirmDialog({
      title: 'Remove On Boarding Guide',
      message: 'Are You Sure You Want to Remove On Boarding Guide?',
      yesCallback: () => {
        this.sendRemoveRequest(onBoardingGuide);
      }
    });
  }

  sendRemoveRequest(onBoardingGuide: OnBoardingGuide) {
    this.apiClientService.onBoardingGuide().deleteOnBoardingGuide(onBoardingGuide.id)
      .subscribe((data: any) => {
        this.onBoardingGuide.splice(this.onBoardingGuide.indexOf(onBoardingGuide), 1);
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'On Boarding Guide is Removed.'
        });
      });
  }

  reorderHandler(newOrder: Order) {

    this.apiClientService.onBoardingGuide().postNewOnBoardingGuideOrder(newOrder)
      .subscribe((data: any) => {
        this.snackBar.open('New On Boarding Guide Order Saved!!', 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
      });
  }

}
