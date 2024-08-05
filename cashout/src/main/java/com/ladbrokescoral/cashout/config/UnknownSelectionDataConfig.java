package com.ladbrokescoral.cashout.config;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.ladbrokescoral.cashout.model.context.IndexedSportsData;
import com.ladbrokescoral.cashout.model.context.SelectionPrice;
import com.ladbrokescoral.cashout.repository.ReactiveRepository;
import com.ladbrokescoral.cashout.repository.SelectionHierarchyStatusRepository;
import com.ladbrokescoral.cashout.service.UnknownSelectionData;
import com.ladbrokescoral.cashout.service.UnknownSelectionDataService;
import java.util.function.Function;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import reactor.core.scheduler.Schedulers;

@Configuration
public class UnknownSelectionDataConfig {

  @Bean
  Function<IndexedSportsData, UnknownSelectionDataService> unknownSelectionDataFunction(
      ReactiveRepository<SelectionPrice> priceRepo,
      SiteServerApi siteServerApi,
      SelectionHierarchyStatusRepository statusRepository) {
    return indexedSportsData ->
        new UnknownSelectionDataService(
            priceRepo,
            statusRepository,
            siteServerApi,
            UnknownSelectionData.create(indexedSportsData),
            Schedulers.boundedElastic());
  }
}
