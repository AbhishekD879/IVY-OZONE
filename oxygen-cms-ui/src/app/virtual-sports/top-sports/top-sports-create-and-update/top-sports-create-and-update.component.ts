import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Breadcrumb } from '@root/app/client/private/models/breadcrumb.model';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import { TopSportsInfo } from '@root/app/virtual-sports/top-sports/models/top-sports.model';
import { TopSportsConstants, defaultTopSportsData } from '@root/app/virtual-sports/top-sports/constants/top-sports.constants';
import { GlobalLoaderService } from '@root/app/shared/globalLoader/loader.service';
import { BrandService } from '@root/app/client/private/services/brand.service';
import { ApiClientService } from '@app/client/private/services/http';
import * as _ from 'lodash';


@Component({
  selector: 'app-top-sports-create-and-update',
  templateUrl: './top-sports-create-and-update.component.html',
  styleUrls: ['./top-sports-create-and-update.component.scss']
})

export class TopSportsCreateAndUpdateComponent implements OnInit {

  public topSportsConstants: any = TopSportsConstants;
  public breadcrumbsData: Breadcrumb[];
  public topSportData: TopSportsInfo;
  public topSportDataMemory: TopSportsInfo;
  public id: string;
  public isLoading: boolean = true;
  public isEdit: boolean = false;

  /**
   * Constructor
   * @param router: Router 
   * @param globalLoaderService: GlobalLoaderService
   * @param route: ActivatedRoute
   * @param dialogService: DialogService
   * @param brandService: BrandService
   * @param apiClientService: ApiClientService
   */
  constructor(
    private router: Router,
    private globalLoaderService: GlobalLoaderService,
    private route: ActivatedRoute,
    private dialogService: DialogService,
    private brandService: BrandService,
    private apiClientService: ApiClientService) { }

  /**
   * ngOnInit
  */
  ngOnInit(): void {
    this.onLoad();
  }

  /**
   * Initialise top sports data on load
   * @returns - {void}
   */
  private onLoad(): void {
    this.id = this.route.snapshot.params.id;
    defaultTopSportsData.brand = this.brandService.brand;
    if (this.id) {
      this.showHideSpinner(true);
      this.apiClientService.virtualHubTopSportsService().getTopSports(this.id).map((response: any) => response.body).subscribe(res => {
        this.topSportDataMemory = JSON.parse(JSON.stringify(res));
        this.topSportData = res;
        this.isLoading = false;
        this.isEdit = true;
        this.breadcrumbsData = [{
          label: 'Top Sports',
          url: '/virtual-hub/top-sports'
        },
        {
          label: this.topSportData.sportsName,
          url: `/virtual-hub/top-sports/${this.id}`
        }];
        this.showHideSpinner(false);
      });
    } else {
      this.topSportData = JSON.parse(JSON.stringify(defaultTopSportsData));
      this.isLoading = false;
      this.isEdit = false;
      this.breadcrumbsData = [{
        label: 'Top Sports',
        url: '/virtual-hub/top-sports'
      }, {
        label: 'Create',
        url: `/virtual-hub/top-sports/create-top-sport`
      }];
    }
  }

  /**
   * Validate the form
   * @returns - {boolean}
   */
  public isValidForm(): boolean {
    if (this.isEdit) {
      return this.isValidEditForm();
    } else {
      return this.isValidCreateForm();
    }
  }

  /**
   * Validate the create form
   * @returns - {boolean}
   */
  private isValidCreateForm(): boolean {
    let isSportsNameValid: boolean = false;

    // sportsName
    if (this.topSportData.sportsName && this.topSportData.sportsName.length > 0) {
      isSportsNameValid = true;
    }

    if (isSportsNameValid) {
      return false;
    } else {
      return true;
    }
  }

  /**
  * Validate the edit form
  * @returns - {boolean}
  */
  private isValidEditForm(): boolean {
    let isBtnDisabled: boolean = true;
    let isFormChanged: boolean = false;

    let isFieldEmpty: boolean = this.isValidCreateForm();

    if (isFieldEmpty) {
      return isBtnDisabled;
    } else {
      if (this.topSportData && this.topSportDataMemory) {
        isFormChanged = _.isEqual(this.topSportDataMemory, this.topSportData);
      }

      if (!isFormChanged) {
        isBtnDisabled = false;
      }

      return isBtnDisabled;
    }
  }

  /**
   * Save changes confirmation
   * @returns - {void}
  */
  public saveChanges(): void {
    let messageStatus: string = this.id ? 'Save' : 'Create';
    this.dialogService.showConfirmDialog({
      title: `${messageStatus} Top Sports`,
      message: `Are you sure you want to ${messageStatus.toLocaleLowerCase()} top sports configuration?`,
      yesCallback: () => {
        this.sendSaveRequest();
      }
    });
  }

  /**
   * Service call for create/update top sports
   * @returns - {void}
  */
  private sendSaveRequest(): void {
    this.showHideSpinner();
    if (this.id) {
      this.apiClientService.virtualHubTopSportsService().updateTopSports(this.topSportData).subscribe((res) => {
        if (res) {
          this.showHideSpinner(false);
          this.uploadNotify();
        }
      }, error => {
        this.showHideSpinner(false);
        this.errorNotify(error);
      });
    } else {
      this.apiClientService.virtualHubTopSportsService().createTopSports(this.topSportData).subscribe((res) => {
        if (res) {
          this.showHideSpinner(false);
          this.uploadNotify();
        }
      }, error => {
        this.showHideSpinner(false);
        this.errorNotify(error);
      });
    }
  }

  /**
   * Upload notification.
   * @param isDelete 
   * @returns - {void}
  */
  private uploadNotify(isDelete: boolean = false): void {
    const self = this;
    let messageStatus: string;
    if (isDelete) {
      messageStatus = 'Removed';
    } else {
      messageStatus = this.id ? 'Saved' : 'Created';
    }
    this.dialogService.showNotificationDialog({
      title: `${messageStatus} Top Sports`,
      message: `Top Sports configuration is ${messageStatus.toLocaleLowerCase()} successfully.`,
      closeCallback() {
        self.router.navigate(['/virtual-hub/top-sports']);
      }
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

  /**
   * Revert changes confirmation
   * @returns - {void}
  */
  public revertChanges(): void {
    this.dialogService.showConfirmDialog({
      title: 'Revert Changes',
      message: 'Are you sure you want to revert the changes?',
      yesCallback: () => {
        this.revertFormChanges();
      }
    });
  }


  /**
   * Revert changes
   * @returns - {void}
  */
  private revertFormChanges(): void {
    if (this.id && this.topSportDataMemory) {
      this.topSportData = JSON.parse(JSON.stringify(this.topSportDataMemory));
    } else {
      this.topSportData = JSON.parse(JSON.stringify(defaultTopSportsData));
    }
  }


  /**
   * To enable and disable active checkbox
   * @returns - {void}
  */
  public activeStatus(): void {
    this.topSportData.isTopSports = !this.topSportData.isTopSports;
  }

  /**
   * Delete confirmation.
   * @returns - {void}
  */
  public remove(): void {
    this.dialogService.showConfirmDialog({
      title: `Remove Top Sports`,
      message: `Are you sure you want to remove the Top Sports?`,
      yesCallback: () => {
        this.removeRequest();
      }
    });
  }

  /**
   * Service call to delete top sports
   * @returns - {void}
  */
  private removeRequest(): void {
    this.showHideSpinner(true);
    this.apiClientService.virtualHubTopSportsService().deleteTopSports(this.topSportData.id).subscribe((res) => {
      if (res) {
        this.showHideSpinner(false);
        this.uploadNotify(true);
        this.router.navigate(['/virtual-hub/top-sports']);
      }
    }, error => {
      this.showHideSpinner(false);
      this.errorNotify(error);
    });
  }
}
