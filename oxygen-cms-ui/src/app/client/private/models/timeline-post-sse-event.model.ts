import {Post} from '@app/client/private/models/timeline-post.model';

export interface TimelinePostSseEvent {
  operation: TimelinePostSseOperation;
  content: Post;
  contentId: string;
  campaignId: string;
}

export enum TimelinePostSseOperation {
  INSERT = 'INSERT',
  UPDATE = 'UPDATE',
  DELETE = 'DELETE'
}
