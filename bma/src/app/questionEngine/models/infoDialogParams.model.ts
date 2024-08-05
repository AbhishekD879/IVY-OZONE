interface IButton {
  caption: string;
  cssClass: string;
  handler: Function;
}

export interface IInfoDialogParams {
  dialogClass: string;
  src: string;
  caption: string;
  text: string;
  buttons: IButton[];
}
