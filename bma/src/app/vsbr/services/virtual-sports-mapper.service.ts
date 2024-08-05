import { Injectable } from '@angular/core';
import {
  ICategoryAliases,
  IVirtualCategoryStructure,
  IVirtualChildCategory
} from '@app/vsbr/models/virtual-sports-structure.model';

@Injectable()
export class VirtualSportsMapperService {
  private categories: IVirtualCategoryStructure[] = [];

  /**
   * Get virtual sports categories data structure
   */
  get structure(): IVirtualCategoryStructure[] {
    return this.categories.filter(category => category.childs.size);
  }

  set structure(categories: IVirtualCategoryStructure[]) {
    this.categories = categories;
  }

  /**
   * Set new parent category to data structure
   * @param parent - parent category
   */
  setParentCategory(parentCategory: IVirtualCategoryStructure): void {
    if (!parentCategory.childs) {
      parentCategory.childs = new Map<string | number, IVirtualChildCategory>();
    }

    this.categories.push(parentCategory);
  }

  /**
   * Set new child category
   * @param parentAlias - alias of parent category
   * @param child - child category
   */
  setChildCategory(parentAlias: string, child: IVirtualChildCategory): void {
    this.categories.forEach((parentCategory: IVirtualCategoryStructure) => {
      if (parentCategory.alias === parentAlias) {
        parentCategory.childs.set(child.classId, child);
      }
    });
  }

  /**
   * Get parent and child categories aliases by class id
   * @param childClassId - class id of child category
   */
  getAliasesByClassId(childClassId: string): ICategoryAliases | undefined {
    const parentCategory: IVirtualCategoryStructure = this.categories.find((parent: IVirtualCategoryStructure): boolean => {
      return parent && parent.childs && parent.childs.has(childClassId.toString());
    });

    if (parentCategory) {
      const parentAlias: string = parentCategory.alias;
      const childAlias: string = parentCategory.childs.get(childClassId.toString()).alias;

      return { parentAlias, childAlias };
    }
  }

  /**
   * Get parent category by parent alias
   * @param parenAlias - alias of parent category
   */
  getParentByAlias(parenAlias: string): IVirtualCategoryStructure {
    return this.categories.find((parent: IVirtualCategoryStructure) => parent.alias === parenAlias);
  }

  /**
   * Get child category by child alias
   * @param childAlias - alias of child category
   */
  getChildByAlias(childAlias: string): IVirtualChildCategory {
    let result: IVirtualChildCategory;

    this.categories.forEach((parent: IVirtualCategoryStructure) => {
      parent.childs.forEach((child: IVirtualChildCategory) => {
        if (child.alias === childAlias) {
          result = child;
        }
      });
    });

    return result;
  }

  /**
   * Get child category by class id
   * @param childAlias - alias of child category
   */
  getChildByClassId(classId: string): IVirtualChildCategory {
    const parentCategory: IVirtualCategoryStructure = this.categories.find((parent: IVirtualCategoryStructure) => {
      return parent.childs && parent.childs.get(classId.toString()) !== undefined;
    });

    return parentCategory && parentCategory.childs.get(classId.toString());
  }

  /**
   * Get class id  of all child categories
   * return {array} class id's
   */
  getAllClasses(): string[] {
    const classes: string[] = [];
    this.categories.forEach((parent: IVirtualCategoryStructure) => {
      if (parent.childs && parent.childs.size) {
        parent.childs.forEach((child: IVirtualChildCategory) => {
          classes.push(child.classId);
        });
      }
    });
    return classes;
  }
}
