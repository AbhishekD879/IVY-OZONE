import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { debounceTime, filter, switchMap } from 'rxjs/operators';
import { Subscription } from 'rxjs/Subscription';
import { MatOptionSelectionChange } from '@angular/material/core';
import { DomSanitizer } from '@angular/platform-browser';

import { IImageData } from '@app/image-manager/model/image-manager.model';
import { ImageLoaderService } from '@app/client/private/services/imageLoader/image-loader-service';
import { IMAGE_MANAGER_SVG_ID_PATTERN } from '@app/image-manager/constants/image-manager.constant';
import { SvgIconSelectConstants } from '@app/shared/constants/svg-icon-select.constants';


@Component({
  selector: 'common-svg-input-select',
  templateUrl: './common-svg-input-select.component.html',
  styleUrls: ['./common-svg-input-select.component.scss']
})
/*** Common Component used to upload svg Based on its type ***/
export class CommonSvgInputSelectComponent implements OnInit, OnDestroy {

  @Input() formFieldsModels;
  @Input() externalForm?: FormGroup;
  @Input() type = '';  /*** Dynamic key name to map the data ***/
  @Input() path = ''; /*** Dynamic path for the image source ***/
  @Input() labelShown;

  public svgSelectConstants:any = SvgIconSelectConstants;
  input: FormControl;
  haveData: boolean = false;
  isError: boolean = false;
  options: IImageData[] = [];
  private subscription$: Subscription;

  constructor(
    public sanitizer: DomSanitizer,
    private imageManageLoader: ImageLoaderService
  ) {
  }

  ngOnInit() {
    this.onInitialLoad();
  }

  private onInitialLoad(): void {
    const initialValue = this.formFieldsModels[this.type] || '';
    this.input = new FormControl(initialValue, [
      Validators.minLength(3),
      Validators.pattern(IMAGE_MANAGER_SVG_ID_PATTERN)
    ]);

    if (this.externalForm) {
      /*** Adding the new type and input to the externalForm ***/
      this.externalForm.addControl(this.type, this.input);
    }

    this.subscription$ = this.input.valueChanges.pipe(
      debounceTime(400),
      filter((value: string) => {
        if (value.length === 0) {
          this.haveData = false;
          this.updateFormFieldModel('');
          this.updateFormFieldModelSvgPath('');
        }
        if (value.length < 3) {
          this.options = [];
        }
        return value.length >= 3 && this.input.valid && !this.input.pristine;
      }),
      switchMap((value: string) => this.imageManageLoader.getData(value))
    ).subscribe((svgData: any) => {
      this.options = [];
      this.options.push({ svgId: '' } as any);
      if (svgData.length > 0) {
        this.haveData = true;
        this.options = [...this.options, ...svgData];
      } else {
        this.haveData = false;
      }
    }, (err) => {
      this.isError = true;
    });
  }

  /*** This method is triggered on mat-option SelectionChange ***/
  public selectChanges(event: MatOptionSelectionChange): void {
    this.updateFormFieldModel(event.source.value);
    this.updateFormFieldModelSvgPath(event.source.value);
  }

  /*** This method handles setting up value for path and type fields of formFieldsModels
  by checking in image manager array ***/
  private updateFormFieldModelSvgPath(value: string): void {
    if (value.length > 0) {
      const selectedOption: IImageData = this.options.find(item => item.svgId === value);
      if (selectedOption) {
        const svgFilename: string = selectedOption.svgFilename.filename;
        let path: string = selectedOption.svgFilename.path;
        if (svgFilename && path) {
          path = path.replace(/\/$|$/, '/');
          this.formFieldsModels[this.path] = path + svgFilename;
        }
      } else {
        this.formFieldsModels[this.path] = null;
        this.formFieldsModels[this.type] = '';
      }
    } else {
      this.formFieldsModels[this.path] = null;
    }
  }

  /*** This method is used to update FormFieldModel ***/
  private updateFormFieldModel(value: string): void {
    this.formFieldsModels[this.type] = value;
  }

  ngOnDestroy() {
    this.subscription$.unsubscribe();
  }
}
