import {Component, OnInit} from '@angular/core';
import {ApiClientService} from '@app/client/private/services/http';
import * as _ from 'lodash';
import {StaticBlock} from '@app/client/private/models/staticblock.model';
import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {DialogService} from '@app/shared/dialog/dialog.service';
import {AddStaticBlockComponent} from '../add-static-block/add-static-block.component';
import {HttpResponse} from '@angular/common/http';
import {TableColumn} from '@app/client/private/models/table.column.model';
import {Router} from '@angular/router';
import {AppConstants} from '@app/app.constants';

@Component({
  selector: 'app-static-blocks-page',
  templateUrl: './static-blocks-page.component.html',
  styleUrls: ['./static-blocks-page.component.scss'],
  providers: [
    DialogService
  ]
})
export class StaticBlocksPageComponent implements OnInit {

  public amountOfStaticBlocks: number = 0;
  public staticBlocks: StaticBlock[] = [];
  public isLoading: boolean = false;
  public searchField: string = '';

  dataTableColumns: Array<TableColumn> = [
    {
      name: 'Title',
      property: 'title',
      link: {
        hrefProperty: 'id',
      },
      type: 'link'
    },
    {
      name: 'Last Updated At',
      property: 'updatedAt',
      type: 'date'
    },
    {
      name: 'Enabled',
      property: 'enabled',
      type: 'boolean'
    }
  ];

  filterProperties: Array<string> = [
    'title'
  ];

  constructor(
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService,
    private router: Router
  ) {
  }

  ngOnInit(): void {
    this.globalLoaderService.showLoader();
    this.isLoading = true;
    this.apiClientService.staticBlocks()
        .findAllByBrand()
        .map(response => {
          return response.body.sort((a: StaticBlock, b: StaticBlock) => {
            return new Date(a.updatedAt) < new Date(b.updatedAt) ? 1 : -1;
          });
        })
        .subscribe((data: StaticBlock[]) => {
      this.isLoading = false;
      this.amountOfStaticBlocks = data.length;
      this.staticBlocks = data;
      this.globalLoaderService.hideLoader();
    }, (error) => {
      this.isLoading = false;
      this.staticBlocks = [];
      this.globalLoaderService.hideLoader();
    });
  }

  public addStaticBlock(): void {
    this.dialogService.showCustomDialog(AddStaticBlockComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'Add New Static Block',
      yesOption: 'Save',
      noOption: 'Cancel',
      yesCallback: (staticBlock: StaticBlock) => {
        this.apiClientService.staticBlocks()
            .add(staticBlock)
            .map((result: HttpResponse<StaticBlock>) => result.body)
            .subscribe((result: StaticBlock) => {
          this.staticBlocks.unshift(result);
          this.router.navigate([`/static-blocks/${result.id}`]);
        }, () => {
          console.error('Can not create static block');
        });
      }
    });
  }

  public get staticBlocksData(): StaticBlock[] {
    if (this.searchField.length > 0) {
      return this.staticBlocks.filter((item) => {
        return ~item.title.toLowerCase().indexOf(this.searchField.toLowerCase());
      });
    } else {
      return this.staticBlocks;
    }
  }

  public removeStaticBlock(staticBlock: StaticBlock): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove Static Block',
      message: `Are You Sure You Want to Remove Static Block ${staticBlock.title}`,
      yesCallback: () => {
        this.apiClientService.staticBlocks().remove(staticBlock.id).subscribe(() => {
          _.remove(this.staticBlocks, {
            id: staticBlock.id
          });
        });
      }
    });
  }

}
