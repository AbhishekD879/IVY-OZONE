import { Component, OnInit, ViewChild } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

import {User} from '../../../client/private/models/user.model';
import {ApiClientService} from '../../../client/private/services/http/index';

@Component({
  templateUrl: './user-page.component.html',
  styleUrls: ['./user-page.component.scss'],
})
export class UserPageComponent implements OnInit {
  public user: User;
  public id: string;
  public alert: any;
  public isLoading: boolean = false;
  private isPasswordChanged = false;
  @ViewChild('actionButtons')
  public actionButtons;

  constructor(
    private _apiClientService: ApiClientService,
    private route: ActivatedRoute,
    private location: Location,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.loadInitialData();
  }

  loadInitialData(): void {
    this.id = this.route.snapshot.paramMap.get('id');
    this.isLoading = true;
    this._apiClientService
        .user()
        .searchesUserById(this.id)
        .map(res => {
          return res.body;
        })
        .subscribe(res => {
          res.confirmPassword = res.password;
          this.user = res;
          this.isLoading = false;
       });
  }

  onPasswordChange() {
    this.isPasswordChanged = true;
  }

  /**
   * Update a User
   * @param {string} user id
   */
  updateUser(): void {
    const currentPass = this.user.password;
    if (!this.isPasswordChanged) {
      this.user.password = '';
    }
    this._apiClientService
        .user()
        .updateUser(this.user)
        .map(res => {
          return res.body;
        })
        .subscribe(res => {
          this.alert = true;
          this.actionButtons.extendCollection(this.user);
        }, error => {
          console.error(error);
        });
    this.user.password = currentPass;
  }

  private removeUser(): void {
    this._apiClientService.user().deleteUser(this.user.id).subscribe(res => {
      this.router.navigate(['/admin/users']);
    }, error => {
      console.error(error);
    });
  }

  public isValidForm(user: User): boolean {
    return !!(user.email &&
              user.email.length > 0 &&
              user.name.last && user.name.last.length > 0 &&
              user.name.first && user.name.first.length > 0 &&
              user.password && user.password.length >= 5 &&
              user.password === user.confirmPassword
            );
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeUser();
        break;
      case 'save':
        this.updateUser();
        break;
      case 'revert':
        this.loadInitialData();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  /**
   * Go back to previous location
   */
  back(): void {
    this.location.back();
  }

}
