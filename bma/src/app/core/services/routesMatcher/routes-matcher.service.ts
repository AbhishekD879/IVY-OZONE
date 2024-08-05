import { Route, UrlSegment, UrlMatchResult, UrlSegmentGroup } from '@angular/router';
import * as _ from 'underscore';

export function equalPathMatcher(urlSegment: UrlSegment[], segmentGroup: UrlSegmentGroup, route: Route): UrlMatchResult {
  if (!segmentGroup.segments.length) {
    return null;
  }

  let paths = route.data.path && route.data.path.split('/');
  paths = _.omit(paths, path => path.indexOf(':') !== -1);

  if (_.every(paths,
      (path: string, i: number) => path === (segmentGroup.segments[i] && segmentGroup.segments[i].path))) {
    return ({ consumed: urlSegment });
  }

  return null;
}
