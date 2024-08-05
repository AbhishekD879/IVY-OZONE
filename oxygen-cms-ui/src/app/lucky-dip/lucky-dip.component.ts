import { Component, OnInit, ViewChild } from '@angular/core';
import { NgForm } from '@angular/forms';
import { ApiClientService } from '@app/client/private/services/http';
import { BrandService } from '@app/client/private/services/brand.service';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { LuckyDip } from '@app/lucky-dip/lucky-dip.model';
import * as _ from 'lodash';
import { TinymceComponent } from '../shared/tinymce/tinymce.component';

@Component({
  selector: 'lucky-dip',
  templateUrl: './lucky-dip.component.html',
  styleUrls: ['./lucky-dip.component.scss']
})

export class LuckyDipComponent implements OnInit {
    @ViewChild('luckyDipForm') luckyDipForm: NgForm;
    @ViewChild('termsAndConditionsURL') tEditor: TinymceComponent;
    @ViewChild('marketDesc') descEditor: TinymceComponent;
    @ViewChild('title') titleEditor: TinymceComponent;

    luckyDip: LuckyDip = {
        id: '',
        brand: this.brandService.brand,
        createdBy: '',
        createdAt: '',
        updatedBy: '',
        updatedAt: '',
        updatedByUserName: '',
        createdByUserName: '',
        luckyDipBannerConfig: {
            animationImgPath: '',
            bannerImgPath: '',
            overlayBannerImgPath: ''
        },
        luckyDipFieldsConfig: {
            title: '',
            desc: '',
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
    luckyDipCopy: LuckyDip = {} as LuckyDip;
    disableSaveBtn: boolean;

    constructor(
        private dialogService: DialogService,
        private brandService: BrandService,
        private apiClientService: ApiClientService
    ) { }

    ngOnInit(): void {
        this.loadInitialData();
    }

    /**
     * update rich text box data
     * @returns - {void}
     */
    updateLuckyDip($event: Event, val: string): void {
      this.luckyDip[val.split('.')[0]][val.split('.')[1]] = $event;
    }

    /**
     * load existing luckyDip data
     * @returns - {void}
     */
    loadInitialData(): void {
        this.apiClientService
            .luckyDipService()
            .getLuckyDipData()
            .subscribe((data: LuckyDip) => {
                if (data.id) {
                    this.luckyDip = JSON.parse(JSON.stringify(data));
                    this.luckyDipCopy = JSON.parse(JSON.stringify(data));
                    if (this.tEditor) {
                      this.tEditor.update(this.luckyDip.luckyDipFieldsConfig.termsAndConditionsURL);
                    }
                    if (this.descEditor) {
                        this.descEditor.update(this.luckyDip.luckyDipFieldsConfig.desc);
                    }
                    if (this.titleEditor) {
                        this.titleEditor.update(this.luckyDip.luckyDipFieldsConfig.title);
                    }
                }
            });
    }

    /**
     * check if form is valid.
     * @returns - {boolean}
     */
    disableSave(): boolean {
        if (this.luckyDipForm?.form.dirty) {
            return (!this.luckyDipForm?.form.valid || this.luckyDip.luckyDipFieldsConfig.termsAndConditionsURL === '' || this.luckyDip.luckyDipFieldsConfig.desc === '' 
            || this.luckyDip.luckyDipFieldsConfig.title === '');
        }
        return true;
    }

    /**
     * Save lucky dip form.
     * @returns - {void}
     */
    saveChanges(): void {
        this.apiClientService
            .luckyDipService()
            .luckyDipData(this.luckyDip, this.luckyDip?.id)
            .subscribe((luckyDipData: LuckyDip) => {
             this.luckyDip = luckyDipData;
             this.luckyDipCopy = JSON.parse(JSON.stringify(luckyDipData));
            if (luckyDipData) {
                this.dialogService.showNotificationDialog({
                title: 'Uploaded',
                message: 'Your Data is uploaded successfully'
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
  * create Luckydip button  disabled check
  */
  isEqualCollection() {
    return _.isEqual(this.luckyDip, this.luckyDipCopy);
  }

}
