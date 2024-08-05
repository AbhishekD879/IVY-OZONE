import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';

import { HeaderMenu } from '@app/client/private/models/headermenu.model';
import { ConfirmDialogComponent } from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import { BrandService } from '@app/client/private/services/brand.service';
import { HttpResponse } from '@angular/common/http';
import { ApiClientService } from '@app/client/private/services/http';

@Component({
  templateUrl: './header-menus-create.component.html',
  styleUrls: ['./header-menus-create.component.scss']
})
export class HeaderMenusCreateComponent implements OnInit {

  public form: FormGroup;
  public headerMenu: HeaderMenu;
  public menuLevels: Array<string> = ['1', '2'];
  public headerMenues: HeaderMenu[];

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService,
    private apiClientService: ApiClientService
  ) { }

  ngOnInit() {
    this.apiClientService.headerMenu()
        .findAllByBrand()
        .map((data: HttpResponse<HeaderMenu[]>) => {
          return data.body;
        })
        .subscribe((headerMenues: HeaderMenu[]) => {
          this.headerMenues = headerMenues;
        });

    this.headerMenu = {
      id: '',
      brand: this.brandService.brand,
      createdAt: '',
      createdBy: '',
      updatedByUserName: '',
      createdByUserName: '',
      updatedAt: '',
      updatedBy: '',

      disabled: false,
      lang: '',
      level: '1',
      linkTitle: '',
      linkTitle_brand: '',
      sortOrder: 0,
      targetUri: '',
      parent: null,
      inApp: true
    };

    this.form = new FormGroup({
      linkTitle: new FormControl('', [Validators.required]),
      targetUri: new FormControl('', [Validators.required]),
      level: new FormControl(this.headerMenu.level, [Validators.required]),
      parent: new FormControl(this.headerMenu.parent, [])
    });
  }

  onParentChanged(event): void {
    this.headerMenu.parent = event.value;
  }

  onLevelChanged(): void {
    this.headerMenu.level = this.form.value.level;
  }

  getHeaderMenu(): HeaderMenu {
    const form = this.form.value;
    this.headerMenu.linkTitle = form.linkTitle;
    this.headerMenu.targetUri = form.targetUri;
    if (this.headerMenu.level === '1') {
      this.headerMenu.parent = null;
    }
    return this.headerMenu;
  }

  closeDialog(): void {
    this.dialogRef.close();
  }
}
