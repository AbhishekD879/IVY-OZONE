import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpResponse } from '@angular/common/http';
import { StaticTextOtfAPIService } from '../../../service/staticTextOtf.api.service';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { Breadcrumb } from '@app/client/private/models/breadcrumb.model';
import { StaticTextOtf } from '@app/client/private/models/staticTextOtf.model';
import { TinymceComponent } from '@app/shared/tinymce/tinymce.component';

@Component({
  selector: 'static-text-otf-page',
  templateUrl: './static-text-edit.component.html',
  styleUrls: ['./static-text-edit.component.scss']
})
export class StaticTextOtfComponent implements OnInit {

  @ViewChild('actionButtons') actionButtons;
  @ViewChild('staticTextPageText1') editor1: TinymceComponent;
  @ViewChild('staticTextPageText3') editor3: TinymceComponent;
  @ViewChild('staticTextPageText4') editor4: TinymceComponent;
  @ViewChild('staticTextPageText5') editor5: TinymceComponent;

  getDataError: string;
  staticTextOtf: StaticTextOtf;
  id: string;
  public breadcrumbsData: Breadcrumb[];
  public labelMapper: {};
  public visibilityMapper: {};

  constructor(
    private dialogService: DialogService,
    private route: ActivatedRoute,
    private router: Router,
    private staticTextOtfAPIService: StaticTextOtfAPIService
  ) {}

  public updateText(htmlMarkup: string, index: number): void {
    this.staticTextOtf['pageText' + index] = htmlMarkup;
  }

  isValidModel(staticTextOtf: StaticTextOtf) {
    return staticTextOtf.pageName.length > 0;
  }

  revertStaticTextChanges() {
    this.loadInitialData();
  }

  removeStaticText() {
    this.staticTextOtfAPIService.deleteStaticTextOtf(this.staticTextOtf.id)
      .subscribe((data: any) => {
        this.dialogService.showNotificationDialog({
          title: 'Remove Completed',
          message: 'Static Text is Removed.'
        });
        this.router.navigate(['/one-two-free/static-text/']);
      });
  }

  /**
   * Make PUT request to server to update
   */
  saveStaticTextChanges() {
    this.staticTextOtfAPIService.putStaticTextOtfsChanges(this.staticTextOtf)
      .map((response: HttpResponse<StaticTextOtf>) => {
        return response.body;
      })
      .subscribe((data: StaticTextOtf) => {
        this.staticTextOtf = data;
        this.actionButtons.extendCollection(this.staticTextOtf);
        this.dialogService.showNotificationDialog({
          title: 'Upload Completed',
          message: 'Static Text Changes are Saved.'
        });
      });
  }

  /**
   * Load initial data to initialize component
   */
  loadInitialData() {
    this.staticTextOtfAPIService.getSingleStaticTextOtfsData(this.id)
      .subscribe((data: any) => {
        this.staticTextOtf = data.body;
        if (this.editor1 && this.editor1.update) {this.editor1.update(this.staticTextOtf.pageText1); }
        if (this.editor3 && this.editor3.update) {this.editor3.update(this.staticTextOtf.pageText3); }
        if (this.editor4 && this.editor4.update) {this.editor4.update(this.staticTextOtf.pageText4); }
        if (this.editor5 && this.editor5.update) {this.editor5.update(this.staticTextOtf.pageText5); }

        this.breadcrumbsData = [{
          label: `One-Two-Free Static Texts`,
          url: `/one-two-free/static-text`
        }, {
          label: this.staticTextOtf.pageName,
          url: `/one-two-free/static-text/${this.staticTextOtf.id}`
        }];
        this.handleDynamicFields(this.staticTextOtf.pageName);
      }, error => {
        this.getDataError = error.message;
      });
  }

  /**
   * Handle which fields to show & how labels to name per page type
   */
  handleDynamicFields(pageName) {
    const visibilityMapper = {
      ctaMain: true,
      cta: true,
      addTextOne: false,
      addTextTwo: false,
      addTextThree: false,
      addTextFour: false,
    };

    const labelMapper = {
      addTextOne: 'Additional Page Text 1',
      addTextTwo: 'Additional Page Text 2',
      addTextThree: 'Additional Page Text 3',
      addTextFour: 'Additional Page Text 4',
    };

    if (pageName === 'Current week tab') {
      labelMapper.addTextOne = 'No current game text';
      labelMapper.addTextTwo = 'Missed deadline text';
      labelMapper.addTextThree = 'Already played text';
      labelMapper.addTextFour = 'You didn`t play text';
      visibilityMapper.addTextOne = true;
      visibilityMapper.addTextTwo = true;
      visibilityMapper.addTextThree = true;
      visibilityMapper.addTextFour = true;
      visibilityMapper.cta = false;
    }

    if (pageName === 'You are in page') {
      visibilityMapper.cta = false;
    }

    this.visibilityMapper = visibilityMapper;
    this.labelMapper = labelMapper;

  }

  ngOnInit() {
    this.id = this.route.snapshot.paramMap.get('id');
    this.loadInitialData();
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeStaticText();
        break;
      case 'save':
        this.saveStaticTextChanges();
        break;
      case 'revert':
        this.revertStaticTextChanges();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }
}
