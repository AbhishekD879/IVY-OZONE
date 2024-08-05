import { Component, OnInit, ViewChild } from '@angular/core';
import { ApiClientService } from '../../client/private/services/http/index';
import { DialogService } from '../../shared/dialog/dialog.service';
import { CreateUserDialogComponent } from './create-user-dialog/create-user-dialog.component';
import { GlobalLoaderService } from '../../shared/globalLoader/loader.service';
import { FullNamePipe } from './full-name.pipe';
import { User } from '../../client/private/models/user.model';
import { CmsAlertComponent } from '../../shared/cms-alert/cms-alert.component';
import { HttpResponse } from '@angular/common/http';
import { DataTableColumn } from '../../client/private/models/dataTableColumn';
import { ActiveInactiveExpired } from '../../client/private/models/activeInactiveExpired.model';

@Component({
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.scss'],
  providers: [FullNamePipe]
})
export class UsersComponent implements OnInit {
  public users: User[] = [];
  public searchField: string = '';
  public isLoading: boolean =  false;
  public dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'User Name',
      property: 'fullName',
      link: {
        hrefProperty: 'id'
      },
      type: 'link'
    },
    {
      name: 'Email',
      property: 'email'
    },
    {
      name: 'Can Access',
      property: 'active',
      type: 'boolean'
    }
  ];
  public searchableProperties: Array<string> = [
    'fullName'
  ];
  public error: string;

  @ViewChild('errorBlock')
  public errorBlock: CmsAlertComponent;

  constructor(
    private _apiClientService: ApiClientService,
    private _dialogService: DialogService,
    private _fullNamePipe: FullNamePipe,
    private globalLoaderService: GlobalLoaderService,
  ) {
  }

  ngOnInit(): void {
    this.isLoading = true;
    this.globalLoaderService.showLoader();
    this._apiClientService
        .user()
        .retrieveAllUsers()
        .map((res: HttpResponse<User[]>) => {
          const usersList: User[] = res.body.filter(user => {
            return user.name !== null;
          }).map((user: User) => {
            user.active = user.status === 'ACTIVE';
            return user;
          });
          return usersList;
      })
      .subscribe((users: User[]) => {
        this.users = this._fullNamePipe.transform(users);
        this.globalLoaderService.hideLoader();
        this.isLoading = false;
    });
  }

  /**
   * Add a new User
   */
  createUser(): void {
    this._dialogService.showCustomDialog(CreateUserDialogComponent, {
      title: 'Create a New User',
      noOption: 'Cancel',
      yesOption: 'Save',
      yesCallback: (user: User) => {
        this._apiClientService
            .user()
            .createUser(user)
            .map((response: HttpResponse<User>) => {
              return response.body;
            })
            .subscribe((res: User) => {
              this.users.push(res);
              this.users = this._fullNamePipe.transform(this.users);
            }, (error) => {
              const message = error && error.error && error.error.message;
              this.errorBlock.showError(message);
            });
      }
    });
  }

  get usersAmount(): ActiveInactiveExpired {
    return {
      active: this.users.length,
      showOnlyTotal: true
    };
  }

  removeHandler(user: User): void {
    const notificationMessage = 'Are You Sure You Want to Remove This User ?';
    this._dialogService.showConfirmDialog({
      title: 'Remove',
      message: notificationMessage,
      yesCallback: () => {
        this._apiClientService.user().deleteUser(user.id).subscribe(res => {
          this.users.splice(this.users.indexOf(user), 1);
        }, error => {
          console.error(error);
        });

        this._dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'User is Removed from Database.'
        });
      }
    });
  }

}
