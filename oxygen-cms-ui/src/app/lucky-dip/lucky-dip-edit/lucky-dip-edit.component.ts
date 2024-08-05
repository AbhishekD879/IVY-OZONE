import { Component, ViewChild } from '@angular/core';
import { NgForm } from '@angular/forms';
import { ApiClientService } from '@app/client/private/services/http';
import { BrandService } from '@app/client/private/services/brand.service';
import { DialogService } from '@app/shared/dialog/dialog.service';
import * as _ from 'lodash';
import { TinymceComponent } from '@app/shared/tinymce/tinymce.component';
import { LUCKYDIP_CONST } from '@app/lucky-dip/constants/luckydip.constants';
import { ActivatedRoute, Router } from '@angular/router';
import { Breadcrumb } from '@root/app/client/private/models';
import { LuckyDipV2 } from '../lucky-dip-v2.model';



@Component({
  selector: 'app-lucky-dip-edit',
  templateUrl: './lucky-dip-edit.component.html'
})

export class LuckyDipEditComponent {

  @ViewChild('luckyDipForm') luckyDipForm: NgForm;
  @ViewChild('actionButtons') actionButtons;
  @ViewChild('termsAndConditionsURL') tEditor: TinymceComponent;
  @ViewChild('welcomeMessage') descEditor: TinymceComponent;
  @ViewChild('title') titleEditor: TinymceComponent;

  luckyDip: LuckyDipV2 = {
    id: '',
    brand: this.brandService.brand,
    createdBy: '',
    createdAt: '',
    updatedBy: '',
    updatedAt: '',
    updatedByUserName: '',
    createdByUserName: '',
    description: '',
    luckyDipConfigLevel: '',
    luckyDipConfigLevelId: '',
    status: false,
    displayOnCompetitions: false,
    luckyDipBannerConfig: {
      animationImgPath: '',
      bannerImgPath: '',
      overlayBannerImgPath: ''
    },
    luckyDipFieldsConfig: {
      title: '',
      welcomeMessage: '',
      betPlacementTitle: '',
      betPlacementStep1: '',
      betPlacementStep2: '',
      betPlacementStep3: '',
      termsAndConditionsURL: '',
      playerCardDesc: '',
      potentialReturnsDesc: '',
      placebetCTAButton: '',
      backCTAButton: '',
      gotItCTAButton: '',
      depositButton: ''
    },
    playerPageBoxImgPath: '',
  };
  public readonly LUCKYDIP_CONST = LUCKYDIP_CONST;
  id: string;
  isReady: boolean;
  public breadcrumbsData: Breadcrumb[];

  constructor(
    private dialogService: DialogService,
    private brandService: BrandService,
    private apiClientService: ApiClientService,
    private route: ActivatedRoute,
    public router: Router
  ) {
    this.validationHandler = this.validationHandler.bind(this);
  }

  ngOnInit(): void {
    this.id = this.route.snapshot.paramMap.get('id');
    this.getLuckyDipDetails(this.id);
  }

  /**
 * Get lucky dip form.
 * @returns - {void}
 */
  public getLuckyDipDetails(id: string) {
    this.apiClientService.luckyDipService().getLuckyDipV2Data(id).subscribe((luckyDipV2: LuckyDipV2) => {
      if (luckyDipV2.id) {
        this.isReady = true;
        this.luckyDip = JSON.parse(JSON.stringify(luckyDipV2));
        this.breadcrumbsData = [{
          label: `Lucky Dip`,
          url: `/lucky-dip/v2`
        }, {
          label: this.luckyDip.description,
          url: `/luckydip/${this.luckyDip.id}`
        }];
        this.actionButtons.extendCollection(this.luckyDip);
        if (this.tEditor) {
          this.tEditor.update(this.luckyDip?.luckyDipFieldsConfig?.termsAndConditionsURL);
        }
        if (this.descEditor) {
          this.descEditor.update(this.luckyDip?.luckyDipFieldsConfig?.welcomeMessage);
        }
        if (this.titleEditor) {
          this.titleEditor.update(this.luckyDip?.luckyDipFieldsConfig?.title);
        }
      }
    }, error => {
      console.error(error.message);
    });
  }

  /**
   * update rich text box data
   * @returns - {void}
   */
  updateLuckyDip($event: Event, val: string): void {
    this.luckyDip[val.split('.')[0]][val.split('.')[1]] = $event;
  }

      /**
     * checks luckyDipConfigLevel
     * @returns - {boolean}
     */
      isSport(): boolean {
        if (this.luckyDip.luckyDipConfigLevel == 'Sports Category ID')
            return true;
    }
    
    /**
     * checks luckyDipConfigLevel
     * @returns - {boolean}
     */
    isType(): boolean {
        if (this.luckyDip.luckyDipConfigLevel == 'Type ID')
            return true;
    }
    
    
    /**
     * checks luckyDipConfigLevel
     * @returns - {boolean}
     */
    isEvent(): boolean {
        if (this.luckyDip.luckyDipConfigLevel == 'Event ID')
            return true;
    }

  /**
   * Save lucky dip form.
   * @returns - {void}
   */
  public saveChanges(): void {
    this.apiClientService
      .luckyDipService()
      .luckyDipV2Data(this.luckyDip, this.luckyDip?.id)
      .subscribe((luckyDipV2Data: LuckyDipV2) => {
        this.luckyDip = luckyDipV2Data;
        this.actionButtons.extendCollection(this.luckyDip);
        if (luckyDipV2Data) {
          this.dialogService.showNotificationDialog({
            title: 'Uploaded',
            message: 'Your Data is uploaded successfully',
            closeCallback: () => {
              this.router.navigate(['lucky-dip/v2']);
            }
          });
          this.luckyDipForm.form.markAsPristine();
        }
      }, error => {
        this.dialogService.showNotificationDialog({
          title: 'Error',
          message: error
        });
      });
  }
  /**
   * Send DELETE API request
   * @param {id} LuckyDipId
   * @returns void
   */
  public removeLuckyDip(id: string) {
    this.apiClientService.luckyDipService().deleteLuckyDip(id).subscribe(() => {
      this.router.navigate(['lucky-dip/v2']);
    }, error => {
      console.error(error.message);
    });
  }

  /**
     * check form fields.
     * @returns - {boolean}
     */
  public validationHandler(): boolean {
    return this.luckyDipForm?.valid && this.isValid();
  }

  /**
     * check rich text box fields.
     * @returns - {boolean}
     */
  isValid(): boolean {
    if (this.luckyDip.luckyDipFieldsConfig.title != '' && this.luckyDip.luckyDipFieldsConfig.welcomeMessage != ''
      && this.luckyDip.luckyDipFieldsConfig.termsAndConditionsURL != '')
      return true;
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeLuckyDip(this.id);
        break;
      case 'save':
        this.saveChanges();
        break;
      case 'revert':
        this.getLuckyDipDetails(this.id);
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

}
