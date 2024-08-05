import { Component, OnInit } from '@angular/core';

import { IMAGE_MANAGER_TABLE_COLUMNS } from '@app/image-manager/constants/image-manager.constant';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { IImageData } from '@app/image-manager/model/image-manager.model';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { ImageManagerService } from '@app/image-manager/services/image-manager.service';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';

@Component({
  selector: 'image-manager-list',
  templateUrl: './image-manager-list.component.html',
  styleUrls: ['./image-manager-list.component.scss']
})
export class ImageManagerListComponent implements OnInit {
  tableColumns = IMAGE_MANAGER_TABLE_COLUMNS;
  tableDataList: IImageData[];
  actions: Array<string> = ['edit', 'remove'];
  searchField: string = '';
  svgList: SafeHtml;

  paginationLimitOptions: number[] = [10, 20, 30, 40, 50, 0];
  paginationLimit: number = this.paginationLimitOptions[1];

  constructor (
    private dialogService: DialogService,
    private imageManagerService: ImageManagerService,
    private globalLoaderService: GlobalLoaderService,
    private sanitizer: DomSanitizer
  ) { }

  ngOnInit() {
    this.globalLoaderService.showLoader();

    this.imageManagerService.getData().subscribe((data: IImageData[]) => {
      this.tableDataList = data;
      this.svgList = this.createSvgList();
      this.globalLoaderService.hideLoader();
    }, () => {
      console.error('Unable to get images data');
      this.globalLoaderService.hideLoader();
    });
  }

  removeHandler(image: IImageData ): void {
    this.dialogService.showDeleteDialog({
      title: 'Remove Image',
      question: `Are you sure you want to remove ${image.svgId} image?`,
      deleteCallback: () => {
        this.imageManagerService.deleteAndUpdateList(this.tableDataList, image.id);
      }
    });
  }

  private createSvgList(): SafeHtml {
    let svgList = '';

    this.tableDataList.forEach((item: IImageData) => {
      svgList += item.svg;
    });

    svgList = svgList.replace(/\\\//g, '');

    return this.sanitizer.bypassSecurityTrustHtml(svgList);
  }
}
