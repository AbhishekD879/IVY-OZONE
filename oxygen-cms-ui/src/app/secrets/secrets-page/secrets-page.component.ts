import { Component, OnInit } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import { AppConstants } from '@app/app.constants';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { ApiClientService } from '@app/client/private/services/http';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { EditSecretEntryComponent } from '@app/secrets/edit-secret-entry/edit-secret-entry.component';
import { SecretInfo, SecretEntry } from '@app/client/private/models/secret.model';
import { TableColumn } from '@app/client/private/models/table.column.model';

@Component({
  selector: 'app-secrets-page',
  templateUrl: './secrets-page.component.html',
  styleUrls: ['./secrets-page.component.scss'],
  providers: [DialogService]
})
export class SecretsPageComponent implements OnInit {
  isLoading: boolean = false;
  secrets: SecretInfo[] = [];
  filterString: string = '';
  filterProperties: string[] = ['name', 'uri'];
  tableColumns: TableColumn[] = [
    {
      name: 'Title',
      property: 'name'
    },
    {
      name: 'Path',
      property: 'uri'
    },
    {
      name: 'Status',
      property: 'enabled',
      type: 'boolean'
    }
  ];

  constructor(
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService,
  ) {
  }

  private static sort(a: SecretEntry, b: SecretEntry) {
    return a.name.toLowerCase() < b.name.toLowerCase() ? -1 : 1;
  }

  ngOnInit(): void {
    this.globalLoaderService.showLoader();
    this.isLoading = true;
    this.apiClientService.secrets()
      .findAllByBrand()
      .map((response: HttpResponse<SecretInfo[]>) => response.body.sort(SecretsPageComponent.sort))
      .subscribe((data: SecretInfo[]) => {
        this.isLoading = false;
        this.secrets = data;
        this.globalLoaderService.hideLoader();
      }, error => {
        console.error('Can not get Secret Entries List', error);
        this.isLoading = false;
        this.secrets = [];
        this.globalLoaderService.hideLoader();
      });
  }

  addSecret(): void {
    this.dialogService.showCustomDialog(EditSecretEntryComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add New Secret Entry',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (secretEntry: SecretEntry) => {
        this.apiClientService.secrets()
          .add(secretEntry)
          .map((result: HttpResponse<SecretInfo>) => result.body)
          .subscribe((secretInfo: SecretInfo) => {
            this.secrets.push(secretInfo);
            this.secrets = this.secrets.sort(SecretsPageComponent.sort);
          }, error => {
            console.error('Can not create Secret Entry', error);
          });
      }
    });
  }

  editSecret(secretInfo: SecretInfo): void {
    this.apiClientService.secrets()
      .getById(secretInfo.id)
      .map((result: HttpResponse<SecretEntry>) => result.body)
      .subscribe((secretEntry: SecretEntry) => {
        this.dialogService.showCustomDialog(EditSecretEntryComponent, {
          width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
          data: secretEntry,
          title: 'Edit Secret Entry',
          yesOption: 'Save',
          noOption: 'Cancel',
          yesCallback: (updatedSecretEntry: SecretEntry) => {
            this.apiClientService.secrets()
              .edit(updatedSecretEntry)
              .map((result: HttpResponse<SecretInfo>) => result.body)
              .subscribe((updatedSecretInfo: SecretInfo) => {
                this.secrets.splice(this.secrets.indexOf(secretInfo), 1, updatedSecretInfo);
                this.secrets = this.secrets.sort(SecretsPageComponent.sort);
              }, error => {
                console.error('Can not update Secret Entry', error);
              });
          }
        });
      });
  }

  removeSecret(secretInfo: SecretInfo): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove Secret Entry',
      message: `Are You sure You want to remove whole Secret Entry "${secretInfo.name}"`,
      yesCallback: () => {
        this.apiClientService.secrets()
          .remove(secretInfo.id)
          .subscribe(() => {
            this.secrets.splice(this.secrets.indexOf(secretInfo), 1);
          }, error => {
            console.error('Can not remove Secret Entry', error);
          });
      }
    });
  }
}

