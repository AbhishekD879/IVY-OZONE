import { ChangeDetectorRef, Component, OnInit, ViewChild } from '@angular/core';
import { ApiClientService } from '@app/client/private/services/http';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { SportCategory } from '@app/client/private/models/sportcategory.model';
import { BetPackModel, FilterModel } from '@app/betpack-market-place/model/bet-pack-banner.model';
import { SportsSurfaceBetsService } from '@app/sports-modules/surface-bets/surface-bets.service';
import { DateRange } from '@app/client/private/models';
import { HttpResponse } from '@angular/common/http';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { Breadcrumb } from '@app/client/private/models';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { MatSelectChange } from '@angular/material/select';
import { MatDialog } from '@angular/material/dialog';
import { BetPackTokenComponent } from '@app/betpack-market-place/betpack-token/betpack-token.component';
import { DataTableColumn } from '@app/client/private/models/dataTableColumn';
import * as _ from 'lodash';
import { BetPackValidationService } from '@app/promotions/service/bet-pack-validation.service';
import { onboardingConstants } from '../constants/betpack-market-place.constants';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'bet-pack-edit',
  templateUrl: './bet-pack-edit.component.html',
  styleUrls: ['./bet-pack-edit.component.scss'],
  providers: [
    DialogService
  ]
})
export class BetPackEditComponent implements OnInit {

  @ViewChild('actionButtons') actionButtons;
  public sportCategories: SportCategory[] = [];
  public betPackData: BetPackModel;
  public isLoading: boolean = false;
  public breadcrumbsData: Breadcrumb[];
  public readonly betpackConstant = onboardingConstants;
  filters: FilterModel[] = [];
  index: number;
  searchField: string = '';
  isedited: boolean = false;
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Free Bet Token ID',
      property: 'tokenId',
      link: {
        hrefProperty: 'id',
        path: 'betpack-market/betpack-token'
      },
    },
    {
      name: 'Free Bet Token Display Text',
      property: 'tokenTitle'
    },
    {
      name: 'Free Bet Token value',
      property: 'tokenValue'
    },
    {
      name: 'Deep Link',
      property: 'deepLinkUrl',
      link: {
        hrefProperty: 'id'
      },
      type: 'link'
    }
  ];

  filterProperties: Array<string> = [
    'tokenId',
    'tokenTitle',
    'tokenValue'
  ];
  dynamicValidators = [Validators.maxLength(100), Validators.required];
  betPackTokenBeforeEdit = [];
  betPackStartDateBeforeEdit: string | Date;
  betPackEditData: FormGroup;
  isReady: boolean;
  hideAction: boolean = true;
  constructor(
    private dialog: MatDialog,
    private activatedRoute: ActivatedRoute,
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService,
    private sportsSurfaceBetsService: SportsSurfaceBetsService,
    private router: Router,
    public betPackValidationService: BetPackValidationService,
    private form: FormBuilder,
    private changeDetectorRef: ChangeDetectorRef,
  ) { }

  ngOnInit(): void {
    this.isedited = false;
    this.betpackCreateGroup();
    this.loadInitData();
    this.apiClientService.betpackService().getFilters().map((response: HttpResponse<FilterModel[]>) => response.body)
      .subscribe((filters: FilterModel[]) => {
        filters?.forEach((filter) => {
          if (filter.filterActive) {
            this.filters.push(filter);
          }
        });
      });

    this.sportsSurfaceBetsService.getSportCategories().subscribe((response) => {
      this.sportCategories = response;
    });
  }

  private betpackCreateGroup() {
    this.betPackEditData = this.form.group({
      betPackId: ['', [Validators.required, Validators.maxLength(25), Validators.pattern(/^[0-9]+$/)]],
      betPackTitle: ['', [Validators.required, Validators.maxLength(50)]],
      betPackPurchaseAmount: ['', [Validators.required, Validators.maxLength(4), Validators.pattern(/^[0-9]+$/)]],
      betPackFreeBetsAmount: ['', [Validators.required, Validators.maxLength(4), Validators.pattern(/^[0-9]+$/)]],
      betPackFrontDisplayDescription: ['', [Validators.required, Validators.maxLength(50)]],
      betPackMoreInfoText: ['', [Validators.required]],
      betPackSpecialCheckbox: [],
      sportsTag: ['', [Validators.required]],
      betPackStartDate: ['', [Validators.required]],
      betPackEndDate: ['', [Validators.required]],
      maxTokenExpirationDate: ['', [Validators.required]],
      id: [''],
      updatedBy: [''],
      updatedAt: [''],
      createdBy: [''],
      createdAt: [''],
      updatedByUserName: [''],
      createdByUserName: [''],
      futureBetPack: [],
      filterBetPack: [],
      filterList: [[]],
      isLinkedBetPack: [],
      linkedBetPackWarningText: [''],
      betPackActive: [],
      triggerID: ['', [Validators.required, Validators.pattern(/^[0-9]+$/)]],
      betPackTokenList: ['', [Validators.required, Validators.minLength(1)]],
      sortOrder: ['', [Validators.required]],
      brand: ['', [Validators.required]],
      deepLinkUrl: [''],
      maxClaims: ['', [Validators.required, Validators.min(1), Validators.pattern(/^[0-9]\d*$/)]],
    })
  }

  /**
   */
  get betpackEditControls() {
    return this.betPackEditData?.controls;
  }

  /**
 * loading betpack initial data
 * @param {boolean} isLoading -;
 */
  private loadInitData(isLoading: boolean = true): void {
    this.globalLoaderService.hideLoader();
    this.isLoading = isLoading;
    this.activatedRoute.params.subscribe((params: Params) => {
      this.hideAction = false;
      this.apiClientService.betpackService().getBetPackById(params['id'])
        .map((res: HttpResponse<BetPackModel>) => res.body)
        .subscribe((editBetPack: BetPackModel) => {
          this.betPackEditData.patchValue(editBetPack);
          this.hideAction = true;
          this.betPackTokenBeforeEdit = _.cloneDeep(this.betPackEditData.value.betPackTokenList);
          this.betPackStartDateBeforeEdit = _.cloneDeep(this.betPackEditData.value.betPackStartDate);
          this.betPackStartDateBeforeEdit = new Date(this.betPackStartDateBeforeEdit);
          this.isReady = true;
          this.updateValidators('isLinkedBetPack', 'linkedBetPackWarningText');
          this.updateValidators('filterBetPack', 'filterList');

          this.tokenListValidation();
          this.breadcrumbsData = [{
            label: 'Bet Packs',
            url: '/betpack-market/betpack-list'
          }, {
            label: this.betPackEditData.value.betPackTitle,
            url: `/betpack-market/${this.betPackEditData.value.id}`
          }];
          this.globalLoaderService.hideLoader();
          this.isLoading = false;
        }, () => {
          this.globalLoaderService.hideLoader();
          this.isLoading = false;
        });
    });
  }

  /**
   * @param  {string} key
   * @param  {string} dependentKey
   */
  private updateValidators(key: string, dependentKey: string): void {
    this.betPackEditData.get(key).valueChanges
      .subscribe(value => {
        if (value) {
          this.betPackEditData.get(dependentKey).setValidators(this.dynamicValidators)
        } else {
          this.betPackEditData.get(dependentKey).setValidators([]);
          this.betPackEditData.get(dependentKey).clearValidators();
          this.betPackEditData.controls[dependentKey].updateValueAndValidity();
        }
      });
  }

  /**
* To delete Betpack
* @returns - {void}
*/
  public removeBetPack(): void {
    const self = this;
    this.apiClientService.betpackService().deleteBetPack(this.betPackEditData.value.id).subscribe(() => {
      this.dialogService.showNotificationDialog({
        title: 'Remove Completed',
        message: 'BetPack is Removed.',
        closeCallback() {
          self.router.navigate([`betpack-market/betpack-list`]);
        }
      });
    });
  }

  /**
  * Save BetPack
  *  @returns - {void}
  */
  public saveChanges(): void {
    const self = this;
    this.hideAction = false;
    this.apiClientService.betpackService()
      .putBetPack(this.betPackEditData.value)
      .map((response: HttpResponse<BetPackModel>) => response.body)
      .subscribe((betPack: BetPackModel) => {
        this.hideAction = true;
        this.betPackEditData.patchValue(betPack);
        this.actionButtons.extendCollection(betPack);

        this.isedited = false;
        this.dialogService.showNotificationDialog({
          title: `Bet Pack Saving`,
          message: `Bet Pack is Saved.`,
          closeCallback() {
            self.router.navigate([`betpack-market/betpack-list/${self.betPackEditData.value.id}`]);
          }
        });
      });
  }

  /**
 * Set filters for betpack
 * @param {MatSelectChange} event -;
 * @returns - {void}
 */
  public setFilters(event: MatSelectChange): void {
    this.betPackEditData.value.filterList = event.value;
  }

  /**
  * to set action items remove,save and revert
  * @param {string} event -;
  * @returns - {void}
  */
  public actionsHandler(event: string): void {
    switch (event) {
      case 'remove':
        this.removeBetPack();
        break;
      case 'save':
        this.saveChanges();
        break;
      case 'revert':
        this.loadInitData();
        break;
      default:
        break;
    }
  }

  /**
   * End Date valid check
   * @returns - {boolean}
   */
  public isEndDateValid(): boolean {
    const displayFromDate = new Date(this.betPackEditData.value.betPackStartDate);
    const displayToDate = new Date(this.betPackEditData.value.betPackEndDate);
    return displayFromDate > displayToDate || (displayFromDate.getDate() === displayToDate.getDate() && displayFromDate.getTime() > displayToDate.getTime());
  }

  /**
   * To Disable Date if betpack start's
   */
  public isDateValid(): boolean {
    if (!this.isedited) {
      const displayFromDate = new Date(this.betPackStartDateBeforeEdit);
      const sysDate = new Date();
      return displayFromDate <= sysDate;
    }
  }
  /**
   Start Date valid check
   * @returns - {boolean}
   */
  public isStartDateValid(): boolean {
    const displayFromDate = new Date(this.betPackEditData.value.betPackStartDate);
    const sysDate = new Date();
    return displayFromDate <= sysDate;
  }
  /**
   * Handle data comes from dataTime component, set promotion property
   * @param {DateRange} data - startDate/endDate in toISOString();
   */
  public handleDisplayDateUpdate(data: DateRange): void {
    this.betPackEditData.value.betPackStartDate = data.startDate;
    this.betPackEditData.value.betPackEndDate = data.endDate;
  }

  /**
    * To remove the tokens
    * @param {number} index -;
    * @param {number} tokenId -;
    */
  public removeToken(index: number, tokenId: number): void {
    if (this.betPackEditData.value.betPackTokenList[index].tokenId === 0) {
      this.betPackEditData.value.betPackTokenList.splice(index, 1);
    } else if (this.betPackEditData.value.betPackTokenList[index].tokenId === tokenId) {
      this.betPackEditData.value.betPackTokenList = this.betPackEditData.value.betPackTokenList.filter((item) => item.tokenId !== tokenId);
    }
  }

  /**
  * On change of filter
  * @returns - {void}
  */
  public onFilterChange(): void {
    /*istanbul ignore else*/
    if (this.betPackEditData.value.filterBetPack) {
      this.betPackEditData.controls['filterList'].reset([]);
    }
  }

  /**
   * @returns any
   */
  onLinkedChange(): void {
    /*istanbul ignore else*/
    if (this.betPackEditData.value.isLinkedBetPack) {
      this.betPackEditData.controls['linkedBetPackWarningText'].reset();
    }
  }

  /**
   * To delete single token
   * @param {any} event -;
   * @returns - {void}
   */
  public removeTokenTable(event): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove Brand',
      message: 'Are You Sure You Want to Remove token?',
      yesCallback: () => {
        const betPackTokenbeforeDel = _.cloneDeep(this.betPackEditData.value.betPackTokenList);
        this.betPackEditData.value.betPackTokenList.splice(this.betPackEditData.value.betPackTokenList.indexOf(event), 1);
        /*istanbul ignore else*/
        if (betPackTokenbeforeDel.length !== this.betPackEditData.value.betPackTokenList.length) {
          this.isedited = true;
        }
        this.tokenListValidation()
      }
    });
  }

  /**
* To delete multiple tokens
* @param {any} event -;
* @returns - {void}
*/
  public removeHandlerMulty(event): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove Brand',
      message: 'Are You Sure You Want to Remove token?',
      yesCallback: () => {
        const betPackTokenbeforeDel = _.cloneDeep(this.betPackEditData.value.betPackTokenList);
        event.forEach(ele => {
          const index = this.betPackEditData.value.betPackTokenList.findIndex(el => el.tokenId === ele);
          this.betPackEditData.value.betPackTokenList.splice(index, 1);
        });
        /* istanbul ignore else */
        if (betPackTokenbeforeDel.length !== this.betPackEditData.value.betPackTokenList.length) {
          this.isedited = true;
        }
      }
    });
  }

  /**
* To create a tokens
* @returns - {void}
*/
  public createToken(): void {
    const tokenIDSet = new Set();
    const tokenArr = [];
    this.betPackEditData.value.betPackTokenList.forEach(ele => {
      tokenIDSet.add(ele.tokenId);
    });
    tokenIDSet.forEach(element => {
      tokenArr.push(element);
    });
    const dialogRef = this.dialog.open(BetPackTokenComponent, {
      width: '700px',
      data: { tokenArr }
    });

    dialogRef.afterClosed().subscribe(token => {
      this.isedited = true;
      if (token) {
        this.betPackEditData.value.betPackTokenList.push(token);
        this.betPackEditData.controls['betPackTokenList'].updateValueAndValidity()
      }
    });
  }

  /**
  * To edit a existing tokens
  * @returns - {void}
  */
  public editPageRoute(event): void {
    const tokenIDSet = new Set();
    const tokenArr = [];
    this.betPackEditData.value.betPackTokenList.forEach(ele => {
      tokenIDSet.add(ele.tokenId);
    });
    tokenIDSet.forEach(element => {
      tokenArr.push(element);
    });
    const dialogRef = this.dialog.open(BetPackTokenComponent, {
      width: '700px',
      data: { event, createEdit: true, tokenArr }
    });
    dialogRef.afterClosed().subscribe(token => {
      this.betPackEditData.value.betPackTokenList.forEach(ele => {
        if (ele.tokenId === event.tokenId) {
          this.index = this.betPackEditData.value.betPackTokenList.findIndex(el => el.tokenId === event.tokenId);
        }
      });
      this.betPackEditData.value.betPackTokenList[this.index] = token;
      /* istanbul ignore else */
      if (this.betPackTokenBeforeEdit !== this.betPackEditData.value.betPackTokenList) {
        this.isedited = true;
      }
    });
  }

  /**
   * End Date valid check
   *  @returns - {boolean}
   */
  public isTokenEndDateValid(): boolean {
    const displayFromDate = new Date(this.betPackEditData.value.betPackStartDate);
    const displayToDate = new Date(this.betPackEditData.value.maxTokenExpirationDate);
    return displayFromDate >= displayToDate;
  }

  /**
  * Handle data comes from dataTime component, set promotion property
  * @param {DateRange} data - startDate/maxtoken in toISOString();
  */
  public handleDisplayTokenDateUpdate(date: string): void {
    this.betPackEditData.value.maxTokenExpirationDate = new Date(date).toISOString();
  }

  updateMoreInfoText(data: string, key: string): void {
    this.betPackEditData.get(key).setValue(data);
    this.changeDetectorRef.detectChanges();
  }

  private tokenListValidation(): void {
    if (this.betPackEditData.value.betPackTokenList.length) {
      this.betPackEditData.controls['betPackTokenList'].setErrors(null);
    } else {
      this.betPackEditData.controls['betPackTokenList'].setErrors({ 'incorrect': true });
    }
  }
}

