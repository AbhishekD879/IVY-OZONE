import {Component, Input, OnInit} from '@angular/core';
import {Breadcrumb, DataTableColumn} from '@root/app/client/private/models';
import {Router} from '@angular/router';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatDialog } from '@angular/material/dialog';

import {AppConstants} from '@app/app.constants';
import {ChildSportsCreateComponent} from '@app/virtual-sports/child-sports/child-sports-create/child-sports-create.component';
import {Order} from '@app/client/private/models/order.model';
import {VirtualSportChild} from '@app/client/private/models/virtualSportChild.model';
import {VirtualSportsChildService} from '@app/virtual-sports/virtual-sports-child.service';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {HttpResponse} from '@angular/common/http';

@Component({
  selector: 'child-sports-list',
  templateUrl: './child-sports-list.component.html',
  styleUrls: ['./child-sports-list.component.scss']
})
export class ChildSportsListComponent implements OnInit {
  childSports: VirtualSportChild[];

  @Input()
  parentSportId: string;

  breadcrumbsData: Breadcrumb[];
  getDataError: string;

  searchField: string = '';
  searchableProperties: Array<string> = ['name'];

  error: string;
  dataTableColumns: DataTableColumn[] = [
    {
      name: 'Title',
      property: 'title',
      link: {
        hrefProperty: 'id',
        path: 'child-sport'
      },
      type: 'link'
    },
    {
      name: 'Active',
      property: 'active',
      type: 'boolean',
    }
  ];

  constructor(private router: Router,
              private dialog: MatDialog,
              private dialogService: DialogService,
              private snackBar: MatSnackBar,
              private globalLoaderService: GlobalLoaderService,
              private virtualSportsService: VirtualSportsChildService) {
  }

  ngOnInit(): void {
    this.loadChildSports();
  }

  private loadChildSports() {
    this.globalLoaderService.showLoader();
    this.virtualSportsService.getVirtualSportsChildrenByParentSportId(this.parentSportId)
      .subscribe((data: HttpResponse<VirtualSportChild[]>) => {
        this.childSports = data.body;
        this.globalLoaderService.hideLoader();
      }, error => {
        this.getDataError = error.message;
        this.globalLoaderService.hideLoader();
      });
  }

  createChildSport() {
    const dialogRef = this.dialog.open(ChildSportsCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      data: {sportId: this.parentSportId}
    });

    dialogRef.afterClosed().subscribe((childSport: VirtualSportChild) => {
      if (childSport) {
        this.virtualSportsService.createVirtualSportChild(childSport)
          .subscribe(response => {
            if (response) {
              this.childSports.push(childSport);
              this.router.navigateByUrl(`/virtual-hub/virtual-sports/child-sport/${response.body.id}`);
            }
          }, error => {
            this.dialogService.showNotificationDialog({
              title: 'Virtual child sport not created properly',
              message: `Couldn\'t save virtual child sport: ${error.message}. Details: ${JSON.stringify(error.error)}`
            });
          });
      }
    });
  }

  onReorder(newOrder: Order) {
    this.virtualSportsService.postChildSportsOrder(newOrder)
      .subscribe((data: any) => {
        this.snackBar.open('NEW CHILD SPORTS ORDER SAVED!!', 'OK!', {
          duration: AppConstants.HIDE_DURATION
        });
      });
  }

  onRemove(childSport: VirtualSportChild): void {
    this.dialogService.showConfirmDialog({
      title: 'Removing Virtual Sport Child',
      message: 'Are You Sure You Want to Remove This Sport Child?',
      yesCallback: () => {
        this.virtualSportsService.deleteVirtualSportChild(childSport.id)
          .subscribe((data: any) => {
            this.childSports = this.childSports.filter(removed => removed.id !== childSport.id);
            this.snackBar.open('CHILD SPORT IS REMOVED!!', 'OK!', {
              duration: AppConstants.HIDE_DURATION
            });
          });
      }
    });
  }
}
