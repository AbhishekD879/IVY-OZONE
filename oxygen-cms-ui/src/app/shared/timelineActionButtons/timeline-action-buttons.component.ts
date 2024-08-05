import { Component, EventEmitter, OnInit, Input, Output } from '@angular/core';
import { DialogService } from '@app/shared/dialog/dialog.service';
import { FormGroup } from '@angular/forms';
import * as _ from 'lodash';
import TimelineUtils from '@app/timeline/timeline-utils';

@Component({
  selector: 'timeline-action-buttons',
  templateUrl: './timeline-action-buttons.component.html'
})
export class TimelineActionButtonsComponent implements OnInit {

  @Input() collection: any;

  @Input() showRemoveButton: boolean = true;

  @Input() nameField: string;

  @Input() form: FormGroup;

  @Input() titleOfSavingModal: string;

  @Output() actionsEmitter = new EventEmitter<string>();

  private actionCollection: any;

  @Input() validateHandler: Function = () => true;
  @Input() validateForSaveAndPublishHandler: Function = () => true;

  constructor(
    private dialogService: DialogService
  ) {}

  ngOnInit() {
    this.extendCollection();
  }

  public extendCollection(collection?: any): void {
    this.actionCollection = _.cloneDeep(collection ? collection : this.collection);
  }

  public saveChanges(): void {
    this.dialogService.showConfirmDialog({
      title: `Saving of: ${this.collection[this.nameField] || this.titleOfSavingModal}`,
      message: `Are You Sure You Want to Save This: ${this.collection[this.nameField] || this.titleOfSavingModal}?`,
      yesCallback: () => {
        this.actionsEmitter.emit('save');
      }
    });
  }

  public saveChangesAndPublish() {
    this.dialogService.showConfirmDialog({
      title: `Saving of: ${this.collection[this.nameField] || this.titleOfSavingModal}`,
      message: `Are You Sure You Want to Save And Publish This: ${this.collection[this.nameField] || this.titleOfSavingModal}?`,
      yesCallback: () => {
        this.actionsEmitter.emit('saveAndPublish');
      }
    });
  }

  public unpublish() {
    this.dialogService.showConfirmDialog({
      title: `Saving of: ${this.collection[this.nameField] || this.titleOfSavingModal}`,
      message: `Are You Sure You Want to Unpublish This: ${this.collection[this.nameField] || this.titleOfSavingModal}?`,
      yesCallback: () => {
        this.actionsEmitter.emit('unpublish');
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
      title: `Remove ${this.collection[this.nameField]}`,
      message: `Are You Sure You Want to Remove : ${this.collection[this.nameField]}?`,
      yesCallback: () => {
        this.actionsEmitter.emit('remove');
      }
    });
  }

  public isValidForSave(): boolean {
    return this.validateHandler(this.collection) && !this.isEqualCollection();
  }

  public isValidForSaveAndPublish(): boolean {
    return this.validateForSaveAndPublishHandler(this.collection) &&
      (!this.isEqualCollection() || TimelineUtils.isNotYetPublished(this.collection));
  }

  public isValidForUnpublish(): boolean {
    return TimelineUtils.isUnpublishable(this.collection); // && !this.isEqualCollection();
  }

  public isEqualCollection(): boolean {
    return _.isEqual(this.actionCollection, this.collection);
  }
}
