import {Injectable} from '@angular/core';
import {Observable} from 'rxjs/Observable';
import {TimelinePostSseEvent} from '@app/client/private/models/timeline-post-sse-event.model';

declare var EventSource;

@Injectable()
export class SseService {
  constructor() {
  }

  observeMessages(sseUrl: string): Observable<TimelinePostSseEvent> {
    return new Observable<TimelinePostSseEvent>(obs => {
      const es = new EventSource(sseUrl);
      es.addEventListener('message', (evt) => {
        console.log(evt.data);
        obs.next(JSON.parse(evt.data));
      });
      return () => es.close();
    });
  }
}
