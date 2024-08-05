import { Component, OnInit, ViewChild } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import { Router, ActivatedRoute, Params } from '@angular/router';

import { DialogService } from '@app/shared/dialog/dialog.service';
import { YourCallAPIService } from '../../service/your-call.api.service';
import { YourCallMarket } from '../../../client/private/models';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';

@Component({
  selector: 'yc-markets-edit',
  templateUrl: './yc-markets-edit.component.html',
  styleUrls: ['./yc-markets-edit.component.scss'],
  providers: [
    DialogService
  ]
})
export class YcMarketsEditComponent implements OnInit {

  getDataError: string;
  public yourCallMarket: YourCallMarket;
  @ViewChild('actionButtons') actionButtons;
  public breadcrumbsData: Breadcrumb[];

  constructor(
    private yourCallAPIService: YourCallAPIService,
    private activatedRoute: ActivatedRoute,
    private dialogService: DialogService,
    private router: Router
  ) { }

  ngOnInit() {
    this.loadInitData();
  }

  saveChanges(): void {
    this.yourCallAPIService
      .putMarketChanges(this.yourCallMarket)
      .map((yourCallMarket: HttpResponse<YourCallMarket>) => {
        return yourCallMarket.body;
      })
      .subscribe((data: YourCallMarket) => {
        this.yourCallMarket = data;
        this.actionButtons.extendCollection(this.yourCallMarket);
        this.dialogService.showNotificationDialog({
          title: `YourCall Market`,
          message: `YourCall Market is Saved`
        });
      });
  }

  revertChanges(): void {
    this.loadInitData();
  }

  removeYourCallMarket(): void {
    this.yourCallAPIService.deleteMarket(this.yourCallMarket.id)
      .subscribe(() => {
        this.router.navigate(['/yc/yc-markets']);
      });
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeYourCallMarket();
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

  isValidForm(yourCallMarket: YourCallMarket): boolean {
    return yourCallMarket.name.length > 0;
  }

  private loadInitData(): void {
    this.getDataError = '';

    this.activatedRoute.params.subscribe((params: Params) => {
      this.yourCallAPIService.getSingleMarket(params['id'])
        .map((yourCallMarket: HttpResponse<YourCallMarket>) => {
          return yourCallMarket.body;
        })
        .subscribe((yourCallMarket: YourCallMarket) => {
          this.yourCallMarket = yourCallMarket;
          this.breadcrumbsData = [{
            label: `YourCall Markets`,
            url: `/yc/yc-markets`
          }, {
            label: this.yourCallMarket.name,
            url: `/yc/yc-markets/${this.yourCallMarket.id}`
          }];
        }, error => {
          this.getDataError = error.message;
        });
    });
  }
}

