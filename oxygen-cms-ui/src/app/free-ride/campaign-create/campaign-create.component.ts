import { Component, OnInit } from '@angular/core';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { DateRange } from '@app/client/private/models/dateRange.model';
import { DialogService } from '../../shared/dialog/dialog.service';
import { FreeRideAPIService } from '../services/free-ride.api.service';
import { BrandService } from '../../client/private/services/brand.service';
import { Router } from '@angular/router';
import { Campaign } from '@app/client/private/models/freeRideCampaign.model';
@Component({
  selector: 'app-campaign-create',
  templateUrl: './campaign-create.component.html',
  styleUrls: ['./campaign-create.component.scss']
})
export class CampaignCreateComponent implements OnInit {
  public breadcrumbsData: Breadcrumb[];
  public newCampaign: Campaign = {
    name: '',
    displayFrom: '',
    displayTo: '',
    openBetCampaignId: '',
    optimoveId: '',
    id: '',
    updatedBy: '',
    updatedAt: '',
    createdBy: '',
    createdAt: '',
    updatedByUserName: '',
    createdByUserName: '',
    brand: this.brandService.brand,
  };
  constructor(
    private dialogService: DialogService,
    private router: Router,
    private freeRideAPIService: FreeRideAPIService,
    private brandService: BrandService,
  ) { }

  ngOnInit(): void {
    this.breadcrumbsData = [{
      label: `Free Ride`,
      url: `/free-ride/campaign`
    }, {
      label: 'Create campaign',
      url: `/free-ride/campaign/create`
    }];
  }

  /**
   * Handle data comes from dataTime component, set promotion property
   * @param {DateRange} data - startDate/endDate in toISOString();
   */
  handleDisplayDateUpdate(data: DateRange): void {
    this.newCampaign.displayFrom = data.startDate;
    this.newCampaign.displayTo = data.endDate;
  }

   /**
   * Campaign Create
   */
  saveCampaignChanges() {
    this.newCampaign.brand = this.brandService.brand;
    this.freeRideAPIService.postNewCampaign(this.newCampaign).subscribe(data => {
      this.newCampaign.id = data.body.id;
      this.finishCampaignCreation();
    });
  }

    /**
   * Button Disabled Check
   */
  isValidModel(): boolean {
    return this.newCampaign &&
      this.newCampaign.name.length > 0 &&
      this.newCampaign.displayTo.length > 0 &&
      this.newCampaign.displayFrom.length > 0 &&
      this.newCampaign.openBetCampaignId.length > 0 &&
      this.newCampaign.optimoveId.length > 0 &&
      this.isEndDateValid() &&
      !this.isPastDate();
  }

   /**
   * On campaign create Completion
   */
  finishCampaignCreation() {
    const self = this;
    this.dialogService.showNotificationDialog({
      title: 'Save Completed',
      message: 'Campaign is Created and Stored.',
      closeCallback() {
        self.router.navigate([`free-ride/campaign/${self.newCampaign.id}`]);
      }
    });
  }

  /**
   * End Date valid check
   */
  isEndDateValid(): boolean {
    const displayFromDate = new Date(this.newCampaign.displayFrom).toDateString();
    const displayToDate = new Date(this.newCampaign.displayTo).toDateString();
    return displayFromDate === displayToDate;
  }

  /**
   * Date Check for past dates
   */
  isPastDate() {
    return (new Date(this.newCampaign.displayFrom).toISOString().substring(0, 10)
    < new Date().toISOString().substring(0, 10)) ||
    (new Date(this.newCampaign.displayTo).toISOString().substring(0, 10)
    < new Date().toISOString().substring(0, 10));
  }
}
