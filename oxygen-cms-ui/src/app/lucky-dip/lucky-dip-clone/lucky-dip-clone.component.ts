import { Component, Inject, OnInit, ViewChild } from '@angular/core';
import * as _ from 'lodash';
import { NgForm } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from "@angular/material/dialog";
import { ConfirmDialogComponent } from "@app/shared/dialog/confirm-dialog/confirm-dialog.component";
import { GlobalLoaderService } from "@root/app/shared/globalLoader/loader.service";
import { LUCKYDIPFORM, LUCKYDIP_DEFAULT_VALUS } from '@app/lucky-dip/constants/luckydip.constants';
import { DialogData, IAddLuckyDip } from '../lucky-dip-v2.model';

@Component({
  selector: 'app-lucky-dip-clone',
  templateUrl: './lucky-dip-clone.component.html'
})
export class LuckyDipCloneComponent implements OnInit {
  public luckyDip: IAddLuckyDip;
  public readonly LUCKYDIPFORM: any = LUCKYDIPFORM;
  public isClone: boolean;
  public isLoading: boolean = false;
  private isCloned: boolean = false;
  private cloneModalData: IAddLuckyDip;
  @ViewChild('luckyDipForm') luckyDipForm: NgForm;

  constructor(
    @Inject(MAT_DIALOG_DATA) public modalData: DialogData,
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private globalLoaderService: GlobalLoaderService
  ) { }

  ngOnInit(): void {
    this.loadAddLuckyDipDefaults();
    this.isClone = this.modalData.data.dialogType === 'clone';
    if (this.isClone) {
      this.cloneModalData = { ...this.modalData.data.dialogData };
      this.cloneModalData.intialLuckyDipId = this.cloneModalData.id
      this.cloneModalData.luckyDipConfigLevel = "Sports Category ID";
      this.cloneModalData.description = "";
      this.cloneModalData.luckyDipConfigLevelId = "";
      this.populateCloneDetails();
    }
  }

  /**
   * Load default values for add luckyDip
   * @returns void
   */
  loadAddLuckyDipDefaults(): void {
    this.luckyDip = {
      ...LUCKYDIP_DEFAULT_VALUS,
    };
  }

  /**
   * Click handler for closing of modal dialog
   * @returns void
   */
  closeDialog(): void {
    this.dialogRef.close({ cloned: this.isCloned, closeCallback: true });
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
   * Returns the added luckyDip instance
   * @returns {IAddLuckyDip}
   */
  addLuckyDip(): IAddLuckyDip {
    if (this.isClone) {
      let { description, luckyDipConfigLevel, luckyDipConfigLevelId, ...cloneData } = this.cloneModalData
      Object.assign(this.luckyDip, cloneData);
    }
    return this.luckyDip
  }

  /**
   * Show or Hide spinner for the api calls
   * @param {boolean} toShow
   * @returns void
   */
  public showHideSpinner(toShow: boolean = true): void {
    toShow
      ? this.globalLoaderService.showLoader()
      : this.globalLoaderService.hideLoader();
    this.isLoading = toShow;
  }

  /**
   * To populate the values of the cloned luckyDip
   */
  private populateCloneDetails(): void {
    Object.keys(this.luckyDip).forEach(key => this.luckyDip[key] = this.cloneModalData[key]);
  }

}

