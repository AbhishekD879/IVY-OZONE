import { Component, EventEmitter, OnInit, Input, Output, DoCheck, ViewChild } from '@angular/core';
import { SvgOptionModel } from '@app/client/private/models/svgOption.model';
import { SvgListComponent } from '@app/shared/svgList/svg-list.component';

@Component({
  selector: 'cms-upload-dropdown',
  templateUrl: './cms-upload-dropdown.component.html'
})
export class CmsUploadDropdownComponent implements OnInit, DoCheck {
  public uploadLabel: string;

  @Input() id: string;

  @Input() name: string;

  @Input() withoutLabel: boolean;

  @Input() label: string;

  @Input() filename: string;

  @Input() disabled: boolean;

  @Output() onImageUpload = new EventEmitter();

  @Output() onImageRemove = new EventEmitter();

  @Input() options: Array<SvgOptionModel>;

  @Input() selected: SvgOptionModel;

  @Output() onDataChange: EventEmitter<any> = new EventEmitter();

  @ViewChild(SvgListComponent) svgList: SvgListComponent;

  constructor() {
    this.selected = new SvgOptionModel('', '', '', '', '');
  }

  ngOnInit(): void {
    this.checkIfFileName();
    this.label = this.label || 'Filename';
    this.uploadLabel = 'Upload';

    this.options.forEach((option: SvgOptionModel) => {
      if (option.name === this.filename) {
        const {fullPath, name, svg, svgId, displayName} = option;
        this.selected = new SvgOptionModel(fullPath, name, svg, svgId, displayName);
      }
    });
  }

  ngDoCheck(): void {
    this.checkIfFileName();
  }

  public hadleUploadImageClick(event) {
    const input = event.target.previousElementSibling.querySelector('input');
    input.click();
  }

  public uploadFile(event: any, name: string): void {
    const formData = new FormData();
    formData.append(name || 'file', event.target.files[0]);

    this.onImageUpload.emit(formData);

    event.target.value = '';
  }

  public removeImage(): void {
    this.onImageRemove.emit();
  }

  private checkIfFileName(): void {
    this.filename = !!this.filename ? this.filename : '';
  }

  /**
   * Remove blank spaces from string
   * @param {string} str
   * @returns {string}
   */
  public removeBlankSpaces (str: string): string {
    return str.split(' ').join('');
  }

  /**
   * Change option value
   * @param {string} value
   */
  public onChange(value: string): void {
    this.onDataChange.emit(value);
  }

}
