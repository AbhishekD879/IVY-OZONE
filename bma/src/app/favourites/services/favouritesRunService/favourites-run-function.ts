// use to execute script when module instantiates(replace run file)

import { FavouritesRunService } from './favourites-run.service';

export function run(favouritesRunService: FavouritesRunService) {
  return () => {
    favouritesRunService.run();
  };
}
