import { Type, ComponentFactory } from '@angular/core';
import { AbstractDialogComponent } from '@shared/components/oxygenDialogs/abstract-dialog';

export interface IDialogEvent {
  type: string;
  params?: IDialogParams;
  name?: string;
  component?: Type<AbstractDialogComponent>|ComponentFactory<any>;
  forceCloseOther: boolean;
  solidOverlay?: boolean;
}

export interface IDialogParams {
  [key: string]: any;
  dialogClass?: string;
  onBeforeClose?: Function;
  closeNative?: Function;
  closeByDocument?: boolean;
  closeByEsc?: boolean;
  isPersistent?: boolean;
}

export interface IDialogButton {
  caption: string;
  cssClass?: string;
  handler?: Function;
}

export interface IDialogLinks {
  caption: string;
  cssClass?: string;
}

export interface IOpenedDialogsMap {
  [key: string]: boolean;
}
