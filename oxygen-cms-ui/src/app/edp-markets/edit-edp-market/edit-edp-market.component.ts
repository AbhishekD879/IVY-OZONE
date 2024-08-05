import { Component, OnInit, ViewChild } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import { Router, ActivatedRoute, Params } from '@angular/router';

import { DialogService } from '../../shared/dialog/dialog.service';
import { ApiClientService } from '../../client/private/services/http/index';
import { GlobalLoaderService } from '../../shared/globalLoader/loader.service';
import { EdpMarket } from '../../client/private/models/edpmarket.model';
import { Breadcrumb } from '../../client/private/models/breadcrumb.model';

@Component({
  selector: 'app-edit-edp-market',
  templateUrl: './edit-edp-market.component.html',
  styleUrls: ['./edit-edp-market.component.scss'],
  providers: [
    DialogService
  ]
})
export class EditEdpMarketComponent implements OnInit {

  @ViewChild('actionButtons') actionButtons;
  public isLoading: boolean = false;
  public edpMarket: EdpMarket;
  public breadcrumbsData: Breadcrumb[];

  constructor(
    private activatedRoute: ActivatedRoute,
    private router: Router,
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService
  ) { }

  ngOnInit() {
    this.loadInitData();
  }

  public isValidForm(edpMarket: EdpMarket): boolean {
    return !!(edpMarket.name && edpMarket.name.length > 0);
  }

  public saveChanges(): void {
    this.apiClientService.edp()
        .edit(this.edpMarket)
        .map((response: HttpResponse<EdpMarket>) => {
          return response.body;
        })
        .subscribe((market: EdpMarket) => {
          this.edpMarket = market;
          this.actionButtons.extendCollection(this.edpMarket);
          this.dialogService.showNotificationDialog({
            title: `EDP Market Saving`,
            message: `EDP Market is Saved.`
          });
    });
  }

  public removeEdpMarket(): void {
    this.apiClientService.edp().remove(this.edpMarket.id).subscribe(() => {
      this.router.navigate(['/edp-markets']);
    });
  }

  public revertChanges(): void {
    this.loadInitData();
  }

  private loadInitData(isLoading: boolean = true): void {
    this.globalLoaderService.showLoader();
    this.isLoading = isLoading;
    this.activatedRoute.params.subscribe((params: Params) => {
      this.apiClientService.edp().getById(params['id']).map((edpResponse: HttpResponse<EdpMarket>) => {
        return edpResponse.body;
      }).subscribe((edpMarket: EdpMarket) => {
        this.edpMarket = edpMarket;
        this.breadcrumbsData = [{
          label: `EDP Markets`,
          url: `/edp-markets`
        }, {
          label: this.edpMarket.name,
          url: `/edp-markets/${this.edpMarket.id}`
        }];
        this.globalLoaderService.hideLoader();
        this.isLoading = false;
      }, () => {
        this.globalLoaderService.hideLoader();
        this.isLoading = false;
      });
    });
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeEdpMarket();
        break;
      case 'save':
        this.saveChanges();
        break;
      case 'revert':
        this.revertChanges();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

}
