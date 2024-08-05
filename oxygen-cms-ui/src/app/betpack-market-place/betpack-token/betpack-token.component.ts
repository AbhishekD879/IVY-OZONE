import { Component, OnInit } from '@angular/core';
import { IToken } from '@app/betpack-market-place/model/bet-pack-banner.model';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ConfirmDialogComponent } from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import { MatDialogRef } from '@angular/material/dialog';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Inject } from '@angular/core';
@Component({
  selector: 'bet-pack-token',
  templateUrl: './betpack-token.component.html',
  styleUrls: ['./betpack-token.component.scss']
})
export class BetPackTokenComponent implements OnInit {
  public form: FormGroup;
  public token: IToken;
  isTokenDuplicated: boolean = false;
  isSavedisable: boolean = true;

  constructor(@Inject(MAT_DIALOG_DATA) public data: { event, createEdit, tokenArr },
    private dialogRef: MatDialogRef<ConfirmDialogComponent>
  ) {
  }

  templateType: string = 'plain';

  ngOnInit() {
    this.token = {
      tokenId: 0,
      tokenTitle: '',
      tokenValue: '',
      deepLinkUrl: '',
      id: ''
    };
    if (this.data.createEdit === true) {
      this.form = new FormGroup({
        tokenId: new FormControl(this.data.event.tokenId, [Validators.required, Validators.maxLength(20),
          Validators.pattern(/^[0-9]\d*$/)]),
        tokenTitle: new FormControl(this.data.event.tokenTitle, [Validators.required, Validators.maxLength(50)]),
        tokenValue: new FormControl(this.data.event.tokenValue, [Validators.required, Validators.pattern(/^(?!0+\.?0*$)\d*(\.\d+)?$/)]),
        deepLinkUrl: new FormControl(this.data.event.deepLinkUrl, [Validators.required])
      });
    } else {
      this.form = new FormGroup({
        tokenId: new FormControl('', [Validators.required, Validators.maxLength(20), Validators.pattern(/^[0-9]\d*$/)]),
        tokenTitle: new FormControl('', [Validators.required, Validators.maxLength(50)]),
        tokenValue: new FormControl('', [Validators.required, Validators.pattern(/^(?!0+\.?0*$)\d*(\.\d+)?$/)]),
        deepLinkUrl: new FormControl('', [Validators.required])
      });
    }
  }

  /**
  * To get the token data while saving.
  * @returns - {IToken}
  */
  public getTemplate(): IToken {
    const form = this.form.value;
    this.token.tokenId = form.tokenId;
    this.token.tokenTitle = form.tokenTitle;
    this.token.tokenValue = form.tokenValue;
    this.token.deepLinkUrl = form.deepLinkUrl;
    this.token.id = form.tokenId;
    return this.token;
  }

  /**
  * to close the dialog.
  * @returns - {void}
  */
  public closeDialog(): void {
    if (!!this.data.createEdit) {
      this.dialogRef.close(this.data.event);
    } else {
      this.dialogRef.close();
    }

  }

  /**
    * to check the token ID is duplicated.
    * @returns - {void}
    */
  public tokenDuplicateCheck(tokenID): void {
    let tokenARRR = [];
    this.isTokenDuplicated = false;
    tokenARRR = this.data.tokenArr;
    (tokenARRR.includes(tokenID)) ? this.isTokenDuplicated = true : this.isTokenDuplicated = false;
  }

  /**
   * to get form data length.
   * @returns - {number}
   */
  public getControlValue(name: any): number {
    return this.form?.controls[name].value?.length;
  }


  /**
  * state of the save button enable or disable.
  * @returns - {boolean}
  */
  public isDisable(): boolean {
    if (this.data.createEdit === true) {
      return this.form.invalid || this.data.event.tokenId === this.form.value.tokenId &&
        this.data.event.tokenTitle === this.form.value.tokenTitle &&
        this.data.event.tokenValue === this.form.value.tokenValue &&
        this.data.event.deepLinkUrl === this.form.value.deepLinkUrl || this.isTokenDuplicated;
    } else {
      return this.form.invalid || this.isTokenDuplicated;
    }
  }
}
