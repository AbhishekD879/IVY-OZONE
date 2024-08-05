import { Component, OnInit, ViewChild } from '@angular/core';
import { BrandService } from '../../client/private/services/brand.service';
import { GlobalLoaderService } from '../../shared/globalLoader/loader.service';
import { ApiClientService } from '../../client/private/services/http';
import { HttpResponse } from '@angular/common/http';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { TinymceComponent } from '../../shared/tinymce/tinymce.component';
import { DialogService } from '../../shared/dialog/dialog.service';
import { popularAccasCardMock } from '../popular-accas-widget/popular-accas-widget.mock';
import { ArrayIdsTypeList, PopularAccasCard, SportCategories } from '../popular-accas-widget/popular-accas-widget.model';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { DateRange } from '../../client/private/models';
import { ActionButtonsComponent } from '../../shared/action-buttons/action-buttons.component';

@Component({
  selector: 'app-popular-accas-widget-card',
  templateUrl: './popular-accas-widget-card.component.html',
  styleUrls: ['./popular-accas-widget-card.component.scss']
})
export class PopularAccasWidgetCardComponent implements OnInit {

  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;
  @ViewChild('informationTextEditor') informationTextEditor: TinymceComponent;
  popularAccaWidgetCardsForm: FormGroup;
  popularAccaWidgetCardsData: PopularAccasCard;
  breadcrumbsData: any[];
  isLoading: boolean = true;
  arrayIdTypes: {label: string, id: string}[];
  isListIdDisabled: boolean;
  sportCategoriesList: { imageTitle: string }[];
  betId: any;
  pageTitle: string;
  popularAccasWidgetCardIcon: any = {};
  dateRangeError: string;

  constructor(
    private brandService: BrandService,
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService,
    private activatedRoute: ActivatedRoute,
    private router: Router
  ) {
    this.arrayIdTypes = ArrayIdsTypeList;
    this.sportCategoriesList = SportCategories;
    this.validationHandler = this.validationHandler.bind(this);
  }

  ngOnInit(): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      this.betId = params['id'];
      this.pageTitle = this.betId ? 'Popular Acca Widget card configurations: ' : 'New Popular Acca Widget card configurations: ';
      this.loadInitialData();
    });
    Object.assign(popularAccasCardMock, {
      brand: this.brandService.brand,
    })
  }

  /*
  *form controls
  */
  get formControls() {
    return this.popularAccaWidgetCardsForm?.controls;
  }

  /**
   * it loads the initial data
   * loadInitialData()
   */
  private loadInitialData(): void {
    this.globalLoaderService.showLoader();

    if (this.betId) {
      this.apiClientService.
        popularAccasWidgetService()
        .getPopularAccasWidgetCardData(this.betId).subscribe((data: { body: any }) => {
          if (data.body.id) {
            this.popularAccaWidgetCardsData = data.body;
            this.createPopuarAccaCardsFormGroup();
            this.selectTypeId(this.formControls.accaIdsType.value, true);
          }
          this.buildBreadCrumbsData();
          this.actionButtons?.extendCollection(this.popularAccaWidgetCardsForm.value);
          this.globalLoaderService.hideLoader();
          this.isLoading = false;
        },
          error => {
            this.isLoading = false;
            this.getDefaultValues();
            this.globalLoaderService.hideLoader();
            this.dialogService.showNotificationDialog({
              title: 'Error occurred',
              message: (error?.error?.message) ? error?.error?.message : 'Ooops... Something went wrong, please contact support team'
            });
          });
    } else {
      this.getDefaultValues();
    }
  }

  getDefaultValues(): void {
    this.popularAccaWidgetCardsData = JSON.parse(JSON.stringify(popularAccasCardMock));
    this.createPopuarAccaCardsFormGroup();
    this.formControls.accaIdsType.setValue('EVENT');
    this.selectTypeId('Event');
    this.formControls.locations.setValue(["Sportbook Homepage"]);
    this.globalLoaderService.hideLoader();
    this.buildBreadCrumbsData();
    this.isLoading = false;
  }

  /**create form group */
  createPopuarAccaCardsFormGroup(): void {
    this.popularAccaWidgetCardsForm = new FormGroup({
      title: new FormControl(this.popularAccaWidgetCardsData.title || ''),
      subTitle: new FormControl(this.popularAccaWidgetCardsData.subTitle || ''),
      icon: new FormControl(this.popularAccaWidgetCardsData.svgId || ''),
      displayFrom: new FormControl(this.popularAccaWidgetCardsData.displayFrom || '', [Validators.required]),
      displayTo: new FormControl(this.popularAccaWidgetCardsData.displayTo || '', [Validators.required]),
      locations: new FormControl(this.popularAccaWidgetCardsData.locations || '', [Validators.required]),
      numberOfTimeBackedLabel: new FormControl(this.popularAccaWidgetCardsData.numberOfTimeBackedLabel || '', [Validators.maxLength(40)]),
      numberOfTimeBackedThreshold: new FormControl(this.popularAccaWidgetCardsData.numberOfTimeBackedThreshold || ''),
      accaIdsType: new FormControl(this.popularAccaWidgetCardsData.accaIdsType || ''),
      listOfIds: new FormControl(this.popularAccaWidgetCardsData.listOfIds || ''),
      marketTemplateIds: new FormControl(this.popularAccaWidgetCardsData.marketTemplateIds || ''),
      accaRangeMin: new FormControl(Number(this.popularAccaWidgetCardsData.accaRangeMin) || '', [Validators.required, Validators.min(2)]),
      accaRangeMax: new FormControl(Number(this.popularAccaWidgetCardsData.accaRangeMax) || '', [Validators.required, Validators.min(2)])
    });
  }

  /**
   * save changes to edit and create
   */
  public saveChanges(): void {
    if (this.popularAccaWidgetCardsData?.id) {
      this.submitChanges('putPopularAccasWidgetCardData', 'Popular accas widget card updated!');
    } else {
      this.submitChanges('postPopularAccasWidgetCardData', 'Popular accas widget card saved!');
    }
  }

  /**
   * check duplicates in list of ids and market name fields
   * @param controlName 
   * @returns 
   */
  hasduplicates(controlName: string): boolean {
    if(this.popularAccaWidgetCardsForm.get(controlName).value) {
    const list = this.popularAccaWidgetCardsForm.get(controlName).value.toString().split(',');
    return new Set(list).size !== list.length;
    }
    return false;
  }

  /**
   * date range validation
   * @returns boolean
   */
  dateRangeValid(): boolean{
    this.dateRangeError = null;

    const startDate = new Date(this.formControls.displayFrom.value).getTime();
    const currentDateString = new Date().toISOString().split("T")[0];
    const startDateString = new Date(this.formControls.displayFrom.value).toISOString().split("T")[0];
    const endDate = new Date(this.formControls.displayTo.value).getTime();

    if (startDateString < currentDateString) {
      this.dateRangeError = '"Display from" date should be today or future. Please amend your schedule.';
      return !this.dateRangeError;
    }

    if (startDate > endDate) {
      this.dateRangeError = '"Display from" date should be less than display to date. Please amend your schedule.';
      return !this.dateRangeError;
    }

    return !this.dateRangeError;
  }

  /**
   * submit changes
   * @param reQuestType 
   * @param message 
   */
  public submitChanges(reQuestType: string, message: string): void {
    this.globalLoaderService.showLoader();
    Object.assign(this.popularAccaWidgetCardsForm.value, {
      brand: this.brandService.brand,
      id : this.popularAccaWidgetCardsData.id,
      displayFrom : this.popularAccaWidgetCardsData.displayFrom,
      displayTo :  this.popularAccaWidgetCardsData.displayTo,
      svgId: this.popularAccaWidgetCardsData.svgId,
      sortOrder: this.popularAccaWidgetCardsData.sortOrder,
      marketTemplateIds: Array.isArray(this.formControls.marketTemplateIds.value)? this.formControls.marketTemplateIds.value : (this.formControls.marketTemplateIds.value.length ? this.formControls.marketTemplateIds.value.split(',') : [])
    })
    this.apiClientService.
      popularAccasWidgetService()[reQuestType](this.popularAccaWidgetCardsForm.value)
      .map((data: HttpResponse<any>) => data.body)
      .subscribe((bsData: PopularAccasCard) => {
        this.popularAccaWidgetCardsData = bsData;
        this.popularAccaWidgetCardsForm.patchValue(bsData);
        let self = this;
        this.actionButtons?.extendCollection(this.popularAccaWidgetCardsForm.value);
        this.globalLoaderService.hideLoader();
        this.dialogService.showNotificationDialog({
          title: 'Popular accas widget card',
          message: message,
          closeCallback() {
            self.router.navigate([self.getUrlToGoBack]);
          }
        });
      }, error => {
        this.globalLoaderService.hideLoader();
        this.dialogService.showNotificationDialog({
          title: 'Error occurred',
          message: (error?.error?.message) || error?.error?.errors?.length && error?.error?.errors[0]?.defaultMessage || 'Ooops... Something went wrong, please contact support team'
        });
      });
  }

  /**
   * action handlers on form save
   * @param event 
   */
  public actionsHandler(event): void {
    switch (event) {
      case "save":
        this.saveChanges();
        break;
      case "revert":
        this.revertChanges();
        break;
      case 'remove':
        this.remove();
        break;
      default:
        console.error("Unhandled Action");
        break;
    }
  }

  /**
   * revrting the changes to onload 
   */
  public revertChanges(): void {
    this.loadInitialData();
  }

  /**
 * 
 *  Creating the BreadCrumbs for the page
 */
   buildBreadCrumbsData():void {
    const title: string = this.popularAccaWidgetCardsData && this.popularAccaWidgetCardsData.id ? this.popularAccaWidgetCardsData.title : 'Create';
    const url = title === 'Create' ? `/most-popular/popular-accas-widget/add` : `/most-popular/popular-accas-widget/edit/${this.popularAccaWidgetCardsData.id}`;
    this.breadcrumbsData = [{
      label: `Popular Acca Widget`,
      url: `/most-popular/popular-accas-widget`
    }, {
      label: title,
      url: url
    }];
  }

  /**
   *form validation
   */
  public validationHandler(): boolean {
    return this.popularAccaWidgetCardsForm && this.popularAccaWidgetCardsForm.valid &&
    this.formControls.accaRangeMin.value <= this.formControls.accaRangeMax.value  &&
    !this.hasduplicates('marketTemplateIds') && !this.hasduplicates('listOfIds') && !this.dateRangeError &&
    (!this.isListIdDisabled ? this.formControls.listOfIds.value?.length : true);
  }

  /**
   * on All acca type slection, handled few valditions
   * @param key 
   * @param isEdit 
   */
  selectTypeId(key: string, isEdit?: boolean): void {
    this.isListIdDisabled = (key === 'ALL');
    !isEdit && this.popularAccaWidgetCardsForm.get('listOfIds').setValue([]);
    !this.isListIdDisabled ? this.popularAccaWidgetCardsForm.get('listOfIds').setValidators(Validators.required) :this.popularAccaWidgetCardsForm.get('listOfIds').clearValidators();
    this.popularAccaWidgetCardsForm.get('listOfIds').updateValueAndValidity();
  }

  /**
   * on date change, set values in form
   * @param data 
   */
  handleDateUpdate(data: DateRange): void {
    this.popularAccaWidgetCardsData.displayFrom = data.startDate;
    this.popularAccaWidgetCardsData.displayTo = data.endDate;
    this.popularAccaWidgetCardsForm.controls['displayFrom'].setValue(data.startDate);
    this.popularAccaWidgetCardsForm.controls['displayTo'].setValue(data.endDate);
    this.dateRangeValid();
  }

  /**on focus out changing string to number in input  */
  changeToNumber(event: any,controlName: string): void {
    this.formControls[controlName].setValue(Number(event.target.value));
  }

  public trackSportByTitle(bets: any): string {
    return bets.imageTitle;
  }

  /**
   * remove card data
   */
  private remove(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.
    popularAccasWidgetService().deletePopularAccasWidgetCardData(this.popularAccaWidgetCardsData.id).subscribe(() => {
      this.globalLoaderService.hideLoader();
      this.router.navigate([this.getUrlToGoBack]);
    }, () => {
      this.globalLoaderService.hideLoader();
    });
  }

  /**
   * url for going back to popular accas configuration page from card configurations page
   */
  private get getUrlToGoBack(): string {
    return `/most-popular/popular-accas-widget`;
  }
}
