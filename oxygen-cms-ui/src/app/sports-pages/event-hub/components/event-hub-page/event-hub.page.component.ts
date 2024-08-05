import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';

import { IEventHub } from '@app/sports-pages/event-hub/models/event-hub.model';
import { EventHubService } from '@app/sports-pages/event-hub/services/event-hub.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { ErrorService } from '@app/client/private/services/error.service';
import { AppConstants } from '@app/app.constants';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';

@Component({
  selector: 'event-hub-page',
  templateUrl: './event-hub.page.component.html',
  styleUrls: ['./event-hub.page.component.scss']
})
export class EventHubPageComponent implements OnInit {
  hubId: string;
  hubIndex: number;
  hubData: IEventHub;
  breadcrumbsData: Breadcrumb[];

  @ViewChild('actionButtons') actionButtons;

  constructor(
    private activatedRoute: ActivatedRoute,
    private eventHubService: EventHubService,
    private globalLoaderService: GlobalLoaderService,
    private errorService: ErrorService,
    private snackBar: MatSnackBar,
    private router: Router
  ) {
    this.validationHandler = this.validationHandler.bind(this);
  }

  ngOnInit(): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      this.hubId = params['hubId'];
      this.loadInitData(this.hubId);
    });
  }

  loadInitData(hubId: string): void {
    this.eventHubService.getHubData(hubId).subscribe((hubData: IEventHub) => {
      this.hubIndex = hubData.indexNumber;
      this.hubData = hubData;
      this.breadcrumbsData = [
        {
          label: 'Event Hub list',
          url: '/sports-pages/event-hub'
        },
        {
          label: `${hubData.title}`,
          url: `/sports-pages/event-hub/${hubData.id}`
        }
      ];
    });
  }

  validationHandler(): boolean {
    return this.hubData.title.length > 0;
  }

  public actionsHandler(event: string): void {
    switch (event) {
      case 'remove':
        this.remove();
        break;
      case 'save':
        this.save();
        break;
      case 'revert':
        this.revert();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  save(): void {
    this.globalLoaderService.showLoader();
    this.eventHubService.updateHubData(this.hubData)
      .subscribe((hubData: IEventHub) => {
        this.hubData = hubData;
        this.actionButtons.extendCollection(this.hubData);
        this.snackBar.open(`Event Hub Saved!`, 'Ok!', {
          duration: AppConstants.HIDE_DURATION,
        });

        this.globalLoaderService.hideLoader();
      }, error => {
        this.errorService.emitError(error.message);
        this.globalLoaderService.hideLoader();
      });
  }

  revert(): void {
    this.loadInitData(this.hubId);
  }

  remove(): void {
    this.globalLoaderService.showLoader();
    this.eventHubService.removeHub(this.hubData)
      .subscribe(() => {
        this.globalLoaderService.hideLoader();
        this.router.navigate(['/sports-pages/event-hub']);
      }, error => {
        console.error(error.message);
        this.globalLoaderService.hideLoader();
      });
  }
}
