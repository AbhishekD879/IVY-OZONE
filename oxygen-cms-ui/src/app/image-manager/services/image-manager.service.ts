import { Inject, Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable } from 'rxjs/Observable';
import { map } from 'rxjs/operators';

import { BRAND, DOMAIN } from '@app/app.module';
import { ImageLoaderService } from '@app/client/private/services/imageLoader/image-loader-service';
import { IImageData } from '@app/image-manager/model/image-manager.model';
import { IMAGE_MANAGER_ROUTES } from '@app/image-manager/constants/image-manager.constant';
import { ByteToKbPipe } from '@app/client/private/pipes/byteToKb.pipe';

@Injectable()
export class ImageManagerService extends ImageLoaderService {

  constructor(
    protected httpClient: HttpClient,
    @Inject(DOMAIN) protected domain: string,
    @Inject(BRAND) protected brand: string,
    protected byteToKbPipe: ByteToKbPipe,
    private router: Router
  ) {
    super(httpClient, domain, brand, byteToKbPipe);
  }

  public deleteAndUpdateList(list: IImageData[], id: string): void {
    this.delete(id).subscribe(
      response => {
        this.updateImageList(list, id);
      }
    );
  }

  public updateImageList(list: IImageData[], id: string): void {
    const index = list.findIndex((obj) => {
      return obj.id === id;
    });

    list.splice(index, 1);
  }

  /**
   * Send request with form data and return internal id of new/updated image
   *
   * @param imageInternalId empty id means "new" image
   * @param formData
   */
  sendImageData(imageInternalId: string = '', formData: FormData): Observable<string> {
    formData.append('brand', this.brand);

    return this.sendRequest('post', `${this.uri}/${imageInternalId}`, formData).pipe(
      map((spriteList: HttpResponse<{[key: string]: string}>) => {
        const imageData = spriteList.body;

        return imageData.id;
      })
    );
  }

  /**
   * Request list of available svg sprites
   */
  getSpriteList(): Observable<string[]> {
    const uri = `${this.uri}/brand/${this.brand}/sprites`;

    return this.sendRequest('get', uri, null).pipe(
      map((spriteList: HttpResponse<string[]>) => spriteList.body)
    );
  }

  /**
   * Request data of single image by its internal id
   */
  getSingleImage(imageInternalId: string): Observable<IImageData> {
    const uri = `${this.uri}/${imageInternalId}`;

    return this.sendRequest('get', uri, null).pipe(
      map((image: HttpResponse<IImageData>) => image.body)
    );
  }

  /**
   * Send delete request for single image then open image list
   *
   * @param imageInternalId
   */
  deleteAndOpenList(imageInternalId: string): void {
    this.delete(imageInternalId).subscribe(
      response => {
        this.router.navigate([IMAGE_MANAGER_ROUTES.base]);
      }
    );
  }
}
