import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {ActivatedRoute, Params, Router} from '@angular/router';
import {AbstractControl, FormControl, FormGroup, Validators} from '@angular/forms';
import {HttpResponse} from '@angular/common/http';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {ApiClientService} from '@app/client/private/services/http';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {Breadcrumb} from '@app/client/private/models/breadcrumb.model';
import {AssetManagement, AssetManagementExt} from '@app/client/private/models/assetManagement.model';
import { ASSETMANAGEMENT } from '@app/asset-management/constants/asset-management-constants';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AppConstants } from '@app/app.constants';

@Component({
  templateUrl: './asset-management-edit.component.html',
  styleUrls: ['./asset-management-edit.component.scss'],
  providers: [
    DialogService
  ]
})
export class AssetManagementEditComponent implements OnInit {
  public isLoading: boolean = false;
  public assetManagement: AssetManagementExt;
  public form: FormGroup;
  public breadcrumbsData: Breadcrumb[];
  readonly teamImageLabel: string  = ASSETMANAGEMENT.EDIT.teamImage;
  readonly addLabel: string = ASSETMANAGEMENT.EDIT.add;
  readonly changeLabel: string = ASSETMANAGEMENT.EDIT.change;
  readonly fiveASideLabel: string = ASSETMANAGEMENT.EDIT.fiveasidetoggle;
  readonly highlightsToggleLabel: string = ASSETMANAGEMENT.EDIT.highlightstoggle;
  readonly errorMaxSizeMsg: string  = ASSETMANAGEMENT.EDIT.maxSize;
  
  @ViewChild('imageUploadInput') private imageUploadInput: ElementRef<HTMLInputElement>;;
  @ViewChild('actionButtons') actionButtons;

  constructor(
    private router: Router,
    private activatedRoute: ActivatedRoute,
    private apiClientService: ApiClientService,
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService,
    private snackBar: MatSnackBar,
  ) {
    this.isValidModel = this.isValidModel.bind(this);
  }

  ngOnInit(): void {
    this.form = new FormGroup({
      teamName: new FormControl('', [Validators.required]),
      secondaryNamesStr: new FormControl(''),
      sportId: new FormControl('', [Validators.required]),
      primaryColour: new FormControl('', [Validators.required]),
      secondaryColour: new FormControl('', [Validators.required]),
      teamsImage: new FormControl(null),
      fiveASideToggle : new FormControl(false),
      highlightCarouselToggle: new FormControl(false)
    });
    this.loadInitData();
  }

  /**
   * Used to show the upload popup when user clicks on the add btn
   * @returns { void }
   */
  public uploadImageHandler(): void {
    this.imageUploadInput.nativeElement.click();
  }

  /**
   * getter used to get the team image form control instance
   * @returns { AbstractControl }
   */
  public get teamsImage(): AbstractControl {
    return this.form.get('teamsImage');
  }


  /**
   * Used to upload the selected team image to the server
   * @param event { target: { files: File[] } }
   * @returns {void}
   */
  public handleImageChange(event: { target: { files: File[] } }): void {
    const [ file ] = event.target.files;
    const fileType = file && file.type;

    if (!(file && file.size)) {
      return;
    }
    
    if (fileType !== ASSETMANAGEMENT.EDIT.fileTypeSupported) {
      this.snackBar.open(ASSETMANAGEMENT.EDIT.fileTypeMsg, ASSETMANAGEMENT.EDIT.fileTypeAction, {
        duration: AppConstants.HIDE_DURATION,
      });
      this.form.controls.teamsImage.reset();
      return;
    }

    if (file.size > ASSETMANAGEMENT.EDIT.teamImageMaxFileSize) {
      this.form.controls.teamsImage.setErrors({'size': true});
      return;
    }
    
    if (this.assetManagement.id) {
      this.globalLoaderService.showLoader();
      this.apiClientService.assetManagements()
      .uploadTeamImage(this.assetManagement.id, file)
      .map((response: HttpResponse<AssetManagementExt>) => response.body)
      .subscribe((data: AssetManagementExt) => {
          this.assetManagement = data;
          this.actionButtons.extendCollection(data);
          this.snackBar.open(`${file.name} ${ASSETMANAGEMENT.EDIT.successupload}`, ASSETMANAGEMENT.EDIT.fileTypeAction, {
            duration: AppConstants.HIDE_DURATION,
          });
          this.globalLoaderService.hideLoader();
        }, error => {
          this.snackBar.open(`${file.name} ${ASSETMANAGEMENT.EDIT.failureupload}` , ASSETMANAGEMENT.EDIT.fileTypeAction, {
            duration: AppConstants.HIDE_DURATION,
          });
          this.form.controls.teamsImage.reset();
          this.globalLoaderService.hideLoader();
        });
    } 
  }

  /**
   * Used to change the label of the file upload depeneding on 
   * the image exist for the team or not
   * @returns {string}
   */
  getUploadBtnName(): string {
    return this.assetManagement.teamsImage ? this.changeLabel : this.addLabel ;
  }

  loadInitData(isLoading: boolean = true): void {
    this.globalLoaderService.showLoader();
    this.isLoading = isLoading;

    this.activatedRoute.params.subscribe((params: Params) => {
      this.apiClientService
        .assetManagements()
        .getSingleAssetManagement(params['id'])
        .map((assetManagement: HttpResponse<AssetManagement>) => {
          return assetManagement.body;
        }).subscribe((assetManagement: AssetManagement) => {
          this.assetManagement = assetManagement as AssetManagementExt;
          this.assetManagement.secondaryNamesStr = assetManagement.secondaryNames ? assetManagement.secondaryNames.toString() : '';
          this.setBreadcrumbsData();
          this.globalLoaderService.hideLoader();
          this.isLoading = false; 
        }, () => {
          this.globalLoaderService.hideLoader();
          this.isLoading = false;
        });
    });
  }

  private setBreadcrumbsData(): void {
    this.breadcrumbsData = [];
    this.breadcrumbsData.push({
      label: `Asset Management`,
      url: `/byb/asset-management`
    });
    this.breadcrumbsData.push({
      label: this.assetManagement.teamName,
      url: `/byb/asset-management/${this.assetManagement.id}`
    });
  }

  save(): void {
    this.globalLoaderService.showLoader();
    this.assetManagement.teamName = this.assetManagement.teamName.toUpperCase();
    this.assetManagement.secondaryNames = this.assetManagement.secondaryNamesStr
      ? this.assetManagement.secondaryNamesStr.split(',').map(item => item.trim().toUpperCase())
      : null;
    this.apiClientService.assetManagements()
      .editAssetManagement(this.assetManagement)
      .map((data: HttpResponse<AssetManagement>) => {
        return data.body;
      })
      .subscribe((data: AssetManagement) => {
        this.assetManagement = data as AssetManagementExt;
        this.assetManagement.secondaryNamesStr = data.secondaryNames ? data.secondaryNames.toString() : '';
        this.actionButtons.extendCollection(this.assetManagement);
        this.dialogService.showNotificationDialog({
          title: 'Asset Management',
          message: 'Asset Management is Saved.'
        });
        this.globalLoaderService.hideLoader();
      }, error => {
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  revert(): void {
    this.loadInitData();
  }

  remove(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.assetManagements()
      .deleteAssetManagement(this.assetManagement.id)
      .subscribe(() => {
        this.globalLoaderService.hideLoader();
        this.router.navigate(['/byb/asset-management/']);
      }, error => {
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.remove();
        break;
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

  isValidModel(assetManagement: AssetManagementExt): boolean {
    return this.form.valid && assetManagement && assetManagement.teamName !== '' && assetManagement.sportId
      && assetManagement.primaryColour !== '' && assetManagement.secondaryColour !== '';
  }
}
