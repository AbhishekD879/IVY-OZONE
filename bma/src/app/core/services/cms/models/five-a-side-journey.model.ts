import { SafeHtml } from '@angular/platform-browser';

export interface IJourneyStaticBlock {
  title: string;
  htmlMarkup: string;
}

export interface IJourneyItem {
  title: string;
  htmlMarkup: SafeHtml;
}

export interface IJourneyStaticBlocks {
  [key: string]: IJourneyStaticBlock;
}

export interface IJourneyItems {
  [key: string]: IJourneyItem;
}
