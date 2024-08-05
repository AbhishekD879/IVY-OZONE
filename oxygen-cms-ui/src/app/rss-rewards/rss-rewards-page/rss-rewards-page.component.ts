import {Component, OnInit, ViewChild} from '@angular/core';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {ActionButtonsComponent} from '@app/shared/action-buttons/action-buttons.component';
import {BrandService} from '@app/client/private/services/brand.service';
import { RssRewards } from '@app/client/private/models/coins-rewards.model';
import { RssRewardsApiService } from '@app/rss-rewards/rss-rewards.api.service';
import { ComponentCanDeactivate } from '@app/client/private/interfaces/pending-changes.guard';
import { GlobalLoaderService } from '@root/app/shared/globalLoader/loader.service';

@Component({
  selector: 'rss-rewards-page',
  templateUrl: './rss-rewards-page.component.html',
  styleUrls: ['./rss-rewards-page.component.scss']
})
export class RssRewardsPageComponent implements OnInit, ComponentCanDeactivate {
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;

  rssRewardsInitialObj: RssRewards = {
    brand: '',
    id: '',
    createdAt: '',
    createdBy: '',
    createdByUserName: '',
    updatedAt: '',
    updatedBy: '',
    updatedByUserName: '',

    enabled: false,
    coins: undefined,
    communicationType: '',
    sitecoreTemplateId: '',
    source: '',
    subSource: '',
    product: ''
  };

  rssRewards: RssRewards;
  rssRewardsCopy: RssRewards;

  constructor(private dialogService: DialogService,
              private brandService: BrandService,
              private api: RssRewardsApiService,
              private globalLoaderService: GlobalLoaderService,) {
    this.rssRewards = this.empty();
  }

  ngOnInit() {
    this.load();
  }
  public canDeactivate() {
    const equal = this.rssRewards.coins === this.rssRewardsCopy.coins &&
    this.rssRewards.communicationType === this.rssRewardsCopy.communicationType &&
    this.rssRewards.enabled === this.rssRewardsCopy.enabled &&
    this.rssRewards.sitecoreTemplateId === this.rssRewardsCopy.sitecoreTemplateId &&
    this.rssRewards.source === this.rssRewardsCopy.source &&
    this.rssRewards.subSource === this.rssRewardsCopy.subSource &&
    this.rssRewards.product === this.rssRewardsCopy.product;
    return equal;
  }
  private load() {
    this.globalLoaderService.showLoader();
    this.api
        .get()
      .subscribe((data: any) => {
        this.globalLoaderService.hideLoader();
        this.rssRewards = data.body;
        this.rssRewardsCopy = { ...this.rssRewards };
        this.actionButtons.extendCollection(this.rssRewards);
      }, error => {
        this.globalLoaderService.hideLoader();
        if (error.status === 404) {
          this.rssRewards = this.empty();
        } else {
          console.log(error);
          this.dialogService.showNotificationDialog({
            title: 'Error occurred',
            message: 'Ooops... Something went wrong, please contact support team'
          });
        }
      });
  }

  actionsHandler(event): void {
    switch (event) {
      case 'save':
        this.save();
        break;
      case 'revert':
        this.revert();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  verifyrssRewardsData(rssRewards: RssRewards): boolean {
    return (!!rssRewards.coins && rssRewards.coins<=500 && rssRewards.coins>=1) && (!!rssRewards.source) && (!!rssRewards.subSource) && (!!rssRewards.product);
  }

  private empty(): RssRewards {
    let rssRewards = { ...this.rssRewardsInitialObj };
    rssRewards.brand = this.brandService.brand;

    return rssRewards;
  }

  private save() {
    this.globalLoaderService.showLoader();
    if (this.rssRewards.createdAt) {
      this.sendRequest('update');
    } else {
      this.sendRequest('create');
    }
  }

  private revert() {
    this.load();
  }

  private sendRequest(requestType) {
    if(!this.rssRewards.brand) this.rssRewards.brand = this.brandService.brand;
    this.api[requestType](this.rssRewards).subscribe((data: {body: RssRewards}) => {
        this.globalLoaderService.hideLoader();
        this.rssRewards = data.body;
        this.rssRewardsCopy = { ...this.rssRewards };
        this.actionButtons.extendCollection(this.rssRewards);
        this.dialogService.showNotificationDialog({
          title: 'Success',
          message: 'Your changes have been saved'
        });
      }, error => {
        this.globalLoaderService.hideLoader();
        console.log(error);
        this.dialogService.showNotificationDialog({
          title: 'Error on saving',
          message: 'Ooops... Something went wrong, please contact support team'
        });
      });
  }
}
