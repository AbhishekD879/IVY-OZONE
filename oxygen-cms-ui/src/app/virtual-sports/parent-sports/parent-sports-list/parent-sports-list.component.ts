import { Component, OnInit } from '@angular/core';
import {Breadcrumb, DataTableColumn} from '@root/app/client/private/models';
import { Router } from '@angular/router';
import {VirtualSportsService} from '@app/virtual-sports/virtual-sports.service';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatDialog } from '@angular/material/dialog';
import {ParentSportsCreateComponent} from '@app/virtual-sports/parent-sports/parent-sports-create/parent-sports-create.component';
import {AppConstants} from '@app/app.constants';
import {VirtualSportParent} from '@app/client/private/models/virtualSportParent.model';
import {Order} from '@app/client/private/models/order.model';
import {DialogService} from '@app/shared/dialog/dialog.service';

@Component({
  selector: 'app-parent-sports-list',
  templateUrl: './parent-sports-list.component.html',
  styleUrls: ['./parent-sports-list.component.scss']
})
export class ParentSportsListComponent implements OnInit {
  breadcrumbsData: Breadcrumb[];
  getDataError: string;

  parentSports: VirtualSportParent[];
  searchField: string = '';
  searchableProperties: Array<string> = ['title'];
  error: string;
  dataTableColumns: DataTableColumn[] = [
    {
      name: 'Title',
      property: 'title',
      link: {
        hrefProperty: 'id',
      },
      type: 'link'
    },
    {
      name: 'Active',
      property: 'active',
      type: 'boolean',
    },
    {
      name: 'Child Links',
      property: 'tracksRefs',
      type: 'array/link',
      link: {
        hrefProperty: 'trackId',
        path: 'child-sport/',
        nameProperty: 'title'
      }
    }
  ];

  constructor(private router: Router,
              private dialogService: DialogService,
              private dialog: MatDialog,
              private snackBar: MatSnackBar,
              private globalLoaderService: GlobalLoaderService,
              private virtualSportsService: VirtualSportsService) {}

  ngOnInit() {
    this.loadVirtualSports();
  }

  private loadVirtualSports() {
    this.globalLoaderService.showLoader();
    this.virtualSportsService.getVirtualSportsByBrand()
      .subscribe((data: any) => {
        this.parentSports = data.body;
        this.virtualSportsService.setSavedvirtualSports(this.parentSports);
        this.globalLoaderService.hideLoader();
      }, error => {
        this.getDataError = error.message;
        this.globalLoaderService.hideLoader();
      });
  }

  createParentSport() {
    const dialogRef = this.dialog.open(ParentSportsCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      data: {}
    });

    dialogRef.afterClosed().subscribe(parentSport => {
      if (parentSport) {
        this.virtualSportsService.createVirtualSportParent(parentSport)
          .subscribe(response => {
            if (response) {
              this.parentSports.push(parentSport);
              this.router.navigateByUrl(`/virtual-hub/virtual-sports/${response.body.id}`);
            }
          });
      }
    });
  }

  onReorder(newOrder: Order) {
    this.virtualSportsService.postSportsOrder(newOrder)
      .subscribe((data: any) => {
        this.snackBar.open('NEW SPORTS ORDER SAVED!!', 'OK!', {
          duration: AppConstants.HIDE_DURATION
        });
      });
  }

  onRemoveClick(parentSport: VirtualSportParent): void {
    this.dialogService.showConfirmDialog({
      title: 'Removing Virtual Sport',
      message: 'Are You Sure You Want to Remove This Sport? All childs will be removed along.',
      yesCallback: () => {
        this.doRemove(parentSport);
      }
    });
  }

  doRemove(parentSport: VirtualSportParent): void {
    this.virtualSportsService.deleteVirtualSportParent(parentSport.id)
      .subscribe((data: any) => {
        this.parentSports = this.parentSports.filter(sport => sport.id !== parentSport.id);
        this.snackBar.open('PARENT SPORT IS REMOVED!!', 'OK!', {
          duration: AppConstants.HIDE_DURATION
        });
      });
  }
}
