import {Component, OnInit} from '@angular/core';
import {ApiClientService} from '../../client/private/services/http';
import * as _ from 'lodash';
import {ExternalLink} from '../../client/private/models/externalLink.model';
import {GlobalLoaderService} from '../../shared/globalLoader/loader.service';
import {DialogService} from '../../shared/dialog/dialog.service';
import {HttpResponse} from '@angular/common/http';
import {TableColumn} from '../../client/private/models/table.column.model';
import {AppConstants} from '../../app.constants';
import {AddExternalLinkComponent} from '../add-external-link/add-external-link.component';

@Component({
  selector: 'app-external-links-page',
  templateUrl: './external-links-page.component.html',
  styleUrls: ['./external-links-page.component.scss'],
  providers: [
    DialogService
  ]
})
export class ExternalLinksPageComponent implements OnInit {

  public amountOfExternalLinks: number = 0;
  public externalLinks: ExternalLink[] = [];
  public isLoading: boolean = false;
  public searchField: string = '';

  dataTableColumns: Array<TableColumn> = [
    {
      name: 'Url',
      property: 'url',
      link: {
        hrefProperty: 'id',
      },
      type: 'link'
    },
    {
      name: 'Target',
      property: 'target'
    }
  ];

  filterProperties: Array<string> = [
    'url'
  ];

  constructor(
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService,
  ) {
  }

  ngOnInit(): void {
    this.globalLoaderService.showLoader();
    this.isLoading = true;
    this.apiClientService.externalLinks()
      .findAllByBrand()
      .map(response => {
        return response.body.sort((a: ExternalLink, b: ExternalLink) => {
          return new Date(a.updatedAt) < new Date(b.updatedAt) ? 1 : -1;
        });
      })
      .subscribe((data: ExternalLink[]) => {
        this.isLoading = false;
        this.amountOfExternalLinks = data.length;
        this.externalLinks = data;
        this.globalLoaderService.hideLoader();
      }, (error) => {
        this.isLoading = false;
        this.externalLinks = [];
        this.globalLoaderService.hideLoader();
      });
  }

  public addExternalLink(): void {
    this.dialogService.showCustomDialog(AddExternalLinkComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add New External Link',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (externalLink: ExternalLink) => {
        this.apiClientService.externalLinks()
          .add(externalLink)
          .map((result: HttpResponse<ExternalLink>) => result.body)
          .subscribe((result: ExternalLink) => {
            this.externalLinks.unshift(result);
          }, () => {
            console.error('Can not create External Link');
          });
      }
    });
  }

  public removeExternalLink(externalLink: ExternalLink): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove External Link',
      message: `Are You Sure You Want to Remove External Link ${externalLink.url}`,
      yesCallback: () => {
        this.apiClientService.externalLinks().remove(externalLink.id).subscribe(() => {
          _.remove(this.externalLinks, {
            id: externalLink.id
          });
        });
      }
    });
  }
}

