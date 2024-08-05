import { Component, EventEmitter, OnInit, Input, Output } from '@angular/core';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { FormGroup } from '@angular/forms';
import * as _ from 'lodash';

@Component({
  selector: 'action-buttons',
  templateUrl: './action-buttons.component.html',
  styleUrls: ['./action-buttons.component.scss']
})
export class ActionButtonsComponent implements OnInit {
  private actionCollection: any;

  @Input() collection: any;

  @Input() showRemoveButton: boolean = true;

  @Input() fieldOrItemName: string;

  @Input() form: FormGroup;

  @Output() actionsEmitter = new EventEmitter<string>();

  @Input() validateHandler: Function = () => true;

  @Input() showRevertButton: boolean = true;

  @Input() isTypeAdd: boolean;

  constructor(
    private dialogService: DialogService
  ) { }

  ngOnInit() {
    this.extendCollection();
  }

  public extendCollection(collection?: any): void {
    this.actionCollection = _.cloneDeep(collection ? collection : this.collection);
  }

  public updateCollectionProperty(property: string, value: any): void {
    this.actionCollection[property] = value;
  }

  public saveChanges(): void {
    this.dialogService.showConfirmDialog({
      title: `Saving of: ${this.collection[this.fieldOrItemName] || this.fieldOrItemName}`,
      message: `Are You sure You want to save this: ${this.collection[this.fieldOrItemName] || this.fieldOrItemName}?`,
      yesCallback: () => {
        this.actionsEmitter.emit('save');
      }
    });
  }

  public revertChanges(): void {
    this.dialogService.showConfirmDialog({
      title: `Revert Changes`,
      message: `Are You Sure You Want to Revert Changes?`,
      yesCallback: () => {
        this.actionsEmitter.emit('revert');
      }
    });
  }

  public remove(): void {
    this.dialogService.showConfirmDialog({
      title: `Remove ${this.collection[this.fieldOrItemName] || this.fieldOrItemName}`,
      message: `Are You Sure You Want to Remove : ${this.collection[this.fieldOrItemName] || this.fieldOrItemName}?`,
      yesCallback: () => {
        this.actionsEmitter.emit('remove');
      }
    });
  }

  public isValidForm(): boolean {
    return this.validateHandler(this.collection);
  }

  public isValidForSave(): boolean {
    return (this.form ? this.form.valid : this.isValidForm()) &&
      !this.isEqualCollection();
  }

  public isEqualCollection(): boolean {
    return _.isEqual(this.actionCollection,  this.collection);
  }
}
