import { HttpErrorResponse, HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';
import { catchError, retry } from 'rxjs/operators';
import { Injectable, Injector } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { AWSFirehoseService } from '@lazy-modules/awsFirehose/service/aws-firehose.service';

@Injectable()
export class RequestsInterceptor implements HttpInterceptor {

  retries = 0;

  constructor(private injector: Injector) { }

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {

    const errorLogger = this.injector.get(AWSFirehoseService);

    return next
      .handle(request)
      .pipe(
        retry(this.retries),
        catchError((error: HttpErrorResponse) => {
          errorLogger.errorLog(error);
          return throwError(error);
        })
      );
  }
}
