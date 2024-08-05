import { AbstractService } from './transport/abstract.service';
import { Configuration } from '../../models/configuration.model';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { TinyMCEImageUploadResponse } from '../../models/tinymce';

@Injectable()
export class TinymceService extends AbstractService<Configuration> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public uploadImage(uploadPage: string, imagePageId: string, imageData: FormData, type?: string)
    : Observable<HttpResponse<TinyMCEImageUploadResponse>> {
    const uploadUrl = (type === 'table') ? `${uploadPage}/upload-csv-file` : `${uploadPage}/${imagePageId}/wysiwyg-image`;
    return this.sendRequest<TinyMCEImageUploadResponse>('post', uploadUrl, imageData);
  }
}
