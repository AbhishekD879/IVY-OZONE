package com.egalacoral.spark.timeform.controller.debug;

import static com.egalacoral.spark.timeform.service.greyhound.TimeformGreyhoundService.GREYHOUND_CACHE_NAME;

import com.egalacoral.spark.timeform.service.greyhound.TimeformBatchService;
import com.egalacoral.spark.timeform.storage.Storage;
import java.util.Date;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TestController {
  @Autowired private TimeformBatchService timeformBatchService;

  @Autowired private Storage storage;

  @GetMapping("/consumeGreyhounds")
  public String consumeGreyhounds() {
    timeformBatchService.consumeGreyhounds(new Date());
    return "OK";
  }

  @GetMapping("/updateFrom")
  public String updateFrom() {
    timeformBatchService.updateForm(new Date());
    return "OK";
  }

  @GetMapping("/consumePerformances")
  public String consumePerformances() {
    timeformBatchService.consumePerformances(new Date());
    return "OK";
  }

  @GetMapping("/consumeRacesWithEntries")
  public String consumeRacesWithEntries() {
    timeformBatchService.consumeRacesWithEntries(new Date());
    return "OK";
  }

  @GetMapping("/test/greyhound/{id}")
  public Object getGreyhound(@PathVariable int id) {
    return storage.getMap(GREYHOUND_CACHE_NAME).get(id);
  }
}
