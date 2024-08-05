import { Component, OnInit, ViewChild } from '@angular/core';
import { SportsModule } from '@app/client/private/models/homepage.model';
import { ILotto, ILottos } from '../lotto.model';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { BrandService } from '@app/client/private/services/brand.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { ApiClientService } from '@app/client/private/services/http';
import { HttpResponse } from '@angular/common/http';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import * as _ from 'lodash';
import {AppConstants} from '@app/app.constants';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { LOTTOS_VALUES } from '../lotto.constants';
@Component({
  selector: 'app-lotto-details',
  templateUrl: './lotto-details.component.html'
})
export class LottoDetailsComponent implements OnInit {
  @ViewChild('actionButtons') actionButtons;
  public module: SportsModule;
  public lotto: ILottos
  public mainLotto: ILotto
  breadcrumbsData: Breadcrumb[];
  public isIMActive: boolean;
  public form: FormGroup;
  brand: string = this.brandService.brand;
  lottoForm: FormGroup;
  public error: string;
  id: string;
  initialTitle: string;
  public isLoading: boolean = false;
  public pageType: string;
  public valid: string = '';
    component: ILotto;
  constructor(
    private brandService: BrandService,
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService,
    private snackBar: MatSnackBar,
    private dialogService: DialogService,
    private route: ActivatedRoute,
    private router: Router,
    ) { 
      this.isIMActive = this.brandService.isIMActive();
    }
  ngOnInit() {
    this.loadInitialData();
  }
  updateBlurb(newBlurbText: string, field: string, infoTitle: string): void {
     this.lottoForm.controls[infoTitle].setValue(newBlurbText);
     this.lotto[field] = this.lottoForm.controls[infoTitle].value;
     this.valid = this.lottoForm.controls[infoTitle].value.replace(/<(.|\n)*?>|&(.|\n)*?;/g, '');
     this.isValid();
  }
  isValid(){
    return this.valid.length > 500;
  }
  private loadInitialData(isLoading: boolean = true): void {
    this.globalLoaderService.showLoader();
    this.isLoading = isLoading;
    this.route.params.subscribe((params: Params) => {
      this.pageType = params.id ? 'edit' : 'add';
      if(this.pageType === 'edit') {
        this.apiClientService.lottosService()
        .getLottery(params['id'])
        .map((lotto: HttpResponse<ILottos>) => {
          return lotto.body;
        }).subscribe((lotto: ILottos) => {
          this.lotto = lotto;
          this.actionButtons?.extendCollection(this.lotto)
          this.setBreadcrumbsData();
          this.createFormGroup();
          this.globalLoaderService.hideLoader();
              this.isLoading = false;
            }, () => {
              this.globalLoaderService.hideLoader();
              this.isLoading = false;
        })
      } else {
        this.lotto = {...LOTTOS_VALUES}
        this.setBreadcrumbsData(true);
        this.globalLoaderService.hideLoader();
        this.isLoading = false;
        this.createFormGroup();  
      }
    })
  }
  createFormGroup() {
      this.lottoForm = new FormGroup ({
        infoTitle: new FormControl(this.lotto.infoMessage || '', [Validators.required])
      })
  }
  private setBreadcrumbsData(isNewLotto: boolean = false): void {
    this.breadcrumbsData = [];
    this.breadcrumbsData.push({
      label: `Lotto Page`,
      url: `/lotto`
    });
    if (isNewLotto) {
      this.breadcrumbsData.push({
        label: `New lotto`,
        url: `/lotto/add`
      });
    } else {
      this.breadcrumbsData.push({
        label: this.lotto.label,
        url: `/lotto/${this.lotto.id}`
      });
    }
  }
  public isValidModel(Lottery: ILottos): boolean {
    return Lottery && Lottery.label && Lottery.label.length <= 50 && 
          Lottery.infoMessage && Lottery.infoMessage.length <= 500 && 
          Lottery.nextLink && Lottery.nextLink.length > 0 &&
          Lottery.ssMappingId && Lottery.ssMappingId.length <= 20 &&
          Lottery.svgId && Lottery.svgId.length > 0  && 
          Lottery.maxPayOut && Lottery.maxPayOut > 0 ;
  }

  public isNewLottoValid(): boolean {
    return !!( this.lotto && this.lotto.label && this.lotto.label.length <= 50
              && this.lotto.ssMappingId && this.lotto.ssMappingId.length <= 20 &&
              this.lotto.nextLink && this.lotto.nextLink.length > 0 )
  }
  createSegment(): void {
    this.dialogService.showConfirmDialog({
      title: `Create Segment: ${this.lotto.label}`,
      message: `Do You Want to Create a Lotto?`,
      yesCallback: () => {
        this.sendNewSegmentInformation();
      }
    });
  }
  public sendNewSegmentInformation(): void {
    this.lotto.brand = this.brand;
    this.apiClientService
      .lottosService()
      .saveLotto(this.lotto)
      .subscribe(data => {
        this.createFormGroup();
        this.lotto.id = data.body.id;
        this.dialogService.showNotificationDialog({
          title: 'Creating Completed',
          message: 'The Segment is Successfully Created.'
        });
        this.router.navigate([`/lotto/${this.lotto.id}`]);
      });
  }
  uploadSvgHandler(file): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.lottosService()
      .uploadSvg(this.lotto.id, file)
      .map((data: HttpResponse<ILotto>) => {
        return data.body;
      })
      .subscribe((data: ILotto) => {
        this.mainLotto = _.extend(data, _.pick(this.lotto, Object.keys(this.form.controls)));
        this.snackBar.open(`Svg Uploaded.`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });
        this.globalLoaderService.hideLoader();
      }, () => {
        this.globalLoaderService.hideLoader();
      });
  }
  actionsHandler(event: string): void {
    switch (event) {
      case 'save':
        this.save();
        break;
      case 'revert':
        this.revert();
        break;
      case 'remove':
        this.removeModule();
        break;
      default:
        break;
    }
  }
  public removeModule(): void {
    this.apiClientService.lottosService().remove(this.lotto.id)
    .subscribe(() => {
      this.router.navigate([`/lotto`])
    })
  }
  private save(): void {
    if (this.lotto.createdAt) {
      this.sendRequest('updateLottoDetails');
    } else {
      this.sendRequest('saveLotto');
    }
  }
  private revert(): void {
    this.loadInitialData();
  }
private sendRequest(requestType: string): void {
  this.lotto.brand = this.brand;
  this.globalLoaderService.showLoader();
  this.apiClientService.lottosService()[requestType](this.lotto)
    .map((response) => response.body)
    .subscribe((data: ILottos) => {
      this.lotto = data;
      this.actionButtons?.extendCollection(this.lotto);
      this.dialogService.showNotificationDialog({
        title: 'Success',
        message: 'Your changes have been saved'
      });
      this.globalLoaderService.hideLoader();
    }, error => {
      this.dialogService.showNotificationDialog({
        title: 'Error on saving',
        message: 'Ooops... Something went wrong, please contact support team'
      });
      this.globalLoaderService.hideLoader();
    });
}
}
