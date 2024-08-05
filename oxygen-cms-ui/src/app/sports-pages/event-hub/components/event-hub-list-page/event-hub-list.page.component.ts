import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { Router } from '@angular/router';
import * as _ from 'lodash';

import { MatSnackBar } from '@angular/material/snack-bar';

import { EventHubService } from '@app/sports-pages/event-hub/services/event-hub.service';
import { IEventHub } from '@app/sports-pages/event-hub/models/event-hub.model';
import { DataTableColumn } from '@app/client/private/models/dataTableColumn';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { ErrorService } from '@app/client/private/services/error.service';
import { AppConstants } from '@app/app.constants';

import { EventHubCreateComponent } from '@app/sports-pages/event-hub/components/event-hub-create/event-hub-create.component';

@Component({
  selector: 'event-hub-list',
  templateUrl: './event-hub-list.page.component.html',
  styleUrls: ['./event-hub-list.page.component.scss']
})
export class EventHubListPageComponent implements OnInit {
  hubs: IEventHub[] = [];
  maxHubsAmount: number = 6;
  getDataError: string;
  searchField: string = '';
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Hub',
      property: 'title',
      link: {
        hrefProperty: 'id'
      },
      type: 'link',
      width: 2
    }
  ];

  constructor(
    private eventHubService: EventHubService,
    private dialogService: DialogService,
    private globalLoaderService: GlobalLoaderService,
    private errorService: ErrorService,
    private snackBar: MatSnackBar,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.eventHubService.getHubList().subscribe((eventHubs: IEventHub[]) => {
      this.hubs = eventHubs;
    });
  }

  isMaxHubAmount(): boolean {
    return this.hubs.length >= this.maxHubsAmount;
  }

  getIndexForNewHub(): number {
    let numbers = '123456';

    _.each(this.hubs, (hub: IEventHub) => {
      numbers = numbers.replace(hub.indexNumber.toString(), '');
    });

    return parseInt(numbers.charAt(0), 10);
  }

  createHub(): void {
    const newHubIndex = this.getIndexForNewHub();

    this.dialogService.showCustomDialog(EventHubCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add New EventHub',
      yesOption: 'Save',
      noOption: 'Cancel',
      data: {
        index: newHubIndex
      },
      yesCallback: (hubData: IEventHub) => {
        this.eventHubService.createHub(hubData)
          .subscribe((createdHubData: IEventHub) => {
            this.router.navigate([`/sports-pages/event-hub/${createdHubData.id}`]);
          }, () => {
            console.error('Can not create Event Hub');
          });
      }
    });
  }

  removeHandler(eventHub: IEventHub): void {
    this.dialogService.showConfirmDialog({
      title: 'Event Hub',
      message: 'Are You Sure You Want to Delete Event Hub?',
      yesCallback: () => {
        this.globalLoaderService.showLoader();
        this.eventHubService.removeHub(eventHub)
          .subscribe(() => {
            _.remove(this.hubs, {id: eventHub.id});

            this.globalLoaderService.hideLoader();
            this.snackBar.open(`Event Hub Deleted!`, 'Ok!', {
              duration: AppConstants.HIDE_DURATION,
            });
          }, error => {
            this.errorService.emitError(error.message);
            this.globalLoaderService.hideLoader();

            return Observable.throw('Error');
          });
      }
    });
  }
}
