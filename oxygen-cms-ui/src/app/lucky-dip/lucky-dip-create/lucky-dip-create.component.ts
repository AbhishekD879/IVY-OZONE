import { Component, ViewChild } from '@angular/core';
import { NgForm } from '@angular/forms';
import { ApiClientService } from '@app/client/private/services/http';
import { BrandService } from '@app/client/private/services/brand.service';
import { DialogService } from '@app/shared/dialog/dialog.service';
import * as _ from 'lodash';
import { TinymceComponent } from '@app/shared/tinymce/tinymce.component';
import { LUCKYDIP_CONST } from '@app/lucky-dip/constants/luckydip.constants';
import { Router } from '@angular/router';
import { LuckyDipV2 } from '../lucky-dip-v2.model';

@Component({
    selector: 'app-lucky-dip-create',
    templateUrl: './lucky-dip-create.component.html'
})

export class LuckyDipCreateComponent {

    breadcrumbsData = [{
        label: `Lucky Dip`,
        url: `/lucky-dip/v2`
    }, {
        label: 'Create Lucky dip ',
        url: `/lucky-dip/create`
    }];
    @ViewChild('luckyDipForm') luckyDipForm: NgForm;
    @ViewChild('termsAndConditionsURL') tEditor: TinymceComponent;
    @ViewChild('welcomeMessage') wsEditor: TinymceComponent;
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
        luckyDipConfigLevel: 'Sports Category ID',
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

    constructor(
        private dialogService: DialogService,
        private brandService: BrandService,
        private apiClientService: ApiClientService,
        private router: Router
    ) { }

    ngOnInit(): void {
    }

    /**
     * update rich text box data
     * @returns - {void}
     */
    updateLuckyDip($event: Event, val: string): void {
        this.luckyDip[val.split('.')[0]][val.split('.')[1]] = $event;
    }

    /**
     * check if form is valid.
     * @returns - {boolean}
     */
    disableSave(): boolean {
        return this.luckyDipForm?.valid && this.isValid();
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
     * check rich text box fields.
     * @returns - {boolean}
     */
    isValid(): boolean {
        if (this.luckyDip.luckyDipFieldsConfig.title != '' && this.luckyDip.luckyDipFieldsConfig.welcomeMessage != ''
            && this.luckyDip.luckyDipFieldsConfig.termsAndConditionsURL != '')
            return true;
    }

    /**
     * Save lucky dip form.
     * @returns - {void}
     */
    saveChanges(): void {
        this.apiClientService
            .luckyDipService()
            .luckyDipV2Data(this.luckyDip, this.luckyDip?.id)
            .subscribe((luckyDipV2Data: LuckyDipV2) => {
                this.luckyDip = luckyDipV2Data;
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

}
