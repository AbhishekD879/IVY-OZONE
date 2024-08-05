import { BmaRunService } from './bma-run.service';

// use to execute script when module instantiates(replace run file)
export function BmaInit(bmaRunService: BmaRunService) {
  return () => {
    bmaRunService.init();
  };
}
