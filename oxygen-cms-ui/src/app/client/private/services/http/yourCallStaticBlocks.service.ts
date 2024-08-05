import { AbstractService } from './transport/abstract.service';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { YourCallStaticBlock } from '../../models';

@Injectable()
export class YourCallStaticBlocksService extends AbstractService<YourCallStaticBlock> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = 'your-call-static-block';
  }

  findAllStaticBlocks(): Observable<HttpResponse<YourCallStaticBlock[]>> {
    const uri = `${this.uri}/brand/${this.brand}`;
    return this.sendRequest<YourCallStaticBlock[]>('get', uri, null);
  }

  createStaticBlock(staticBlock: YourCallStaticBlock): Observable<HttpResponse<YourCallStaticBlock>> {
    return this.sendRequest<YourCallStaticBlock>('post', this.uri, staticBlock);
  }

  getSingleStaticBlock(id: string): Observable<HttpResponse<YourCallStaticBlock>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<YourCallStaticBlock>('get', uri, null);
  }

  editStaticBlock(staticBlock: YourCallStaticBlock): Observable<HttpResponse<YourCallStaticBlock>> {
    const uri = `${this.uri}/${staticBlock.id}`;
    return this.sendRequest<YourCallStaticBlock>('put', uri, staticBlock);
  }

  deleteStaticBlock(id: string): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }
}
