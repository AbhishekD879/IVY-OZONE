import { SafeHtml } from '@angular/platform-browser';

export interface IStaticBlockContent {
  service: string;
  content: SafeHtml;
}

export interface IStaticBlockConfig {
  [key: string]: IStaticBlockContent;
}


