import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { map } from 'rxjs/operators';

import { IImageData } from '@app/image-manager/model/image-manager.model';
import { AbstractService } from '@app/client/private/services/http/transport/abstract.service';
import { ByteToKbPipe } from '@app/client/private/pipes/byteToKb.pipe';

@Injectable()
export class ImageLoaderService extends AbstractService<IImageData[]> {

  constructor(
    protected httpClient: HttpClient,
    protected domain: string,
    protected brand: string,
    protected byteToKbPipe: ByteToKbPipe
  ) {
    super(httpClient, domain, brand);

    this.uri = 'svg-images';
  }

  public getData(svgId: string = null): Observable<IImageData[]> {
    let uri = this.uri + '/brand/' + this.brand;
    if (svgId) {
      uri = `${uri}?search=${svgId}&active=true`;
    }
    return this.sendRequest('get', uri, null).pipe(
      map((imgList: HttpResponse<IImageData[]>) => {
        const list = [];

        imgList.body.map((obj: IImageData) => {
          if (obj.svgFilename) {
            Object.assign(obj, {
              name: obj.svgFilename.originalname,
              imageSize: this.byteToKbPipe.transform(obj.svgFilename.size),
              preview: this.wrapSVGTag(obj.svg, obj.svgId),
              isIconActive: obj.active
            });

            list.push(obj);
          }
        });
        return list;
      })
    );
  }

  public getDataForBrandAndSprite(sprite: string): Observable<IImageData[]> {
    const uri = this.uri + '/brand/' + this.brand + '/sprite/' + sprite;

    return this.sendRequest('get', uri, null).pipe(
      map((imgList: HttpResponse<IImageData[]>) => {
        const list = [];

        imgList.body.map((obj: IImageData) => {
          if (obj.svgFilename) {
            Object.assign(obj, {
              name: obj.svgFilename.originalname,
              imageSize: this.byteToKbPipe.transform(obj.svgFilename.size),
              preview: this.wrapSVGTag(obj.svg, obj.svgId),
              isIconActive: obj.active
            });

            list.push(obj);
          }
        });
        return list;
      })
    );
  }

  private wrapSVGTag(svg: string, svgID: string): string {
    return `<svg>${svg}<use xlink:href="#${svgID}"/></svg>`;
  }
}
