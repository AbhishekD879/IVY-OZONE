import { Injectable } from '@angular/core';
import { AbstractService } from '@app/client/private/services/http/transport/abstract.service';
import { SecretEntry, SecretInfo } from '@app/client/private/models/secret.model';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';

@Injectable()
export class SecretsService extends AbstractService<SecretInfo[]> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = 'secret';
  }

  public findAllByBrand(): Observable<HttpResponse<SecretInfo[]>> {
    return this.sendRequest<SecretInfo[]>('get', `${this.uri}/brand/${this.brand}`, null);
  }

  public remove(id: string): Observable<HttpResponse<void>> {
    return this.delete(id);
  }

  public add(secret: SecretEntry): Observable<HttpResponse<SecretInfo>> {
    return this.sendRequest<SecretInfo>('post', this.uri, secret);
  }

  public getById(id: string): Observable<HttpResponse<SecretEntry>>  {
    return this.sendRequest<SecretEntry>('get', `${this.uri}/${id}/decoded`, null);
  }

  public edit(secret: SecretEntry): Observable<HttpResponse<SecretInfo>> {
    return this.sendRequest<SecretInfo>('put', `${this.uri}/${secret.id}`, secret);
  }
}
