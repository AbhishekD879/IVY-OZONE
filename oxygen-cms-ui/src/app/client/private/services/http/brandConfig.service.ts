import {AbstractService} from './transport/abstract.service';
import {Configuration} from '../../models/configuration.model';
import {Injectable} from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import {Brand} from '../../models/brand.model';
import {IConfigGroup} from '../../../../system-configuration/config-page/models/IConfigGroup';

@Injectable()
export class BrandConfigService extends AbstractService<Configuration> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `configuration/brand/${this.brand}`;
  }

  public findAllByBrand(): Observable<HttpResponse<Brand[]>> {
    return this.sendRequest<Brand[]>('get', this.uri, null);
  }

  public saveSystemConfigurateByBrand(config): Observable<HttpResponse<any>> {
    const uri = `structure/brand/${this.brand}`;
    return this.sendRequest<any>('put', uri, config);
  }

  public postNewSystemConfigurationGroupByBrand(configGroup: IConfigGroup): Observable<HttpResponse<any>> {
    const uri = `${this.uri}/element`;
    return this.sendRequest<any>('post', uri, configGroup);
  }

  public putSystemConfigurationGroupUpdateByBrand(configGroup: IConfigGroup): Observable<HttpResponse<any>> {
    const uri = `${this.uri}/element/${configGroup.id}`;
    return this.sendRequest<any>('put', uri, configGroup);
  }

  public deleteSystemConfigurationGroupByBrand(groupId: number): Observable<HttpResponse<any>> {
    const uri = `${this.uri}/element/${groupId}`;
    return this.sendRequest<any>('delete', uri, {});
  }

  public uploadImage(groupName: string, fieldName: string, file: FormData): Observable<HttpResponse<void>> {
    const uri = `structure/brand/${this.brand}/${groupName}/${fieldName}/image`;
    return this.sendRequest<void>('post', uri, file);
  }

  public removeImage(groupName: string, fieldName: string): Observable<HttpResponse<void>> {
    const uri = `structure/brand/${this.brand}/${groupName}/${fieldName}/image`;
    return this.sendRequest<void>('delete', uri, null);
  }

  public uploadSvg(groupName: string, fieldName: string, file: FormData): Observable<HttpResponse<void>> {
    const uri = `structure/brand/${this.brand}/${groupName}/${fieldName}/svg`;
    return this.sendRequest<void>('post', uri, file);
  }
}
