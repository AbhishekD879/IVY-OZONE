import { Component, OnInit, ViewChild } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import { Router, ActivatedRoute, Params } from '@angular/router';

import { DialogService } from '@app/shared/dialog/dialog.service';
import { YourCallAPIService } from '../../service/your-call.api.service';
import { YourCallLeague } from '../../../client/private/models';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';

@Component({
  selector: 'yc-leagues-edit',
  templateUrl: './yc-leagues-edit.component.html',
  styleUrls: ['./yc-leagues-edit.component.scss'],
  providers: [
    DialogService
  ]
})
export class YcLeaguesEditComponent implements OnInit {

  getDataError: string;
  public yourCallLeague: YourCallLeague;
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
        .putLeagueChanges(this.yourCallLeague)
        .map((yourCallLeague: HttpResponse<YourCallLeague>) => {
          return yourCallLeague.body;
        })
        .subscribe((data: YourCallLeague) => {
          this.yourCallLeague = data;
          this.actionButtons.extendCollection(this.yourCallLeague);
          this.dialogService.showNotificationDialog({
            title: `YourCall League`,
            message: `YourCall League is Saved`
          });
    });
  }

  revertChanges(): void {
    this.loadInitData();
  }

  removeYourCallLeague(): void {
    this.yourCallAPIService.deleteLeague(this.yourCallLeague.id)
        .subscribe(() => {
      this.router.navigate(['/yc/yc-leagues']);
    });
  }

  isValidForm(yourCallLeague: YourCallLeague): boolean {
    return yourCallLeague.name.length > 0 && !!yourCallLeague.typeId;
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeYourCallLeague();
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

  private loadInitData(): void {
    this.getDataError = '';

    this.activatedRoute.params.subscribe((params: Params) => {
      this.yourCallAPIService.getSingleLeague(params['id'])
        .map((yourCallLeague: HttpResponse<YourCallLeague>) => {
          return yourCallLeague.body;
        })
        .subscribe((yourCallLeague: YourCallLeague) => {
          this.yourCallLeague = yourCallLeague;
          this.breadcrumbsData = [{
            label: `Banach Leagues`,
            url: `/yc/yc-leagues`
          }, {
            label: this.yourCallLeague.name,
            url: `/yc/yc-leagues/${this.yourCallLeague.id}`
          }];
        }, error => {
          this.getDataError = error.message;
        });
    });
  }
}

