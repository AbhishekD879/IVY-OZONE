import { Injectable } from '@angular/core';

import { IModuleExtension } from './module-extension.model';

@Injectable()
export class ModuleExtensionsStorageService {
  private extendersList: IModuleExtension[] = [];

  addToList(value: IModuleExtension): void {
    this.extendersList.push(value);
  }

  getList(): IModuleExtension[] {
    return this.extendersList;
  }
}
