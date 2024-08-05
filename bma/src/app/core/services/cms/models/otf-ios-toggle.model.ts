import { IBase } from './base.model';

export interface IOtfIosToggle extends IBase {
  url: string;
  text: string;
  urlText: string;
  closeCtaText: string;
  proceedCtaText: string;
  iosAppOff: true;
}
