import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpResponse, HttpUrlEncodingCodec, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

class DataQueryEncoder extends HttpUrlEncodingCodec {
  encodeKey(k: string): string {
    k = super.encodeKey(k);
    return k.replace(/\+/gi, '%2B');
  }
  encodeValue(v: string): string {
    v = super.encodeValue(v);
    return v.replace(/\+/gi, '%2B');
  }
}

@Injectable()
export abstract class AbstractService<T> {

  protected uri;
  protected headers = new HttpHeaders();

  constructor(protected http: HttpClient, protected domain: string, protected brand: string) {}

  protected save(item: T): Observable<HttpResponse<any>> {
    return this.sendRequest<any>('post', this.uri, null);
  }

  protected update(item: T): Observable<HttpResponse<T>> {
    return this.sendRequest<T>('put', this.uri, null);
  }

  protected findAll(): Observable<HttpResponse<T[]>> {
    return this.sendRequest<T[]>('get', this.uri, null);
  }

  protected findById(id: string): Observable<HttpResponse<T>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<T>('get', uri, null);
  }

  protected delete(id: string): Observable<HttpResponse<any>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<any>('delete', uri, null);
  }

  protected getListBySegment(segment: string): Observable<HttpResponse<T>> {
    const uri = `${this.uri}/brand/${this.brand}/segment/${segment}`;
    return this.sendRequest<T>('get', uri, null);
  }

  /* tslint:disable */
  // Alejandro Del Rio Albrechet
  protected sendRequest<T>(method: string, uri: string, body: any, queryParams?: any): Observable<HttpResponse<T>> {
    const headers = new HttpHeaders({
      'Authorization': localStorage.getItem('token') || '',
      'Accept': 'application/json',
      'Brand': this.brand
    });

    let request;

    if (method === 'get') {
      const getParams: any = this.buildQueryString(body);

      request = this.http.get<T>(this.domain + uri, {
        headers,
        observe: 'response',
        params: getParams
      });
    } else if (method === 'put') {
      const params: any = this.buildQueryString(queryParams);

      request = this.http.put<T>(this.domain + uri, body, {
        headers,
        observe: 'response',
        params: params
      });
    }  else if (method === 'patch') {
      const params: any = this.buildQueryString(queryParams);

      request = this.http.patch<T>(this.domain + uri, body, {
        headers,
        observe: 'response',
        params: params
      });
    } else if (method === 'post') {
      const params: any = this.buildQueryString(queryParams);

      request = this.http.post<T>(this.domain + uri, body, {
        headers,
        observe: 'response',
        params: params
      });
    } else if (method === 'delete') {
      const params: any = this.buildQueryString(body);

      request = this.http.delete<T>(this.domain + uri, {
        headers,
        observe: 'response',
        params: params
      });
    } else {
      console.error('Unsupported request: ' + method);
      return Observable.throw('Unsupported request: ' + method);
    }

    return request;
  }
  /* tslint:enable */

  protected buildQueryString(data): HttpParams {
    return new HttpParams({
      encoder: new DataQueryEncoder(),
      [typeof data === 'string' ? 'fromString' : 'fromObject']: data
    });
  }
}
