
import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { HttpResponse } from '@angular/common/http';
import { TinymceComponent } from './../../shared/tinymce/tinymce.component';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { ApiClientService } from '@app/client/private/services/http';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { StatContentInfo, StaticEventTitle, StatOption } from '@app/client/private/models/statContentInfo.model';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { BrandService } from '@app/client/private/services/brand.service';
import { SportsModulesBreadcrumbsService } from '@app/sports-modules/sports-modules-breadcrumbs.service';
import { DateRange } from '@app/client/private/models/dateRange.model';
import * as _ from 'lodash';

@Component({
  selector: 'app-stat-content',
  templateUrl: './stat-content.component.html',
  styleUrls: ['./stat-content.component.scss']
})

export class StatContentComponent implements OnInit {
  public isLoading: boolean = false;
  public statContentInfo: StatContentInfo;
  public breadcrumbsData: Breadcrumb[];
  public warningMessage: string;
  public pageType: string;
  @ViewChild('htmlMarkup') editor: TinymceComponent;
  public hubId: string;
  public StatInfoOptions: StatOption[] = [];
  public saveNew: boolean = false;
  public isDisabled: boolean = false;
  private statisticalCollection: any;


  constructor(
    private activatedRoute: ActivatedRoute,
    private router: Router,
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService,
    private brandService: BrandService,
    private sportsModulesBreadcrumbsService: SportsModulesBreadcrumbsService,
  ) {
    this.isValidModel = this.isValidModel.bind(this);
  }

  ngOnInit() {
    this.loadInitialData();
  }

  private createInitialData(): void {
    this.statContentInfo = {
      createdAt: null,
      createdBy: null,
      updatedByUserName: null,
      createdByUserName: null,
      updatedAt: null,
      updatedBy: null,
      brand: this.brandService.brand,
      title: '',
      marketType: '',
      content: '',
      enabled: false,
      eventId: '',
      marketId: '',
      startTime: new Date().toISOString(),
      endTime: new Date(new Date().setHours(24)).toISOString(),
      id: ''
    };
  }

  /**
   * Initial data Loading method
   * Get content data from sevrer or create new content object
   */
  private loadInitialData(): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      this.hubId = params['hubId'];
      this.pageType = params.id ? 'edit' : 'add';
      if (this.pageType === 'edit') {
        this.isDisabled = true;
        this.showHideSpinner();
        this.apiClientService
          .statContentInfoService()
          .getById(params.id)
          .map((moduleResponse: HttpResponse<StatContentInfo>) => {
            return moduleResponse.body;
          })
          .subscribe((statContentInfo: StatContentInfo) => {
            this.statContentInfo = statContentInfo;
            this.extendCollection(this.statContentInfo)
            this.loadStatContentDropDown(statContentInfo);
            if (this.editor) {
              this.editor.update(this.statContentInfo.content);
            }
            this.initBreadcrumbs(params);
            this.showHideSpinner(false);
          }, () => {
            this.showHideSpinner(false);
            this.router.navigate(['/stat-content-info']);
          });
      } else {
        this.createInitialData();
        this.loadStatContentDropDown(this.brandService);
        this.initBreadcrumbs(params);
      }
    });
  }

  /**
  *  Statistical Content Information marketTypes.
  */

  loadStatContentDropDown(statContentInfo) {
    this.StatInfoOptions.push({ text: "Price Boost(PB)", type: "ladbrokes", value: "PB" });
    this.StatInfoOptions.push({ text: "Super Price Boost(SPB)", type: "ladbrokes", value: "SPB" });
    this.StatInfoOptions.push({ text: "Big Match Odds Booster​(BMOB)", type: "bma", value: "BMOB" });
    this.StatInfoOptions.push({ text: "Odds Booster​(OB)", type: "bma", value: "OB" });
    this.StatInfoOptions = this.StatInfoOptions.filter(brand => brand.type === statContentInfo.brand);
  }

  /**
 * Get event based title.
 */
  getEventTitle(event) {
    var eventId = event.target.value;
    if (eventId) {
      this.apiClientService
        .statContentInfoService()
        .getEventTitleById(eventId)
        .map((moduleResponse: HttpResponse<StaticEventTitle>) => {
          return moduleResponse.body;
        })
        .subscribe((statContentInfo: StaticEventTitle) => {
          this.statContentInfo.title = statContentInfo.eventTitle;
        })
    }


  }

  /**
  * Save and create another Statistical Content Information.
  */

  saveCreateNew() {
    this.saveNew = true;
    this.saveChanges(this.saveNew);
  }

  /**
   * Show confirmation dialog and create Statistical Content Information.
   */
  saveChanges(saveNew) {
    this.dialogService.showConfirmDialog({
      title: `Saving of: Statistical Content Information`,
      message: `Are You sure You want to save this: Statistical Content Information?`,
      yesCallback: () => {
        if (this.hubId || this.pageType === 'edit') {
          this.updateContent(saveNew)
        }
        else {
          this.sendNewContentInformation(saveNew);
        }
      }
    });
  }

  /**
   * Send create Statistical Content Information API request.
   */
  sendNewContentInformation(saveNew) {
    const self = this
    this.showHideSpinner(true);
    this.apiClientService.statContentInfoService()
      .add(this.statContentInfo)
      .subscribe(data => {
        this.statContentInfo.id = data.body.id;
        this.showHideSpinner(false);
        this.dialogService.showNotificationDialog({
          title: 'Create Completed',
          message: 'Statistical Content Information is Successfully Created.',
          closeCallback() {
            if (saveNew) {
              self.editor.update('');
              self.router.navigateByUrl('/', { skipLocationChange: true }).then(() => {
                self.router.navigate(['stat-content-info/add']);
              });
              self.createInitialData();
            } else {
              self.router.navigate(['stat-content-info']);
            }
          }
        });
      });
  }

  /**
   * Send API request to Update Content data.
   */
  updateContent(saveNew) {
    const self = this
    this.apiClientService.statContentInfoService()
      .edit(this.statContentInfo)
      .map((content: HttpResponse<StatContentInfo>) => content.body)
      .subscribe((data: StatContentInfo) => {
        this.statContentInfo = data;
        this.dialogService.showNotificationDialog({
          title: 'Update Completed',
          message: 'Statistical Content Changes are Saved.',
          closeCallback: () => {
            if (saveNew) {
              self.router.navigate(['stat-content-info/add']);
            } else {
              self.router.navigate(['stat-content-info']);
            }
          }
        });
      });
  }


  /**
   * Cancle and redirect to the Parent
   */
  cancleChanges() {
    this.router.navigate(['stat-content-info']);
  }


  /**
 * Send server API request to delete Statistical Content
 */
  removeContent() {
    this.dialogService.showConfirmDialog({
      title: `Remove Statistical Content Information`,
      message: `Are You Sure You Want to Remove : Statistical Content Information?`,
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        this.apiClientService.statContentInfoService()
          .remove(this.statContentInfo.id)
          .subscribe(data => {
            this.dialogService.showNotificationDialog({
              title: 'Remove Completed',
              message: 'Statistical Content is Removed.'
            });
            this.navigateTo();
          });
      }
    });



  }

  /**
   * Handle data comes from dataTime component, set promotion property
   * @param {DateRange} data - startDate/endDate in toISOString();
   */
  handleVisibilityDateUpdate(data: DateRange): void {
    this.statContentInfo.startTime = data.startDate;
    this.statContentInfo.endTime = data.endDate;
  }


  /**
   * Init bredcrumbs paths data to view.
   */
  initBreadcrumbs(params: Params) {
    const isEdit = this.pageType === 'edit';
    if (this.hubId) {
      this.sportsModulesBreadcrumbsService.getBreadcrubs(params, {
        customBreadcrumbs: [
          {
            label: isEdit ? this.statContentInfo.title : 'create'
          }
        ]
      }).subscribe((breadcrubs: Breadcrumb[]) => {
        this.breadcrumbsData = breadcrubs;
      });
    } else {
      this.breadcrumbsData = [{
        label: `Statistical Content Information`,
        url: `/stat-content-info`
      }, {
        label: isEdit ? this.statContentInfo.title : 'create',
        url: isEdit ? `/stat-content-info/edit/${this.statContentInfo.id}` : '/stat-content-info/add'
      }];
    }
  }

  showHideSpinner(toShow: boolean = true): void {
    toShow ? this.globalLoaderService.showLoader() : this.globalLoaderService.hideLoader();
    this.isLoading = toShow;
  }

  /**
   * Validate input with type of number to not set value less than 1.
   */
  validateMinValue(e): boolean {
    if ((e.keyCode < 48 || e.keyCode > 57) ||
      (e.target.value.length === 0 && e.keyCode === 48)) {
      return false;
    }
  }

  /**
   * Auto Navigate to creted content with Id
   * Auto Navigate back when content deleted
   * @param moduleId
   */
  navigateTo(moduleId?: string): void {
    let linkToNavigate = '';
    const moduleUrl = `${this.breadcrumbsData[this.breadcrumbsData.length - 2].url}`;
    if (moduleId) {
      if (this.hubId) {
        linkToNavigate = `${moduleUrl}/stat-content-info/edit/${this.statContentInfo.id}`;
      } else {
        linkToNavigate = `/stat-content-info/edit/${this.statContentInfo.id}`;
      }
    } else {
      if (this.hubId) {
        linkToNavigate = moduleUrl;
      } else {
        linkToNavigate = '/stat-content-info';
      }
    }
    this.router.navigate([linkToNavigate]);
  }


  /**
 * Base model validation with checking required fields.
 * @return {boolean}
 */
  public isValidModel(): boolean {
    return this.statContentInfo && this.statContentInfo.title !== '' &&
      this.statContentInfo.marketType !== '' &&
      this.statContentInfo.eventId !== '' &&
      this.statContentInfo.marketId !== '' &&
      this.statContentInfo.startTime !== '' &&
      this.statContentInfo.endTime !== '' &&
      this.isValidForSave();
  }



  public update(data: string): void {
    this.statContentInfo.content = data;
  }

  public extendCollection(collection?: any): void {
    this.statisticalCollection = _.cloneDeep(collection ? collection : this.statContentInfo);
  }

  public isValidForSave(): boolean {
    return !this.isEqualCollection();
  }

  public isEqualCollection(): boolean {
    return _.isEqual(this.statisticalCollection, this.statContentInfo);
  }
}
