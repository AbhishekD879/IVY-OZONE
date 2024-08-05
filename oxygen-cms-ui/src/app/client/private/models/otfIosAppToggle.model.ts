import {Base} from './base.model';

export interface OtfIosAppToggle extends Base {
  text: string;
  iosAppOff: boolean;
  url: string;
  urlText: string;
  closeCtaText: string;
  proceedCtaText: string;
}
