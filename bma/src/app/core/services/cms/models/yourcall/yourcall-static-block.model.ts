import { IBase } from '../base.model';
import { SafeHtml } from '@angular/platform-browser';

export interface IYourCallStaticBlock extends IBase {
  title_brand: string;
  title: string;
  lang: string;
  enabled: boolean;
  htmlMarkup: SafeHtml;
}
