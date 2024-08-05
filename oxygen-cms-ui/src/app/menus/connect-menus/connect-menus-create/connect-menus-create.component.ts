import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';

import { ConnectMenu } from '../../../client/private/models/connectmenu.model';
import { ConfirmDialogComponent } from '../../../shared/dialog/confirm-dialog/confirm-dialog.component';
import { BrandService } from '../../../client/private/services/brand.service';
import { ApiClientService } from '../../../client/private/services/http';

@Component({
  templateUrl: './connect-menus-create.component.html',
  styleUrls: ['./connect-menus-create.component.scss']
})
export class ConnectMenusCreateComponent implements OnInit {
  public connectMenus: Array<ConnectMenu>;
  public form: FormGroup;
  public connectMenu: ConnectMenu;
  public menuLevels: Array<string> = ['1', '2'];

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService,
    private apiClientService: ApiClientService,
  ) { }

  ngOnInit() {
    this.apiClientService.connectMenu()
      .findAllByBrand()
      .map(response => {
        return response.body;
      })
      .subscribe((data: ConnectMenu[]) => {
        this.connectMenus = data;
        console.log(this.connectMenus);
      });

    this.connectMenu = {
      id: '',
      updatedAt: '',
      updatedBy: '',
      createdAt: '',
      createdBy: '',
      parent: null,
      updatedByUserName: '',
      createdByUserName: '',

      linkTitleBrand: '',
      sortOrder: 0,
      linkTitle: '',
      level: '',
      lang: '',
      brand: this.brandService.brand,
      showItemFor: '',
      svg: '',
      svgId: '',
      inApp: true,
      disabled: false,
      upgradePopup: false,
      targetUri: '',
      linkSubtitle: '',

      svgFilename: {
        filename: '',
        originalfilename: '',
        path: '',
        size: 0,
        filetype: ''
      }
    };
    this.form = new FormGroup({
      linkTitle: new FormControl('', [Validators.required]),
      linkSubtitle: new FormControl('', []),
      targetUri: new FormControl('', [Validators.required]),
      parent: new FormControl(this.connectMenu.parent, []),
      level: new FormControl('', [])
    });
  }

  onParentChanged(event): void {
    this.connectMenu.parent = event.value;
  }

  onLevelChanged(): void {
    this.connectMenu.level = this.form.value.level;
  }

  getConnectMenu(): ConnectMenu {
    const form = this.form.value;
    this.connectMenu.linkTitle = form.linkTitle;
    this.connectMenu.targetUri = form.targetUri;
    return this.connectMenu;
  }

  closeDialog(): void {
    this.dialogRef.close();
  }
}
