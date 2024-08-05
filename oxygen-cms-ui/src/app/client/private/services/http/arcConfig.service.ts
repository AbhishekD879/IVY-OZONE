import { AbstractService } from '@app/client/private/services/http/transport/abstract.service';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { IARC, IArcConfig, IMasterGroup } from '@app/client/private/models/arcConfig.model';
import { ArcConfigurationConstants } from '@app/arc-configurations/arc-configuration.constant';


@Injectable()
export class ARCConfigService extends AbstractService<IARC[]> {

  public readonly ARCCONFIG = ArcConfigurationConstants;

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = 'arc-profiles';
  }


  /**
   * Updates the configuration
   * @param arcConfig  { IARC }
   * @returns { HttpResponse<IARC> }
   */
  public updateConfig(arcConfig: IArcConfig[]): Observable<HttpResponse<void>> {
    const url = `${this.uri}/${this.brand}`;
    return this.sendRequest<void>('put', url, arcConfig);
  }

  /**
   * Retrieves the Master Data
   * @returns { HttpResponse<IARC> }
   */
  public getMasterData(): Observable<HttpResponse<IMasterGroup[]>> {
    const url = `arc-master-data`;
    return this.sendRequest<IMasterGroup[]>('get', url, null);
  }

  /**
   * Retrieves the configuration
   * @returns { HttpResponse<IARC> }
   */
  public getConfig(): Observable<HttpResponse<IArcConfig[]>> {
    const url = `${this.uri}/brand/${this.brand}`
    return this.sendRequest<IArcConfig[]>('get', url, null);
  }

  /**
   * Deletes the configuration
   * @returns { HttpResponse<void> }
   */
  public deleteConfig(id: string): Observable<HttpResponse<void>> {
    const url = `arc-profile/${this.brand}/${id}`;
    return this.sendRequest<void>('delete', url, null);
  }
}