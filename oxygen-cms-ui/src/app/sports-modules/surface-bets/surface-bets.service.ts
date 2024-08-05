import { Injectable } from '@angular/core';
import { SurfaceBet } from '@app/client/private/models/surfaceBet.model';
import { catchError, map, switchMap } from 'rxjs/operators';
import { Observable } from 'rxjs/Observable';
import { HttpResponse } from '@angular/common/http';
import { ApiClientService } from '@app/client/private/services/http';
import { SportCategory } from '@app/client/private/models/sportcategory.model';

@Injectable()
export class SportsSurfaceBetsService {
  constructor(private apiClientService: ApiClientService) {
  }

  public getSportCategories(): Observable<SportCategory[]> {
    return this.apiClientService.sportCategoriesService().getSportCategories()
      .map((data: HttpResponse<SportCategory[]>) => {
        return data.body;
      });
  }

  public saveWithIcon(bet: SurfaceBet, icon: File): Observable<SurfaceBet> {
    return this.apiClientService.sportsSurfaceBets().save(bet).pipe(
      map((data: HttpResponse<SurfaceBet>) => {
        return data.body;
      }),
      catchError(response => {
        return Observable.throw(this.generateErrorMsg(response));
      }),
      switchMap((newBet: SurfaceBet) => {
        if (icon) {
          return this.uploadIcon(newBet.id, icon)
            .map((uploadResponseData: HttpResponse<SurfaceBet>) => {
              return uploadResponseData && uploadResponseData.body;
            });
        }

        return Observable.of(newBet);
      }),
      catchError(response => {
        if (response && response.error) {
          return Observable.throw(`Sport surface bet was created, but Image not uploaded. Error: ${this.generateErrorMsg(response)}`);
        } else {
          return Observable.throw(response);
        }
      })
    );
  }

  public uploadIcon(betId: string, file: File): Observable<HttpResponse<SurfaceBet>> {
    const formData = new FormData();
    formData.append('file', file);
    return this.apiClientService.sportsSurfaceBets().uploadIcon(betId, formData);
  }

  private generateErrorMsg(response): string {
    let message = '';
    if (response && response.error && response.error.errors) {
      response.error.errors.forEach(function (error) {
        message = `${error.field || ''} ${error.defaultMessage}. \n`;
      });
    }
    return message || 'Unknown error';
  }

}
