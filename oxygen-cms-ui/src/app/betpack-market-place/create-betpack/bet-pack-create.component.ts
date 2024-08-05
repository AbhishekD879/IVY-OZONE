import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { ApiClientService } from '@app/client/private/services/http';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { SportCategory } from '@app/client/private/models/sportcategory.model';
import { BetPackModel, FilterModel, IToken } from '../model/bet-pack-banner.model';
import { SportsSurfaceBetsService } from '@app/sports-modules/surface-bets/surface-bets.service';
import { DateRange } from '@app/client/private/models';
import { HttpResponse } from '@angular/common/http';
import { MatSelectChange } from '@angular/material/select';
import { DataTableColumn } from '@app/client/private/models/dataTableColumn';
import { MatDialog } from '@angular/material/dialog';
import { BetPackTokenComponent } from '@app/betpack-market-place/betpack-token/betpack-token.component';
import * as _ from 'lodash';
import { Router } from '@angular/router';
import { BetPackValidationService } from '@app/promotions/service/bet-pack-validation.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { BrandService } from '@app/client/private/services/brand.service';

@Component({
  selector: 'bet-pack-create',
  templateUrl: './bet-pack-create.component.html',
  styleUrls: ['./bet-pack-create.component.scss']
})
export class BetPackCreateComponent implements OnInit {
  public sportCategories: SportCategory[] = [];
  public betPackData: BetPackModel;
  filters: FilterModel[] = [];
  searchField: string = '';
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
  dynamicValidators = [Validators.maxLength(100),Validators.required];
  tokenDelList: IToken[] = [];
  index: number;
  isedited: boolean = false;
  betPackCreateData: FormGroup;
  hideAction: boolean = false;

  constructor(
    private dialog: MatDialog,
    private dialogService: DialogService,
    private apiClientService: ApiClientService,
    private sportsSurfaceBetsService: SportsSurfaceBetsService,
    private brandService: BrandService,
    private router: Router,
    public betPackValidationService: BetPackValidationService,
    private form:FormBuilder,
    private cd: ChangeDetectorRef,
  ) { }


  ngOnInit(): void {
    this.betpackCreateGroup();
    this.setErrors(!this.betPackCreateData.value.betPackTokenList.length,'betPackTokenList')
    this.updateValidators('isLinkedBetPack','linkedBetPackWarningText');
    this.updateValidators('filterBetPack','filterList');
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

  private updateValidators(key: string, dependentKey: string): void {
    this.betPackCreateData.get(key).valueChanges
      .subscribe(value => {
        if (value) {
          this.betPackCreateData.get(dependentKey).setValidators(this.dynamicValidators)
        } else {
          this.betPackCreateData.get(dependentKey).setValidators([]);
          this.betPackCreateData.get(dependentKey).clearValidators();
          this.betPackCreateData.controls[dependentKey].updateValueAndValidity();
        }
      });
  }

  /**
   * @returns void
   */
  private betpackCreateGroup(): void {
    this.betPackCreateData = this.form.group({
      betPackId: [null, [Validators.required, Validators.maxLength(25),Validators.pattern(/^[0-9]+$/)]],
      betPackTitle: ['', [Validators.required, Validators.maxLength(50)]],
      betPackPurchaseAmount: [null, [Validators.required, Validators.maxLength(4),Validators.pattern(/^[0-9]+$/)]],
      betPackFreeBetsAmount: [null, [Validators.required, Validators.maxLength(4),Validators.pattern(/^[0-9]+$/)]],
      betPackFrontDisplayDescription: ['', [Validators.required, Validators.maxLength(50)]],
      betPackMoreInfoText: ['', [Validators.required]],
      betPackSpecialCheckbox: [false,[Validators.required]],
      sportsTag: [[], [Validators.required]],
      betPackStartDate: [null, [Validators.required]],
      betPackEndDate: [null, [Validators.required]],
      maxTokenExpirationDate: [new Date(), [Validators.required]],
      futureBetPack: [false,[Validators.required]],
      filterBetPack: [false,[Validators.required]],
      filterList: [[]],
      isLinkedBetPack: [false,[Validators.required]],
      linkedBetPackWarningText: [''],
      betPackActive: [false,[Validators.required]],
      triggerID: [null, [Validators.required,Validators.pattern(/^[0-9]+$/)]],
      betPackTokenList: [[],[Validators.required]],
      sortOrder: [''],
      brand: [this.brandService.brand, [Validators.required]],
      id: [''],
      updatedBy: [''],
      updatedAt: [''],
      createdBy: [''],
      createdAt: [''],
      updatedByUserName: [''],
      createdByUserName: [''],
      maxClaims: [null, [Validators.required,Validators.pattern(/^[0-9]+$/),Validators.min(1)]],
    })
  }

  get betpackDataControls() {
    return this.betPackCreateData?.controls;
  }

  /**
   */
  bpIsValid(): boolean {
    return this.betPackCreateData?.valid;
  }

  /**
  * Save BetPack
  * @returns - {void}
  */
  public saveBetPackChanges(): void {
    this.apiClientService.betpackService().postBetPack(this.betPackCreateData.value)
      .map((betpackResponse: HttpResponse<BetPackModel>) => betpackResponse.body)
      .subscribe(data => {
        this.betPackCreateData.value.id = data.id;
        this.finishBetPackCreation();
        this.hideAction = true;
      });
  }

  /**
  * Setting filter data
  * @returns - {void}
  */
  public setFilters(event: MatSelectChange): void {
    this.betPackCreateData.value.filterList = event.value;
  }

  /**
  * On betPack create Completion
  * @returns - {void}
  */
  public finishBetPackCreation(): void {
    this.isedited = false;
    const self = this;
    this.dialogService.showNotificationDialog({
      title: 'Save Completed',
      message: 'BetPack is Created and Stored.',
      closeCallback() {
        self.router.navigate([`betpack-market/betpack-list/${self.betPackCreateData.value.id}`]);
      }
    });
  }

  /**
   * End Date valid check
   */
  public isEndDateValid(): boolean {
    const displayFromDate = new Date(this.betPackCreateData.value.betPackStartDate);
    const displayToDate = new Date(this.betPackCreateData.value.betPackEndDate);
    return displayFromDate > displayToDate;
  }

  /**
   * Handle data comes from dataTime component, set promotion property
   * @param {DateRange} data - startDate/endDate in toISOString();
   */
  public handleDisplayDateUpdate(data: DateRange): void {
    this.betPackCreateData.value.betPackStartDate = data.startDate;
    this.betPackCreateData.value.betPackEndDate = data.endDate;
    this.betPackCreateData.patchValue({
      betPackStartDate: data.startDate,
      betPackEndDate: data.endDate
    })
    this.setErrors(new Date(this.betPackCreateData.value.betPackEndDate) < new Date(this.betPackCreateData.value.betPackStartDate),'betPackEndDate')
  }

  /**
  * On change of filter
  * @returns - {void}
  */
  public onFilterChange(): void {
    if (this.betPackCreateData.value.filterBetPack) {
      this.betPackCreateData.controls['filterList'].reset([]);
    }
  }

 /**
 * To delete single token
 * @returns - {void}
 */
  public removeTokenTable(event): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove Brand',
      message: 'Are You Sure You Want to Remove token?',
      yesCallback: () => {
        this.betPackCreateData.value.betPackTokenList.splice(this.betPackCreateData.value.betPackTokenList.indexOf(event), 1);
        if (this.betPackCreateData.value.betPackTokenList.length === 0) {
          this.isedited = false;
        }
        this.setErrors(!this.betPackCreateData.value.betPackTokenList.length,'betPackTokenList')
      }
    });
  }

  /**
 * To delete multiple tokens
 * @returns - {void}
 */
  public removeHandlerMulty(event): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove Brand',
      message: 'Are You Sure You Want to Remove token?',
      yesCallback: () => {
        event.forEach(ele => {
          const index = this.betPackCreateData.value.betPackTokenList.findIndex(el => el.tokenId === ele);
          this.betPackCreateData.value.betPackTokenList.splice(index, 1);
        });
        if (this.betPackCreateData.value.betPackTokenList.length === 0) {
          this.isedited = false;
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
    this.betPackCreateData.value.betPackTokenList.forEach(ele => {
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
        this.betPackCreateData.value.betPackTokenList.push(token);
        this.betPackCreateData.controls['betPackTokenList'].updateValueAndValidity();
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
    this.betPackCreateData.value.betPackTokenList.forEach(ele => {
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
      this.isedited = true;
      this.betPackCreateData.value.betPackTokenList.forEach(ele => {
        if (ele.tokenId === event.tokenId) {
          this.index = this.betPackCreateData.value.betPackTokenList.findIndex(el => el.tokenId === event.tokenId);
        }
      });
      this.betPackCreateData.value.betPackTokenList[this.index] = token;
    });
  }

  /**
   * Token Max End Date valid check
   * @returns - {boolean}
   */
  public isTokenEndDateValid(): boolean {
    const displayFromDate = new Date(this.betPackCreateData.value.betPackStartDate);
    const displayToDate = new Date(this.betPackCreateData.value.maxTokenExpirationDate);
    this.setErrors(displayFromDate > displayToDate,'maxTokenExpirationDate')
    return displayFromDate > displayToDate;
  }

  /**
  * Handle data comes from dataTime component, set promotion property
  * @param {DateRange} data - startDate/maxtoken in toISOString();
  */
  public handleDisplayTokenDateUpdate(date: string): void {
    this.betPackCreateData.value.maxTokenExpirationDate = new Date(date).toISOString();
    this.betPackCreateData.patchValue({
      maxTokenExpirationDate: this.betPackCreateData.value.maxTokenExpirationDate
    })
  }
  
  /**
   * @param  {string} event
   * @returns void
   */
  setInfoText(event: string): void {
    this.betPackCreateData.value.betPackMoreInfoText = event;
    this.betPackCreateData.controls['betPackMoreInfoText'].setValue(event);
    this.betPackCreateData.controls["betPackMoreInfoText"].updateValueAndValidity();
    this.cd.detectChanges();
  }

  /**
   * @param  {} condition
   * @param  {} dependentkey
   */
  private setErrors(condition: boolean ,dependentkey: string): void{
    if(condition) {
      this.betPackCreateData.controls[dependentkey].setErrors({'incorrect': true});
    } else {
      this.betPackCreateData.controls[dependentkey].setErrors(null);
    }
  }
}
