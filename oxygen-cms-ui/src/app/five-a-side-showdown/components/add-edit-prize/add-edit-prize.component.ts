import { Component, ElementRef, Inject, OnInit, ViewChild } from '@angular/core';
import { NgForm } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { BrandService } from '@app/client/private/services/brand.service';
import { UPLOAD_BTNS } from '@app/five-a-side-showdown/constants/contest-manager.constants';
import {
  DEFAULT_FILENAME, ICON_PROPERTIES, PRIZE_DEFAULT_VALUES, PRIZE_FORM, PRIZE_MANAGER_FORM_ERRORS,
  PRIZE_TYPES, PRIZE_TYPES_MAPPER, SIGNPOSTING_PROPERTIES, SUPPORTED_FILE_TYPES,
  SVG_ERROR_NOTIFICATION
} from '@app/five-a-side-showdown/constants/pay-table.constants';
import { HTMLInputEvent } from '@app/five-a-side-showdown/models/contest-manager';
import { IPrize } from '@app/five-a-side-showdown/models/prize-manager';
import { ConfirmDialogComponent } from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import { DialogService } from '@app/shared/dialog/dialog.service';

@Component({
  selector: 'app-add-edit-prize',
  templateUrl: './add-edit-prize.component.html',
  styleUrls: ['./add-edit-prize.component.scss'],
})
export class AddEditPrizeComponent implements OnInit {
  @ViewChild('prizeForm') prizeForm: NgForm;
  @ViewChild('signpostingSvgFileInput')
  signpostingSvgFileInput: ElementRef<HTMLInputElement>;

  @ViewChild('iconSvgFileInput') iconSvgFileInput: ElementRef<HTMLInputElement>;
  prize: IPrize;
  prizeTypes: string[] = PRIZE_TYPES;
  prizeTypesMapper: any = PRIZE_TYPES_MAPPER;
  errors: {[key: string]: string} = PRIZE_MANAGER_FORM_ERRORS;
  title: string;
  readonly PRIZE_FORM: {[key: string]: string} = PRIZE_FORM;
  constructor(private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private dialogService: DialogService,
    private brandService: BrandService,
    @Inject(MAT_DIALOG_DATA) public dialog: { title: string, data: IPrize}) { }

  ngOnInit(): void {
    this.prize = {
      ...this.prize,
      ...PRIZE_DEFAULT_VALUES,
      icon: {...DEFAULT_FILENAME},
      signPosting: {...DEFAULT_FILENAME},
      brand: this.brandService.brand,
      ...JSON.parse(JSON.stringify(this.dialog.data))
    };
    this.validateSvgFile('icon');
    this.validateSvgFile('signPosting');
    this.title = this.dialog.title;
    this.setSVGImage(ICON_PROPERTIES.OUTPUT, ICON_PROPERTIES.INPUT);
    this.setSVGImage(SIGNPOSTING_PROPERTIES.OUTPUT, SIGNPOSTING_PROPERTIES.INPUT);
  }

  /**
   * Run file type and size validations,
   *  update related file fields
   *
   * @param event
   */
  validateAndUpdateFileFields(event: { target: { files: File[] }},
    fieldName: string): void {
    const file = event.target.files[0];

    if (!file) { return; }

    const fileType = file.type;

    if (!SUPPORTED_FILE_TYPES.includes(fileType)) {
      this.dialogService.showNotificationDialog({
        title: SVG_ERROR_NOTIFICATION.title,
        message: SVG_ERROR_NOTIFICATION.message
      });
      return;
    } else {
      this.prize[fieldName].originalname = file.name;
      this.prize[fieldName].svgId = this.transformName(file.name);
      this.updatePrizeImages(file, fieldName);
    }
  }

  /**
   * Handle the click for upload image
   * @param {HTMLInputEvent} event
   */
  handleUploadImageClick(event: HTMLInputEvent): void {
    const input = event.target.parentElement.previousElementSibling.querySelector(
      'input'
    );
    input.click();
  }

  /**
   * Get the button name for the upload
   * @param {string} fileName
   */
  getButtonName(fileName: string): string {
    return fileName && fileName.length > 0
      ? UPLOAD_BTNS.changeFileLabel
      : UPLOAD_BTNS.uploadFileLabel;
  }

  /**
   * To avoid special characters
   * @param  event
   * @returns
   */
    blockSpecialChars(event: HTMLInputEvent): void {
      event.target.value = event.target.value.replace(/[^a-zA-Z0-9]/g, '');
    }

  /**
   * To save changes
   */
  saveChanges(): IPrize {
    return this.prize;
  }

  /**
   * Handling white spaces between numbers
   * @param  {} isEntries
   */
  handleWhiteSpaces(isEntries) {
    if (isEntries) {
      this.prize.numberOfEntries = this.prize.numberOfEntries.replace(/\s/g, '');
    } else {
      this.prize.percentageOfField = this.prize.percentageOfField.replace(/\s/g, '');
    }
  }

  /**
   * To remove toggle on other than freebet types
   */
  onPrizeTypeChange($event): void {
    if ($event.value === this.prizeTypesMapper.FREEBET && !this.dialog.data.freebetOfferId) {
      this.prize.freebetOfferId = this.dialog.data.defaultOfferIds.freebetOfferId;
    }

    if ($event.value === this.prizeTypesMapper.TICKET && !this.dialog.data.freebetOfferId) {
      this.prize.freebetOfferId = this.dialog.data.defaultOfferIds.ticketOfferId;
    }

    if (!this.prize.freebetOfferId) {
      if ($event.value === this.prizeTypesMapper.TICKET) {
        this.prize.freebetOfferId = this.dialog.data.freebetOfferId ? this.dialog.data.freebetOfferId : this.dialog.data.defaultOfferIds.ticketOfferId;
      }
      if ($event.value === this.prizeTypesMapper.FREEBET) {
        this.prize.freebetOfferId = this.dialog.data.freebetOfferId ? this.dialog.data.freebetOfferId : this.dialog.data.defaultOfferIds.freebetOfferId;
      }
    }
  }

  /**
   * To avoid special characters
   * @param  event
   * @returns
   */
  blockSpecialCharsExMin(event) {
    event.target.value = event.target.value.indexOf('-') === 0 ?
    event.target.value.replace(/[!@#$^&()_+]/g, '').replace('-', '').replace(/[a-zA-Z]/g, '') :
    event.target.value.replace(/[!@#$^&()_+]/g, '').replace(/[a-zA-Z]/g, '');
  }


  /***
   * To cose dialog
   */
  closeDialog() {
    this.dialogRef.close();
  }

  /**
   * To fetch svgid from file name
   * @param {string} value
   * @returns {string}
   */
  private transformName(value: string): string {
    const noFileTypeName = value.includes('.') ? value.slice(0, value.lastIndexOf('.')) : value;
    return noFileTypeName.toLowerCase().replace(/#/g, '').replace(/\s/g, '');
  }

  /**
   * To Validate Svg file
   * @param {string} type
   * @returns {void}
   */
  private validateSvgFile(type: string): void {
    if (!this.prize[type]) {
      this.prize[type] = {...DEFAULT_FILENAME};
    }
  }

  /**
   * To update prize images
   * @param {File} file
   * @param {string} fieldName
   * @returns {void}
   */
  private updatePrizeImages(file: File, fieldName: string): void {
    this.prizeForm.form.markAsDirty();
    if (fieldName === 'icon') {
      this.prize.prizeIcon = file;
    } else if (fieldName === 'signPosting') {
      this.prize.prizeSignposting = file;
    }
  }

  /**
   * Remove the image based on the selected file input (icon / Sponsor logo)
   * @param {string} fieldName
   */
  removeImage(fieldName: string): void {
    const ICONFILE: string = 'icon';
    const SIGNPOSTINGFILE: string = 'signPosting';
    this.prizeForm.form.markAsDirty();
    if (fieldName === SIGNPOSTINGFILE) {
      this.prize.prizeSignposting = null;
      this.prize.signPosting.originalname = '';
      this.prize.signPosting.svgId = '';
      this.signpostingSvgFileInput.nativeElement.value = '';
    } else if (fieldName === ICONFILE) {
      this.prize.prizeIcon = null;
      this.prize.icon.originalname = '';
      this.prize.icon.svgId = '';
      this.iconSvgFileInput.nativeElement.value = '';
    }
  }

  /**
   * To Set Svg image properties
   * @param output
   * @param input
   */
  private setSVGImage(output: string, input: string): void {
    if (this.dialog.data && this.dialog.data[input] &&
      this.dialog.data[input].filename) {
      this.prize[output] = this.dialog.data[input];
    }
  }

}
