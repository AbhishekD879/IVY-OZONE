import { Component, EventEmitter, OnInit, Input, Output, DoCheck } from '@angular/core';
import { DialogService } from '../dialog/dialog.service';
import { Filename } from '../../client/private/models/filename.model';

@Component({
  selector: 'cms-upload',
  templateUrl: './cms-upload.component.html',
  styleUrls: ['./cms-upload.component.scss']
})
export class CmsUploadComponent implements OnInit, DoCheck {
  public uploadLabel: string;

  @Input() name: string;

  @Input() withoutLabel: boolean;

  @Input() label: string;

  @Input() filename: Filename;

  @Input() disabled: boolean;

  @Input() maxFileSizeKb?: number;

  @Input() acceptFileTypes?: string;

  @Output() onImageUpload = new EventEmitter();

  @Output() onImageValidationViolated = new EventEmitter();

  @Output() onImageRemove = new EventEmitter();

  constructor(
    private dialogService: DialogService
  ) { }

  ngOnInit(): void {
    this.checkIfFileName();
    this.label = this.label || 'Filename';
    this.uploadLabel = !!this.filename.filename ? 'Change File' : 'Upload File';
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

    if (this.validateFileForSize(event)) {
      this.onImageUpload.emit(formData);
    }

    event.target.value = '';
  }

  public validateFileForSize(event) {
    const fileInfo = event.target && event.target.files && event.target.files[0];
    if (fileInfo) {
      const fileSizeKb = fileInfo.size / 1024;
      if (this.maxFileSizeKb && (this.maxFileSizeKb < fileSizeKb)) {
        this.onImageValidationViolated.emit(`Max image size is ${this.maxFileSizeKb} KB`);
        return false;
      }
    }

    return true;
  }

  public removeImage(event: any): void {
    this.dialogService.showConfirmDialog({
      title: 'Remove file.',
      message: 'Are You Sure You Want to Remove file?',
      yesCallback: () => {
        this.onImageRemove.emit();
      }
    });
  }

  private checkIfFileName(): void {
    this.filename = !!this.filename ? this.filename : {
      filename: null,
      path: '',
      size: 0,
      filetype: null
    };
  }

}
