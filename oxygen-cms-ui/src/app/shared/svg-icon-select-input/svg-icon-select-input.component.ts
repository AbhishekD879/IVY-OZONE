import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { debounceTime, filter, switchMap } from 'rxjs/operators';
import { Subscription } from 'rxjs/Subscription';
import { MatOptionSelectionChange } from '@angular/material/core';
import { DomSanitizer } from '@angular/platform-browser';

import { IImageData } from '@app/image-manager/model/image-manager.model';
import { ImageLoaderService } from '@app/client/private/services/imageLoader/image-loader-service';
import { IMAGE_MANAGER_SVG_ID_PATTERN } from '@app/image-manager/constants/image-manager.constant';

@Component({
  selector: 'svg-icon-select-input',
  templateUrl: './svg-icon-select-input.component.html',
  styleUrls: ['./svg-icon-select-input.component.scss']
})
export class SvgIconSelectInputComponent implements OnInit, OnDestroy {

  @Input() formFieldsModels;
  @Input() externalForm?: FormGroup;
  @Input() controlName?:any='svgId'

  input: FormControl;
  haveData: boolean = false;
  options: IImageData[] = [];
  private subscription$: Subscription;

  constructor(
    public sanitizer: DomSanitizer,
    private imageManageLoader: ImageLoaderService
  ) {
  }

  ngOnInit() {
    const initialValue = this.formFieldsModels.svgId || '';
    this.input = new FormControl(initialValue, [
      Validators.minLength(3),Validators.pattern(IMAGE_MANAGER_SVG_ID_PATTERN)]);      
    if (this.externalForm) {
      this.externalForm.addControl(this.controlName, this.input);
    }

    this.subscription$ = this.input.valueChanges.pipe(
      debounceTime(400),
      filter((value: string) => {
        if (value?.length === 0) {
          this.haveData = false;
          this.updateFormFieldModel('');
        }
        if (value?.length < 3) {
          this.options = [];
        }
        return value?.length >= 3 && this.input.valid && !this.input.pristine;
      }),
      switchMap((value: string) => this.imageManageLoader.getData(value))
    ).subscribe((data) => {
      this.options = [];
      this.options.push({svgId: ''} as any);

      if (data.length > 0) {
        this.haveData = true;
        this.options = [...this.options, ...data];
      } else {
        this.haveData = false;
      }
    });
  }

  private updateFormFieldModel(value: string): void {
    this.formFieldsModels.svgId = value;
  }

  selectChanges(event: MatOptionSelectionChange) {
    this.updateFormFieldModel(event.source.value);
  }

  ngOnDestroy() {
    this.subscription$.unsubscribe();
  }
}
