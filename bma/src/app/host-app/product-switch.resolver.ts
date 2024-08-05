import { ActivatedRouteSnapshot, ResolveFn } from "@angular/router";
import { inject } from '@angular/core';
import { ProductService} from '@frontend/vanilla/core';
import { ProductActivatorService } from '@frontend/vanilla/shared/product-activation';

export const ProductSwitchResolver:ResolveFn<any> = async(route: ActivatedRouteSnapshot) =>{
  const product = getProduct(route);

  if (!product) {
    throw new Error(`ProductSwitchResolver requires 'product' property to be specified on routes 'data'.`);
  }

  if (product !== inject(ProductService).current.name) {
    await inject(ProductActivatorService).activate(product);
  }
}

function getProduct(route: ActivatedRouteSnapshot) {
  let node = route.root;
  let result = null;
  while (node != null) {
    if (node.data && node.data['product']) {
      result = node.data['product'];
    }
    node = node.children && node.children[0];
  }
  return result;
}

