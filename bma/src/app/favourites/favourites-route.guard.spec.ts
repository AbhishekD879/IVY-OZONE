import { FavouritesRouteGuard } from './favourites-route.guard';
import { FavouritesService } from './services/favourites.service';
import { TestBed } from '@angular/core/testing';

describe('SignUpRouteGuard', () => {
  it('should call' , ()=> {
    TestBed.configureTestingModule({
      providers: [
        {
          provide: FavouritesService,
          useValue: { showFavourites: () => false, },
        },
      ],
    });

    const guard = TestBed.runInInjectionContext(FavouritesRouteGuard as any);
    expect(guard).toBeFalsy();
  })
});

