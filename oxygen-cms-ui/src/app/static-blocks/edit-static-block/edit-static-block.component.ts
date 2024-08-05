import { TinymceComponent } from '@app/shared/tinymce/tinymce.component';
import { Component, OnInit, ViewChild } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { GlobalLoaderService } from '@app/shared/globalLoader/loader.service';
import { ApiClientService } from '@app/client/private/services/http';
import { StaticBlock } from '@app/client/private/models/staticblock.model';
import { HttpResponse } from '@angular/common/http';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { ActionButtonsComponent } from '@app/shared/action-buttons/action-buttons.component';

@Component({
  selector: 'app-edit-static-block',
  templateUrl: './edit-static-block.component.html',
  styleUrls: ['./edit-static-block.component.scss'],
  providers: [
    DialogService
  ]
})
export class EditStaticBlockComponent implements OnInit {

  public breadcrumbsData: Breadcrumb[];
  public isLoading: boolean = false;
  public staticBlock: StaticBlock;
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;
  @ViewChild('htmlMarkup') editor: TinymceComponent;

  constructor(
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService,
    private activatedRoute: ActivatedRoute,
    private dialogService: DialogService,
    private router: Router
  ) { }

  ngOnInit() {
    this.loadInitData();
  }

  updateStaticBlock(htmlMarkup: string, eventType: string): void {
    this.staticBlock.htmlMarkup = htmlMarkup;
  }

  saveChanges(): void {
    this.globalLoaderService.showLoader();
    this.apiClientService.staticBlocks()
        .edit(this.staticBlock)
        .map((staticBlock: HttpResponse<StaticBlock>) => {
          return staticBlock.body;
        })
        .subscribe((data: StaticBlock) => {
          this.staticBlock = data;
          this.actionButtons.extendCollection(this.staticBlock);
          this.globalLoaderService.hideLoader();
          this.dialogService.showNotificationDialog({
            title: `Static Block`,
            message: `Static Block is Saved.`
          });
        });
  }

  revertChanges(): void {
    this.loadInitData(false);
  }

  removeStaticBlock(): void {
    this.apiClientService.staticBlocks().remove(this.staticBlock.id).subscribe(() => {
      this.router.navigate(['/static-blocks']);
    });
  }

  isValidForm(staticBlock: StaticBlock): boolean {
    return !!(staticBlock.title && staticBlock.title_brand && staticBlock.uri);
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

  private loadInitData(isLoading: boolean = true): void {
    this.globalLoaderService.showLoader();
    this.isLoading = isLoading;
    this.activatedRoute.params.subscribe((params: Params) => {
      this.apiClientService.staticBlocks().getById(params['id']).map((staticBlock: HttpResponse<StaticBlock>) => {
        return staticBlock.body;
      }).subscribe((staticBlock: StaticBlock) => {
        this.staticBlock = staticBlock;
        this.globalLoaderService.hideLoader();
        this.isLoading = false;
        this.breadcrumbsData = [{
          label: `Static Blocks`,
          url: `/static-blocks`
        }, {
          label: this.staticBlock.title,
          url: `/static-blocks/${this.staticBlock.id}`
        }];
        if (this.editor) {
          this.editor.update(this.staticBlock.htmlMarkup);
        }
      }, () => {
        this.globalLoaderService.hideLoader();
        this.isLoading = false;
      });
    });
  }
}
