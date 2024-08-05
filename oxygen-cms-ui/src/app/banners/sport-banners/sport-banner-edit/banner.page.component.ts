import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { DialogService } from '../../../shared/dialog/dialog.service';
import { BannersApiService } from '../service/banners.api.service';
import { Banner } from '../../../client/private/models/banner.model';
import { DateRange } from '../../../client/private/models/dateRange.model';
import { HttpResponse } from '@angular/common/http';
import { Breadcrumb } from '../../../client/private/models/breadcrumb.model';
import {SportCategory} from '../../../client/private/models/sportcategory.model';

// @ts-ignore
declare var tinymce: any;

@Component({
  selector: 'single-banner-page',
  templateUrl: './banner.page.component.html',
  styleUrls: ['./banner.page.component.scss']
})
export class BannerPageComponent implements OnInit {
  banner: Banner;
  id: string;
  sportCategories: Array<SportCategory> = [];

  @ViewChild('actionButtons') actionButtons;
  public breadcrumbsData: Breadcrumb[];

  constructor(
    private dialogService: DialogService,
    private route: ActivatedRoute,
    private router: Router,
    private bannersApiService: BannersApiService
  ) {}

  loadInitialData() {
    // load current banner data
    this.bannersApiService.getSingleBannerData(this.id)
      .subscribe((data: any) => {
        this.banner = data.body;
        this.breadcrumbsData = [{
          label: 'Banners',
          url: '/banners/sport-banners'
        }, {
          label: this.banner.imageTitle,
          url: `/banners/sport-banners/${this.banner.id}`
        }];
      }, error => {
        this.router.navigate(['/sso-pages']);
      });

    // load sport categories to map promotion
    this.bannersApiService.getSportCategories()
      .map((data: HttpResponse<SportCategory[]>) => data.body)
      .subscribe((data: SportCategory[]) => {
        this.sportCategories = data;
      });
  }

  /**
   * On input change.
   * transform viplevels input text to numbers separated by comma
   * @param event
   */
  transformToNumber(event) {
    event.target.value = event.target.value
      .replace(/[A-Za-z_.]*/gi, '')
      .replace(/,+/gi, ',')
      .replace(/[`~!@#$%^&*()_|+\-=?;:'".<>\{\}\[\]\\\/]/gi, '');
  }

  isVipLevelValid() {
    const vipLevelsData = this.banner.vipLevelsInput || '';
    return vipLevelsData.length === 0 ||
      (vipLevelsData.length > 0 && !isNaN(parseInt(vipLevelsData.replace(/\,/gi, ''), 10)));
  }

  /**
   * Handle data comes from dataTime component, set promotion property
   * @param {DateRange} data - startDate/endDate in toISOString();
   */
  handleDateUpdate(data: DateRange) {
    this.banner.validityPeriodStart = data.startDate;
    this.banner.validityPeriodEnd = data.endDate;
  }

  /**
   * Upload file on input change event.
   * @param event
   */
  uploadFile(event, isDesktop) {
    const files = event.target.files;
    const formData = new FormData();

    // uploaded file
    formData.append('file', files[0]);
    formData.append('desktopImage', isDesktop);

    this.bannersApiService.postNewBannerImage(this.banner.id, formData)
      .subscribe((data: any) => {
        // update uploaded image name to show inside input
        if (!isDesktop && data.body.uriMedium) {
          this.banner.uriMedium = data.body.uriMedium;
        }

        if (isDesktop && data.body.desktopUriMedium) {
          this.banner.desktopUriMedium = data.body.desktopUriMedium;
        }
        this.dialogService.showNotificationDialog({
          title: 'Upload Completed',
          message: 'New Image is Uploaded.'
        });
      });
  }

  hadleUploadImageClick(event) {
    const input = event.target.previousElementSibling.querySelector('input');

    input.click();
  }

  removeImage(isDesktop) {
    this.bannersApiService.deleteBannerImage(this.banner.id, isDesktop)
      .subscribe(data => {

        if (isDesktop) {
          this.banner.desktopUriMedium = '';
        } else {
          this.banner.uriMedium = '';
        }

        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'Image is Removed.'
        });
      });
  }

  revertChanges() {
    this.loadInitialData();
  }

  /**
   * Send DELETE API request
   * @param {Banner} banner
   */
  removeBanner() {
    this.bannersApiService.deleteBanner(this.banner.id)
      .subscribe((data: any) => {
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'Banner is Removed.'
        });
        this.router.navigate(['/banners/sport-banners']);
      });
  }

  /**
   * Make PUT request to server to update
   */
  saveChanges() {
    this.bannersApiService.putBannerChanges(this.banner)
      .map((response: HttpResponse<Banner>) => {
        return response.body;
      })
      .subscribe((data: Banner) => {
        this.banner = data;
        this.actionButtons.extendCollection(this.banner);
        this.dialogService.showNotificationDialog({
          title: 'Upload Completed',
          message: 'Banner Changes are Saved.'
        });
      });
  }

  ngOnInit() {
    this.id = this.route.snapshot.paramMap.get('id');

    this.loadInitialData();
  }

  public isValidForm(banner: Banner): boolean {
    return banner.imageTitle && banner.imageTitle.length > 0;
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeBanner();
        break;
      case 'save':
        this.saveChanges();
        break;
      case 'revert':
        this.revertChanges();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  public onShowToCustomerChange(value: string): void {
    this.banner.showToCustomer = value;
  }
}
