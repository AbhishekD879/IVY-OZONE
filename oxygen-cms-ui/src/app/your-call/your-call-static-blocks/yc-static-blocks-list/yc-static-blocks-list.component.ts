import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { HttpResponse } from '@angular/common/http';
import { Router } from '@angular/router';

import { DialogService } from '@app/shared/dialog/dialog.service';
import { YourCallStaticBlock } from '@app/client/private/models/yourcallstaticblock.model';
import { YourCallAPIService } from '../../service/your-call.api.service';
import { YcStaticBlocksCreateComponent } from '../yc-static-blocks-create/yc-static-blocks-create.component';
import { DataTableColumn } from '@app/client/private/models/dataTableColumn';
import { ActiveInactiveExpired } from '@app/client/private/models/activeInactiveExpired.model';
import { AppConstants } from '@app/app.constants';

@Component({
  selector: 'app-yc-static-blocks-list',
  templateUrl: './yc-static-blocks-list.component.html',
  styleUrls: ['./yc-static-blocks-list.component.scss']
})
export class YcStaticBlocksListComponent implements OnInit {
  yourCallStaticBlockData: Array<YourCallStaticBlock>;
  getDataError: string;
  searchField: string = '';
  dataTableColumns: Array<DataTableColumn> = [
    {
      name: 'Title',
      property: 'title',
      link: {
        hrefProperty: 'id'
      },
      type: 'link'
    },
    {
      name: 'HTML Markup',
      property: 'htmlMarkup',
      type: 'html'
    },
    {
      name: 'Enabled',
      property: 'enabled',
      type: 'boolean'
    },
    {
      name: 'Active for 5 A Side',
      property: 'fiveASide',
      type: 'boolean'
    }
  ];

  filterProperties: Array<string> = [
    'title'
  ];


  constructor(
    private dialog: MatDialog,
    private dialogService: DialogService,
    private staticBlockAPIService: YourCallAPIService,
    private router: Router
  ) { }

  get staticBlocksAmount(): ActiveInactiveExpired {
    const activeStaticBlocks = this.yourCallStaticBlockData && this.yourCallStaticBlockData.filter(block => block.enabled);
    const activeStaticBlocksAmount = activeStaticBlocks && activeStaticBlocks.length;
    const inactiveStaticBlocksAmount = this.yourCallStaticBlockData.length - activeStaticBlocksAmount;

    return {
      active: activeStaticBlocksAmount,
      inactive: inactiveStaticBlocksAmount
    };
  }

  ngOnInit(): void {
    this.staticBlockAPIService.getStaticBlocksList()
      .subscribe((data: any) => {
        this.yourCallStaticBlockData = data.body;
      }, error => {
        this.getDataError = error.message;
      });
  }

  createStaticBlock(): void {
    const dialogRef = this.dialog.open(YcStaticBlocksCreateComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      data: {}
    });

    dialogRef.afterClosed().subscribe(newStaticBlock => {
      if (newStaticBlock) {
        this.staticBlockAPIService.createStaticBlock(newStaticBlock)
          .map((yourCallStaticBlock: HttpResponse<YourCallStaticBlock>) => {
            return yourCallStaticBlock.body;
          })
          .subscribe((yourCallStaticBlock: YourCallStaticBlock) => {
            if (yourCallStaticBlock) {
              this.yourCallStaticBlockData.push(yourCallStaticBlock);
              this.router.navigate([`/yc/yc-static-blocks/${yourCallStaticBlock.id}`]);
            }
          });
      }
    });
  }

  /**
   * Handle deleting Static Block
   * @param {YourCallStaticBlock} staticBlock
   */
  removeStaticBlock(staticBlock: YourCallStaticBlock): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove YourCall Static Block.',
      message: 'Are You Sure You Want to Remove YourCall Static Block?',
      yesCallback: () => {
        this.sendRemoveRequest(staticBlock);
      }
    });
  }

  /**
   * Send DELETE API request
   * @param {YourCallStaticBlock} staticBlock
   */
  sendRemoveRequest(staticBlock: YourCallStaticBlock): void {
    this.staticBlockAPIService.deleteStaticBlock(staticBlock.id)
      .subscribe((data: any) => {
        this.yourCallStaticBlockData.splice(this.yourCallStaticBlockData.indexOf(staticBlock), 1);
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'YourCall Static Block is Removed.'
        });
      });
  }

}
