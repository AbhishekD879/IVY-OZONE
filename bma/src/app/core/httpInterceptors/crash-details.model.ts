import { UrlSegment } from '@angular/router';

export interface ICrashDetails {
  params: Object;
  segment: UrlSegment[];
  date: string;
  timestamp: number;
  url: string;
  method: null;
  status: null;
  statusText: string;
  device: Object;
  environment: string;
}
