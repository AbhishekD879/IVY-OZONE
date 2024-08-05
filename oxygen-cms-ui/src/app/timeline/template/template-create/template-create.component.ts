import {Component, OnInit} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {ConfirmDialogComponent} from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import {BrandService} from '@app/client/private/services/brand.service';
import {TimelineTemplate} from '@app/client/private/models/timelineTemplate.model';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-template-create',
  templateUrl: './template-create.component.html',
  styleUrls: []
})
export class TemplateCreateComponent implements OnInit {

  public form: FormGroup;
  public template: TimelineTemplate;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService
  ) {
  }

  templateType: string = 'plain';

  ngOnInit() {
    this.template = {
      id: '',
      brand: this.brandService.brand,
      createdBy: '',
      createdAt: '',
      updatedBy: '',
      updatedAt: '',
      updatedByUserName: '',
      createdByUserName: '',
      name: '',
      postIconSvgId: undefined,
      headerIconSvgId: undefined,
      headerText: '',
      yellowHeaderText: '',
      subHeader: '',
      isYellowSubHeaderBackground: false,
      eventId: '',
      selectionId: '',
      topRightCornerImage: {
        filename: '',
        originalname: '',
        path: '',
        size: 0,
        filetype: ''
      },
      betPromptHeader: '',
      text: '',
      showLeftSideRedLine: false,
      showLeftSideBlueLine: false,
      showTimestamp: false,
      showRedirectArrow: false,
      showRacingPostLogoInHeader: false,
      postHref: '',
      isSpotlightTemplate: false,
      isVerdictTemplate: false
    };
    this.form = new FormGroup({
      name: new FormControl('', [Validators.required]),
      templateType: new FormControl()
    });
  }

  getTemplate(): TimelineTemplate {
    const form = this.form.value;
    this.template.name = form.name;
    this.template.isSpotlightTemplate = (this.templateType === 'spotlight');
    this.template.isVerdictTemplate = (this.templateType === 'verdict');
    return this.template;
  }

  closeDialog(): void {
    this.dialogRef.close();
  }

}
