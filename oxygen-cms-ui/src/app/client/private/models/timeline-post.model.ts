import {Base} from './base.model';
import {TimelineTemplate} from '@app/client/private/models/timelineTemplate.model';

export interface Post extends Base {
  name: string;
  template: TimelineTemplate;
  campaignId: string;
  campaignName: string;
  pinned: boolean;
  publishedAt: string;
  postStatus: string;
  brand: string;
  isChanged: boolean;
  spotlight?: any;
  isSpotlight?: boolean;
  isVerdict?: boolean;
}

