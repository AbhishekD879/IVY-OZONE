import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { BrandService } from '@app/client/private/services/brand.service';
import { IMAGE_MANAGER_SVG_ID_PATTERN } from '@app/image-manager/constants/image-manager.constant';
import { ApiClientService } from '@app/client/private/services/http';
import { HttpResponse } from '@angular/common/http';
import { MystableModel } from '@app/mystable-configurations/mystable.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AppConstants } from '../app.constants';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { MyStableConstants } from '@app/mystable-configurations/mystable-configurations.constants'


@Component({
  selector: 'app-mystable-configurations',
  templateUrl: './mystable-configurations.component.html',
  styleUrls: ['./mystable-configurations.component.scss']
})
export class MystableConfigurationsComponent implements OnInit {

  public MyStableConstants: any = MyStableConstants;
  public disabled: boolean = false;
  public carousel: boolean = false;
  public antepost: boolean = false;
  public mybets: boolean = false;
  public settledBets: boolean = false;
  public crcActive: boolean = false;
  public myStableForm: FormGroup;
  public myStableData: MystableModel;
  public isLoading: boolean = false;
  public hideAction: boolean = true;
  public myStableEntryPoint: object = {};
  public stableIcon: object = {};
  public saveStableIcon: object = {};
  public noteIcon: object = {};
  public myStableSignposting: object = {};
  public myStableNotesSignposting: object = {};
  public myStableBookmarkIcon: object = {};
  public myStableInprogressBookmarkIcon: object = {};
  public myStableUnbookmarkIcon: object = {};
  public myStableNoHorsesIcon: object = {};
  public myStableTodayRunningHorseCarousel: object = {};
  public crcLogoImage: object = {};
  public crcSignposting: object = {};
  public crcWhiteBookmark: object = {};
  public crcBlackBookmark: object = {};
  public isCoral: boolean;

  constructor(
    private brandService: BrandService,
    private formBuilder: FormBuilder,
    private apiClientService: ApiClientService,
    private snackBar: MatSnackBar,
    private globalLoaderService: GlobalLoaderService
  ) {
  }

  ngOnInit(): void {
    this.myStableformData();
    this.loadIntialData();
    this.isCoral = (this.brandService.brand === 'bma')
    if (this.isCoral) {
      this.myStableForm.addControl('crcActive', this.formBuilder.control(false, [Validators.required]));
      this.myStableForm.addControl('crcLabel', this.formBuilder.control('', [Validators.required, Validators.maxLength(100)]));
      this.myStableForm.addControl('crcSaveAllText', this.formBuilder.control('', [Validators.required, Validators.maxLength(15)]));
      this.myStableForm.addControl('crcGotoRacingClubText', this.formBuilder.control('', [Validators.required, Validators.maxLength(30)]));
      this.myStableForm.addControl('crcGotoRacingClubUrl', this.formBuilder.control('', [Validators.required, Validators.maxLength(100)]));
    }
  }

  get mystableDataControls() {
    return this.myStableForm?.controls;
  }

  activeStatus(): void {
    this.disabled = !this.disabled;
  }

  carouselStatus(): void {
    this.carousel = !this.carousel;
  }

  antepostStatus(): void {
    this.antepost = !this.antepost;
  }

  myBetsStatus(): void {
    this.mybets = !this.mybets;
  }

  settledbetsStatus(): void {
    this.settledBets = !this.settledBets;
  }

  crcActiveStatus(): void {
    this.crcActive = !this.crcActive;
  }

  loadIntialData(isLoading: boolean = true): void {
    this.showHideSpinner();
    this.hideAction = false;
    this.apiClientService.myStableService().getMyStableData().map((response: HttpResponse<MystableModel>) => response.body)
      .subscribe((res: MystableModel) => {
        if (res) {
          this.myStableData = res;
          this.disabled = res.active;
          this.carousel = res.horsesRunningToday;
          this.antepost = res.antePost;
          this.mybets = res.mybets;
          this.settledBets = res.settledBets;
          this.crcActive = res.crcActive;
          this.myStableForm.patchValue(res);
          this.hideAction = true;
          this.showHideSpinner(false);
        } else {
          this.hideAction = true;
          this.showHideSpinner(false);
        }
      })
  }

  myStableformData(): void {
    this.myStableForm = this.formBuilder.group({
      brand: [this.brandService.brand, [Validators.required]],
      active: [false, [Validators.required]],
      entryPointLabel: ['', [Validators.required, Validators.maxLength(15),]],
      editLabel: ['', [Validators.required, Validators.maxLength(15)]],
      saveLabel: ['', [Validators.required, Validators.maxLength(15)]],
      horsesRunningToday: [false, [Validators.required]],
      antePost: [false, [Validators.required]],
      emptyStableLabel1: ['', [Validators.required, Validators.maxLength(30)]],
      noHorsesCtaButton: ['', [Validators.required, Validators.maxLength(30)]],
      emptyStableLabel2: ['', [Validators.required, Validators.maxLength(100)]],
      todayRunningHorsesText: ['', [Validators.required, Validators.maxLength(50)]],
      horseCountExceededMsg: ['', [Validators.required, Validators.maxLength(100)]],
      mybets: [false, [Validators.required]],
      stableTooltipText: ['',[ Validators.maxLength(50)]],
      settledBets: [false, [Validators.required]],
    });
  }

  ngAfterViewChecked(): void {
    this.myStableForm.get('entryPointIcon')?.setValidators([Validators.required, Validators.minLength(3), Validators.pattern(IMAGE_MANAGER_SVG_ID_PATTERN)]);
    this.myStableForm.get('editIcon')?.setValidators([Validators.required, Validators.minLength(3), Validators.pattern(IMAGE_MANAGER_SVG_ID_PATTERN)]);
    this.myStableForm.get('saveIcon')?.setValidators([Validators.required, Validators.minLength(3), Validators.pattern(IMAGE_MANAGER_SVG_ID_PATTERN)]);
    this.myStableForm.get('editNoteIcon')?.setValidators([Validators.required, Validators.minLength(3), Validators.pattern(IMAGE_MANAGER_SVG_ID_PATTERN)]);
    this.myStableForm.get('signpostingIcon')?.setValidators([Validators.required, Validators.minLength(3), Validators.pattern(IMAGE_MANAGER_SVG_ID_PATTERN)]);
    this.myStableForm.get('notesSignPostingIcon')?.setValidators([Validators.required, Validators.minLength(3), Validators.pattern(IMAGE_MANAGER_SVG_ID_PATTERN)]);
    this.myStableForm.get('bookmarkIcon')?.setValidators([Validators.required, Validators.minLength(3), Validators.pattern(IMAGE_MANAGER_SVG_ID_PATTERN)]);
    this.myStableForm.get('inProgressIcon')?.setValidators([Validators.required, Validators.minLength(3), Validators.pattern(IMAGE_MANAGER_SVG_ID_PATTERN)]);
    this.myStableForm.get('unbookmarkIcon')?.setValidators([Validators.required, Validators.minLength(3), Validators.pattern(IMAGE_MANAGER_SVG_ID_PATTERN)]);
    this.myStableForm.get('noHorsesIcon')?.setValidators([Validators.minLength(3), Validators.pattern(IMAGE_MANAGER_SVG_ID_PATTERN)]);
    this.myStableForm.get('todayRunningHorsesSvg')?.setValidators([Validators.required, Validators.minLength(3), Validators.pattern(IMAGE_MANAGER_SVG_ID_PATTERN)]);
    this.myStableForm.get('crcLogo')?.setValidators([Validators.required, Validators.minLength(3), Validators.pattern(IMAGE_MANAGER_SVG_ID_PATTERN)]);
    this.myStableForm.get('crcSignPostingIcon')?.setValidators([Validators.required, Validators.minLength(3), Validators.pattern(IMAGE_MANAGER_SVG_ID_PATTERN)]);
    this.myStableForm.get('crcWhiteBookmarkIcon')?.setValidators([Validators.required, Validators.minLength(3), Validators.pattern(IMAGE_MANAGER_SVG_ID_PATTERN)]);
    this.myStableForm.get('crcBlackBookmarkIcon')?.setValidators([Validators.required, Validators.minLength(3), Validators.pattern(IMAGE_MANAGER_SVG_ID_PATTERN)]);
  }

  /**
* To show or hide spinner
* @param {boolean} toShow
*/
  private showHideSpinner(toShow: boolean = true): void {
    toShow ? this.globalLoaderService.showLoader() : this.globalLoaderService.hideLoader();
    this.isLoading = toShow;
  }

  public actionsHandler(event: string): void {
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

  save(isLoading: boolean = true): void {
    this.showHideSpinner();
    this.hideAction = false;
    if (this.myStableData && this.myStableData.id) {
      this.apiClientService.myStableService().putMyStableData(this.myStableForm.value, this.myStableData.id).map((response: HttpResponse<MystableModel>) => response.body)
        .subscribe(res => {
          if (res) {
            this.myStableData = res;
            this.hideAction = true;
            this.loadIntialData();
            this.snackBar.open('My Stable Configuration Is Updated.', 'Ok!', {
              duration: AppConstants.HIDE_DURATION,
            });
            this.showHideSpinner(false);
          }
        });
    } else {
      this.apiClientService.myStableService().postMyStableData(this.myStableForm.value).map((response: HttpResponse<MystableModel>) => response.body)
        .subscribe(res => {
          if (res) {
            this.myStableData = res;
            this.hideAction = true;
            this.loadIntialData();
            this.snackBar.open('My Stable Configuration Is Saved.', 'Ok!', {
              duration: AppConstants.HIDE_DURATION,
            });
            this.showHideSpinner(false);
          }
        });
    }
  }


  revert(): void {
    this.loadIntialData();
  }

  crcLabelValidate(): void {
    if (this.myStableForm.get('crcLabel').value.length > 100) {
      this.myStableForm.get('crcLabel').setErrors({ 'maxlength': true });
    }
  }

  crcSaveAllTextValidate(): void {
    if (this.myStableForm.get('crcSaveAllText').value.length > 15) {
      this.myStableForm.get('crcSaveAllText').setErrors({ 'maxlength': true });
    }
  }
  crcGotoRacingClubTextValidate(): void {
    if (this.myStableForm.get('crcGotoRacingClubText').value.length > 30) {
      this.myStableForm.get('crcGotoRacingClubText').setErrors({ 'maxlength': true });
    }
  }
  crcGotoRacingClubUrlValidate(): void {
    if (this.myStableForm.get('crcGotoRacingClubUrl').value.length > 100) {
      this.myStableForm.get('crcGotoRacingClubUrl').setErrors({ 'maxlength': true });
    }
  }
}
