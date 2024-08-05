import { TinymceComponent } from '@app/shared/tinymce/tinymce.component';
import { Component, OnInit, ViewChild } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { HttpResponse } from '@angular/common/http';
import { YourCallStaticBlock } from '@app/client/private/models/yourcallstaticblock.model';
import { YourCallAPIService } from '../../service/your-call.api.service';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { ActionButtonsComponent } from '@app/shared/action-buttons/action-buttons.component';

@Component({
  selector: 'app-yc-static-blocks-edit',
  templateUrl: './yc-static-blocks-edit.component.html',
  styleUrls: ['./yc-static-blocks-edit.component.scss']
})
export class YcStaticBlocksEditComponent implements OnInit {

  public yourCallStaticBlock: YourCallStaticBlock;
  public isLoading: boolean = false;
  public breadcrumbsData: Breadcrumb[];
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;
  @ViewChild('htmlMarkup') editor: TinymceComponent;

  constructor(
    private staticBlockAPIService: YourCallAPIService,
    private globalLoaderService: GlobalLoaderService,
    private activatedRoute: ActivatedRoute,
    private dialogService: DialogService,
    private router: Router
  ) { }

  ngOnInit() {
    this.loadInitData();
  }

  public isValidForm(yourCallStaticBlock: YourCallStaticBlock): boolean {
    return yourCallStaticBlock.title && yourCallStaticBlock.title.length > 0;
  }

  private loadInitData(isLoading: boolean = true): void {
    this.globalLoaderService.showLoader();
    this.isLoading = isLoading;
    this.activatedRoute.params.subscribe((params: Params) => {
      this.staticBlockAPIService.getSingleStaticBlock(params['id']).map((yourCallStaticBlock: HttpResponse<YourCallStaticBlock>) => {
        return yourCallStaticBlock.body;
      }).subscribe((yourCallStaticBlock: YourCallStaticBlock) => {
        this.yourCallStaticBlock = yourCallStaticBlock;
        this.globalLoaderService.hideLoader();
        this.isLoading = false;
        this.breadcrumbsData = [{
          label: `BYB Static Blocks`,
          url: `/yc/yc-static-blocks`
        }, {
          label: this.yourCallStaticBlock.title,
          url: `/yc/yc-static-blocks/${this.yourCallStaticBlock.id}`
        }];
        if (this.editor) {
          this.editor.update(this.yourCallStaticBlock.htmlMarkup);
        }
      }, () => {
        this.globalLoaderService.hideLoader();
        this.isLoading = false;
      });
    });
  }

  saveChanges(): void {
    this.staticBlockAPIService
      .putStaticBlockChanges(this.yourCallStaticBlock)
      .map((yourCallStaticBlock: HttpResponse<YourCallStaticBlock>) => {
        return yourCallStaticBlock.body;
      })
      .subscribe((data: YourCallStaticBlock) => {
        this.yourCallStaticBlock = data;
        this.actionButtons.extendCollection(this.yourCallStaticBlock);
        this.dialogService.showNotificationDialog({
          title: `YourCall Static Block`,
          message: `YourCall Static Block is Saved`
        });
      });
  }

  revertChanges(): void {
    this.loadInitData();
  }

  removeStaticBlock(): void {
    this.staticBlockAPIService.deleteStaticBlock(this.yourCallStaticBlock.id)
      .subscribe(() => {
        this.router.navigate(['/yc/yc-static-blocks']);
      });
  }

  updateStaticBlock(htmlMarkup: string, eventType: string): void {
    this.yourCallStaticBlock.htmlMarkup = htmlMarkup;
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeStaticBlock();
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
