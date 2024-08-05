import {Component, OnInit} from '@angular/core';
import {BrandService} from '@app/client/private/services/brand.service';
import {Breadcrumb} from '@app/client/private/models/breadcrumb.model';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {Router} from '@angular/router';
import {DateRange} from '@app/client/private/models/dateRange.model';
import {Campaign, CampaignStatus} from '@app/client/private/models/campaign.model';
import {CampaignApiService} from '@app/timeline/service/campaign-api.service';
import { MatSelectChange } from '@angular/material/select';

@Component({
  selector: 'campaign-create',
  templateUrl: './campaign-create.component.html'
})
export class CampaignCreateComponent implements OnInit {
  public breadcrumbsData: Breadcrumb[];
  newCampaign: Campaign;

  campaignStatusesRef = CampaignStatus;
  campaignStatuses(): Array<string> {
    return Object.keys(this.campaignStatusesRef);
  }

  constructor(private brandService: BrandService,
              private campaignApiService: CampaignApiService,
              private dialogService: DialogService,
              private router: Router) {
  }

  ngOnInit() {
    this.newCampaign = {
      id: '',
      name: '',
      updatedBy: '',
      updatedAt: '',
      createdBy: '',
      createdAt: '',
      displayFrom: '',
      displayTo: '',
      updatedByUserName: '',
      createdByUserName: '',
      displayed: false,
      highlighted: false,

      status: CampaignStatus.OPEN,
      messagesToDisplayCount: undefined,

      isChanged: false,
      brand: this.brandService.brand,
    };
    this.breadcrumbsData = [{
      label: `Campaigns`,
      url: `/timeline/campaign`
    }, {
      label: 'Create campaign',
      url: `/timeline/campaign/create/`
    }];
  }

  setStatus(status: MatSelectChange) {
    this.newCampaign.status = status.value;
  }

  isValidModel(): boolean {
    const titleValid: boolean = this.newCampaign.name.trim().length > 0;
    const displayFromValid: boolean = this.newCampaign.displayFrom.trim().length > 0;
    const displayToValid: boolean = this.newCampaign.displayTo.trim().length > 0;
    const initialNumberOfMessagesValid: boolean = this.newCampaign.messagesToDisplayCount !== undefined;

    return titleValid && displayFromValid && displayToValid && initialNumberOfMessagesValid;
  }

  public saveCampaignChanges(): void {
    this.campaignApiService.createCampaign(this.newCampaign)
      .subscribe(data => {
        this.newCampaign.id = data.body.id;
        this.finishCampaignCreation();
      });
  }

  finishCampaignCreation(): void {
    const self = this;
    this.dialogService.showNotificationDialog({
      title: 'Save Completed',
      message: 'Campaign is Created and Stored.',
      closeCallback() {
        self.router.navigate([`timeline/campaign/edit/${self.newCampaign.id}`]);
      }
    });
  }

  handleDisplayDateUpdate(data: DateRange): void {
    this.newCampaign.displayFrom = new Date(data.startDate).toISOString();
    this.newCampaign.displayTo = new Date(data.endDate).toISOString();
  }
}
