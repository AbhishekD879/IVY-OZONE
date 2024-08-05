import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';

import { TopGame } from '../../../client/private/models/topgame.model';
import { ConfirmDialogComponent } from '../../../shared/dialog/confirm-dialog/confirm-dialog.component';
import { BrandService } from '../../../client/private/services/brand.service';

@Component({
  templateUrl: './top-games-create.component.html',
  styleUrls: ['./top-games-create.component.scss']
})
export class TopGamesCreateComponent implements OnInit {

  public topGame: TopGame;
  public form: FormGroup;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService
  ) { }

  ngOnInit() {
    this.topGame = {
      id: '',
      updatedBy: '',
      updatedAt: '',
      createdBy: '',
      createdAt: '',
      updatedByUserName: '',
      createdByUserName: '',
      sortOrder: 0,
      widthMediumIcon: 0,
      heightMediumIcon: 0,
      widthSmallIcon: 0,
      heightSmallIcon: 0,
      widthMedium: 0,
      heightMedium: 0,
      widthSmall: 0,
      heightSmall: 0,
      spriteClass: '',
      imageTitle: '',
      lang: '',
      brand: this.brandService.brand,
      collectionType: '',
      disabled: false,
      path: '',
      alt: '',
      targetUri: '',
      uriMedium: '',
      uriMediumIcon: '',
      uriSmall: '',
      uriSmallIcon: '',
      heightLarge: 0,
      heightLargeIcon: 0,
      widthLarge: 0,
      widthLargeIcon: 0,
      uriLargeIcon: '',
      uriLarge: '',
      filename: {
        filename: '',
        originalfilename: '',
        path: '',
        size: 0,
        filetype: ''
      },
      icon: {
        filename: '',
        originalfilename: '',
        path: '',
        size: 0,
        filetype: ''
      }
    };
    this.form = new FormGroup({
      imageTitle: new FormControl('', [Validators.required])
    });
  }

  getTopGame(): TopGame {
    const form = this.form.value;
    this.topGame.imageTitle = form.imageTitle;
    return this.topGame;
  }

  closeDialog(): void {
    this.dialogRef.close();
  }
}
