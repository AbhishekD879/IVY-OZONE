import {Component, OnInit} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';

import {ConfirmDialogComponent} from '../../../shared/dialog/confirm-dialog/confirm-dialog.component';
import {MenuItem} from '../../../client/private/models';


@Component({
  selector: 'app-competition-add',
  templateUrl: './menu-add.component.html'
})
export class MenuAddComponent implements OnInit {
  public form: FormGroup;
  public menuItem: MenuItem;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
  ) {}

  ngOnInit() {
    this.menuItem = {
      label: '',
      path: '',
      displayOrder: null,
      icon: '',
      active: true,
      'sub-menus': []
    };

    this.form = new FormGroup({
      label: new FormControl(this.menuItem.label, [Validators.required]),
      path: new FormControl(this.menuItem.path, [Validators.required]),
      displayOrder: new FormControl(this.menuItem.displayOrder, []),
      icon: new FormControl(this.menuItem.icon, []),
      active: new FormControl(this.menuItem.active, [Validators.required]),
    });
  }

  public closeDialog(): void {
    this.dialogRef.close();
  }
}
