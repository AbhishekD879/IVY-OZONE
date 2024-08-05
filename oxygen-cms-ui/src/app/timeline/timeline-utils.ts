import {Post} from '@app/client/private/models/timeline-post.model';
import {PostStatus} from '@app/client/private/models/timelinePostStatus.model';

export default class TimelineUtils {
  static isPublishable(post: Post) { return post.postStatus !== PostStatus.PUBLISHED; }
  static isNotYetPublished(post: Post) { return TimelineUtils.isPublishable(post); }
  static isUnpublishable(post: Post) { return post.postStatus === PostStatus.PUBLISHED; }
}
