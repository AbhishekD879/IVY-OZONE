import { Component, OnInit } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { ConfirmDialogComponent } from '../../../shared/dialog/confirm-dialog/confirm-dialog.component';
import { User } from '../../../client/private/models/user.model';

@Component({
  selector: 'create-user-dialog',
  templateUrl: './create-user-dialog.component.html',
  styleUrls: [
    './create-user-dialog.component.scss'
  ]
})
export class CreateUserDialogComponent implements OnInit {
  public user: User;

  constructor(
    public dialogRef: MatDialogRef<ConfirmDialogComponent>
  ) {
  }

  ngOnInit(): void {
    this.user = {
      id: '',
      isAdmin: false,
      email: '',
      password: '',
      confirmPassword: '',
      status: 'ACTIVE',
      active: true,
      name: {
        first: '',
        last: '',
      }
    };
  }

  public closeDialog(): void {
    this.dialogRef.close();
  }

  public getUser(): User {
    return this.user;
  }

  public isValidUser(): boolean {
    return this.user.email &&
      this.user.email.length > 0 &&
      this.user.name.first && this.user.name.first.length > 0 &&
      this.user.name.last && this.user.name.last.length > 0 &&
      this.user.password.length >= 5 &&
      this.user.confirmPassword.length >= 5 &&
      this.user.password === this.user.confirmPassword;
  }
}
