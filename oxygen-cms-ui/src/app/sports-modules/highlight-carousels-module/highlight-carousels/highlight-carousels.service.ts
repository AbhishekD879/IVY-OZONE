import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { SportsHighlightCarousel } from '@app/client/private/models/sportsHighlightCarousel.model';
import { HttpResponse } from '@angular/common/http';
import { catchError, map, switchMap } from 'rxjs/operators';
import { ApiClientService } from '@app/client/private/services/http';
import { IEventHub } from '@app/sports-pages/event-hub/models/event-hub.model';

@Injectable()

export class SportsHighlightCarouselsService  {

  constructor(private apiClientService: ApiClientService) {
  }

  public saveWithIcon(carousel: SportsHighlightCarousel, icon: File): Observable<SportsHighlightCarousel> {
    return this.apiClientService.sportsHighlightCarousel().save(carousel).pipe(
      map((data: HttpResponse<SportsHighlightCarousel>) => {
        return data.body;
      }),
      catchError(response => {
        return Observable.throw(this.generateErrorMsg(response));
      }),
      switchMap((createdSportsHighlightCarousel: SportsHighlightCarousel) => {
        if (icon) {
          return this.uploadIcon(createdSportsHighlightCarousel.id, icon)
            .map((uploadResponseData: HttpResponse<SportsHighlightCarousel>) => {
              return uploadResponseData && uploadResponseData.body;
            });
        }

        return Observable.of(createdSportsHighlightCarousel);
      }),
      catchError(response => {
        if (response && response.error) {
          return Observable.throw('Sport Highlight Carousel was created, but Image not uploaded. Error: '
            + this.generateErrorMsg(response));
        } else {
          return Observable.throw(response);
        }
      })
    );
  }

  getHubIndex(hubId: string): Observable<number> {
    return this.apiClientService.eventHub().getEventHubById(hubId)
      .map((hubData: IEventHub) => {
        return hubData.indexNumber;
      });
  }

  public uploadIcon(carouselId: string, file: File): Observable<HttpResponse<SportsHighlightCarousel>> {
    const formData = new FormData();
    formData.append('file', file);
    return this.apiClientService.sportsHighlightCarousel().uploadIcon(carouselId, formData);
  }

  private generateErrorMsg(response): string {
    let message = '';
    if (response && response.error && response.error.errors) {
      response.error.errors.forEach(function (error) {
        message += `${error.field || ''} ${error.defaultMessage}. \n`;
      });
    }
    return message || 'Unknown error';
  }
}
