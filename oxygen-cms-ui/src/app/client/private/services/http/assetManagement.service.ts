import { AbstractService } from './transport/abstract.service';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import {AssetManagement, AssetManagementExt} from '@app/client/private/models/assetManagement.model';

@Injectable()
export class AssetManagementService extends AbstractService<AssetManagement> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = 'asset-management';
  }

  findAllAssetManagements(): Observable<HttpResponse<AssetManagement[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<AssetManagement[]>('get', uri, null);
  }

  createAssetManagement(league: AssetManagement): Observable<HttpResponse<AssetManagement>> {
    return this.sendRequest<AssetManagement>('post', this.uri, league);
  }

  getSingleAssetManagement(id: string): Observable<HttpResponse<AssetManagement>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<AssetManagement>('get', uri, null);
  }

  editAssetManagement(assetManagement: AssetManagement): Observable<HttpResponse<AssetManagement>> {
    const uri = `${this.uri}/${assetManagement.id}`;
    return this.sendRequest<AssetManagement>('put', uri, assetManagement);
  }

  deleteAssetManagement(id: string): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  /**
   * Upload the provided team image to the asset id
   * @param teamId 
   * @param teamImage 
   * @returns Observable<HttpResponse<AssetManagementExt>>
   */
  public uploadTeamImage(teamId: string, teamImage: File): Observable<HttpResponse<AssetManagementExt>> {
    const formData = new FormData();
    formData.append('svgImage', teamImage);
    const uri = `${this.uri}/uploadimage/${teamId}`;
    return this.sendRequest<any>('post', uri, formData);
  }
}
