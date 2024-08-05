import {
  Component,
  Input,
  OnInit
} from '@angular/core';
import { 
  LazyPromotionIconsComponent  as AppLazyPromotionIconsComponent
} from '@lazy-modules/lazyPromotionIcons/components/lazy-promotion-icons.component';

@Component({
  selector: 'lazy-promotion-icons',
  templateUrl: '../../../../../app/lazy-modules/lazyPromotionIcons/components/lazy-promotion-icons.component.html',
  styleUrls: ['./lazy-promotion-icons.component.scss']
})
export class LazyPromotionIconsComponent extends AppLazyPromotionIconsComponent implements OnInit {
  @Input() isLazyBIRSignpost: boolean = false;

  ngOnInit(): void {
    super.ngOnInit();
  }
}
